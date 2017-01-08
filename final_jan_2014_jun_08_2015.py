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

#almost all code for this part is the same as the final_all part. Only differences are in scraping. Will point them out, and won't comment on anything else 

os.chdir('/Users/berkayadlim/Desktop/Project_Scrape')



#first page isn't needed for this part. so scrape only pages between 130-180. They correspond to articles written between Jan2014-Jun082015
parsing_list=[] 
soup_list=[] 
content_list=range(0,51)

i=0
x=0

for x in range(52): 
    soup_list.append("soup"+str(x+1))

for i in range(52): 
    parsing_list.append("p"+str(i+1))

a=0

for a in range(0,51): #only difference here is that you do "a+130 instead of a+2 bc you want pages between 130-180
    parsing_list[a]=urllib.urlopen("http://www.reuters.com/news/archive/turkey?view=page&page=" + str(a+130) + "&pageSize=10").read()
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


all_summaries=[]
for date in rest_of_pages:
    for item in rest_of_pages[date]:
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

%time doc_matrix = vectorizer.fit_transform(all_summaries) 

print(doc_matrix.shape)

terms = vectorizer.get_feature_names()

from sklearn.cluster import KMeans
km=KMeans(n_clusters=5,n_init=20,max_iter=10000000).fit(doc_matrix) 

clusters = km.labels_.tolist()


from collections import Counter

print Counter(clusters)

from sklearn.externals import joblib 

joblib.dump(km,'K_Means_Jan_2014_Jun_08_2015.pkl') 

#km = joblib.load('K_means_Jan_2014_Jun_08_2015.pkl')
#clusters = km.labels_.tolist()
from __future__ import print_function

print("Cluster Terms:")
print()

sorted_centroids = km.cluster_centers_.argsort()[:, ::-1] 

for i in range(5):
    print("Cluster %d words:" % i, end='')
    
    for ind in sorted_centroids[i, :10]: 
        print(' %s' % words_df.ix[terms[ind].split(' ')].values.tolist()[0][0].encode('utf-8', 'ignore'), end=',')
    print() 
    
