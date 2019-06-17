#!/bin/bash
echo We are only regenerating the figure with the following command:
echo "    python3 ../experiments/error_plot_full.py"
echo ...
python3 ../experiments/error_plot_full.py
echo Figure regenerated as full_comparisons.png

echo =================
echo Should you wish to rerun all experiments, run the following:
echo "    python3 ../experiments/tests_full.py"
echo Note: this command will take days to weeks, depending on how
echo many cores you have available to you. You may edit the "test_reps"
echo parameters within the file to decrease runtime/decrease accuracy.
echo
echo Also, note that that command will append to the full_results-*
echo files present in this directory. Simply delete the existing 
echo full_results-* files to regenerate anew.


