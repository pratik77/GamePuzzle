from flask_api import FlaskAPI, status, exceptions
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = FlaskAPI(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:rootpass@localhost:3306/puzzle_game'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:admin@localhost:5432/PuzzleGame'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://sql12351269:QbmN5dQw7T@sql12.freemysqlhosting.net:3306/sql12351269'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///covid4New.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db, compare_type=True)