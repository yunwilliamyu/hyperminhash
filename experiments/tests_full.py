# Testing code below
from __future__ import print_function
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
import hyperminhash_tests  # noqa: E402

print("======================================================================")
print("=    Running full tests to regenerate Figure 6 of paper              =")
print("=    Results will be printed to full_results-*                       =")
print("======================================================================")

print("Running HyperMinHash-6-4-4 tests (64 buckets of 8 bits each, 4 bits of which are the LogLog counter")
# Initially run everything 8 times
hyperminhash_tests.hmh_test_range(11, 11, 2, 6, 4, 4, collision_correction="false", test_range=24, test_reps=8, prefix="full")  # Jaccard = 2/20 = 1/10
hyperminhash_tests.hmh_test_range(2, 2, 1, 6, 4, 4, collision_correction="false", test_range=27, test_reps=8, prefix="full")  # Jaccard = 1/3
hyperminhash_tests.hmh_test_range(3, 3, 2, 6, 4, 4, collision_correction="false", test_range=27, test_reps=8, prefix="full")  # Jaccard = 1/2
hyperminhash_tests.hmh_test_range(19, 19, 18, 6, 4, 4, collision_correction="false", test_range=24, test_reps=8, prefix="full")  # Jaccard = 18/20 = 9/10
# Then reduce the error for the low ranges where there might be overlap
hyperminhash_tests.hmh_test_range(11, 11, 2, 6, 4, 4, collision_correction="false", test_range=23, test_reps=8, prefix="full")  # Jaccard = 2/20 = 1/10
hyperminhash_tests.hmh_test_range(2, 2, 1, 6, 4, 4, collision_correction="false", test_range=26, test_reps=8, prefix="full")  # Jaccard = 1/3
hyperminhash_tests.hmh_test_range(3, 3, 2, 6, 4, 4, collision_correction="false", test_range=26, test_reps=8, prefix="full")  # Jaccard = 1/2
hyperminhash_tests.hmh_test_range(19, 19, 18, 6, 4, 4, collision_correction="false", test_range=23, test_reps=8, prefix="full")  # Jaccard = 18/20 = 9/10
# Then reduce the error for the low ranges where there might be overlap
hyperminhash_tests.hmh_test_range(11, 11, 2, 6, 4, 4, collision_correction="false", test_range=20, test_reps=16, prefix="full")  # Jaccard = 2/20 = 1/10
hyperminhash_tests.hmh_test_range(2, 2, 1, 6, 4, 4, collision_correction="false", test_range=23, test_reps=16, prefix="full")  # Jaccard = 1/3
hyperminhash_tests.hmh_test_range(3, 3, 2, 6, 4, 4, collision_correction="false", test_range=23, test_reps=16, prefix="full")  # Jaccard = 1/2
hyperminhash_tests.hmh_test_range(19, 19, 18, 6, 4, 4, collision_correction="false", test_range=20, test_reps=64, prefix="full")  # Jaccard = 18/20 = 9/10
# Then reduce the error for the low ranges where there might be overlap
hyperminhash_tests.hmh_test_range(11, 11, 2, 6, 4, 4, collision_correction="false", test_range=15, test_reps=64, prefix="full")  # Jaccard = 2/20 = 1/10
hyperminhash_tests.hmh_test_range(2, 2, 1, 6, 4, 4, collision_correction="false", test_range=18, test_reps=64, prefix="full")  # Jaccard = 1/3
hyperminhash_tests.hmh_test_range(3, 3, 2, 6, 4, 4, collision_correction="false", test_range=18, test_reps=64, prefix="full")  # Jaccard = 1/2
hyperminhash_tests.hmh_test_range(19, 19, 18, 6, 4, 4, collision_correction="false", test_range=15, test_reps=64, prefix="full")  # Jaccard = 18/20 = 9/10

print("Running MinHash-6-0-8 tests (64 buckets of 8 bits each)")
# Initially run everything 8 times
hyperminhash_tests.hmh_test_range(11, 11, 2, 6, 0, 8, collision_correction="false", test_range=24, test_reps=8, prefix="full")  # Jaccard = 2/20 = 1/10
hyperminhash_tests.hmh_test_range(2, 2, 1, 6, 0, 8, collision_correction="false", test_range=27, test_reps=8, prefix="full")  # Jaccard = 1/3
hyperminhash_tests.hmh_test_range(3, 3, 2, 6, 0, 8, collision_correction="false", test_range=27, test_reps=8, prefix="full")  # Jaccard = 1/2
hyperminhash_tests.hmh_test_range(19, 19, 18, 6, 0, 8, collision_correction="false", test_range=24, test_reps=8, prefix="full")  # Jaccard = 18/20 = 9/10
# Then reduce the error for the low ranges where there might be overlap
hyperminhash_tests.hmh_test_range(11, 11, 2, 6, 0, 8, collision_correction="false", test_range=23, test_reps=8, prefix="full")  # Jaccard = 2/20 = 1/10
hyperminhash_tests.hmh_test_range(2, 2, 1, 6, 0, 8, collision_correction="false", test_range=26, test_reps=8, prefix="full")  # Jaccard = 1/3
hyperminhash_tests.hmh_test_range(3, 3, 2, 6, 0, 8, collision_correction="false", test_range=26, test_reps=8, prefix="full")  # Jaccard = 1/2
hyperminhash_tests.hmh_test_range(19, 19, 18, 6, 0, 8, collision_correction="false", test_range=23, test_reps=8, prefix="full")  # Jaccard = 18/20 = 9/10
# Then reduce the error for the low ranges where there might be overlap
hyperminhash_tests.hmh_test_range(11, 11, 2, 6, 0, 8, collision_correction="false", test_range=20, test_reps=16, prefix="full")  # Jaccard = 2/20 = 1/10
hyperminhash_tests.hmh_test_range(2, 2, 1, 6, 0, 8, collision_correction="false", test_range=23, test_reps=16, prefix="full")  # Jaccard = 1/3
hyperminhash_tests.hmh_test_range(3, 3, 2, 6, 0, 8, collision_correction="false", test_range=23, test_reps=16, prefix="full")  # Jaccard = 1/2
hyperminhash_tests.hmh_test_range(19, 19, 18, 6, 0, 8, collision_correction="false", test_range=20, test_reps=64, prefix="full")  # Jaccard = 18/20 = 9/10
# Then reduce the error for the low ranges where there might be overlap
hyperminhash_tests.hmh_test_range(11, 11, 2, 6, 0, 8, collision_correction="false", test_range=15, test_reps=64, prefix="full")  # Jaccard = 2/20 = 1/10
hyperminhash_tests.hmh_test_range(2, 2, 1, 6, 0, 8, collision_correction="false", test_range=18, test_reps=64, prefix="full")  # Jaccard = 1/3
hyperminhash_tests.hmh_test_range(3, 3, 2, 6, 0, 8, collision_correction="false", test_range=18, test_reps=64, prefix="full")  # Jaccard = 1/2
hyperminhash_tests.hmh_test_range(19, 19, 18, 6, 0, 8, collision_correction="false", test_range=15, test_reps=64, prefix="full")  # Jaccard = 18/20 = 9/10

print("Running MinHash-5-0-16 tests (32 buckets of 16 bits each)")
# Initially run everything 8 times
hyperminhash_tests.hmh_test_range(11, 11, 2, 5, 0, 16, collision_correction="false", test_range=24, test_reps=8, prefix="full")  # Jaccard = 2/20 = 1/10
hyperminhash_tests.hmh_test_range(2, 2, 1, 5, 0, 16, collision_correction="false", test_range=27, test_reps=8, prefix="full")  # Jaccard = 1/3
hyperminhash_tests.hmh_test_range(3, 3, 2, 5, 0, 16, collision_correction="false", test_range=27, test_reps=8, prefix="full")  # Jaccard = 1/2
hyperminhash_tests.hmh_test_range(19, 19, 18, 5, 0, 16, collision_correction="false", test_range=24, test_reps=8, prefix="full")  # Jaccard = 18/20 = 9/10
# Then reduce the error for the low ranges where there might be overlap
hyperminhash_tests.hmh_test_range(11, 11, 2, 5, 0, 16, collision_correction="false", test_range=23, test_reps=8, prefix="full")  # Jaccard = 2/20 = 1/10
hyperminhash_tests.hmh_test_range(2, 2, 1, 5, 0, 16, collision_correction="false", test_range=26, test_reps=8, prefix="full")  # Jaccard = 1/3
hyperminhash_tests.hmh_test_range(3, 3, 2, 5, 0, 16, collision_correction="false", test_range=26, test_reps=8, prefix="full")  # Jaccard = 1/2
hyperminhash_tests.hmh_test_range(19, 19, 18, 5, 0, 16, collision_correction="false", test_range=23, test_reps=8, prefix="full")  # Jaccard = 18/20 = 9/10
# Then reduce the error for the low ranges where there might be overlap
hyperminhash_tests.hmh_test_range(11, 11, 2, 5, 0, 16, collision_correction="false", test_range=20, test_reps=16, prefix="full")  # Jaccard = 2/20 = 1/10
hyperminhash_tests.hmh_test_range(2, 2, 1, 5, 0, 16, collision_correction="false", test_range=23, test_reps=16, prefix="full")  # Jaccard = 1/3
hyperminhash_tests.hmh_test_range(3, 3, 2, 5, 0, 16, collision_correction="false", test_range=23, test_reps=16, prefix="full")  # Jaccard = 1/2
hyperminhash_tests.hmh_test_range(19, 19, 18, 5, 0, 16, collision_correction="false", test_range=20, test_reps=64, prefix="full")  # Jaccard = 18/20 = 9/10
# Then reduce the error for the low ranges where there might be overlap
hyperminhash_tests.hmh_test_range(11, 11, 2, 5, 0, 16, collision_correction="false", test_range=15, test_reps=64, prefix="full")  # Jaccard = 2/20 = 1/10
hyperminhash_tests.hmh_test_range(2, 2, 1, 5, 0, 16, collision_correction="false", test_range=18, test_reps=64, prefix="full")  # Jaccard = 1/3
hyperminhash_tests.hmh_test_range(3, 3, 2, 5, 0, 16, collision_correction="false", test_range=18, test_reps=64, prefix="full")  # Jaccard = 1/2
hyperminhash_tests.hmh_test_range(19, 19, 18, 5, 0, 16, collision_correction="false", test_range=15, test_reps=64, prefix="full")  # Jaccard = 18/20 = 9/10

print("======================================================================")
