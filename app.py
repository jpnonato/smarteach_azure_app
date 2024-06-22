from flask import Flask

app = Flask(__name__)

@app.get('/')
def teste123():
    return '<h1>---------IS WORKING now!!!--------- <h1>', 200


if __name__ == '__main__':
    app.run()
