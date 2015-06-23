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


            c = Counter(all_words)
            total_words = sum(c.itervalues())

            # to change value for each dictionary item
            # for key in c:
            #     c[key] *= 2
