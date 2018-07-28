from django.shortcuts import render
#from django.http import HttpResponse
from newsapi import NewsApiClient
import json
from datetime import datetime,timedelta
import pymysql
from .models import News_Info,News_Tags,User_Upvotes_Data,User_Downvotes_Data,Expert_Upvotes_Data,Expert_Downvotes_Data
import os

#ML
import csv
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

def train():

    train_data = []
    train_target = []

    f = open(os.path.dirname(os.path.realpath(__file__)) + "/train_data3.csv", "r",encoding="utf-8")
    reader = csv.DictReader(f)
    for row in reader:
        text = row["title"] + row["text"]
        label = row["Label"]
        if label == "FAKE":
            train_data.append(text)
            train_target.append(label)

    f = open(os.path.dirname(os.path.realpath(__file__)) + "/india.csv", "r",encoding="utf-8")
    reader = csv.DictReader(f)
    for row in reader:
        text = row["Text"]
        train_data.append(text)
        train_target.append("REAL")

    f = open(os.path.dirname(os.path.realpath(__file__)) + "/train2.csv", "r",encoding="utf-8")
    reader = csv.DictReader(f)
    for row in reader:
        text = row["title"] + row["text"]
        label = row["label"]
        train_data.append(text)
        train_target.append(label)

    f = open(os.path.dirname(os.path.realpath(__file__)) + "/onion.csv", "r",encoding="utf-8")
    reader = csv.DictReader(f)
    for row in reader:
        text = row["text"]
        train_data.append(text)
        train_target.append("FAKE")

    print(len(train_data))

    all_data = train_data

    data = []
    target = []

    r = 0
    f = 0

    for i in range(len(all_data)):
        if train_target[i] == "REAL":
            r += 1
            data.append(train_data[i])
            target.append(train_target[i])

        if r == 6115:
            break

    for i in range(len(all_data)):
        if train_target[i] == "FAKE":
            f += 1
            data.append(train_data[i])
            target.append(train_target[i])

        if f == 6115:
            break

    list_of_dict = []

    for i in range(len(train_data)):
        dict = {}
        dict["text"] = train_data[i]
        dict["label"] = train_target[i]
        list_of_dict.append(dict)

    print(len(list_of_dict))

    import random
    random.shuffle(list_of_dict)

    X_train = []
    X_train_target = []

    X_test = []
    X_test_target= []

    i = 0
    for item in list_of_dict:
        if i % 5 == 0:
            X_test.append(item["text"])
            X_test_target.append(item["label"])
        else:
            X_train.append(item["text"])
            X_train_target.append(item["label"])
        i += 1

    print(len(X_test))
    print(len(X_train))

    text_clf = Pipeline([('vect', CountVectorizer()),('tfidf', TfidfTransformer()),('clf', SGDClassifier(loss='hinge', penalty='l2',alpha=1e-3, random_state=42,max_iter=5, tol=None)),])
    text_clf.fit(X_train, X_train_target)

    return text_clf

def predict(user_input,text_clf):
    X_test = [user_input]

    predicted = text_clf.predict(X_test)
    return predicted

def news_fetch():
        newsapi = NewsApiClient(api_key='20e5b31190a646078d5917d3dbb0d1f6')

        #f1=open("news_source_ids.txt","r")
        #news_sources=f1.read()
        #f1.close()


        d1=datetime.today()
        d2=d1-timedelta(days=7)

        '''top_headlines = newsapi.get_top_headlines( sources='the-times-of-india',
                                          category='general',
                                          language='en',
                                          country='in')'''
        all_articles = newsapi.get_everything(
                                              sources='the-times-of-india',
                                              domains='indiatimes.com,thehindu.com,timesofindia.indiatimes.com',
                                              language='en',
                                              from_parameter=str(d2.date()),
                                              to=str(d1.date()),
                                              sort_by='publishedAt',
                                              page='1')

        articles=all_articles['articles']
        #articles = top_headlines['articles']
        for news in articles:
            news_id = news["publishedAt"]
            author= news["author"]
            url= news["url"]
            source=news["source"]
            title = news["title"]
            description = news["description"]
            publishedAt = news["publishedAt"]
            urlToImage = news["urlToImage"]

            test=News_Info.objects.filter(news_id=news_id)
            if list(test)==[] and news_id != None:
                News_Info.objects.create(news_id=news_id,author=author,url=url,source=source,title=title,description=description,publishedAt=publishedAt,urlToImage=urlToImage,score=0,user_upvotes=0,user_downvotes=0,expert_upvotes=0,expert_downvotes=0)

        return all_articles
        #return top_headline

        #all_arts={}
        #all_arts['articles']=[entry for entry in News_Info.objects.values()]

        #return all_arts


# Create your views here.
def index(request):
    if request.session.has_key('username'):
        username = request.session['username']

    #return HttpResponse("<h2>Hey!, newscards up and runningself.</h2>")
    all_articles = news_fetch()
    articles=all_articles['articles']
    text_clf = train()
    for item in articles:
        if item['title']!=None and item['description']!=None:
            input_news = item['title']+item['description']
            input_news= input_news.replace("'","")
            input_news= input_news.replace('"','')
            result = predict(input_news,text_clf)
            bin=0
            if result=="REAL":
                bin=1
            if item['publishedAt'] != None :
                News_Info.objects.filter(news_id=item['publishedAt']).update(score=bin)
                item['score']=bin

    context = {"input_news":input_news, "result":result}

    #request.session['name'] = request.POST['first_name']
    return render(request, 'newscards/index.html', all_articles)
'''
def upvote_def(request):
    print("Upvoting")
'''
