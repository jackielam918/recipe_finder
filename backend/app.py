import os

from flask import Flask, render_template, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask import jsonify

load_dotenv('environment/.env')
database_uri = 'postgresql+psycopg2://{dbuser}:{dbpass}@{dbhost}/{dbname}'.format(
    dbuser=os.environ['DBUSER'],
    dbpass=os.environ['DBPASS'],
    dbhost=os.environ['DBHOST'],
    dbname=os.environ['DBNAME']
)

app = Flask(__name__)
app.config.update(
    SQLALCHEMY_DATABASE_URI=database_uri,
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

# initialize the database connection
db = SQLAlchemy(app)

# initialize database migration management
migrate = Migrate(app, db)


@app.route('/')
def home():
    return 'pamplemouse'


@app.route('/ingredient', methods=['POST'])
def hello():
    data = request.get_json()
    ret = {data.get('ingredient'): [1, 2, 3]}
    return jsonify(ret)

