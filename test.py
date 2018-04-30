#!/usr/bin/env python3
import sys
import main

testFile = 'test.ics'
testLines = list(open(testFile))

def test_main():
    main.main(open(testFile), sys.stdout, sys.stderr)

def test_getTail():
    res = main._getTail(testLines)
    print(res)

def test_printRecords():
    main._printRecords(main._getRecords(testLines))

