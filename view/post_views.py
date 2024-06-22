from flask import request

from controller import *

def post_routes(app):

    @app.post('/teacher')
    def register_teacher():
        data = request.get_json()
        return insert_new_teacher(data)

    @app.post('/admin')
    def register_admin():
        data = request.get_json()
        return insert_new_admin(data)
    
    @app.post('/class')
    def register_class():
        data = request.get_json()
        return insert_new_class(data)
    
    @app.post('/student')
    def register_student():
        data = request.get_json()
        return insert_new_student(data)
    
    @app.post('/class/activity')
    def register_new_class_activity():
        data = request.get_json()
        return insert_new_class_activity(data)
    
    @app.post('/login')
    def check_user_credentials_to_signin():
        data = request.get_json()
        return signin_user(data)
    