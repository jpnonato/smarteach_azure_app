import logging
import os
import urllib.parse
from flask import Flask, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv
from services import get_items_data


app = Flask(__name__, static_folder=None)

# from app.view import init_app

# init_app(app)
CORS(app)

load_dotenv()

DB_USER = urllib.parse.quote_plus(os.getenv('DB_USER'))
PASSWORD = urllib.parse.quote_plus(os.getenv('PASSWORD'))
STR_CONNECTION = os.getenv('DB_STR_CONNECTION').format(DB_USER, PASSWORD)

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


@app.get('/admin')
def show_admins():
    admin_list = get_items_data(admin_collection.find({}))

    return jsonify(admin_list), 200


if __name__ == '__main__':
    logging.info(">>>><<<<<  app started!")
    app.run(host="0.0.0.0", port=8000)
