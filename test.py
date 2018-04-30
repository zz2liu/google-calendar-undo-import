#!/usr/bin/env python3
# run test: pytest test.py -sv
import sys
import main

testFile = 'test.ics'
testLines = list(open(testFile))

def _test_main():
    main.main(open(testFile), sys.stdout, sys.stderr)

def test_getHead():
    res = main._getHead(testLines)
    print(res)

def test_getTail():
    res = main._getTail(testLines)
    print(res)

def test_getRecords():
    res = list(main._getRecords(testLines))
    print(res)
    # senity check
    lines = [line for rec in res for line in rec] 
    resAgain = list(main._getRecords(lines))
    assert resAgain == res

def test__printRecords():
    main._printRecords(main._getRecords(testLines))

def test_printRecords_less():
    recs = list(main._getRecords(testLines))
    main.printRecords(recs)

def test_printRecords_more():
    recs = list(main._getRecords(testLines))
    main.printRecords(recs + recs)

def test_parseRecordPlus():
    comps = list(main._parseRecordPlus(testLines))
    print(comps)

def test_main_new():
    main.main_new(testLines, outfile=open('tmp.ics','w'))

