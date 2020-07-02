from src.service.Services import Services
from src.utils.Response import Response
from flask_restful import Resource
from flask_restful import Api
from flask import request, json
from src.utils.Constants import SUCCESS
from src.utils.database import db
import datetime
from src.models.model import Competitions

class EndCompetition(Resource, Response):
    service = Services()
    def get(self):
        try:
            competition = self.service.endCompetition()
            self.service.removeDbInstance()
            return self.response("200", "false", {}, SUCCESS)
        except Exception as err:
            self.service.removeDbInstance()
            return self.errorResponse(err)
            
