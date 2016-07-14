#!/usr/bin/env bash
# Execute the python script payment_median_degree.py 
# Rolling median calculations are performed in this script.
# Pass input and outupt file names using -i and -o parameters
# Input Directory: ./venmo_input
# output Directory: ./venmo_output
#
date
python ./src/payment_median_degree.py -i ./venmo_input/venmo-trans.txt -o ./venmo_output/output.txt

