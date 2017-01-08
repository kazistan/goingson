#!/usr/bin/python

# Import Modules
from __future__ import print_function
import sys
import os
from politics import commonwealth as cwc, worldaffairs as wac
import xmllist as xml_list
import pandas as pd

# Main Function
def main():

    # Define Empty List to Build Goings On Calendar
    goingson = []

    # Load Commonwealth Club Data
    goingson.append(cwc.commonwealthXML(xml_list.cwc))

    # Load World Affairs Council Data
    goingson.append(wac.worldaffairsXML(xml_list.wac))

    # Combine Result
    goingson = pd.concat(goingson, axis=0)
    goingson.sort_values('date', inplace = True)
    goingson.index = range(len(goingson.index))

    # Output Results
    try:
        arg1 = sys.argv[1]
    except IndexError:
        print("Usage: main.py <directory>")
        sys.exit(1)

    assert os.path.isdir(arg1), '<directory> is not absolute path: %r' % arg1

    goingson.to_csv(arg1 + 'goingson.csv')

    pass


if __name__ == '__main__':
    main()