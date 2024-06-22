import urllib.parse
from bson import ObjectId
from flask import jsonify
from pymongo import MongoClient

from .request_services import *
from .model import Activity, Admin, Class, Student, Teacher

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



def insert_new_class_activity(data):

    is_wrong_data = Activity.verify_new_class_activity_data(data, classes_collection)  
    if is_wrong_data: 
        return is_wrong_data, 400
    
    is_registered_teacher = verify_user_email(data.get('teacher_email'), teacher_collection.find({}))
    if not is_registered_teacher:
        return "Professor inexistente!", 400

    day, month, year = data.get('date').split('/')
    time_interval = data.get('time')

    new_activity = Activity(**data).__dict__
    class_profile = classes_collection.find_one({'number': int(data.get('class_number'))})
    class_profile['timeline'][year][month][day].update({time_interval: new_activity})

    new_values = {"$set": class_profile}
    classes_collection.update_one({'number': data.get('class_number')}, new_values)

    return 'Nova Aula registrada com sucesso!', 201


def get_month_class_activities(class_number, date):

    month, year = date.split('-')
    classes_data = classes_collection.find({})

    is_existent_data = Class.verify_if_exist_class_data(class_number, classes_data)  

    if not is_existent_data: 
        return "Turma inexistente", 400

    class_profile = classes_collection.find_one({'number': class_number})
    monthly_activities = class_profile['timeline'][year][month]

    return jsonify(monthly_activities), 200


def update_class_activity_profile(data):

    class_number = data.get('class_number')
    classes_data = classes_collection.find({})
    is_existent_data = Class.verify_if_exist_class_data(class_number, classes_data)  

    if not is_existent_data: 
        return "Turma inexistente", 400
 
    available_class_keys = ['teachers', 'students', 'subject', 'class_number', 'date', 'time']

    wrong_properties = verify_update_sent_data_request(data, available_class_keys)
    if wrong_properties:
        return wrong_properties, 400

    day, month, year = data.get('date').split('/')
    time_interval = data.get('time')

    class_profile = classes_collection.find_one({'number': class_number})
    current_activity = class_profile['timeline'][year][month][day][time_interval]

    for key in data.keys():
        if key not in ['class_number', 'date', 'time']:
            current_activity.update({key: data[key]})

    class_profile.update({"last_update_date": update_time_data()})

    new_values = {"$set": class_profile}
    classes_collection.update_one({'number': class_number}, new_values)

    return 'Aula atualizada com sucesso!', 200


def delete_class_activity_profile(data):

    class_number = data.get('class_number')
    classes_data = classes_collection.find({})

    is_existent_data = Class.verify_if_exist_class_data(class_number, classes_data)  
    if not is_existent_data: 
        return "Turma inexistente", 400
    
    available_class_keys = ['teachers', 'students', 'subject', 'class_number', 'date', 'time']
    wrong_properties = verify_update_sent_data_request(data, available_class_keys)

    if wrong_properties:
        return wrong_properties, 400
    
    day, month, year = data.get('date').split('/')
    time_interval = data.get('time')

    class_profile = classes_collection.find_one({'number': class_number})
    current_day_activity = class_profile['timeline'][year][month][day]

    if time_interval not in current_day_activity.keys():
        return 'Atividade inexistente', 400
    
    current_day_activity.pop(time_interval)
    new_values = {"$set": class_profile}
    classes_collection.update_one({'number': class_number}, new_values)

    return 'Aula removida com sucesso', 200



def get_available_admins():

    admin_list = get_items_data(admin_collection.find({}))

    return jsonify(admin_list), 200


def insert_new_admin(data: dict):

    is_wrong_data = Admin.verify_new_admin_data(data)

    if is_wrong_data: 
        return is_wrong_data, 400

    is_same_email = verify_user_email(data["email"], admin_collection.find({}))

    if is_same_email: 
        return is_same_email, 409

    new_Admin = Admin(**data)
    admin_collection.insert_one(new_Admin.__dict__)

    return 'Novo Administrador registrado com sucesso!', 201


def delete_admin_profile(data):

    wrong_data_request = verify_request_data(data, admin_collection)
    if wrong_data_request: 
        return wrong_data_request, 400

    admin_id = ObjectId(data['id'])
    admin = admin_collection.delete_one({'_id': admin_id})

    if admin:
        admin_collection.delete_one({'_id': admin_id})
        return 'Perfil de Administrador deletado com sucesso!', 200
    else:
        return 'Administrador não encontrado', 400


def update_admin_profile(data):

    wrong_data_request = verify_request_data(data, admin_collection)
    if wrong_data_request: 
        return wrong_data_request, 400

    user_id = data.get('id')
    available_student_keys = ['name', 'email', 'password', 'id']

    wrong_properties = verify_update_sent_data_request(data, available_student_keys)
    if wrong_properties:
        return wrong_properties, 400


    update_data = {key: data[key] for key in data.keys() if key != 'id'}

    if update_data:
        new_values = {"$set": update_data}
        admin_collection.update_one({'_id': ObjectId(user_id)}, new_values)
        admin_collection.update_one({'_id': ObjectId(user_id)}, update_time_data())

        return 'Perfil de Administrador atualizado com sucesso!', 200


def get_admin_profile(user_id):

    wrong_request_data = verify_request_data({'id': user_id}, admin_collection, 'GET')
    if wrong_request_data:
        return wrong_request_data, 400
    
    admin_profile = get_data_by_id(user_id, admin_collection)

    return jsonify(admin_profile), 200



def get_available_classes():

    classes_list = get_items_data(classes_collection.find({}))
    return jsonify(classes_list), 200


def get_class_profile(class_id):

    wrong_request_data = verify_request_data({'id': class_id}, classes_collection, 'GET')
    if wrong_request_data:
        return wrong_request_data, 400

    class_profile = classes_collection.find_one({'_id': ObjectId(class_id)})
    class_profile = get_data_by_id(class_id, classes_collection)

    return jsonify(class_profile), 200


def insert_new_class(data):

    is_wrong_data = Class.verify_new_class_data(data)
    if is_wrong_data: 
        return is_wrong_data, 400
    
    classes_data = classes_collection.find({})
    is_inexistent_data = Class.verify_if_exist_class_data(data.get('number'), classes_data)
    
    if is_inexistent_data: 
        return is_inexistent_data, 400  

    new_class = Class(**data)
    classes_collection.insert_one(new_class.__dict__)

    return 'Nova turma registrada com sucesso!', 201


def update_class_profile(data):

    wrong_data_request = verify_request_data(data, classes_collection, 'PATCH')
    if wrong_data_request: 
        return wrong_data_request, 400

    class_id = data.get('id')
    available_class_keys = ['teachers', 'students', 'number', 'id']

    wrong_properties = verify_update_sent_data_request(data, available_class_keys)
    if wrong_properties:
        return wrong_properties, 400

    for key in data.keys():

        if key != 'id':
            new_values = {"$set": {key: data[key]}}
            classes_collection.update_one({'_id' : ObjectId(class_id)}, new_values)
    
    classes_collection.update_one({'_id' : ObjectId(class_id)}, update_time_data())

    return 'Turma atualizada com sucesso', 200


def delete_class_profile(data):

    wrong_data = verify_request_data(data, classes_collection)
    if wrong_data:
        return wrong_data, 400
 
    class_id = {"_id": ObjectId(data.get("id"))}
    classes_collection.delete_one(class_id)

    return 'Turma removida com sucesso', 200



def get_available_students():

    student_list = get_items_data(student_collection.find({}))

    return jsonify(student_list), 200


def insert_new_student(data: dict):

    is_wrong_data = Student.verify_student_data(data)

    if is_wrong_data: 
        return is_wrong_data, 400
    
    classes_data = classes_collection.find({})
    class_number = data.get('class_number')
    is_existent_class = Class.verify_if_exist_class_data(class_number, classes_data)

    if not is_existent_class: 
        return "Turma inexistente", 400  
    
    student_email = data.get("email")
    is_same_email = verify_user_email( student_email, student_collection.find({}))

    if is_same_email: 
        return is_same_email, 409
    
    new_student = Student(**data)
    student_collection.insert_one(new_student.__dict__)
    student_data = get_user_by_email(student_email, student_collection)

    selected_class = classes_collection.find_one({'number': int(class_number)})
    class_id = selected_class.get('_id')
    class_students = selected_class.get('students')

    if student_data not in class_students:
        class_students.append(student_data)
        update_class_profile({'id': class_id, 'students': class_students})
    
    return 'Novo aluno cadastrado com sucesso!', 201


def update_student_profile(data):
    
    wrong_data_request = verify_request_data(data, student_collection, 'PATCH')
    if wrong_data_request: 
        return wrong_data_request, 400

    user_id = data.get('id')
    
    available_student_keys = ['name', 'email', 'password', 'class_number', 'id']

    wrong_properties = verify_update_sent_data_request(data, available_student_keys)
    if wrong_properties:
        return wrong_properties, 400

    for key in data.keys():

        if key != 'id':
            new_values = {"$set": {key: data[key]} }
            student_collection.update_one({'_id' : ObjectId(user_id)}, new_values)
    
    student_collection.update_one({'_id' : ObjectId(user_id)}, update_time_data())

    return 'Perfil de Estudante atualizado com sucesso!', 200


def delete_student_profile(data):

    wrong_data_request = verify_request_data(data, student_collection)
    if wrong_data_request: 
        return wrong_data_request, 400
    
    user_id = data.get('id')
    student_data = get_data_by_id(user_id, student_collection)
    student_collection.delete_one({"_id": ObjectId(user_id) })
    
    selected_class = classes_collection.find_one({'number': student_data.get('class_number')})
    class_id = selected_class.get('_id')
    class_students = selected_class.get('students')

    filtered_class_students = [student for student in class_students if student['_id'] != user_id]
    update_class_profile({'id': class_id, 'students': filtered_class_students})

    return 'Perfil de Estudante deletado com sucesso!', 200


def get_student_profile(user_id):

    wrong_request_data = verify_request_data({'id': user_id}, student_collection, 'GET')
    if wrong_request_data:
        return wrong_request_data, 400
    
    teacher_profile = get_data_by_id(user_id, student_collection)

    return jsonify(teacher_profile), 200



def get_available_teachers():

    teacher_list = get_items_data(teacher_collection.find({}))

    return jsonify(teacher_list), 200


def get_teacher_profile(user_id):

    wrong_request_data = verify_request_data({'id': user_id}, teacher_collection, 'GET')
    if wrong_request_data:
        return wrong_request_data, 400
    
    teacher_profile = get_data_by_id(user_id, teacher_collection)

    return jsonify(teacher_profile), 200


def insert_new_teacher(data: dict):

    is_wrong_data = Teacher.verify_new_teacher_data(data)  

    if is_wrong_data: 
        return is_wrong_data, 400

    teacher_email = data.get('email')
    is_same_email = verify_user_email(teacher_email, teacher_collection.find({}))

    if is_same_email: 
        return is_same_email, 409
    
    inexistent_class_numbers = []

    for class_number in data.get("classes"):
        is_existent_class = Class.verify_if_exist_class_data(class_number, classes_collection.find({}))

        if not is_existent_class:
           inexistent_class_numbers.append(class_number)

    if inexistent_class_numbers:
        return "Turma(s) inexistente(s):{}".format(inexistent_class_numbers), 400

    new_teacher = Teacher(**data)
    teacher_collection.insert_one(new_teacher.__dict__)
    teacher_data = get_user_by_email(teacher_email, teacher_collection)

    for class_number in data.get("classes"):
        selected_class = classes_collection.find_one({'number': int(class_number)})
        class_id = selected_class.get('_id')
        class_teachers = selected_class.get('teachers')

        if teacher_data not in class_teachers:
            class_teachers.append(teacher_data)
            update_class_profile({'id': class_id, 'teachers': class_teachers})

    return 'Novo Professor registrado com sucesso!', 201
    

def update_teacher_profile(data):

    wrong_data_request = verify_request_data(data, teacher_collection, 'PATCH')
    if wrong_data_request: 
        return wrong_data_request, 400

    user_id = data.get('id')
    available_teacher_keys = ['name', 'email', 'password', 'classes', 'subject', 'period', 'id']

    wrong_properties = verify_update_sent_data_request(data, available_teacher_keys)
    if wrong_properties:
        return wrong_properties, 400

    for key in data.keys():

        if key != 'id':
            new_values = {"$set": {key: data[key]} }
            teacher_collection.update_one({'_id' : ObjectId(user_id)}, new_values)
    
    teacher_collection.update_one({'_id' : ObjectId(user_id)}, update_time_data())

    return 'Perfil de Professor atualizado com sucesso!', 200


def delete_teacher_profile(data):
    
    wrong_data_request = verify_request_data(data, teacher_collection)
    if wrong_data_request: 
        return wrong_data_request, 400
    
    user_id = data.get('id')
    teacher_data = get_data_by_id(user_id, teacher_collection)
    teacher_collection.delete_one({"_id": ObjectId(user_id)})

    for class_number in teacher_data.get("classes"):
        selected_class = classes_collection.find_one({'number': class_number})
        class_id = selected_class.get('_id')
        class_teachers = selected_class.get('teachers')

        filtered_class_teachers = [teacher for teacher in class_teachers if teacher['_id'] != user_id]
        update_class_profile({'id': class_id, 'teachers': filtered_class_teachers})

    return 'Perfil de Professor deletado com sucesso!', 200 
