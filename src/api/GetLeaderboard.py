from src.service.Services import Services
from src.utils.Response import Response
from flask_restful import Resource
from flask import request, json
from src.utils.Constants import SUCCESS
from src.utils.database import db
class GetLeaderboard(Resource, Response):
    service = Services()
    def get(self):
        try: 
            responseData = self.service.getLeaderboard(request.data)    
            self.service.removeDbInstance()
            return responseData
        except Exception as err:
            self.service.removeDbInstance()
            return self.errorResponse(err)