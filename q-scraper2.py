# Ryan Kerr
# q-scraper.py
# python web scraper for the Harvard Q guide

from __future__ import print_function
from bs4 import BeautifulSoup
from urllib2 import urlopen
import requests
import csv

BASE_URL = "https://webapps.fas.harvard.edu/course_evaluation_reports/fas/list?yearterm=2014_1"
LOGIN_URL = "https://www.pin1.harvard.edu/cas/login?service=https%3A%2F%2Fwww.pin1.harvard.edu%2Fpin%2Fauthenticate%3F__authen_application%3DFAS_CS_COURSE_EVAL_REPORTS%26original_request%3D%252Fcourse_evaluation_reports%252Ffas%252Flist%253F"

# with help from Nikhil Benesch's gist:
# https://gist.github.com/benesch/43515655b1f877779522

# This session ID can be obtained by signing into the Q from your
# browser and inspecting the value of the JSESSIONID cookie. It expires
# frequently!
SESSION_ID = '6EA803C3E5E3B46999FA7A69CF2D3EEA'
 
# Q URLs
Q_BASE = "https://webapps.fas.harvard.edu/course_evaluation_reports/fas/"
Q_LIST = 'https://webapps.fas.harvard.edu/course_evaluation_reports/fas/list?yearterm=2014_1'

# helper for making soup using cookies
def make_soup(section_url): 
    session = requests.Session()
    session.cookies = requests.utils.cookiejar_from_dict({
        'JSESSIONID': SESSION_ID
    })
    session.verify = False
    request = session.get(section_url)
    return BeautifulSoup(request.text, "lxml")
 
# takes base url and returns array of department drop-down pages
def get_class_links(section_url):
    soup = make_soup(section_url)
    triangles = soup.find_all("a", "remove_link")
    link_list = []
    for triangle in triangles:
        link = triangle.get("href")
        l = Q_LIST + "&" + link.split("?")[-1]
        if not l in link_list:
            link_list.append(l)
    return link_list

def get_classes(section_url):
    soup = make_soup(section_url)
    selected_dept = section_url.split("#")[-1]
    depts = soup.find_all("div", "course-block")
    classes = []
    for dept in depts:
        if dept.find("span", "course-block-title")["title"] == selected_dept:
            # now dept is the course-block of our department
            courses = dept.find_all("li", "course")
            for course in courses:
                c = Q_BASE + course.a["href"]
                classes.append(c)
    return classes

def get_reviews(section_url):
    course_id = section_url.split("?")[-1]
    review_link = Q_BASE + "view_comments.html?" + course_id + "&qid=1487&sect_num="
    soup = make_soup(review_link)
    course_name = soup.find("h1").get_text(strip=True)
    review_elts = soup.find_all("p")
    reviews = map(lambda x: x.get_text(strip=True), review_elts) 
    # this is because first two <p> elements are not reviews
    return (course_name, reviews[2:])

# all_classes = []

class_links = get_class_links(Q_LIST)

dept_classes = get_classes(class_links[14])

class1 = get_reviews(dept_classes[1])


with open("data/course1.csv", "wb") as csvout:
    writer = csv.writer(csvout)
    row = [class1[0]]
    for c in class1[1]:
        row.append(c)
    writer.writerow(row)

# for i, link in enumerate(class_links):
#     if link == "https://webapps.fas.harvard.edu/course_evaluation_reports/fas/list?yearterm=2014_1&dept=Engineering and Applied Sciences#Engineering and Applied Sciences":
#         print(i)