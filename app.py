from flask import Flask,jsonify
from pymongo import MongoClient
import urllib.parse

from services import get_items_data

app = Flask(__name__)

DB_USER = urllib.parse.quote_plus('smarTeachAdmin')
PASSWORD = urllib.parse.quote_plus('i9vii-d@5V*4_TR')
URL_CONNECTION = "mongodb+srv://{}:{}@cluster0.zhk40vn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
STR_CONNECTION = URL_CONNECTION.format(DB_USER, PASSWORD)

client = MongoClient(STR_CONNECTION)

db = client['SmarTeach']
db_collections = db.list_collection_names()
app_collections = ['Professores', 'Alunos', 'Admins', 'Turmas']

if db_collections != app_collections:
    for collection_name in app_collections:
        if collection_name not in db_collections:
            db.create_collection(collection_name)

teacher_collection = db.get_collection('Professores')
student_collection = db.get_collection('Alunos')
admin_collection = db.get_collection('Admins')
classes_collection = db.get_collection('Turmas')

@app.get('/')
def teste123():
    return '<h1>---------IS WORKING now7!!!--------- <h1>', 200

@app.get('/admin')
def teste777():
    data_list = [data for data in admin_collection.find({})]

    for index, elt in enumerate(data_list):
        data_list[index] = {key: elt[key] if key != '_id' else str(elt[key]) for key in elt}


    return jsonify(data_list), 200



if __name__ == '__main__':
    app.run()
