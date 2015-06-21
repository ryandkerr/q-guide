# Ryan Kerr
# q-scraper.py
# python web scraper for the Harvard Q guide

from bs4 import BeautifulSoup
from urllib2 import urlopen
import csv

BASE_URL = "https://webapps.fas.harvard.edu/course_evaluation_reports/fas/list?yearterm=2014_1"

# helper for making soup
def make_soup(url):
  html = urlopen(url).read()
  s = BeautifulSoup(html, "lxml")
  return s

# takes base url and returns array of department drop-down pages
def get_class_links(section_url):
    soup = make_soup(section_url)
    print soup

    depts = soup.find_all("div", "course-block-head")
    print depts

    # triangles = soup.find_all("a", "remove_link")
    
    # print triangles

    # link_list = []
    # for triangle in triangles:
    #     link = triangle.get("href")
    #     if not l in link_list:
    #         link_list.append(link)
    link_list = []
    for dept in depts:
        d = dept.find("span")["title"]
        base = "https://webapps.fas.harvard.edu/course_evaluation_reports/fas/list?dept="
        link_list.append(base + d)

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
                classes.append(course.a["href"])

    return classes

all_classes = []

class_links = get_class_links(BASE_URL)

print class_links