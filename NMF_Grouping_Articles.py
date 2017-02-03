#import the stuff you need
import numpy as np
import pandas as pd
import nltk
import re
import codecs
from sklearn import feature_extraction
import mpld3
import os
from bs4 import BeautifulSoup 
import urllib

os.chdir('/Users/berkayadlim/Desktop/Project_Scrape')

#I will first scrape the articles, then do some cleaning, then apply the algorithm, and finally will display output
#super not-pythonic stuff going on here. i didn't have time. 



_01_2014=[]
_02_2014=[]
_03_2014=[]
_04_2014=[]
_05_2014=[]
_06_2014=[]
_07_2014=[]
_08_2014=[]
_09_2014=[]
_10_2014=[]
_11_2014=[]
_12_2014=[]
_01_2015=[]
_02_2015=[]
_03_2015=[]
_04_2015=[]
_05_2015=[]
_06_2015=[]
_07_2015=[]
_08_2015=[]
_09_2015=[]
_10_2015=[]
_11_2015=[]
_12_2015=[]
_01_2016=[]
_02_2016=[]
_03_2016=[]
_04_2016=[]
_05_2016=[]
_06_2016=[]
_07_2016=[]
_08_2016=[]
_09_2016=[]
_10_2016=[]
_11_2016=[]
_12_2016=[]
_01_2017=[]


#you don't necessarily need the first page for this analysis, so let's only do rest of the pages
parsing_list=[] 
soup_list=[] 
content_list=range(0,182)



i=0
x=0

for x in range(183): 
    soup_list.append("soup"+str(x+1))

for i in range(183): 
    parsing_list.append("p"+str(i+1))

a=0

for a in range(0,182): 
    parsing_list[a]=urllib.urlopen("http://www.reuters.com/news/archive/turkey?view=page&page=" + str(a+2) + "&pageSize=10").read()
    soup_list[a]=BeautifulSoup(parsing_list[a],"lxml")
    content_list[a]=soup_list[a].find_all("div",class_="story-content")    

rest_of_pages={} 

prefix="http://www.reuters.com" 

b=0

while b<len(content_list): 
    for element in content_list[b]:
        date = element.find(class_="timestamp").get_text()
    # Date already exists, add dictionary of link and summary to list of articles for the day
        if date in rest_of_pages.keys():
            rest_of_pages[date].append({"link": prefix + element.a["href"], "summary": element.p.get_text()})
    # Date does not exist, create a list of dictionaries for that date
        else:
            rest_of_pages[date]=[{"link": prefix + element.a["href"], "summary": element.p.get_text()}]

     
    b+=1       


from datetime import datetime
    
    
rest_of_pages_x={datetime.strptime(k,'%b %d %Y'):v for k,v in rest_of_pages.items()} #convert keys to datetime format so you can boolean

#start grouping the articles. tedious stuff ahead. 

#first, put the links of articles written in same months in the same lists 

for key,value in rest_of_pages_x.iteritems():
    if datetime(2014,1,1,0,0)<=key<=datetime(2014,1,31,0,0):
        _01_2014.append(value)
                    

for key,value in rest_of_pages_x.iteritems():
    if datetime(2014,2,1,0,0)<=key<=datetime(2014,2,28,0,0):
        _02_2014.append(value)

for key,value in rest_of_pages_x.iteritems():
    if datetime(2014,3,1,0,0)<=key<=datetime(2014,3,31,0,0):
        _03_2014.append(value)
        
for key,value in rest_of_pages_x.iteritems():
    if datetime(2014,4,1,0,0)<=key<=datetime(2014,4,30,0,0):
        _04_2014.append(value)

for key,value in rest_of_pages_x.iteritems():
    if datetime(2014,5,1,0,0)<=key<=datetime(2014,5,31,0,0):
        _05_2014.append(value)
for key,value in rest_of_pages_x.iteritems():
    if datetime(2014,6,1,0,0)<=key<=datetime(2014,6,30,0,0):
        _06_2014.append(value)
        
for key,value in rest_of_pages_x.iteritems():
    if datetime(2014,7,1,0,0)<=key<=datetime(2014,7,31,0,0):
        _07_2014.append(value)

for key,value in rest_of_pages_x.iteritems():
    if datetime(2014,8,1,0,0)<=key<=datetime(2014,8,31,0,0):
        _08_2014.append(value)
        
for key,value in rest_of_pages_x.iteritems():
    if datetime(2014,9,1,0,0)<=key<=datetime(2014,9,30,0,0):
        _09_2014.append(value)
        
for key,value in rest_of_pages_x.iteritems():
    if datetime(2014,10,1,0,0)<=key<=datetime(2014,10,31,0,0):
        _10_2014.append(value)
        
for key,value in rest_of_pages_x.iteritems():
    if datetime(2014,11,1,0,0)<=key<=datetime(2014,11,30,0,0):
        _11_2014.append(value)

for key,value in rest_of_pages_x.iteritems():
    if datetime(2014,12,1,0,0)<=key<=datetime(2014,12,31,0,0):
        _12_2014.append(value)

for key,value in rest_of_pages_x.iteritems():
    if datetime(2015,1,1,0,0)<=key<=datetime(2015,1,31,0,0):
        _01_2015.append(value)
        
for key,value in rest_of_pages_x.iteritems():
    if datetime(2015,2,1,0,0)<=key<=datetime(2015,2,28,0,0):
        _02_2015.append(value)

for key,value in rest_of_pages_x.iteritems():
    if datetime(2015,3,1,0,0)<=key<=datetime(2015,3,31,0,0):
        _03_2015.append(value)

for key,value in rest_of_pages_x.iteritems():
    if datetime(2015,4,1,0,0)<=key<=datetime(2015,4,30,0,0):
        _04_2015.append(value)
        
for key,value in rest_of_pages_x.iteritems():
    if datetime(2015,5,1,0,0)<=key<=datetime(2015,5,31,0,0):
        _05_2015.append(value)

for key,value in rest_of_pages_x.iteritems():
    if datetime(2015,6,1,0,0)<=key<=datetime(2015,6,30,0,0):
        _06_2015.append(value)
for key,value in rest_of_pages_x.iteritems():
    if datetime(2015,7,1,0,0)<=key<=datetime(2015,7,31,0,0):
        _07_2015.append(value)
for key,value in rest_of_pages_x.iteritems():
    if datetime(2015,8,1,0,0)<=key<=datetime(2015,8,31,0,0):
        _08_2015.append(value)

for key,value in rest_of_pages_x.iteritems():
    if datetime(2015,9,1,0,0)<=key<=datetime(2015,9,30,0,0):
        _09_2015.append(value)
        
for key,value in rest_of_pages_x.iteritems():
    if datetime(2015,10,1,0,0)<=key<=datetime(2015,10,31,0,0):
        _10_2015.append(value)
        
for key,value in rest_of_pages_x.iteritems():
    if datetime(2015,11,1,0,0)<=key<=datetime(2015,11,30,0,0):
        _11_2015.append(value)
        
for key,value in rest_of_pages_x.iteritems():
    if datetime(2015,12,1,0,0)<=key<=datetime(2015,12,31,0,0):
        _12_2015.append(value)
        
for key,value in rest_of_pages_x.iteritems():
    if datetime(2016,1,1,0,0)<=key<=datetime(2016,1,31,0,0):
        _01_2016.append(value)

for key,value in rest_of_pages_x.iteritems():
    if datetime(2016,2,1,0,0)<=key<=datetime(2016,2,28,0,0):
        _02_2016.append(value)        
for key,value in rest_of_pages_x.iteritems():
    if datetime(2016,3,1,0,0)<=key<=datetime(2016,3,31,0,0):
        _03_2016.append(value)
for key,value in rest_of_pages_x.iteritems():
    if datetime(2016,4,1,0,0)<=key<=datetime(2016,4,30,0,0):
        _04_2016.append(value)        

for key,value in rest_of_pages_x.iteritems():
    if datetime(2016,5,1,0,0)<=key<=datetime(2016,5,31,0,0):
        _05_2016.append(value)        
        
for key,value in rest_of_pages_x.iteritems():
    if datetime(2016,6,1,0,0)<=key<=datetime(2016,6,30,0,0):
        _06_2016.append(value)        
        
for key,value in rest_of_pages_x.iteritems():
    if datetime(2016,7,1,0,0)<=key<=datetime(2016,7,31,0,0):
        _07_2016.append(value)        
        
for key,value in rest_of_pages_x.iteritems():
    if datetime(2016,8,1,0,0)<=key<=datetime(2016,8,31,0,0):
        _08_2016.append(value)
        
for key,value in rest_of_pages_x.iteritems():
    if datetime(2016,9,1,0,0)<=key<=datetime(2016,9,30,0,0):
        _09_2016.append(value)
        
for key,value in rest_of_pages_x.iteritems():
    if datetime(2016,10,1,0,0)<=key<=datetime(2016,10,31,0,0):
        _10_2016.append(value)        
        
for key,value in rest_of_pages_x.iteritems():
    if datetime(2016,11,1,0,0)<=key<=datetime(2016,11,30,0,0):
        _11_2016.append(value)        
        
for key,value in rest_of_pages_x.iteritems():
    if datetime(2016,12,1,0,0)<=key<=datetime(2016,12,31,0,0):
        _12_2016.append(value)        
        
for key,value in rest_of_pages_x.iteritems():
    if datetime(2017,1,1,0,0)<=key<=datetime(2017,1,31,0,0):
        _01_2017.append(value)        
        
flatten = lambda l: [item for sublist in l for item in sublist]  #since you worked with lists of lists, flatten them 

_01_2014=flatten(_01_2014)
_02_2014=flatten(_02_2014)
_03_2014=flatten(_03_2014)
_04_2014=flatten(_04_2014)
_05_2014=flatten(_05_2014)
_06_2014=flatten(_06_2014)
_07_2014=flatten(_07_2014)
_08_2014=flatten(_08_2014)
_09_2014=flatten(_09_2014)
_10_2014=flatten(_10_2014)
_11_2014=flatten(_11_2014)
_12_2014=flatten(_12_2014)
_01_2015=flatten(_01_2015)
_02_2015=flatten(_02_2015)
_03_2015=flatten(_03_2015)
_04_2015=flatten(_04_2015)
_05_2015=flatten(_05_2015)
_06_2015=flatten(_06_2015)
_07_2015=flatten(_07_2015)
_08_2015=flatten(_08_2015)
_09_2015=flatten(_09_2015)
_10_2015=flatten(_10_2015)
_11_2015=flatten(_11_2015)
_12_2015=flatten(_12_2015)
_01_2016=flatten(_01_2016)
_02_2016=flatten(_02_2016)
_03_2016=flatten(_03_2016)
_04_2016=flatten(_04_2016)
_05_2016=flatten(_05_2016)
_06_2016=flatten(_06_2016)
_07_2016=flatten(_07_2016)
_08_2016=flatten(_08_2016)
_09_2016=flatten(_09_2016)
_10_2016=flatten(_10_2016)
_11_2016=flatten(_11_2016)
_12_2016=flatten(_12_2016)
_01_2017=flatten(_01_2017)


#now, you have a list of dictionaries for each month. Items in the dictionaries are the links and summaries of articles. Next step is to 
#scrape the relevant content using the links

def clean(soup): #this is a function that allows me to scrape only the relevant content
    content_1=[]
    content_2=[]
    final_content=[]
    for p in soup('p'):
        content_1.append(p.get_text())
    for x in soup.find_all(class_='story'):
        content_2.append(x.p.get_text())
    intersection=list(set(content_1) & set(content_2))
    for y in soup('p'):
        if y.get_text() not in intersection:
            
            


            final_content.append(y.get_text())
            
                
    return final_content

#put all links in lists for each month (still not pythonic) 

links_01_2014=[]
links_02_2014=[]
links_03_2014=[]
links_04_2014=[]
links_05_2014=[]
links_06_2014=[]
links_07_2014=[]
links_08_2014=[]
links_09_2014=[]
links_10_2014=[]
links_11_2014=[]
links_12_2014=[]
links_01_2015=[]
links_02_2015=[]
links_03_2015=[]
links_04_2015=[]
links_05_2015=[]
links_06_2015=[]
links_07_2015=[]
links_08_2015=[]
links_09_2015=[]
links_10_2015=[]
links_11_2015=[]
links_12_2015=[]
links_01_2016=[]
links_02_2016=[]
links_03_2016=[]
links_04_2016=[]
links_05_2016=[]
links_06_2016=[]
links_07_2016=[]
links_08_2016=[]
links_09_2016=[]
links_10_2016=[]
links_11_2016=[]
links_12_2016=[]
links_01_2017=[]

for i in _01_2014:
    links_01_2014.append(i['link'])
for i in _02_2014:
    links_02_2014.append(i['link'])
for i in _03_2014:
    links_03_2014.append(i['link'])
for i in _04_2014:
    links_04_2014.append(i['link'])
for i in _05_2014:
    links_05_2014.append(i['link'])
for i in _06_2014:
    links_06_2014.append(i['link'])
for i in _07_2014:
    links_07_2014.append(i['link'])
for i in _08_2014:
    links_08_2014.append(i['link'])
for i in _09_2014:
    links_09_2014.append(i['link'])
for i in _10_2014:
    links_10_2014.append(i['link'])
for i in _11_2014:
    links_11_2014.append(i['link'])
for i in _12_2014:
    links_12_2014.append(i['link'])
for i in _01_2015:
    links_01_2015.append(i['link'])
for i in _02_2015:
    links_02_2015.append(i['link'])
for i in _03_2015:
    links_03_2015.append(i['link'])
for i in _04_2015:
    links_04_2015.append(i['link'])
for i in _05_2015:
    links_05_2015.append(i['link'])
for i in _06_2015:
    links_06_2015.append(i['link'])
for i in _07_2015:
    links_07_2015.append(i['link'])
for i in _08_2015:
    links_08_2015.append(i['link'])
for i in _09_2015:
    links_09_2015.append(i['link'])
for i in _10_2015:
    links_10_2015.append(i['link'])
for i in _11_2015:
    links_11_2015.append(i['link'])
for i in _12_2015:
    links_12_2015.append(i['link'])
for i in _01_2016:
    links_01_2016.append(i['link'])
for i in _02_2016:
    links_02_2016.append(i['link'])
for i in _03_2016:
    links_03_2016.append(i['link'])
for i in _04_2016:
    links_04_2016.append(i['link'])
for i in _05_2016:
    links_05_2016.append(i['link'])
for i in _06_2016:
    links_06_2016.append(i['link'])
for i in _07_2016:
    links_07_2016.append(i['link'])
for i in _08_2016:
    links_08_2016.append(i['link'])
for i in _09_2016:
    links_09_2016.append(i['link'])
for i in _10_2016:
    links_10_2016.append(i['link'])
for i in _11_2016:
    links_11_2016.append(i['link'])
for i in _12_2016:
    links_12_2016.append(i['link'])
for i in _01_2017:
    links_01_2017.append(i['link'])

#start scraping for each link list

soup_list_01_2014=[]
for i in links_01_2014:
    soup_list_01_2014.append(BeautifulSoup(urllib.urlopen(i).read() ,'lxml'))
soup_list_02_2014=[]
for i in links_02_2014:
    soup_list_02_2014.append(BeautifulSoup(urllib.urlopen(i).read() ,'lxml'))
soup_list_03_2014=[]
for i in links_03_2014:
    soup_list_03_2014.append(BeautifulSoup(urllib.urlopen(i).read() ,'lxml'))
soup_list_04_2014=[]
for i in links_04_2014:
    soup_list_04_2014.append(BeautifulSoup(urllib.urlopen(i).read() ,'lxml'))
soup_list_05_2014=[]
for i in links_05_2014:
    soup_list_05_2014.append(BeautifulSoup(urllib.urlopen(i).read() ,'lxml'))
soup_list_06_2014=[]
for i in links_06_2014:
    soup_list_06_2014.append(BeautifulSoup(urllib.urlopen(i).read() ,'lxml'))
soup_list_07_2014=[]
for i in links_07_2014:
    soup_list_07_2014.append(BeautifulSoup(urllib.urlopen(i).read() ,'lxml'))
soup_list_08_2014=[]
for i in links_08_2014:
    soup_list_08_2014.append(BeautifulSoup(urllib.urlopen(i).read() ,'lxml'))
soup_list_09_2014=[]
for i in links_09_2014:
    soup_list_09_2014.append(BeautifulSoup(urllib.urlopen(i).read() ,'lxml'))
soup_list_10_2014=[]
for i in links_10_2014:
    soup_list_10_2014.append(BeautifulSoup(urllib.urlopen(i).read() ,'lxml'))
soup_list_11_2014=[]
for i in links_11_2014:
    soup_list_11_2014.append(BeautifulSoup(urllib.urlopen(i).read() ,'lxml'))
soup_list_12_2014=[]
for i in links_12_2014:
    soup_list_12_2014.append(BeautifulSoup(urllib.urlopen(i).read() ,'lxml'))
soup_list_01_2015=[]
for i in links_01_2015:
    soup_list_01_2015.append(BeautifulSoup(urllib.urlopen(i).read() ,'lxml'))
soup_list_02_2015=[]
for i in links_02_2015:
    soup_list_02_2015.append(BeautifulSoup(urllib.urlopen(i).read() ,'lxml'))
soup_list_03_2015=[]
for i in links_03_2015:
    soup_list_03_2015.append(BeautifulSoup(urllib.urlopen(i).read() ,'lxml'))
soup_list_04_2015=[]
for i in links_04_2015:
    soup_list_04_2015.append(BeautifulSoup(urllib.urlopen(i).read() ,'lxml'))
soup_list_05_2015=[]
for i in links_05_2015:
    soup_list_05_2015.append(BeautifulSoup(urllib.urlopen(i).read() ,'lxml'))
soup_list_06_2015=[]
for i in links_06_2015:
    soup_list_06_2015.append(BeautifulSoup(urllib.urlopen(i).read() ,'lxml'))
soup_list_07_2015=[]
for i in links_07_2015:
    soup_list_07_2015.append(BeautifulSoup(urllib.urlopen(i).read() ,'lxml'))
soup_list_08_2015=[]
for i in links_08_2015:
    soup_list_08_2015.append(BeautifulSoup(urllib.urlopen(i).read() ,'lxml'))
soup_list_09_2015=[]
for i in links_09_2015:
    soup_list_09_2015.append(BeautifulSoup(urllib.urlopen(i).read() ,'lxml'))
soup_list_10_2015=[]
for i in links_10_2015:
    soup_list_10_2015.append(BeautifulSoup(urllib.urlopen(i).read() ,'lxml'))
soup_list_11_2015=[]
for i in links_11_2015:
    soup_list_11_2015.append(BeautifulSoup(urllib.urlopen(i).read() ,'lxml'))
soup_list_12_2015=[]
for i in links_12_2015:
    soup_list_12_2015.append(BeautifulSoup(urllib.urlopen(i).read() ,'lxml'))
soup_list_01_2016=[]
for i in links_01_2016:
    soup_list_01_2016.append(BeautifulSoup(urllib.urlopen(i).read() ,'lxml'))
soup_list_02_2016=[]
for i in links_02_2016:
    soup_list_02_2016.append(BeautifulSoup(urllib.urlopen(i).read() ,'lxml'))
soup_list_03_2016=[]
for i in links_03_2016:
    soup_list_03_2016.append(BeautifulSoup(urllib.urlopen(i).read() ,'lxml'))
soup_list_04_2016=[]
for i in links_04_2016:
    soup_list_04_2016.append(BeautifulSoup(urllib.urlopen(i).read() ,'lxml'))
soup_list_05_2016=[]
for i in links_05_2016:
    soup_list_05_2016.append(BeautifulSoup(urllib.urlopen(i).read() ,'lxml'))
soup_list_06_2016=[]
for i in links_06_2016:
    soup_list_06_2016.append(BeautifulSoup(urllib.urlopen(i).read() ,'lxml'))
soup_list_07_2016=[]
for i in links_07_2016:
    soup_list_07_2016.append(BeautifulSoup(urllib.urlopen(i).read() ,'lxml'))
soup_list_08_2016=[]
for i in links_08_2016:
    soup_list_08_2016.append(BeautifulSoup(urllib.urlopen(i).read() ,'lxml'))
soup_list_09_2016=[]
for i in links_09_2016:
    soup_list_09_2016.append(BeautifulSoup(urllib.urlopen(i).read() ,'lxml'))
soup_list_10_2016=[]
for i in links_10_2016:
    soup_list_10_2016.append(BeautifulSoup(urllib.urlopen(i).read() ,'lxml'))
soup_list_11_2016=[]
for i in links_11_2016:
    soup_list_11_2016.append(BeautifulSoup(urllib.urlopen(i).read() ,'lxml'))
soup_list_12_2016=[]
for i in links_12_2016:
    soup_list_12_2016.append(BeautifulSoup(urllib.urlopen(i).read() ,'lxml'))
soup_list_01_2017=[]
for i in links_01_2017:
    soup_list_01_2017.append(BeautifulSoup(urllib.urlopen(i).read() ,'lxml'))
    
articles_01_2014=[]
for i in range(len(soup_list_01_2014)):
    articles_01_2014.append("".join(clean(soup_list_01_2014[i])))
articles_02_2014=[]
for i in range(len(soup_list_02_2014)):
    articles_02_2014.append("".join(clean(soup_list_02_2014[i])))
articles_03_2014=[]
for i in range(len(soup_list_03_2014)):
    articles_03_2014.append("".join(clean(soup_list_03_2014[i])))
articles_04_2014=[]
for i in range(len(soup_list_04_2014)):
    articles_04_2014.append("".join(clean(soup_list_04_2014[i])))
articles_05_2014=[]
for i in range(len(soup_list_05_2014)):
    articles_05_2014.append("".join(clean(soup_list_05_2014[i])))
articles_06_2014=[]
for i in range(len(soup_list_06_2014)):
    articles_06_2014.append("".join(clean(soup_list_06_2014[i])))
articles_07_2014=[]
for i in range(len(soup_list_07_2014)):
    articles_07_2014.append("".join(clean(soup_list_07_2014[i])))
articles_08_2014=[]
for i in range(len(soup_list_08_2014)):
    articles_08_2014.append("".join(clean(soup_list_08_2014[i])))
articles_09_2014=[]
for i in range(len(soup_list_09_2014)):
    articles_09_2014.append("".join(clean(soup_list_09_2014[i])))
articles_10_2014=[]
for i in range(len(soup_list_10_2014)):
    articles_10_2014.append("".join(clean(soup_list_10_2014[i])))
articles_11_2014=[]
for i in range(len(soup_list_11_2014)):
    articles_01_2014.append("".join(clean(soup_list_11_2014[i])))
articles_12_2014=[]
for i in range(len(soup_list_12_2014)):
    articles_12_2014.append("".join(clean(soup_list_12_2014[i])))
articles_01_2015=[]
for i in range(len(soup_list_01_2015)):
    articles_01_2015.append("".join(clean(soup_list_01_2015[i])))
articles_02_2015=[]
for i in range(len(soup_list_02_2015)):
    articles_02_2015.append("".join(clean(soup_list_02_2015[i])))
articles_03_2015=[]
for i in range(len(soup_list_03_2015)):
    articles_03_2015.append("".join(clean(soup_list_03_2015[i])))
articles_04_2015=[]
for i in range(len(soup_list_04_2015)):
    articles_04_2015.append("".join(clean(soup_list_04_2015[i])))
articles_05_2015=[]
for i in range(len(soup_list_05_2015)):
    articles_05_2015.append("".join(clean(soup_list_05_2015[i])))
articles_06_2015=[]
for i in range(len(soup_list_06_2015)):
    articles_06_2015.append("".join(clean(soup_list_06_2015[i])))
articles_07_2015=[]
for i in range(len(soup_list_07_2015)):
    articles_07_2015.append("".join(clean(soup_list_07_2015[i])))
articles_08_2015=[]
for i in range(len(soup_list_08_2015)):
    articles_08_2015.append("".join(clean(soup_list_08_2015[i])))
articles_09_2015=[]
for i in range(len(soup_list_09_2015)):
    articles_09_2015.append("".join(clean(soup_list_09_2015[i])))
articles_10_2015=[]
for i in range(len(soup_list_10_2015)):
    articles_10_2015.append("".join(clean(soup_list_10_2015[i])))
articles_11_2015=[]
for i in range(len(soup_list_11_2015)):
    articles_11_2015.append("".join(clean(soup_list_11_2015[i])))
articles_12_2015=[]
for i in range(len(soup_list_12_2015)):
    articles_12_2015.append("".join(clean(soup_list_12_2015[i])))
articles_01_2016=[]
for i in range(len(soup_list_01_2016)):
    articles_01_2016.append("".join(clean(soup_list_01_2016[i])))
articles_02_2016=[]
for i in range(len(soup_list_02_2016)):
    articles_02_2016.append("".join(clean(soup_list_02_2016[i])))
articles_03_2016=[]
for i in range(len(soup_list_03_2016)):
    articles_03_2016.append("".join(clean(soup_list_03_2016[i])))
articles_04_2016=[]
for i in range(len(soup_list_04_2016)):
    articles_04_2016.append("".join(clean(soup_list_04_2016[i])))
articles_05_2016=[]
for i in range(len(soup_list_05_2016)):
    articles_05_2016.append("".join(clean(soup_list_05_2016[i])))
articles_06_2016=[]
for i in range(len(soup_list_06_2016)):
    articles_06_2016.append("".join(clean(soup_list_06_2016[i])))
articles_07_2016=[]
for i in range(len(soup_list_07_2016)):
    articles_07_2016.append("".join(clean(soup_list_07_2016[i])))
articles_08_2016=[]
for i in range(len(soup_list_08_2016)):
    articles_08_2016.append("".join(clean(soup_list_08_2016[i])))
articles_09_2016=[]
for i in range(len(soup_list_09_2016)):
    articles_09_2016.append("".join(clean(soup_list_09_2016[i])))
articles_10_2016=[]
for i in range(len(soup_list_10_2016)):
    articles_10_2016.append("".join(clean(soup_list_10_2016[i])))
articles_11_2016=[]
for i in range(len(soup_list_11_2016)):
    articles_11_2016.append("".join(clean(soup_list_11_2016[i])))
articles_12_2016=[]
for i in range(len(soup_list_12_2016)):
    articles_12_2016.append("".join(clean(soup_list_12_2016[i])))
articles_01_2017=[]
for i in range(len(soup_list_01_2017)):
    articles_01_2017.append("".join(clean(soup_list_01_2017[i])))
               
#next, since you want to treat each month as if it's only one article, join all articles for each month

articles_01_2014_j=" ".join(articles_01_2014)
articles_02_2014_j=" ".join(articles_02_2014)
articles_03_2014_j=" ".join(articles_03_2014)
articles_04_2014_j=" ".join(articles_04_2014)
articles_05_2014_j=" ".join(articles_05_2014)
articles_06_2014_j=" ".join(articles_06_2014)
articles_07_2014_j=" ".join(articles_07_2014)
articles_08_2014_j=" ".join(articles_08_2014)
articles_09_2014_j=" ".join(articles_09_2014)
articles_10_2014_j=" ".join(articles_10_2014)
articles_11_2014_j=" ".join(articles_11_2014)
articles_12_2014_j=" ".join(articles_12_2014)
articles_01_2015_j=" ".join(articles_01_2015)
articles_02_2015_j=" ".join(articles_02_2015)
articles_03_2015_j=" ".join(articles_03_2015)
articles_04_2015_j=" ".join(articles_04_2015)
articles_05_2015_j=" ".join(articles_05_2015)
articles_06_2015_j=" ".join(articles_06_2015)
articles_07_2015_j=" ".join(articles_07_2015)
articles_08_2015_j=" ".join(articles_08_2015)
articles_09_2015_j=" ".join(articles_09_2015)
articles_10_2015_j=" ".join(articles_10_2015)
articles_11_2015_j=" ".join(articles_11_2015)
articles_12_2015_j=" ".join(articles_12_2015)
articles_01_2016_j=" ".join(articles_01_2016)
articles_02_2016_j=" ".join(articles_02_2016)
articles_03_2016_j=" ".join(articles_03_2016)
articles_04_2016_j=" ".join(articles_04_2016)
articles_05_2016_j=" ".join(articles_05_2016)
articles_06_2016_j=" ".join(articles_06_2016)
articles_07_2016_j=" ".join(articles_07_2016)
articles_08_2016_j=" ".join(articles_08_2016)
articles_09_2016_j=" ".join(articles_09_2016)
articles_10_2016_j=" ".join(articles_10_2016)
articles_11_2016_j=" ".join(articles_11_2016)
articles_12_2016_j=" ".join(articles_12_2016)
articles_01_2017_j=" ".join(articles_01_2017)

#finally, create your master article list containing 37 elements. one for each month. you will use this to run the algorithm on

master_article_list=[]
master_article_list.append(articles_01_2014_j)
master_article_list.append(articles_02_2014_j)
master_article_list.append(articles_03_2014_j)
master_article_list.append(articles_04_2014_j)
master_article_list.append(articles_05_2014_j)
master_article_list.append(articles_06_2014_j)
master_article_list.append(articles_07_2014_j)
master_article_list.append(articles_08_2014_j)
master_article_list.append(articles_09_2014_j)
master_article_list.append(articles_10_2014_j)
master_article_list.append(articles_11_2014_j)
master_article_list.append(articles_12_2014_j)
master_article_list.append(articles_01_2015_j)
master_article_list.append(articles_02_2015_j)
master_article_list.append(articles_03_2015_j)
master_article_list.append(articles_04_2015_j)
master_article_list.append(articles_05_2015_j)
master_article_list.append(articles_06_2015_j)
master_article_list.append(articles_07_2015_j)
master_article_list.append(articles_08_2015_j)
master_article_list.append(articles_09_2015_j)
master_article_list.append(articles_10_2015_j)
master_article_list.append(articles_11_2015_j)
master_article_list.append(articles_12_2015_j)
master_article_list.append(articles_01_2016_j)
master_article_list.append(articles_02_2016_j)
master_article_list.append(articles_03_2016_j)
master_article_list.append(articles_04_2016_j)
master_article_list.append(articles_05_2016_j)
master_article_list.append(articles_06_2016_j)
master_article_list.append(articles_07_2016_j)
master_article_list.append(articles_08_2016_j)
master_article_list.append(articles_09_2016_j)
master_article_list.append(articles_10_2016_j)
master_article_list.append(articles_11_2016_j)
master_article_list.append(articles_12_2016_j)
master_article_list.append(articles_01_2017_j)

#pickle it for later use since you've worked so hard on it. 

from sklearn.externals import joblib
joblib.dump(master_article_list,'master_article_list_mnf.pkl')
               
               
               
               
               


    







