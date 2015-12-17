
# coding: utf-8

# ### Helpers and librares

# In[126]:

# Ryan Kerr
# q-scraper2.py
# python web scraper for the Harvard Q guide

from bs4 import BeautifulSoup
import time
import random
import os
import requests
import pdb

BASE_URL = "https://webapps.fas.harvard.edu/course_evaluation_reports/fas/list?yearterm=2014_1"

# with help from Nikhil Benesch's gist:
# https://gist.github.com/benesch/43515655b1f877779522
# This session ID can be obtained by signing into the Q from your
# browser and inspecting the value of the JSESSIONID cookie. It expires
# frequently!
SESSION_ID = '84EEB5679A1FBDC22F7B3FB4E22FC452'
 
# Q URLs
Q_BASE = "https://webapps.fas.harvard.edu/course_evaluation_reports/fas/"
Q_LIST = 'https://webapps.fas.harvard.edu/course_evaluation_reports/fas/list?yearterm=2014_1'

# helper for getting page source using cookies
def get_page_source(section_url):
    session = requests.Session()
    session.cookies = requests.utils.cookiejar_from_dict({
        'JSESSIONID': SESSION_ID
    })
    session.verify = False
    try:
        request = session.get(section_url)
        return request.text
    except requests.exceptions.ConnectionError:
        print "Connection Refused, waiting 3 minutes and trying again"
        time.sleep(180)
        return get_page_source(section_url)
 


# #### Actually scrape the pages for a given year

# In[128]:

"""
The soution here is not elegant but it works. Go to the
q page for a given semester and click all of the arrows
to expand each department. Then "save as" the page to the
data folder for this project. This way we can access all
of the course links (because they need to be expanded
manually).
"""
courses = []
with open("data/Course Evaluations_ Course Page_spring2015.html", "r") as f:
    html = f.read()
    soup = BeautifulSoup(html, "lxml")
    courses = soup.find_all("li", attrs={"class": "course"})
course_urls = map(lambda x: x.find("a")["href"], courses)
course_ids  = map(lambda x: x[-5:], course_urls)

# create folder to store scraped pages
semester = "2015_spring"
file_dump = semester + "_pages"
if not os.path.exists(file_dump):
    os.mkdir(file_dump)

# save all scraped class pages
for i, course_url in enumerate(course_urls):
    # this if statement is so we can restart after
    # connction errors from the page we left off
    if i >= 0:
        print str(i) + " / " + str(len(course_urls)) 
        time.sleep(2 + random.uniform(0.0, 3.0))

        # save original page with aggregate statistics
        with open(file_dump+"/class"+str(i)+"main.txt", "wb") as f:
            f.write(get_page_source(course_url).encode("ascii", "ignore"))

        time.sleep(2 + random.uniform(0.0, 3.0))
        course_id = course_url[-5:]
        review_url = "https://webapps.fas.harvard.edu/course_evaluation_reports/fas/view_comments.html?course_id=" + str(course_id) + "&qid=1487&sect_num=" 

        # this scrapes the page with all student reviews
        with open(file_dump+"/class"+str(i)+"reviews.txt", "wb") as f:
            f.write(get_page_source(review_url).encode("ascii", "ignore"))

