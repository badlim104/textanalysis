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

#since the URL structure is different for the first page, scrape the content for it seperately
p0 = urllib.urlopen('http://www.reuters.com/news/archive/turkey?view=page&page=1').read() 
soup = BeautifulSoup(p0,'lxml')
content=soup.find_all("div",class_="story-content") 

#create a dictionary within a list within a dictionary. outermost keys will be dates, next layer will be a list of dictionaries where for
#each article there's the link and the summary.
first_page={}
prefix="http://www.reuters.com/" #since the links in the page source are not complete, create this and append the rest 
for element in content:
    date = element.find(class_="timestamp").get_text()
    # Date already exists, add dictionary of link and summary to list of articles for the day
    if date in first_page.keys():
        first_page[date].append({"link": prefix + element.a["href"], "summary": element.p.get_text()})
    # Date does not exist, create a list of dictionaries for that date
    else:
        first_page[date]=[{"link": prefix + element.a["href"], "summary": element.p.get_text()}]
        

#now on to the rest of the pages. for this, do some nice for and while loops
parsing_list=[] #list for p0,p1,p2,p3 etc
soup_list=[] #create a list with x entries so that you also have soup1,soup2,soup3 etc. 
content_list=range(0,179)



i=0
x=0

for x in range(180): #create some placeholders so you can iterate over the lists and the replace the placeholders as you go
    soup_list.append("soup"+str(x+1))

for i in range(180): 
    parsing_list.append("p"+str(i+1))

a=0

for a in range(0,179): #this is where we parse the content for each page and put the raw data in a list
    parsing_list[a]=urllib.urlopen("http://www.reuters.com/news/archive/turkey?view=page&page=" + str(a+2) + "&pageSize=10").read()
    soup_list[a]=BeautifulSoup(parsing_list[a],"lxml")
    content_list[a]=soup_list[a].find_all("div",class_="story-content")    #get the objects on each page with type "div" and class "Story-content"

rest_of_pages={} 

prefix="http://www.reuters.com" 

b=0

while b<len(content_list): #this is where you create the dictionary within a list within a dictionary for the rest of the pages
    for element in content_list[b]:
        date = element.find(class_="timestamp").get_text()
    # Date already exists, add dictionary of link and summary to list of articles for the day
        if date in rest_of_pages.keys():
            rest_of_pages[date].append({"link": prefix + element.a["href"], "summary": element.p.get_text()})
    # Date does not exist, create a list of dictionaries for that date
        else:
            rest_of_pages[date]=[{"link": prefix + element.a["href"], "summary": element.p.get_text()}]

     
    b+=1       

all_pages=first_page.copy() #merge the content for the first page and the rest of the pages
all_pages.update(rest_of_pages)



all_summaries=[] #since you will only be working with summaries, create a list of summaries taken from the nested dictionary
for date in all_pages:
    for item in all_pages[date]:
        all_summaries.append(item['summary'])


#now we're done with scraping, and have a list of the summaries for all articles. on to the cleaning!         

#you shouldn't use stopwords in your analysis. luckily Python has an easy way of doing that. The nltk library has a list of stopwords.
#assign these to a variable called "stopwords"
stopwords = nltk.corpus.stopwords.words('english')
from nltk.stem.snowball import SnowballStemmer #you also need the roots of the words (stems). Python to the rescue. Use the snowballstemmer
stemmer = SnowballStemmer("english") 

#here, you define two functions. One for tokenizing the sentences and words, and one for stemming AND tokenizing

def token_stem(text):
    # tokenize by sentence and word. this way you ensure you get rid of punctuations
    tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    tokens_with_letters = []
    # use the regex library to search only for items that contain letters. this will enable you to eliminate punctuation
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            tokens_with_letters.append(token)
    stems = [stemmer.stem(t) for t in tokens_with_letters] #"stems" part
    return stems


def token(text): #difference between this one and the one above is the "stems" part
    #same as above
    tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    tokens_with_letters = []
    # same as above
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            tokens_with_letters.append(token)
    return tokens_with_letters

#make two lists, one for tokenized&stemmed, one for tokenized only words. you will put this in a dataframe so that you can see 
#which stem belongs to which word (it will basically be used for labeling purposes)
word_list_stemmed = []
word_list_tokenized = []
for i in all_summaries:
    allwords_stemmed = token_stem(i) #for each item in 'all_summaries', tokenize&stem
    word_list_stemmed.extend(allwords_stemmed) #extend the 'word_list_stemmed' list
    
    allwords_tokenized = token(i)
    word_list_tokenized.extend(allwords_tokenized) #this one's the word list for the tokenized (these aren't stemmed)
    
#use Pandas for the dataframe
words_df=pd.DataFrame({'words':word_list_tokenized},index=word_list_stemmed)

from sklearn.feature_extraction.text import TfidfVectorizer #now create a vector of words for each document, Tfidf is explained in the paper


tfidf_vectorizer = TfidfVectorizer(max_df=0.8, max_features=200000,
                                 min_df=0.005, stop_words='english',
                                 use_idf=True, tokenizer=token_stem, ngram_range=(1,3))

%time tfidf_matrix = tfidf_vectorizer.fit_transform(all_summaries) #fit the vectorizer into your list of summaries 

print(tfidf_matrix.shape) #explanation of a tfidf matrix is provided in the paper 

terms = tfidf_vectorizer.get_feature_names()  #features (stems) used in the analysis (after max_df and min_df is applied)

#cleaning is done. now the fun part. we apply the algorithm and see how it does

from sklearn.cluster import KMeans 
km=KMeans(n_clusters=5,n_init=20,max_iter=10000000).fit(tfidf_matrix) #to assess how well this does, you can use km.inertia_

clusters = km.labels_.tolist() # algorithm used 5 clusters, each summary belongs to one cluster. put these cluster numbers in a list

from collections import Counter

print Counter(clusters) #take a look at how many items belong to each cluster 

from sklearn.externals import joblib #import the joblib module so you can pickle your model. ".to_pickle" doesn't work because this is not a dataframe 

joblib.dump(km,'K_Means.pkl') #pickle the model for later use 

#km = joblib.load('K_means.pkl') #if you want to, this is how you load a model from a pickle. uncomment to run code
#clusters = km.labels_.tolist()

from __future__ import print_function #now do some indexing and grouping so you can display the results nicely

print("Cluster Terms:")
print()

order_centroids = km.cluster_centers_.argsort()[:, ::-1] #choose the words that are closest to the centroid for each doc.

for i in range(5):
    print("Cluster %d words:" % i, end='')
    
    for ind in order_centroids[i, :20]: #change the 20 to look at however many words you want
        print(' %s' % words_df.ix[terms[ind].split(' ')].values.tolist()[0][0].encode('utf-8', 'ignore'), end=',')
    print() 
    print()     


        


