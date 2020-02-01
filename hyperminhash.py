#!/usr/bin/env python3
'''Used to run all HyperMinHash experiments'''
import sys
assert(sys.version_info.major >= 3)

import hashlib
import mmh3
import numpy as np
import math
import os
import copy
import decimal
import time
import struct
import bitstring


def packbits(b, L):
    '''Returns a bytestring corresponding to a packed array of integers, using at most b bits per integer. We prepend with a (b, len(L)) as 64-bit unsigned integers'''
    assert(b <= 64)
    params = struct.pack("<2Q", b, len(L))
    array = bitstring.BitArray()
    for x in L:
        array += bitstring.BitArray(uint=x, length=b)
    if len(array) % 8 != 0:
        pad = 8 - (len(array) % 8)
        array += bitstring.BitArray(uint=0, length=pad)
    return params + array.bytes


def unpackbits(X):
    '''Returns a tuple (b, L) corresponding to a list of unsigned b-bit integers, from X'''
    params = X[0:16]
    b, length = struct.unpack("<2Q", params)
    L = np.zeros(length, dtype=np.uint64)
    array = bitstring.BitArray(X[16:])
    array = bitstring.BitStream(array)
    for i in range(length):
        L[i] = array.read(b).uint
    return (b, L)


def num_bytes_packbits(b, n):
    '''Returns number of bytes needed to pack n b-bit integers, plus two 64-bit integers'''
    raw = b * n
    if raw % 8 != 0:
        pad = 8 - (raw % 8)
    else:
        pad = 0
    padded_bytes = (raw + pad) // 8
    return 16 + padded_bytes


class HyperMinHash:
    '''Class that stores HyperMinHash sketch

       Defines an HLL structure augmented with a b-bit kpartition minhash, and takes l as a generator

    '''
    def __init__(self, bucketbits, bucketsize, subbucketsize, collision_correction="approx"):
        '''2^bucketbits is number of buckets used to store hashes,
           bucketsize is the number of bits for the LogLog hash
           subbucketsize is the number of bits for the bbit hash

            collision_correction={"approx", "precise", "false")
                approx --> use approximate fast expected collision function
                precise --> use big decimals and do the exact calculation
                false --> don't use expected collision function

           '''
        if bucketsize > 6:  # Using bucketsize > 6 would require >64 bits in the hash function
            raise ValueError('bucketsize for HyperMinHash implementation cannot be greater than 6')
        if bucketbits + subbucketsize > 64:
            raise ValueError('Sum of bucketbits and subbucketsize cannot exceed 64')
        if subbucketsize <= 8:
            self._subbucket_type = np.uint8
        elif subbucketsize <= 16:
            self._subbucket_type = np.uint16
        elif subbucketsize <= 32:
            self._subbucket_type = np.uint32
        elif subbucketsize <= 64:
            self._subbucket_type = np.uint64
        self._hll_type = np.uint8

        self.bucketbits = bucketbits
        self.bucketsize = bucketsize
        self.subbucketsize = subbucketsize
        self.hll = np.zeros(2**bucketbits, dtype=self._hll_type)
        self.bbit = np.zeros(2**bucketbits, dtype=self._subbucket_type)
        self.collision_correction = collision_correction

        self._bbit_mask = 2**self.subbucketsize - 1
        self._bucketbit_shift = 64 - self.bucketbits

    def serialize(self):
        '''Returns a Bytes object that can be reconstructed into a HyperMinHash sketch'''
        params = struct.pack("<3L", self.bucketbits, self.bucketsize, self.subbucketsize)
        cc = bytes(self.collision_correction[0], "utf-8")
        hll_bytes = packbits(self.bucketsize + 1, self.hll)
        bbit_bytes = packbits(self.subbucketsize, self.bbit)
        ans = params + cc + hll_bytes + bbit_bytes
        return ans

    @classmethod
    def deserialize(cls, byte_array):
        '''Unserializes a Bytes object that has been packed by serialize'''
        params = byte_array[0:12]
        bucketbits, bucketsize, subbucketsize = struct.unpack("<3L", params)
        cc = byte_array[12:13].decode("utf-8")
        if cc == 'a':
            collision_correction = "approx"
        elif cc == 'p':
            collision_correction = "precise"
        elif cc == 'f':
            collision_correction = "false"
        else:
            raise ValueError("Invalid collision_correction code in deserialization")
        obj = cls(bucketbits, bucketsize, subbucketsize, collision_correction)
        start_hll = 13
        end_hll = start_hll + num_bytes_packbits(bucketsize + 1, 2**bucketbits)
        end_bbit = end_hll + num_bytes_packbits(subbucketsize, 2**bucketbits)
        hll_b, hll_L = unpackbits(byte_array[start_hll:end_hll])
        obj.hll = hll_L.astype(obj._hll_type)
        bbit_b, bbit_L = unpackbits(byte_array[end_hll:end_bbit])
        obj.bbit = bbit_L.astype(obj._subbucket_type)
        return obj

    def triple_hash(self, item):
        '''Returns a triple i, val, aug hashed values, where i is bucketbits,
        val is the position of the leading one in a 64-bit integer, and aug is the bits
        to go in the subbuckets'''

        y, h2 = mmh3.hash64(str(item).encode())
        val = 64 + 1 - int(np.uint64(y)).bit_length()
        val = min(val, 2**self.bucketsize)

        h2prime = int(np.uint64(h2))
        i = h2prime >> self._bucketbit_shift
        aug = h2prime & self._bbit_mask

        return (i, val, aug)

    def update(self, l):
        '''Inserts a list of items l into the sketch'''
        hash_lists = (self.triple_hash(item) for item in l)
        for i, val, aug in hash_lists:
            if self.hll[i] > val:
                pass
            # this only works because we've already checked that bucket_i[0] <> val. Do not reorder
            elif self.hll[i] < val or self.bbit[i] > aug:
                self.hll[i] = val
                self.bbit[i] = aug

    def count(self):
        '''Returns an estimate of the cardinality of the unique items inserted into the sketch

        Returns cardinality based on either the HLL estimator, or the MinHash
        estimator given here:
        http://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=365694

        Will try the HLL estimator, and if the value is above 2^(10 + bucketsize), switches
        to MinHash

        Also uses MinHash estimator if bucketsize = 0
        '''

        hll_count = hll_estimator(self.hll)
        if hll_count < 2**(self.bucketbits + 10) and self.bucketsize > 0:
            ans = hll_count
        else:
            if self.bucketsize == 0:
                vals = self.bbit.astype(np.float64) / 2**self.subbucketsize
            else:
                vals = 2**-self.hll.astype(np.float64) * (1 + self.bbit.astype(np.float64) / 2**self.subbucketsize)
            if sum(vals) == 0:
                ans = float('Inf')
            else:
                ans = len(vals) * len(vals) / sum(vals)
        return ans

    def __len__(self):
        '''Returns:
            int: number of buckets used for hash values
        '''
        return len(self.hll)

    def filled_buckets(self):
        '''Returns:
            int: number of buckets that have a nonzero value
        '''
        empty = sum(np.logical_and(self.hll == 0, self.bbit == 0))
        return len(self.hll) - empty

    def __add__(self, other):
        '''Returns the union of two HyperMinHash sketches, or more precisely, the
        HyperMinHash sketch of the union'''
        assert(self.bucketbits == other.bucketbits)
        assert(self.bucketsize == other.bucketsize)
        assert(self.subbucketsize == other.subbucketsize)
        result = HyperMinHash(self.bucketbits, self.bucketsize, self.subbucketsize, collision_correction=self.collision_correction)
        for i in range(len(result.hll)):
            if self.hll[i] == other.hll[i]:
                result.hll[i] = self.hll[i]
                result.bbit[i] = min(self.bbit[i], other.bbit[i])
            elif self.hll[i] < other.hll[i]:
                result.hll[i] = other.hll[i]
                result.bbit[i] = other.bbit[i]
            elif self.hll[i] > other.hll[i]:
                result.hll[i] = self.hll[i]
                result.bbit[i] = self.bbit[i]
        return result

    def __eq__(self, other):
        '''Returns True iff all parameters and buckets match'''
        return ((self.bucketbits == other.bucketbits)
                and (self.bucketsize == other.bucketsize)
                and (self.subbucketsize == other.subbucketsize)
                and (self.collision_correction == other.collision_correction)
                and np.array_equal(self.hll, other.hll)
                and np.array_equal(self.bbit, other.bbit))

    def __ne__(self, other):
        '''Returns False iff all parameters and buckets match'''
        return not (self == other)

    def jaccard(self, other):
        '''Determines the Jaccard index of two sets using HyperMinHash sketches of them

        Note that the Jaccard index is undefined when both sets are empty.
        We choose to return a Jaccard index of 0 in that case, as this makes
        the intersection computation return the expected value of 0.
        '''
        # Can only intersect if generation parameters were the same
        assert(self.bucketbits == other.bucketbits)
        assert(self.bucketsize == other.bucketsize)
        assert(self.subbucketsize == other.subbucketsize)
        self_nonzeros = np.logical_or(self.hll != 0, self.bbit != 0)
        matches_with_zeros = np.logical_and(self.hll == other.hll, self.bbit == other.bbit)
        matches = np.logical_and(self_nonzeros, matches_with_zeros)

        match_num = sum(matches)

        union = self + other

        if self.collision_correction == "approx":
            collisions = float(collision_estimate_final(self.count(), other.count(), bucketsize=self.bucketsize, abb1=self.subbucketsize, bucketbits=self.bucketbits))
        elif self.collision_correction == 'precise':
            collisions = float(expected_collisions(self.count(), other.count(), bucketsize=self.bucketsize, abb1=self.subbucketsize, bucketbits=self.bucketbits))
        else:
            collisions = 0

        intersect_size = match_num - collisions
        union_filled_buckets = union.filled_buckets()
        if union_filled_buckets == 0:
            jaccard = 0
        else:
            jaccard = intersect_size / union.filled_buckets()
        return jaccard

    def intersection(self, other):
        '''Intersects two HyperMinHash sketches and computes:
                Intersection cardinality
                Jaccard index
                bucket matches
                Union cardinality
                '''
        union = self + other
        union_cardinality = union.count()
        jaccard = self.jaccard(other)

        # Number of filled buckets
        intersect_size = int(np.round(jaccard * union.filled_buckets()))
        return jaccard * union_cardinality, jaccard, intersect_size, union_cardinality


def hll_estimator(buckets):
    '''Returns cardinality based on HLL estimator, given a list of buckets,
    each with a single integer specifying the maximum number of leading zeros
    within that bucket.
    '''
    buckets = np.float64(np.asarray((buckets)))
    bucketnum = len(buckets)
    if bucketnum == 16:
        alpha = 0.673
    elif bucketnum == 32:
        alpha = 0.697
    elif bucketnum == 64:
        alpha = 0.709
    else:
        alpha = 0.7213 / (1 + 1.079 / bucketnum)

    res = alpha * bucketnum**2 * 1 / sum([2**-val for val in buckets])
    if res <= (5. / 2.) * bucketnum:
        V = sum(val == 0 for val in buckets)
        if V != 0:
            res2 = bucketnum * math.log(bucketnum / V)  # linear counting
        else:
            res2 = res
    elif res <= (1. / 30.) * (1 << 32):
        res2 = res
    else:
        res2 = -(1 << 32) * math.log(1 - res / (1 << 32))
    return res2


def expected_collisions(x_size, y_size, bucketbits=0, bucketsize=6, abb1=10, decimal_prec=True):
    '''Expected number of collisions (exact, assuming sufficient precision)'''
    num_hll_buckets = 2**bucketsize
    if (decimal_prec):
        decimal.getcontext().prec = 100
        decimal.getcontext().Emax = 10000000
        cp = decimal.Decimal(0)
        n = decimal.Decimal(x_size)
        m = decimal.Decimal(y_size)
        b = decimal.Decimal(abb1)
        bb2 = decimal.Decimal(2**bucketbits)
    else:
        cp = 0
        n = x_size
        m = y_size
        b = abb1
        bb2 = 2**bucketbits
    for i_ in range(num_hll_buckets):
        i = i_ + 1
        for j in range(2**abb1):
            if i != num_hll_buckets:
                b1 = (2**b + j) / (2**(i + b))
                b2 = (2**b + j + 1) / (2**(i + b))
            else:
                b1 = (j / (2**(i + b - 1)))
                b2 = ((j + 1) / (2**(i + b - 1)))
            b1 = b1 / 2**bucketbits
            b2 = b2 / 2**bucketbits
            pr_x = (1 - b1)**n - (1 - b2)**n
            pr_y = (1 - b1)**m - (1 - b2)**m
            cp = cp + pr_x * pr_y
    return cp * bb2


def collision_estimate_hll_divided(x_size, y_size, bucketbits=0, bucketsize=6, abb1=10):
    '''Estimates collisions by just summing up the collision probability within HyperLogLog buckets, and then dividing by 2^[# subbuckets]'''
    cp = 0
    n = x_size
    m = y_size
    bb2 = 2**bucketbits
    num_hll_buckets = 2**bucketsize

    for i_ in range(num_hll_buckets):
        i = i_ + 1
        if i != num_hll_buckets:
            b1 = 2**(-i)
            b2 = 2**(-i + 1)
        else:
            b1 = 0
            b2 = 2**(-i + 1)
        b1 = b1 / 2**bucketbits
        b2 = b2 / 2**bucketbits
        pr_x = (1 - b1)**n - (1 - b2)**n
        pr_y = (1 - b1)**m - (1 - b2)**m
        cp = cp + pr_x * pr_y

    return cp * bb2 / 2**abb1


def collision_estimate_final(x_size, y_size, bucketbits=0, bucketsize=6, abb1=10):
    '''Estimates collisions by using an asymptotic approximation for large cardinalities, or using collision_estimate0 for small cardinalities.

    Gives up on superhuge cardinalities'''
    n = max(x_size, y_size)
    m = min(x_size, y_size)
    p = bucketbits
    qhat = 2**bucketsize  # num_hll_buckets
    r = abb1

    # Constant factor 0.169919487159739093975315012348630288992889
    if n > 2**(qhat + r + p - 10):
        # can't use approximations, but many collisions
        raise ValueError("Cardinalities too large for approximate collision error handling: {} > {}".format(n, 2**(qhat + r + p - 10)))
        return -1
    elif n > 2**(p + 5):
        # Use high cardinality approximation

        # ratio_factor = n*m/((n+m)*(n+m-1))
        # approximate it for floating point big numbers
        ratio = n / m
        ratio_factor = 4 * ratio / (1 + ratio)**2

        return 0.169919487159739093975315012348630288992889 * 2**p * ratio_factor / 2**r
    else:
        return collision_estimate_hll_divided(x_size, y_size, bucketbits, bucketsize, abb1)
