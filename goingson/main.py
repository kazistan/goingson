#!/usr/bin/python

# Import Modules
from __future__ import print_function
import sys
import os
import pandas as pd
import datetime
from politics import commonwealth as cwc, worldaffairs as wac
from music import anotherplanet as ape, fillmore as fillmore, sfsymphony as sfs
from art import sfmoma as moma


# Main Function
def main():

    # Print Begin to Cmdline
    sys.stdout.write("%s\n" % ('-' * len('Goings On About San Francisco')) +
                     "Goings On About \033[94mSan Francisco\033[0m\n" +
                     "%s\n" % ('-' * len('Goings On About San Francisco')))

    # Define Empty List to Build Goings On Calendar
    goingson = []

    # Politics
    sys.stdout.write("\n%-20s\n" % ('-'*((20-len(' Politics '))/2) + ' Politics ' + '-'*((20-len(' Politics '))/2)))
    goingson.append(cwc.commonwealthXML())  # Commonwealth Club
    goingson.append(wac.worldaffairsXML())  # World Affairs Council

    # Music
    sys.stdout.write("\n%-20s\n" % ('-' * ((20 - len(' Music ')) / 2) + ' Music ' + '-' * ((20 - len(' Music ')) / 2)))
    goingson.append(ape.apentertainmentHTML())  # Another Planet Entertainment
    goingson.append(fillmore.fillmoreHTML())  # The Fillmore
    goingson.append(sfs.sfsymphonyHTML())  # SF Symphony

    # Art
    sys.stdout.write("\n%-20s\n" % ('-' * ((20 - len(' Art ')) / 2) + ' Art ' + '-' * ((20 - len(' Art ')) / 2)))
    goingson.append(moma.sfmomaHTML())  # SFMoMA

    # Combine Result
    goingson = pd.concat(goingson, axis=0)
    goingson.sort_values('date', inplace = True)
    goingson.index = range(len(goingson.index))

    # Restrict to Current/Future Events
    dt = datetime.datetime.today()
    goingson = goingson[goingson.date >= datetime.date(dt.year, dt.month, dt.day)]

    # Output Results
    try:
        arg1 = sys.argv[1]
    except IndexError:
        print("Usage: main.py <directory>")
        sys.exit(1)

    assert os.path.isdir(arg1), '<directory> is not absolute path: %r' % arg1

    goingson.to_csv(arg1 + 'goingson.csv')
    sys.stdout.write('\nFile saved to: %sgoingson.csv\n' % arg1)

    return


if __name__ == '__main__':
    main()