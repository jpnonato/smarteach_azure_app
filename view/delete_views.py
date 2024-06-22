from flask import request

from .controller import delete_teacher_profile, delete_student_profile, delete_class_profile, delete_class_activity_profile, delete_admin_profile


def delete_routes(app):
    @app.delete('/teacher')
    def delete_teacher_data_profile():
        data = request.get_json()
        return delete_teacher_profile(data)
    
    @app.delete('/student')
    def delete_student_data_profile():
        data = request.get_json()
        return delete_student_profile(data)
         
    @app.delete('/class')
    def delete_class_data_profile():
        data = request.get_json()
        return delete_class_profile(data)
    
    @app.delete('/class/activity')
    def delete_activity_class_data_profile():
        data = request.get_json()
        return delete_class_activity_profile(data)

    @app.delete('/admin')
    def delete_admin_data_profile():
        data = request.get_json()
        return delete_admin_profile(data)