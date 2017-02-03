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



master_article_list=joblib.load('master_article_list_mnf.pkl')




from sklearn.feature_extraction.text import TfidfVectorizer 


vectorizer = TfidfVectorizer(max_df=0.95, max_features=200000,    #create your tfidf vectorizer with necessary parameters
                                 min_df=2, stop_words='english',
                                 use_idf=True,ngram_range=(1,3))

dtm = vectorizer.fit_transform(master_article_list).toarray() #fit the vectorizer into your list of summaries 
vocab = np.array(vectorizer.get_feature_names()) #get your feature names. this will be necessary because you want to identify top words for each salient topic


print(dtm.shape) 

print (len(vocab))

from sklearn.decomposition import NMF
from sklearn import decomposition
from __future__ import print_function



n_topics = 20 #this is arbitrary, you can play around with it. It produced good results for me though. 
n_top_words = 20

clf = decomposition.NMF(n_components=n_topics, random_state=1) #here you define your k 

doctopic = clf.fit_transform(dtm) #apply NMF to your document-term matrix (tfidf matrix)

print (doctopic.shape) #check if you get 37*20 (in our case)

topic_words = []  #get top 20 words for each salient topic. put them in a list 
for topic in clf.components_:
    word_idx = np.argsort(topic)[::-1][0:n_top_words]
    topic_words.append([vocab[i] for i in word_idx])

#make a list of article dates. You will use the index of this list to pinpoint dates and weights 
article_dates =['01/2014','02/2014','03/2014','04/2014','05/2014','06/2014','07/2014','08/2014','09/2014','10/2014',
                '11/2014','12/2014',
                '01/2015','02/2015','03/2015','04/2015','05/2015','06/2015','07/2015','08/2015',
                '09/2015','10/2015','11/2015','12/2015',
                '01/2016','02/2016','03/2016','04/2016','05/2016','06/2016','07/2016','08/2016','09/2016','10/2016',
                '11/2016','12/2016',
                '01/2017']

article_dates = np.asarray(article_dates)

num_groups = len(set(article_dates)) #this is how many documents you have 

print (article_dates) #I basically used the indexes of the doctopic, topic_words and article_dates to pinpoint where to look. It's a manual process, but it works like a charm.
print (topic_words[3])
print (doctopic[0])

doctopic_T=doctopic.transpose() #I want to plot. so I transpose. Not really mandatory but it was more comfortable for me to plot this way

from datetime import datetime
for i in article_dates:
    i=datetime.strptime(i,'%m/%Y')
    
%matplotlib inline #plot for EU Immigration Deal 
import datetime
import matplotlib.pyplot as plt
from matplotlib.pyplot import Figure
plt.figure(figsize=(10,7))
plt.plot(doctopic_T[0])
plt.xticks(range(0,37),article_dates,fontsize=8)
plt.xticks(rotation=60)
plt.suptitle('EU Immigration Deal',fontsize=15)

plt.show()
print (topic_words[0])
    
%matplotlib inline #plot for Elections 
import datetime
import matplotlib.pyplot as plt
from matplotlib.pyplot import Figure
plt.figure(figsize=(10,7))
plt.plot(doctopic_T[4])
plt.xticks(range(0,37),article_dates,fontsize=8)
plt.xticks(rotation=60)
plt.suptitle('Elections',fontsize=15)

plt.show()
print (topic_words[4])
 
%matplotlib inline   #plot for Coup Attempt
import datetime
import matplotlib.pyplot as plt
from matplotlib.pyplot import Figure
plt.figure(figsize=(10,7))
plt.plot(doctopic_T[2])
plt.xticks(range(0,37),article_dates,fontsize=8)
plt.xticks(rotation=60)
plt.suptitle('Coup Attempt',fontsize=15)
plt.show()
print (topic_words[2])


%matplotlib inline #Plot for Corruption Scandal 
import datetime
import matplotlib.pyplot as plt
from matplotlib.pyplot import Figure
plt.figure(figsize=(10,7))
plt.plot(doctopic_T[14])
plt.xticks(range(0,37),article_dates,fontsize=8)
plt.xticks(rotation=60)
plt.suptitle('Corruption Scandal',fontsize=15)
plt.show()
print (topic_words[14])

%matplotlib inline #Plot for Siege of Kobani
import datetime
import matplotlib.pyplot as plt
from matplotlib.pyplot import Figure
plt.figure(figsize=(10,7))
plt.plot(doctopic_T[3])
plt.xticks(range(0,37),article_dates,fontsize=8)
plt.xticks(rotation=60)
plt.suptitle('Siege of Kobani',fontsize=15)
plt.show()
print (topic_words[3])



