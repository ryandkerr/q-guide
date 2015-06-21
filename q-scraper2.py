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


# br = Browser()
# br.open(LOGIN_URL)

# br.select_form(nr = 0)
# br["username"] = "20904151"
# br["password"] = "password"
# log_in = br.submit()

# print log_in.read()


# with help from Nikhil Benesch's gist:
# https://gist.github.com/benesch/43515655b1f877779522

# This session ID can be obtained by signing into the Q from your
# browser and inspecting the value of the JSESSIONID cookie. It expires
# frequently!
SESSION_ID = '6EA803C3E5E3B46999FA7A69CF2D3EEA'
 
# Q URLs
Q_ROOT = 'https://webapps.fas.harvard.edu/course_evaluation_reports/fas/list?yearterm=2014_1'

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
        l = Q_ROOT + "&" + link.split("?")[-1]
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
                c = "https://webapps.fas.harvard.edu/course_evaluation_reports/fas/" + course.a["href"]
                classes.append(c)

    return classes

# all_classes = []

class_links = get_class_links(Q_ROOT)

dept_classes = get_classes(class_links[0])

print(dept_classes)
