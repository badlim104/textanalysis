import numpy as np
import pandas as pd
import nltk
from sklearn.externals import joblib
import re
import codecs
from sklearn import feature_extraction
import mpld3
import os
from bs4 import BeautifulSoup
import urllib

os.chdir('/Users/berkayadlim/Desktop/Project_Scrape')



links_06082015_01072017=joblib.load("links_062082015_01072017.pkl")


soup_list=[]

for i in links_06082015_01072017:
    soup_list.append(BeautifulSoup(urllib.urlopen(i).read() ,'lxml'))

    
def clean(soup):
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

article_list=[]
for i in range(len(soup_list)):
    article_list.append("".join(clean(soup_list[i])))

print len(article_list)    

#joblib.dump(article_list,'article_list_06082015_01072017.pkl') 


#article_list = joblib.load('article_list_06082015_01072017.pkl')

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
for i in article_list:
    allwords_stemmed = token_stem(i) #for each item in 'all_summaries', tokenize&stem
    word_list_stemmed.extend(allwords_stemmed) #extend the 'word_list_stemmed' list
    
    allwords_tokenized = token(i)
    word_list_tokenized.extend(allwords_tokenized) #this one's the word list for the tokenized (these aren't stemmed)
    
#use Pandas for the dataframe
words_df=pd.DataFrame({'words':word_list_tokenized},index=word_list_stemmed)

from sklearn.feature_extraction.text import TfidfVectorizer #now create a vector of words for each document, Tfidf is explained in the paper


vectorizer = TfidfVectorizer(max_df=0.8, max_features=200000,
                                 min_df=0.005, stop_words='english',
                                 use_idf=True, tokenizer=token_stem, ngram_range=(1,3))

%time tfidf_matrix = vectorizer.fit_transform(article_list) #fit the vectorizer into your list of summaries 

print(tfidf_matrix.shape) 

terms = vectorizer.get_feature_names()  #features (stems) used in the analysis (after max_df and min_df is applied)

#cleaning is done. now the fun part. we apply the algorithm and see how it does

from sklearn.cluster import KMeans 
km=KMeans(n_clusters=6,n_init=20,max_iter=10000000).fit(tfidf_matrix) #to assess how well this does, you can use km.inertia_

clusters = km.labels_.tolist() # algorithm used 5 clusters, each summary belongs to one cluster. put these cluster numbers in a list

#from collections import Counter

#print Counter(clusters) #take a look at how many items belong to each cluster 

from sklearn.externals import joblib #import the joblib module so you can pickle your model. ".to_pickle" doesn't work because this is not a dataframe 

joblib.dump(km,'K_Means_01192017.pkl') #pickle the model for later use 

from __future__ import print_function #now do some indexing and grouping so you can display the results nicely

print("Cluster Terms:")
print()

sorted_centroids = km.cluster_centers_.argsort()[:, ::-1] #choose the words that are closest to the centroid for each doc.

for i in range(6):
    print("Cluster %d words:" % i, end='')
    
    for ind in sorted_centroids[i, :6]: #change the 6 to look at however many words you want
        print(' %s' % words_df.ix[terms[ind].split(' ')].values.tolist()[0][0].encode('utf-8', 'ignore'), end=',')
    print() 
