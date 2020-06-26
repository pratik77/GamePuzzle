from service.Services import Services
from utils.Response import Response
from flask_restful import Resource
from flask_restful import Api
from flask import request, json
from utils.Constants import SUCCESS
from utils.database import db
import datetime
from models.model import Competitions

class StartCompetition(Resource, Response):
    service = Services()
    def post(self):
        try:
            competition = self.service.startCompetition()
            self.service.removeDbInstance()
            return self.response("200", competition["hasError"], competition["data"], competition["message"])
        except Exception as err:
            self.service.removeDbInstance()
            return self.errorResponse(err)
            
