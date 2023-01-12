import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import re
import sys

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
collection = db.collection('main')

def search_birthday(search_word):
    docs = collection.where("name","==",search_word).get()
    result = []
    for doc in docs:
        result.append(doc.to_dict())
    return result

def lazy_search(search_word):
    docs = collection.get()
    result = []
    for doc in docs:
        if search_word in doc.to_dict()['name']:
            result.append(doc.to_dict())
    return result

def add(data):
    index = re.search(r"\d",data)
    name = re.sub(' +', ' ', data[:index.start()]).strip()
    dob = re.sub(' +', ' ', data[index.start():]).strip()
    collection.add({'name':name,'DOB':dob})


def search_all():
    docs = collection.get()
    result = []
    for doc in docs:
        result.append(doc.to_dict())
    return result


def edit(data):
    name = data[0].strip()
    dob = data[1].strip()
    newName = data[2].strip()
    newDOB = data[3].strip()
    docs = collection.where("name","==",name).get()
    for doc in docs:
        if doc.to_dict()['DOB'] == dob:
            key = doc.id
            collection.document(key).update({"name":newName,"DOB":newDOB})

def deleteOne(data):
    index = re.search(r"\d",data)
    dob = re.sub(' +', ' ', data[index.start():]).strip()
    name = re.sub(' +', ' ', data[:index.start()]).strip()
    docs = collection.where("name","==",name).get()
    for doc in docs:
        if doc.to_dict()['DOB'] == dob and doc.to_dict()['name'] == name:
            key = doc.id
            collection.document(key).delete()