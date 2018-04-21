#!/usr/bin/env python3

import unittest
import numpy as np
from hyperminhash import HyperMinHash

def is_within_relerr(x, ex, relerr):
    return (x * (1-relerr) <= ex <= x*(1+relerr))

class BaseTestCases:
    class TestHyperMinHash(unittest.TestCase):
        def setUp_with_params(self, seed, x_size, y_size, int_size, bucketbits, bucketsize, subbucketsize, collision_correction):
            np.random.seed(seed)
            self.x_size = x_size
            self.y_size = y_size
            self.int_size = int_size
            self.bucketbits = bucketbits
            self.bucketsize = bucketsize
            self.subbucketsize = subbucketsize
            self.collision_correction = collision_correction
            self.hmx = HyperMinHash(self.bucketbits, self.bucketsize, self.subbucketsize, collision_correction=self.collision_correction)
            self.hmy = HyperMinHash(self.bucketbits, self.bucketsize, self.subbucketsize, collision_correction=self.collision_correction)
            
            batch = np.random.random(self.int_size)
            self.hmx.update(batch)
            self.hmy.update(batch)

            batch = np.random.random(self.x_size - self.int_size)
            self.hmx.update(batch)

            batch = np.random.random(self.y_size - self.int_size)
            self.hmy.update(batch)

            self.hmu = self.hmx + self.hmy
            self.union_size = self.x_size + self.y_size - self.int_size
            self.rel_error = 1/np.sqrt(2**self.bucketbits)
            self.jaccard = self.int_size / self.union_size
        def test_union_cardinality(self):
            estimated_union = self.hmu.count()
            self.assertTrue(is_within_relerr(self.union_size, estimated_union, 2*self.rel_error),
                    "\nTrue union cardinality: " + str(self.union_size) + "\nEst union_cardinality: " + str(estimated_union))
        def test_jaccard_index(self):
            estimated_jaccard = self.hmx.jaccard(self.hmy)
            self.assertTrue(is_within_relerr(self.jaccard, estimated_jaccard, 2*self.rel_error),
                    "\nTrue jaccard: " + str(self.jaccard) + "\nEst jaccard: " + str(estimated_jaccard))
        def test_count_X(self):
            estimated_x_size = self.hmx.count()
            self.assertTrue(is_within_relerr(self.x_size, estimated_x_size, 2*self.rel_error),
                    "\nTrue X cardinality: " + str(self.x_size) + "\nEst x_size: " + str(estimated_x_size))
        def test_count_Y(self):
            estimated_y_size = self.hmy.count()
            self.assertTrue(is_within_relerr(self.y_size, estimated_y_size, 2*self.rel_error),
                    "\nTrue Y cardinality: " + str(self.y_size) + "\nEst y_size: " + str(estimated_y_size))
        def test_not_equal(self):
            self.assertTrue(self.hmx != self.hmy)
    class TestSerialization(unittest.TestCase):
        def setUp_with_params(self, seed, x_size, bucketbits, bucketsize, subbucketsize, collision_correction):
            np.random.seed(seed)
            self.hmx = HyperMinHash(bucketbits, bucketsize, subbucketsize, collision_correction=collision_correction)
            batch = np.random.random(x_size)
            self.hmx.update(batch)
        def test_round_trip(self):
            bytes_array = self.hmx.serialize()
            hmy = HyperMinHash.deserialize(bytes_array)
            #self.assertTrue(self.hmx == hmy)
            #self.assertTrue(np.array_equal(self.hmx.bbit, hmy.bbit))
            self.assertTrue(np.array_equal(self.hmx.hll, hmy.hll))
        def test_self_equality(self):
            self.assertTrue(self.hmx == self.hmx)

class Test_HMH_1(BaseTestCases.TestHyperMinHash):
    def setUp(self):
        self.setUp_with_params(314159000, 10000, 10000, 5000, 8, 6, 8, "approx")
        
class Test_HMH_2(BaseTestCases.TestHyperMinHash):
    def setUp(self):
        self.setUp_with_params(314159001, 10000, 2000, 1000, 8, 6, 8, "false")
        
class Test_HMH_3(BaseTestCases.TestHyperMinHash):
    def setUp(self):
        self.setUp_with_params(314159003, 10000, 2000, 1000, 8, 0, 8, "false")

class Test_HMH_4(BaseTestCases.TestHyperMinHash):
    def setUp(self):
        self.setUp_with_params(314159006, 10000, 2000, 500, 8, 0, 10, "false")

class Test_Serialization1(BaseTestCases.TestSerialization):
    def setUp(self):
        self.setUp_with_params(314159000, 10000, 8, 6, 8, "false")

class Test_Serialization2(BaseTestCases.TestSerialization):
    def setUp(self):
        self.setUp_with_params(314159000, 5000, 6, 0, 8, "false")

if __name__ == '__main__':
    unittest.main()
