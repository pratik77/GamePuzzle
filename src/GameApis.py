from flask import Flask
from flask_restful import Api
from api.Submit import Submit
from api.GenerateGameName import GenerateGameName
from api.GenerateHelloMsg import GenerateHelloMsg
from api.InsertUserToDB import InsertUserToDB
from api.SubmitAnswer import SubmitAnswer
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate   
from utils.database import *
import configparser
import getopt
import logging
import time
from models import model

# app = Flask(__name__)
# api = Api(app)

api = Api(app)
# app.config['SECRET_KEY'] = b"\x9c\x9a\xd7qam\x95W\xeb\xbc\x88O'T\x12\\\x99\x11\n[\xfd\xaa\rL"

CORS(app)
api.add_resource(Submit, '/submit')
api.add_resource(GenerateGameName, '/generateGameName')
api.add_resource(GenerateHelloMsg, '/generateHelloMsg')
api.add_resource(InsertUserToDB, '/insertUserToDB')
api.add_resource(SubmitAnswer, '/submitAnswer')
if __name__ == '__main__':

    confFile = None
    # handle the command line parameter to receive the configuration file
    # try:

    #     # confFile = "conf/setting.cfg"
    # except:

    #     print("errorCode ")
    #     sys.exit(1)
    try:
        # cmdConfig = configparser.ConfigParser()
        app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
    except Exception as err:
        print(err)