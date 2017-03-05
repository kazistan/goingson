#!/usr/bin/python

# Import Modules
from __future__ import print_function
import sys
import os
import xmllist as xml_list
import pandas as pd
import datetime
from politics import commonwealth as cwc, worldaffairs as wac
from music import anotherplanet as ape, fillmore as fillmore, sfsymphony as sfs
from art import sfmoma as moma


# Main Function
def main():

    # Define Empty List to Build Goings On Calendar
    goingson = []

    # Politics
    sys.stdout.write("\n%-20s\n" % ('-'*((20-len(' Politics '))/2) + ' Politics ' + '-'*((20-len(' Politics '))/2)))
    goingson.append(cwc.commonwealthXML(xml_list.cwc))  # Commonwealth Club
    sys.stdout.write("[%-2s] %s\n" % ('\033[92m' + 'ok' + '\033[0m', 'Commonwealth Club'))
    goingson.append(wac.worldaffairsXML(xml_list.wac))  # World Affairs Council
    sys.stdout.write("[%-2s] %s\n" % ('\033[92m' + 'ok' + '\033[0m', 'World Affairs Council'))

    # Music
    sys.stdout.write("\n%-20s\n" % ('-' * ((20 - len(' Music ')) / 2) + ' Music ' + '-' * ((20 - len(' Music ')) / 2)))
    goingson.append(ape.apentertainmentHTML(xml_list.ape))  # Another Planet Entertainment
    sys.stdout.write("[%-2s] %s\n" % ('\033[92m' + 'ok' + '\033[0m', 'Another Planet Entertainment'))
    goingson.append(fillmore.fillmoreHTML(xml_list.fillmore))  # The Fillmore
    sys.stdout.write("[%-2s] %s\n" % ('\033[92m' + 'ok' + '\033[0m', 'The Fillmore'))
    goingson.append(sfs.sfsymphonyHTML()) # SF Symphony

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

    return


if __name__ == '__main__':
    main()