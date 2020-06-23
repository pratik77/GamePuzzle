from service.Services import Services
from utils.Response import Response
from flask_restful import Resource
from flask import request, json
from utils.Constants import SUCCESS
from utils.database import db
class GetUserGamePlayData(Resource, Response):
    service = Services()
    def post(self):
        try: 
            responseData = self.service.userGameplayData(request.data)
            self.service.removeDbInstance()
            return responseData
        except Exception as err:
            return self.errorResponse(err)
