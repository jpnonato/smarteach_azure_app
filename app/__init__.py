from flask import Flask
from flask_cors import CORS
import logging

app = Flask(__name__, static_folder=None)

from app.view import init_app

init_app(app)
CORS(app)

if __name__ == '__main__':
    logging.info(">>>><<<<<  app started!!")
    app.run(host="0.0.0.0", port=8000)
