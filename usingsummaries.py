from bs4 import BeautifulSoup
import urllib
import json
from collections import Counter

p0 = urllib.urlopen('http://www.reuters.com/news/archive/turkey?view=page&page=1').read()
soup = BeautifulSoup(p0,'lxml')

content=soup.find_all("div",class_="story-content") #get the objects on the html page with type "div" and class "Story-content"

#first page and the rest of the pages will have a different method for scraping since the URL convention is different after pg1

first_page={} #nested dictionary with dates at outermost, and links and summaries in a list of dictionaries for each date. 
prefix="http://www.reuters.com/" #links in the html are not complete, create this prefix and append the href to this


for element in content:
    date = element.find(class_="timestamp").get_text()
    # Date already exists, add dictionary of link and summary to list of articles for the day
    if date in first_page.keys():
        first_page[date].append({"link": prefix + element.a["href"], "summary": element.p.get_text()})
    # Date does not exist, create a list of dictionaries for that date
    else:
        first_page[date]=[{"link": prefix + element.a["href"], "summary": element.p.get_text()}]
    
    
parsing_list=[] #list for p0,p1,p2,p3 etc
soup_list=[] #create a list with 65 entries so that you also have soup1,soup2,soup3 etc. 
content_list=range(0,78)

#list for the contents of each page. has 66 entries 

i=0
x=0

for x in range(79): #put the variables in soup_list (soup1,soup2 etc.)
    soup_list.append("soup"+str(x+1))

for i in range(79): 
    parsing_list.append("p"+str(i+1))

a=0

for a in range(0,78): #read the URLs and assign them to variables in soup_list (soup1,soup2 etc)
    parsing_list[a]=urllib.urlopen("http://www.reuters.com/news/archive/turkey?view=page&page=" + str(a+2) + "&pageSize=10").read()
    soup_list[a]=BeautifulSoup(parsing_list[a],"lxml")
    content_list[a]=soup_list[a].find_all("div",class_="story-content")    #get the objects on each page with type "div" and class "Story-content"
    
#each element in content_list contains 10 elements. it's a list of lists. this is for parsing mostly


titles_2={} #dictionary that will have the content (title, date, link) for pages 2-68

prefix="http://www.reuters.com" #since the links in the html are not complete, you need to create this prefix to add to the beginning of everyone of them

b=0

while b<len(content_list):
    for element in content_list[b]:
        date = element.find(class_="timestamp").get_text()
    # Date already exists, add dictionary of link and summary to list of articles for the day
        if date in titles_2.keys():
            titles_2[date].append({"link": prefix + element.a["href"], "summary": element.p.get_text()})
    # Date does not exist, create a list of dictionaries for that date
        else:
            titles_2[date]=[{"link": prefix + element.a["href"], "summary": element.p.get_text()}]

     
    b+=1       


import json #use JSON to write the nested dictionaries into files, have a nice naming convention for each


universal_content_dict=titles_2.copy()
universal_content_dict.update(first_page) #create a universal dictionary with all the pages' content in it 



with open("Universal_Content.json","w") as writeJSON: #dump universal_content_dict in JSON file
    json.dump(universal_content_dict,writeJSON)

universal_word_list=[] 

for key,item in universal_content_dict.iteritems(): #make a list of lists out of the contents in the summary keys in universal_content_dict
    for x in item:
        x['summary']=x['summary'].lower()
        universal_word_list.append(x['summary'].split())

flatten=lambda universal_word_list:[item for sublist in universal_word_list for item in sublist] #function to make universal_word_list one big list
universal_word_list=flatten(universal_word_list)    


new_list=[]    #this is super hacky, but other methods don't seem to work. Create a new list and put the stripped items in it. append the rest.

for x in universal_word_list:#get rid of unwanted symbols in your words
    if '"' in x:
        x=x.strip('"')
        new_list.append(x)
    elif '.' in x:    
        x=x.strip('.')
        new_list.append(x)
    elif ':' in x:
        x=x.strip(':')
        new_list.append(x)
    elif ',' in x:
        x=x.strip(',')
        new_list.append(x)
    
    else:
        new_list.append(x)
        
universal_word_counts=Counter(new_list)#count each word in list. put them in a dictionary. 

#now create the positive dictionary with the words you need
for i in universal_word_counts.keys(): #put your super-arbitrary threshold of 161>x>1 on the word count, and get rid of the words that are above it
    if universal_word_counts[i]>=161:
        del universal_word_counts[i]
    elif universal_word_counts[i]<=1:
        del universal_word_counts[i]
        




    


        


