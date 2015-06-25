# Ryan Kerr
# counter.py
# reads q-guide csv and counts most-used words

from __future__ import division
import csv
import json
import re
from collections import Counter

# reading in test data csv and creating dictionary
def export_test():
    with open("data/test_q.csv", "rb") as test_csv:
        test = csv.reader(test_csv)
        all_words = []
        for row in test:
            if row[0] == "APCOMP 209: Data Science":
                for i, review in enumerate(row):
                    words = re.findall(r'\w+', review)
                    all_words += words
        lower_words = [word.lower() for word in all_words]
        d = Counter(lower_words)
        return d

def seas_dept():
    with open("data/course1.csv", "rb") as input:
        reader = csv.reader(input)
        all_words = []
        for row in reader:
            for i, review in enumerate(row):
                words = re.findall(r'\w+', review)
                all_words += words
        lower_words = [word.lower() for word in all_words]
        d = Counter(lower_words)
        return d

# functional-esque programming in python!
def pct_dict(diction):
    d = dict(diction)
    total_words = sum(d.itervalues())
    for key in d:
        d[key] /= total_words
    return d

def compare_dicts(d1, d2):
    d = dict(d1)
    for key in d:
        d[key] -= d2[key]
    return d

def make_json(file_name, diction):
    d = [{"text":key, "size":value} for key,value in diction.items()]
    j = json.dumps(d)
    with open(file_name, "w") as export:
        print >> export, j


seas = seas_dept()
pct_seas = pct_dict(seas)

test1 = export_test()
pct_test = pct_dict(test1)

test_final = compare_dicts(pct_test, pct_seas)

make_json("data/seas.json", pct_seas)
make_json("data/test_adjusted.json", test_final)
