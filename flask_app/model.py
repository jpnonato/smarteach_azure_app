from .request_services import verify_data_format
from datetime import datetime
from calendar import isleap

class Activity():
    def __init__(self, **kwargs):
        self.name = kwargs['name']
        self.subject = kwargs["subject"]
        self.teacher_email = kwargs["teacher_email"]
    
    @staticmethod
    def verify_new_class_activity_data(data, collection):
        
        if not data.get('class_number'):
            return 'Necessario enviar o campo "number" e o seu respectivo valor numérico'

        classes_data = collection.find({})
        class_number = int(data.get('class_number'))
        class_data = collection.find_one({'number': class_number})
        activity_date = data.get('date') or ''
        activity_time = data.get('time')
        
        db_classes_number_list = [x.get('number') for x in classes_data]
        if class_number not in db_classes_number_list:
            return 'Turma inexistente'
        
        if not activity_date:
            return 'Necessário enviar o data desta aula'
        
        if not verify_data_format(activity_date, "DATE"):
            return 'Formato da data inválido! ele deve ser: "dd/mm/aaaa"'
        
        if not activity_date:
            return 'Necessário enviar o horário desta aula'

        if verify_data_format(activity_time, "TIME"):
            return 'Formato do horário inválido! ele deve ser: hh:min'
        
        day, month, year = activity_date.split('/')

        daily_class_list = [x for x in class_data.get('timeline').get(year).get(month).get(day)]
        if activity_time in daily_class_list:
                return 'Já existe uma aula registrada neste horário!'




class Admin():
  
    def __init__(self, **kwargs):
        self.name = kwargs['name']
        self.email = kwargs['email']
        self.password = kwargs['password']
        self.register_date = datetime.now().strftime("%d/%m/%Y - %H:%M")
        self.last_update_date = datetime.now().strftime("%d/%m/%Y - %H:%M") 
    

    @staticmethod
    def verify_new_admin_data(data: dict):

        available_keys = ['email','name', 'password']

        data_keys = data.keys()

        if len(data_keys) < 3:
            return f'há campos faltantes no corpo da requisição.'

        wrong_keys = [key for key in data_keys if key not in available_keys]

        if wrong_keys:
            return f'Campos incorretos inseridos na requisição: {wrong_keys}'
        
        none_values = {key for key in data if not data[key]}

        if none_values:
            return f'Foi atribuido um valor nulo nas seguintes propriedades: {none_values}'
        
        wrong_values = none_values = {key for key in data if type(data[key]) is not str and type(data[key]) is not list }

        if wrong_values:
            return f'Valores incorretos foram atribuidos as seguintes propriedades: {none_values}'



class Class():
    def __init__(self, **kwargs):
        self.number = int(kwargs['number'])
        self.teachers = []
        self.students = []
        self.timeline = create_month_timeline(datetime.now().year)
        self.register_date = datetime.now().strftime("%d/%m/%Y - %H:%M")
        self.last_update_date = datetime.now().strftime("%d/%m/%Y - %H:%M") 
    
    @staticmethod
    def verify_new_class_data(data):

        class_number = data.get('number')

        if not class_number:
            return 'Necessario enviar o campo "number" e o seu respectivo valor'
        
        if type(class_number) == str:
            if not class_number.isnumeric():
                return 'O valor da propriedade "number" deve ser um número maior ou igual a 100 e menor que 10000'

        if type(class_number) != int and type(class_number) != str:
            return 'O valor da propriedade "number" deve ser um número inteiro, maior ou igual a 100 e menor que 10000'
        
        if int(class_number) < 100 or int(class_number) >= 10000:
            return 'O valor da propriedade "number" deve ser um número inteiro, maior ou igual a 100 e menor que 10000'

    @staticmethod
    def verify_if_exist_class_data(number, classes_data):

        db_classes_number_list = [x.get('number') for x in classes_data]
        
        if int(number) in db_classes_number_list:
            return 'Já existe uma turma registrada com este número'


def create_month_timeline(year):

    d_28 = [2]
    d_30 = [4,6,9,11]

    month_timeline = {}
    leap_year = True if isleap(year) else False

    for month in range(1,13):
        days_range = 31
        if month in d_30:
            days_range -= 1
        elif month in d_28 and leap_year:
            days_range -= 2
        elif month in d_28:
            days_range -= 3 
        
        days_timeline ={}
        for day in range(1, days_range + 1):
            str_day = fill_str_number(day)
            days_timeline.update({str_day: {}})

        str_month = fill_str_number(month)
        month_timeline[str_month] = days_timeline

    return {str(year): month_timeline}


def fill_str_number(number):

        if number < 10:
            return f'0{str(number)}'
        else:
            return str(number)



class Student():
    def __init__(self, **kwargs):
        self.name = kwargs['name']
        self.email = kwargs['email']
        self.password = kwargs['password']
        self.class_number = int(kwargs['class_number'])
    
    @staticmethod
    def verify_student_data(data: dict):
    
        available_keys = ['name', 'email', 'password', 'class_number']
        class_number = data.get('class_number')
        data_keys = data.keys()

        if len(data_keys) < 4:
            return f'há campos faltantes no corpo da requisição.'

        wrong_keys = [key for key in data_keys if key not in available_keys]

        if wrong_keys:
            return f'Campos incorretos inseridos na requisição: {wrong_keys}'
        
        none_values = {key for key in data if not data[key]}

        if none_values:
            return f'Foi atribuido um valor nulo nas seguintes propriedades: {none_values}'
        
        wrong_values = none_values = {key for key in data if type(data[key]) is not str and type(data[key]) is not int }

        if wrong_values:
            return f'Valores incorretos foram atribuidos as seguintes propriedades: {none_values}'
        
        if type(class_number) == str:
            if not class_number.isnumeric():
                return 'Valor incorreto atribuído a propriedade class_number'
            
        if type(class_number) != int and type(class_number) != str:
            return 'Valor incorreto atribuído a propriedade class_number'



class Teacher():
    def __init__(self, **kwargs):
        self.name = kwargs['name']
        self.email = kwargs['email']
        self.password = kwargs['password']
        self.period = kwargs['period']
        self.subject= kwargs['subject']
        self.classes = [int(elt) for elt in kwargs['classes']]
        self.register_date = datetime.now().strftime("%d/%m/%Y - %H:%M")
        self.last_update_date = datetime.now().strftime("%d/%m/%Y - %H:%M") 
    

    @staticmethod
    def verify_new_teacher_data(data: dict):

        available_keys = ['email' ,'name', 'password', 'subject', 'classes', 'period']
        class_list = data.get("classes")
        data_keys = data.keys()

        if len(data_keys) < 6:
            return f'há campos faltantes no corpo da requisição.'

        wrong_keys = [key for key in data_keys if key not in available_keys]

        if wrong_keys:
            return f'Campos incorretos inseridos na requisição: {wrong_keys}'
        
        none_values = {key for key in data if not data[key] and type(data[key]) != list}

        if none_values:
            return f'Foi atribuido um valor nulo nas seguintes propriedades: {none_values}'
        
        wrong_values = none_values = {key for key in data if type(data[key]) is not str and type(data[key]) is not list }

        if wrong_values:
            return f'Valores incorretos foram atribuidos as seguintes propriedades: {none_values}'
        
        for class_number in class_list:
            
            if type(class_number) == str:
                if not class_number.isnumeric():
                    return 'Valor incorreto atribuído a propriedade class_number'
                
            if type(class_number) != int and type(class_number) != str:
                return 'Valor incorreto atribuído a propriedade class_number'
            