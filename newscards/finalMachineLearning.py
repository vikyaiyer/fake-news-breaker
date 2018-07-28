import csv
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer


def train():

    train_data = []
    train_target = []

    f = open("train_data3.csv", "r",encoding="utf-8")
    reader = csv.DictReader(f)
    for row in reader:
        text = row["title"] + row["text"]
        label = row["Label"]
        if label == "FAKE":
            train_data.append(text)
            train_target.append(label)

    f = open("india.csv", "r",encoding="utf-8")
    reader = csv.DictReader(f)
    for row in reader:
        text = row["Text"]
        train_data.append(text)
        train_target.append("REAL")

    f = open("train2.csv", "r",encoding="utf-8")
    reader = csv.DictReader(f)
    for row in reader:
        text = row["title"] + row["text"]
        label = row["label"]
        train_data.append(text)
        train_target.append(label)

    f = open("onion.csv", "r",encoding="utf-8")
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

def predict(user_input):
    X_test = [user_input]
    text_clf = train()
    predicted = text_clf.predict(X_test)
    return predicted



input = "Obama is alive"
text = input.replace("'", "")
text = text.replace('"', '')


predicted = predict(text)
print(predicted)