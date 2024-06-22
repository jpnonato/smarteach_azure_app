from flask import Flask,jsonify

from view import init_app

app = Flask(__name__)

# @app.get('/')
# def teste123():
#     return '<h1>---------IS WORKING now 7.4 !4--------- <h1>', 200

# @app.get('/admin')
# def teste777():
#     data_list = get_items_data(admin_collection.find({}))
#     return jsonify(data_list), 200

init_app(app)

if __name__ == '__main__':
    app.run()
