
from flask import Flask, jsonify


app = Flask(__name__, static_folder=None)


@app.get('/admin')
def show_admins():

    data_list = [{
            "1": 1000
        },
        {
            "2":2000
        }
    ]


    return jsonify(data_list), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
