from flask import Flask, send_from_directory
from flask_restful import Api
from flask_jwt import JWT
from datetime import timedelta
from flask_app.db import db
from Resources.news import News
from flask_cors import CORS

app = Flask(__name__, static_url_path='', static_folder='frontend/build')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_EXPIRATION_DELTA'] = timedelta(minutes=15)

app.secret_key = 'yoav'
api = Api(app)

CORS(app)


@app.before_first_request
def create_tables():
    db.init_app(app)
    db.create_all()


# @app.route('/')
# def serve():
#     return send_from_directory()

api.add_resource(News, '/news/<string:topic>')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
