#!/usr/bin/env python2

import sys
import csv
import os

import random

__INPUT_DIR__ = "../mndo_input/"

__WORKERS__ = 8

def parse_keys(filename):

    keys = []
    with open(filename, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            if "name" in row:
                continue
            keys.append(row[0])

    return keys

def merge_keys(keys, master_filename):

    with open(master_filename, 'w') as outfile:
        for key in keys:

            fname = __INPUT_DIR__ + key + ".inp"

            with open(fname) as infile:
                outfile.write(infile.read())



if __name__ == "__main__":

    csv_file = sys.argv[1]

    keys = parse_keys(csv_file)

    print len(keys)

    for run in range(10):

        for size in [1000, 2000, 4000, 8000]:

            random.shuffle(keys)

            dir_name = "%4i_%02i" % (size, run)

            os.mkdir(dir_name)

            for tid in range(1, __WORKERS__+1):

                start = (tid - 1) * size // __WORKERS__
                end = tid * size // __WORKERS__
                master = keys[start:end]

                master_filename = dir_name + "/master%i.inp" % (tid)
                print master_filename
                merge_keys(master, master_filename)

                print start, end

            test_filename = dir_name + "/test.inp"
            test = keys[end:]
            merge_keys(test, test_filename)
