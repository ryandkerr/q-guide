# Ryan Kerr
# counter.py
# reads q-guide csv and counts most-used words

import csv
import re
from collections import Counter

with open("data/test_q.csv", "rb") as test_csv:
    test = csv.reader(test_csv)
    for row in test:
        if row[0] == "APCOMP 209: Data Science":
            all_words = []
            for i, review in enumerate(row):
                words = re.findall(r'\w+', review)
                all_words += words


            print all_words



            # c = Counter(row)
            # print c