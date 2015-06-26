# Ryan Kerr
# counter.py
# reads q-guide csv and counts most-used words

from __future__ import division
import csv
import json
import re
from collections import Counter

# reading in test data csv and creating dictionary
def count_row(row):
    all_words = []
    for review in row:
        words = re.findall(r'\w+', review)
        all_words += words
    lower_words = [word.lower() for word in all_words]
    d = Counter(lower_words)
    return d

def export_all(file_name):
    global pct_seas
    with open("data/course1.csv", "rb") as reader:
        read = csv.reader(reader)
        js_out = []
        for row in read:
            course_name = row[0]
            d = compare_dicts(pct_dict(count_row(row)), pct_seas)
            pruned = prune_dict(d, 40)
            r = [{"text":key, "size":value} for key,value in pruned.items()]
            j = [{"course": course_name, "reviews": r}]
            js_out.append(j)
        js = json.dumps(js_out)
        with open(file_name, "w") as export:
            print >> export, js

def export_test():
    with open("data/course1.csv", "rb") as test_csv:
        test = csv.reader(test_csv)
        all_words = []
        for row in test:
            if row[0] == "COMPSCI 109: Data Science":
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

def prune_dict(diction, n=None):
    d = dict(diction)
    prune_words = ["a", "the", "of", "in", "to", "an", "is", "if", "course",
                   "class", "for", "you", "i", "was", "were", "from", "and",
                   "this", "are", "be", "will"]
    for word in prune_words:
        try:
            del d[word]
        except KeyError:
            pass
    d = dict(Counter(d).most_common(n))
    return d

def make_json(file_name, diction):
    d = [{"text":key, "size":value} for key,value in diction.items()]
    j = json.dumps(d)
    with open(file_name, "w") as export:
        print >> export, j


seas = seas_dept()
pct_seas = pct_dict(seas)

# test1 = export_test()
# pct_test = pct_dict(test1)

# test_final = prune_dict(compare_dicts(pct_test, pct_seas), 40)
export_all("data/all_classes.json")

make_json("data/seas.json", pct_seas)
# make_json("data/test_adjusted.json", test_final)
