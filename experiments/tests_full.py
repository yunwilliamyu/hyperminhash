# Testing code below
from __future__ import print_function
import hyperminhash_tests

print("======================================================================")
print("=    Running full tests to regenerate Figure 6 of paper              =")
print("=    Results will be printed to full_results-*                       =")
print("======================================================================")

print("Running HyperMinHash-8-4-4 tests (256 buckets of 8 bits each, 4 bits of which are the LogLog counter")
hyperminhash_tests.hmh_test_range(2, 2, 1, 8, 4, 4, collision_correction="false", test_range=30, test_reps=120, prefix="full")

print("Running MinHash-8-0-8 tests (256 buckets of 8 bits each)")
hyperminhash_tests.hmh_test_range(2, 2, 1, 8, 0, 8, collision_correction="false", test_range=29, test_reps=120, prefix="full")

print("Running MinHash-7-0-16 tests (256 buckets of 8 bits each)")
hyperminhash_tests.hmh_test_range(2, 2, 1, 7, 0, 16, collision_correction="false", test_range=19, test_reps=120, prefix="full")

print("======================================================================")
