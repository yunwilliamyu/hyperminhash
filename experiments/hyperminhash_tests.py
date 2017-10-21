# Testing code below
import os, sys
dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(dir_path)
sys.path.append(parent_dir)
from hyperminhash import *

import pathos.multiprocessing as mp

def hmh_test_range(x_size, y_size, int_size, bucketbits, bucketsize, abb1, collision_correction='approx', test_range=20, test_reps=4, prefix="full"):
    multiplier = [2**i for i in range(test_range)]
    pool = mp.Pool(processes=None)
    def parallel_helper_func(m):
        return hyperminhash_test(x_size*m, y_size*m, int_size*m, bucketbits, bucketsize, abb1, collision_correction=collision_correction)

    with open(prefix + '_results-{}-{}-{}-{}.txt'.format(bucketbits, bucketsize, abb1, collision_correction), 'a') as f:
    #if True:
        for m in multiplier:
            starttime = time.time()
            results = pool.map(parallel_helper_func, [m]*test_reps)
            endtime = time.time()
            elapsedtime = endtime - starttime
    #        results = [parallel_helper_func(x) for x in [m]*25]
            for item in results:
                flat_item = [str(i) for sublist in item for i in sublist]
                print("\t".join(flat_item), file=f, flush=True)
            print("Multiplier:\t{}\t|\tTime (s):\t{}".format(m, elapsedtime), flush=True)


def hyperminhash_test(x_size, y_size, int_size, bucketbits, bucketsize, abb1, collision_correction='approx'):
    np.random.seed(int.from_bytes(os.urandom(4), byteorder='big' ))
    hmx = HyperMinHash(bucketbits, bucketsize, abb1, collision_correction=collision_correction)
    hmy = HyperMinHash(bucketbits, bucketsize, abb1, collision_correction=collision_correction)

    batch_size = 10000


    #intersection_set = np.random.random(int_size)
    #hmx.update(intersection_set)
    #hmy.update(intersection_set)
    counter = int_size
    while counter != 0:
        if counter > batch_size:
            batch = np.random.random(batch_size)
            counter = counter - batch_size
        else:
            batch = np.random.random(counter)
            counter = 0
        hmx.update(batch)
        hmy.update(batch)


    counter = x_size - int_size
    while counter != 0:
        if counter > batch_size:
            batch = np.random.random(batch_size)
            counter = counter - batch_size
        else:
            batch = np.random.random(counter)
            counter = 0
        hmx.update(batch)

    counter = y_size - int_size
    while counter != 0:
        if counter > batch_size:
            batch = np.random.random(batch_size)
            counter = counter - batch_size
        else:
            batch = np.random.random(counter)
            counter = 0
        hmx.update(batch)

    hllmin_int = hmx.intersection(hmy)

    return [(x_size, y_size, int_size), hllmin_int]
