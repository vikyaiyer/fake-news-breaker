text = raw_input("Enter a query: ")
print text
import itertools, nltk, string
grammar=r'KT: {(<JJ>* <NN.*>+ <IN>)? <JJ>* <NN.*>+}'    
    # exclude candidates that are stop words or entirely punctuation
punct = set(string.punctuation)
stop_words = set(nltk.corpus.stopwords.words('english'))
    # tokenize, POS-tag, and chunk using regular expressions
chunker = nltk.chunk.regexp.RegexpParser(grammar)
tagged_sents = nltk.pos_tag_sents(nltk.word_tokenize(sent) for sent in nltk.sent_tokenize(text))
all_chunks = list(itertools.chain.from_iterable(nltk.chunk.tree2conlltags(chunker.parse(tagged_sent)) for tagged_sent in tagged_sents))
    # join constituent chunk words into a single chunked phrase
candidates = [' '.join(word for word, pos, chunk in group).lower()
              for key, group in itertools.groupby(all_chunks, lambda (word,pos,chunk): chunk != 'O') if key]
keys=[]
for cand in candidates:
    if cand not in stop_words and not all(char in punct for char in cand):
        keys.append(cand)
print keys

from newsapi import NewsApiClient
import json
import csv

newsapi = NewsApiClient(api_key='0d788dbca30d4dc8ac0758fbe36f5ec0')


f1=open("news_source_ids.txt","r")
news_sources=f1.read()
f1.close()

articles=[]
x=0
query = ' OR '.join(keys)
# /v2/everything
for i in range(1,2):
    all_articles = newsapi.get_everything( q=query,
                                          sources=news_sources,
                                          #domains='bbc.co.uk,techcrunch.com,indiatimes.com,thehindu.com,timesofindia.indiatimes.com',
                                          from_parameter='2007-03-02',
                                          to='2018-03-23',
                                          language='en',
                                          sort_by='relevancy', 
                                          page_size='20',
                                          page=str(i))
    
    articles +=all_articles['articles']
    if len(articles)== x:
        break
    x=len(articles)
    print len(articles)
c=1
#articles=all_articles['articles']
'''
'''
st_lis=[]
for art in articles:
    
    print str(c)+"."
    st=""
    bt=""
    kt=""
    if art['title']==None or art['description']==None:
        continue
    st+=art['title'].encode('ascii','ignore')+" "+art['description'].encode('ascii','ignore')
    bt+=art['url'].encode('ascii','ignore')+" "
    kt+=art['title'].encode('ascii','ignore')+" "
    #print st
    print kt
    print bt
    sda=st.split(" ")
    
    lis=sda[:-1]
    lis=" ".join(lis)
    lis=lis.encode('ascii','ignore')
    li=[]
    li.append(lis)
    st_lis.append(lis)
    c=c+1
    
st_lis = list(set(st_lis))

print st_lis

import nltk, string
from sklearn.feature_extraction.text import TfidfVectorizer

#nltk.download('punkt') # if necessary...
data=st_lis
stemmer = nltk.stem.porter.PorterStemmer()
remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)

def stem_tokens(tokens):
    return [stemmer.stem(item) for item in tokens]

def normalize(text):
    return stem_tokens(nltk.word_tokenize(text.lower().translate(remove_punctuation_map)))

vectorizer = TfidfVectorizer(tokenizer=normalize, stop_words='english')

def cosine_sim(text1, text2):
    tfidf = vectorizer.fit_transform([text1, text2])
    return ((tfidf * tfidf.T).A)[0,1]

cos=[]
for i in range(len(data)):
    cos.append(cosine_sim(text,data[i]))
print max(cos),cos.index(max(cos))
print data[cos.index(max(cos))]
