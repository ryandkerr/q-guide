
# coding: utf-8

# In[79]:

from bs4 import BeautifulSoup
import numpy as np
import csv
import pdb
import os


# In[84]:

review1 = ""
with open("2015_spring_pages/class0main.txt") as f:
    review1 = BeautifulSoup(f.read(), "lxml")

review990 = ""
with open("2015_spring_pages/class990main.txt") as f:
    review990 = BeautifulSoup(f.read(), "lxml")


# Class name

# In[49]:

review1.find("h1").text.encode("ascii")


# Summary Statistics

# In[76]:

t = review1.find("div", attrs={"id": "summaryStats"}).text.split("\n")
t = map(lambda x: x.strip(" "), t)
print "Enrollment:", t[2]
print "Reviews:   ", t[4]


# Overall Scores

# In[29]:

overall = review1.find("td", text="Course Overall")


# In[61]:

score_dist = overall.next_sibling
score_dist.find("img")["alt"].split(" ")[1:6]


# In[31]:

num_reviews = score_dist.next_sibling
int(num_reviews.text)


# In[32]:

mean_score = num_reviews.next_sibling
float(mean_score.text)


# Workload

# In[50]:

workload = review1.find("td", text="Workload (hours per week)")


# In[62]:

workload_dist = workload.next_sibling
workload_dist.find("img")["alt"].split(" ")[1:6]


# In[43]:

workload_responses = workload_dist.next_sibling
int(workload_responses.text)


# In[46]:

mean_workload = workload_responses.next_sibling
float(mean_workload.text)


# Recommendation

# In[51]:

recommend = review1.find("td", text="Would You Recommend")


# In[63]:

recommend_dist = recommend.next_sibling
recommend_dist.find("img")["alt"].split(" ")[1:6]


# In[56]:

recommend_responses = recommend_dist.next_sibling
int(recommend_responses.text)


# In[57]:

mean_recommend = recommend_responses.next_sibling
float(mean_recommend.text)


# In[78]:

get_ipython().run_cell_magic(u'bash', u'', u'grep "error encountered" 2015_spring_pages/*')


# From the above search we see that there are 14 classes where an error occurred getting results. However, the error occurred for both the summary statistisc page and the student reviews page, which suggests that the error did not have to do with improper scraping, but somethin on Harvard's end

# ### Actual parsing script

# In[107]:

def make_soup(file_path):
    with open(file_path, "rb") as f:
        html = f.read()
        soup = BeautifulSoup(html, "lxml")
        return soup
    
def broken_page(soup):
    """Returns True if the page was broken/did not have grades"""
    ps = soup.find_all("p")
    ps = map(lambda x: x.text, ps)
    unexpected_error = True in map(lambda x: "unexpected error" in x, ps)
    
    no_grades = soup.find("div", id="nogrades") != None    
    return no_grades or unexpected_error
    


# In[109]:

with open("data/2015_spring_summaries.csv", "wb") as csvout:
    writer = csv.writer(csvout)
    writer.writerow(["course",
                     "semester",
                     "enrolled",
                     "reviews",
                     "o1",
                     "o2",
                     "o3",
                     "o4",
                     "o5",
                     "overall_reviews",
                     "overall_mean",
                     "w1",
                     "w2",
                     "w3",
                     "w4",
                     "w5",
                     "workload_reviews",
                     "workload_mean",
                     "r1",
                     "r2",
                     "r3",
                     "r4",
                     "r5",
                     "recommend_reviews",
                     "recommend_mean"])
    
    target_dir = "2015_spring_pages/"
    target_semester = "spring 2015"
    
    # for class file in directory
    for fname in os.listdir(target_dir):
        if "main" in fname:
            fpath = target_dir + fname
            soup = make_soup(fpath)
            
            # search to see if error page
            if not broken_page(soup):
                # parse info from page
                try:
                    course = soup.find("h1").text.encode("ascii")
                except:
                    pdb.set_trace()
                    
                semester = target_semester
                
                t = soup.find("div", attrs={"id": "summaryStats"}).text.split("\n")
                t = map(lambda x: x.strip(" "), t)
                enrolled = t[2]
                reviews  = t[4]
                
                # overall rating scores
                o = soup.find("td", text="Course Overall")
                o_dist = o.next_sibling.find("img")["alt"].split(" ")[1:6]
                overall_reviews = int(o.next_sibling.next_sibling.text)
                overall_mean = float(o.next_sibling.next_sibling.next_sibling.text)
                
                # workload scores
                try:
                    w = soup.find("td", text="Workload (hours per week)")
                    w_dist = w.next_sibling.find("img")["alt"].split(" ")[1:6]
                    workload_reviews = int(w.next_sibling.next_sibling.text)
                    workload_mean = float(w.next_sibling.next_sibling.next_sibling.text)
                except:
                    w_dist = [0, 0, 0, 0, 0]
                    workload_reviews = 0
                    workload_mean = None
                
                # recommendation scores
                r = soup.find("td", text="Would You Recommend")
                r_dist = r.next_sibling.find("img")["alt"].split(" ")[1:6]
                recommend_reviews = int(r.next_sibling.next_sibling.text)
                recommend_mean = float(r.next_sibling.next_sibling.next_sibling.text)
                
                writer.writerow([course,
                                 semester,
                                 enrolled,
                                 reviews,
                                 o_dist[0],
                                 o_dist[1],
                                 o_dist[2],
                                 o_dist[3],
                                 o_dist[4],
                                 overall_reviews,
                                 overall_mean,
                                 w_dist[0],
                                 w_dist[1],
                                 w_dist[2],
                                 w_dist[3],
                                 w_dist[4],
                                 workload_reviews,
                                 workload_mean,
                                 r_dist[0],
                                 r_dist[1],
                                 r_dist[2],
                                 r_dist[3],
                                 r_dist[4],
                                 recommend_reviews,
                                 recommend_mean])

