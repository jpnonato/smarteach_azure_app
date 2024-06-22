from flask import request

from .controller import get_teacher_profile, get_available_teachers, get_available_classes, get_available_admins, get_admin_profile, get_available_students, get_class_profile, get_month_class_activities, get_student_profile


def get_routes(app):
    @app.get('/')
    def teste123():
        return '<h1>---------IS WORKING now 7.9 !9999--------- <h1>', 200

    @app.get('/teacher')
    def show_teachers():
        return get_available_teachers()
    
    @app.get('/teacher/profile/<teacher_id>')
    def show_teacher_profile(teacher_id):
        return get_teacher_profile(teacher_id)
    
    @app.get('/class')
    def show_classes():
        return get_available_classes()
    
    @app.get('/class/profile/<class_id>')
    def show_class_profile(class_id):
        return get_class_profile(class_id)
    
    @app.get('/class/activity/<int:class_number>/<date>')
    def show_monthly_class_activities_data(class_number, date):
        return get_month_class_activities(class_number, date)
    
    @app.get('/student')
    def show_students():
        return get_available_students()
    
    @app.get('/student/profile/<student_id>')
    def show_student_profile(student_id):
        return get_student_profile(student_id)
    
    
    @app.get('/admin')
    def show_admins():
        return get_available_admins()
    
    @app.get('/admin/profile/<admin_id>')
    def show_admin_profile(admin_id):
        return get_admin_profile(admin_id)
