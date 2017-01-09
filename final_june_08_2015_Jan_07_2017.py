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




p0 = urllib.urlopen('http://www.reuters.com/news/archive/turkey?view=page&page=1').read() 
soup = BeautifulSoup(p0,'lxml')
content=soup.find_all("div",class_="story-content") 

first_page={}
prefix="http://www.reuters.com/" 
for element in content:
    date = element.find(class_="timestamp").get_text()

    if date in first_page.keys():
        first_page[date].append({"link": prefix + element.a["href"], "summary": element.p.get_text()})

    else:
        first_page[date]=[{"link": prefix + element.a["href"], "summary": element.p.get_text()}]
        


parsing_list=[] 
soup_list=[] 
content_list=range(0,128)



i=0
x=0

for x in range(129): 
    soup_list.append("soup"+str(x+1))

for i in range(129): 
    parsing_list.append("p"+str(i+1))

a=0

for a in range(0,128): 
    parsing_list[a]=urllib.urlopen("http://www.reuters.com/news/archive/turkey?view=page&page=" + str(a+2) + "&pageSize=10").read()
    soup_list[a]=BeautifulSoup(parsing_list[a],"lxml")
    content_list[a]=soup_list[a].find_all("div",class_="story-content")    

rest_of_pages={} 

prefix="http://www.reuters.com" 

b=0

while b<len(content_list): 
    for element in content_list[b]:
        date = element.find(class_="timestamp").get_text()

        if date in rest_of_pages.keys():
            rest_of_pages[date].append({"link": prefix + element.a["href"], "summary": element.p.get_text()})

        else:
            rest_of_pages[date]=[{"link": prefix + element.a["href"], "summary": element.p.get_text()}]

     
    b+=1       

all_pages=first_page.copy()
all_pages.update(rest_of_pages)



all_summaries=[] 
for date in all_pages:
    for item in all_pages[date]:
        all_summaries.append(item['summary'])






stopwords = nltk.corpus.stopwords.words('english')
from nltk.stem.snowball import SnowballStemmer 
stemmer = SnowballStemmer("english") 



def token_stem(text):

    tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    tokens_with_letters = []

    for token in tokens:
        if re.search('[a-zA-Z]', token):
            tokens_with_letters.append(token)
    stems = [stemmer.stem(t) for t in tokens_with_letters] #"stems" part
    return stems


def token(text): 

    tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    tokens_with_letters = []

    for token in tokens:
        if re.search('[a-zA-Z]', token):
            tokens_with_letters.append(token)
    return tokens_with_letters

word_list_stemmed = []
word_list_tokenized = []
for i in all_summaries:
    allwords_stemmed = token_stem(i)
    word_list_stemmed.extend(allwords_stemmed)
    
    allwords_tokenized = token(i)
    word_list_tokenized.extend(allwords_tokenized)
    

words_df=pd.DataFrame({'words':word_list_tokenized},index=word_list_stemmed)

from sklearn.feature_extraction.text import TfidfVectorizer


vectorizer = TfidfVectorizer(max_df=0.8, max_features=200000,
                                 min_df=0.005, stop_words='english',
                                 use_idf=True, tokenizer=token_stem, ngram_range=(1,3))

%time tfidf_matrix = vectorizer.fit_transform(all_summaries) 

print(tfidf_matrix.shape) 

terms = vectorizer.get_feature_names()  



from sklearn.cluster import KMeans 
km=KMeans(n_clusters=6,n_init=20,max_iter=10000000).fit(tfidf_matrix) 

clusters = km.labels_.tolist() 

from collections import Counter

print Counter(clusters) 

from sklearn.externals import joblib 

joblib.dump(km,'K_Means_June_08_2015_Jan_07_2017.pkl') 

from __future__ import print_function 

print("Cluster Terms:")
print()

sorted_centroids = km.cluster_centers_.argsort()[:, ::-1] 

for i in range(6):
    print("Cluster %d words:" % i, end='')
    
    for ind in sorted_centroids[i, :5]: 
        print(' %s' % words_df.ix[terms[ind].split(' ')].values.tolist()[0][0].encode('utf-8', 'ignore'), end=',')
    print() 
    print() 
