from flask import Flask
from flask_cors import CORS

app = Flask(__name__, static_folder=None)

from app.view import init_app

init_app(app)
CORS(app)




