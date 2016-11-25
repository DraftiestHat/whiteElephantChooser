#!/usr/bin/python
import argparse
import string
import random
import re
import sys

parser = argparse.ArgumentParser(description='Takes lists of people and randomly matches them with other people. You can also have another file of people that are disallowed from giving each other things.',fromfile_prefix_chars='@')
parser.add_argument("people")
parser.add_argument("noteq")

numErrs = 0

args = parser.parse_args()

ppl = open(args.people, 'r')
neq = open(args.noteq, 'r')

names = set()
nAllowed = set()

for line in ppl:
    nameList = re.split(';|,|\|',line)
    for name in nameList:
        if (name.strip() != ""):
            names.add(name.strip())

for line in neq:
    m = dict()
    nameToList = re.split(':', line)
    notAllowed = re.split(',;',nameToList[1])
    if nameToList[0] not in names:
        print nameToList[0] + " is not in the list of names!"
        numErrs+=1
    m[nameToList[0]] = notAllowed

if numErrs > 0:
    sys.exit()

removed = set()
choices = dict()
b = True

while b:
    try:
        for name in names:
            try:
                notAllowed = m[name]
            except Exception:
                pass
            x = set()
            for other in names:
                if name != other and other not in notAllowed and other not in removed:
                    x.add(other)
            choices[name] = random.choice(list(x))
            removed.add(choices[name])
        b = False
    except Exception:
        removed.clear()
        choices.clear()
        print "Nope"

for key in choices:
    print key + " gets " + choices[key]
