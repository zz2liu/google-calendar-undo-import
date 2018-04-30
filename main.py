#!/usr/bin/env python3
USAGE = '''python PROG.py original.ics > cleaned.ics'''
import sys
from datetime import date

# config
importDate = '' #example '2018-04-30', default=today
flagRecBegin = 'BEGIN:VEVENT'
flagRecEnd = 'END:VEVENT'
flagRecPrint = ('SUMMARY:', 'DTSTART')
nRecPrint = 5 #the first and last n records to be printed.

# begin
importDate = importDate or date.today().isoformat().replace('-','')
flagRecRemove = f'CREATED:{importDate.replace("-", "")}'
isRecBegin = lambda x: x.startswith(flagRecBegin)
isRecEnd = lambda x: x.startswith(flagRecEnd)

def isImported(rec):
    for line in rec:
        if line.startswith(flagRecRemove):
            return True

def _getHead(lines):
    res = []
    for line in lines:
        if isRecBegin(line):
            return res
        res.append(line)

def _getTail(lines):
    res = []
    for line in lines:
        res.append(line)
        if isRecEnd(line):
            res = []
    return res

def _getRecords(lines):
    curr = []
    for line in lines:
        if isRecBegin(line):
            curr = []
        curr.append(line)
        if isRecEnd(line):
            yield curr

def _getTail(lines):
    res = []
    for line in lines:
        res.append(line)
        if isRecEnd(line):
            res = []
    return res

def _getRecords(lines):
    curr = []
    for line in lines:
        if isRecBegin(line):
            curr = []
        curr.append(line)
        if isRecEnd(line):
            yield curr
def parseFile(lines):
    head = _getHead(lines)
    records = _getRecords(lines)
    tail = _getTail(lines)
    return head, records, tail

def filterRecs(records):
    for rec in records:
        if not isImported(rec):
            yield rec

def writeFile(head, cleaned, tail, outfile):
    outfile.writelines(head)
    for res in cleaned:
        outfile.writelines(res)
    outfile.writelines(tail)

def _printRecords(records, file=sys.stderr):
    for rec in records:
        for line in rec:
            if line.startswith(flagRecPrint):
                file.write(line)
        file.write('\n')

def printRecords(records, file=sys.stderr):
    if len(records) <= nRecPrint*2:
        _printRecords(records, file=file)
    else:
        _printRecords(records[:nRecPrint], file=file)
        print('...\n', file=file)
        _printRecords(records[-nRecPrint:], file=file)

def main(lines, outfile, errfile): #, importDate=''):
    lines = list(lines)
    head, records, tail = parseFile(lines)

    # for message
    records = list(records)
    cleaned = list(filterRecs(records))
    print(f'{len(cleaned)}/{len(records)} left after removing events with {flagRecRemove}.\n', file=errfile)
    printRecords(cleaned)

    # output
    writeFile(head, cleaned, tail, outfile)

###############################################################
# Next: a simplified version, tested
def _parseRecordPlus(lines):
    curr = []
    for line in lines:
        if isRecBegin(line):
            if curr:
                yield curr, False #header/median
            curr = []
        curr.append(line)
        if isRecEnd(line):
            yield curr, True #record: no valid check of beginning
    if curr:
        yield curr, False #tailer

def main_new(lines, outfile=sys.stdout, errfile=sys.stderr): #, importDate=''):
    count = 0
    for c, is_rec in _parseRecordPlus(lines):
        if is_rec and isImported(c):
            count += 1
        else:
            outfile.writelines(c)
    print(f'{count} records with {flagRecRemove} removed.', file=errfile)

if __name__ == '__main__':
    args = sys.argv[1:]
    #global importDate

    if len(args) == 1:
        fromFile, = sys.argv[1:]
    #elif len(args) == 2:
    #    fromFile, importDate = sys.argv[1:]
    else:
        print(USAGE, file=sys.stderr)

    main(open(fromFile), sys.stdout, sys.stderr) # importDate)


