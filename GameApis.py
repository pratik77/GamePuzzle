from flask import Flask
from flask_restful import Api
from src.api.Submit import Submit
from src.api.SubmitAnswer import SubmitAnswer
from src.api.GiveUpQuestion import GiveUpQuestion
from flask_cors import CORS, cross_origin
from src.api.GetUserGamePlayData import GetUserGamePlayData
from src.api.StartCompetition import StartCompetition
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate   
from src.utils.database import *
import configparser
import getopt
import logging
import time
from src.models import model
from src.api.GetLeaderboard import GetLeaderboard
from src.api.GetSubmissionDetailsAndLeaderboard import GetSubmissionDetailsAndLeaderboard
from src.api.EndCompetition import EndCompetition

# app = Flask(__name__)
# api = Api(app)

api = Api(app)
# app.config['SECRET_KEY'] = b"\x9c\x9a\xd7qam\x95W\xeb\xbc\x88O'T\x12\\\x99\x11\n[\xfd\xaa\rL"

CORS(app, support_credentials=True)
api.add_resource(Submit, '/submit')
api.add_resource(GetUserGamePlayData, '/getUserGamePlayData')
api.add_resource(GetLeaderboard, '/getLeaderboard')
api.add_resource(GetSubmissionDetailsAndLeaderboard, '/getSubmissionDetailsAndLeaderboard')
api.add_resource(GiveUpQuestion, '/giveUpQuestion')
api.add_resource(SubmitAnswer, '/submitAnswer')
api.add_resource(StartCompetition,'/startCompetition')
api.add_resource(EndCompetition,'/endCompetition')
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