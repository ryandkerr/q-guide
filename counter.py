# Ryan Kerr
# counter.py
# reads q-guide csv and counts most-used words

import csv
from collections import Counter

with open("data/test_q.csv", "rb") as test_csv:
    test = csv.reader(test_csv)
    for row in test:
        print row[3]
