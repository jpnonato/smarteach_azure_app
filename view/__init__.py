# from .delete_views import delete_routes
# from .get_views import get_routes
# from .patch_views import patch_routes
# from .post_views import post_routes

from flask import jsonify
from pymongo import MongoClient
import urllib.parse
from services import get_items_data


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

def init_app(app):

    @app.get('/')
    def teste123():
        return '<h1>---------IS WORKING now 7.9 !$&--------- <h1>', 200

    @app.get('/admin')
    def teste777():
        data_list = get_items_data(admin_collection.find({}))
        return jsonify(data_list), 200
