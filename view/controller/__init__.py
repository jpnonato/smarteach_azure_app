import os
import urllib.parse
from pymongo import MongoClient

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


def signin_user(data):
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return 'Necessário enviar email e password do usuário!', 404
    
    for collection in [student_collection, teacher_collection, admin_collection]:

        user = collection.find_one({'email': email})
        collection_name = collection.name

        if not user:
            continue
        
        if user.get('password') == password:
            user_level = 1

            if collection.name == 'Professores':
                user_level += 1

            elif collection.name == 'Admins':
                user_level += 2

            user_info = {
                'user_level': str(user_level),
                'name': user.get('name'),
                'user_class': user.get('class_number') if collection_name == "Alunos" else user.get('classes')
            }

            return user_info, 200
        
        else:
            return 'Senha incorreta', 400 

    return 'Usuário não registrado!', 400
