from flask import Flask, send_from_directory
from flask_restful import Api
from flask_app.Resources.news import News
from flask_app.Resources.score_logs import ScoreLogs
from flask_cors import CORS
from flask_app.db import db

app = Flask(__name__, static_url_path='', static_folder='frontend/build')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.secret_key = 'yoav'
CORS(app)
api = Api(app)


@app.before_first_request
def create_tables():
    db.init_app(app)
    db.create_all()


@app.route('/')
def serve():
    return send_from_directory(app.static_folder, 'index.html')


api.add_resource(News, '/news/<string:topic>')
api.add_resource(ScoreLogs, '/score_logs/')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
