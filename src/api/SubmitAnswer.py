from src.service.Services import Services
from src.utils.Response import Response
from flask_restful import Resource
from flask_restful import Api
from flask import request, json
from src.utils.Constants import SUCCESS
from src.utils.database import db

class SubmitAnswer(Resource, Response):
    service = Services()
    def post(self):
        try:
            userAnswer = self.service.submit(request.data)
            #self.service.removeDbInstanceAndCommit()
            self.service.removeDbInstance()
            return self.response("200", userAnswer["hasError"], userAnswer["data"], userAnswer["message"])
        except Exception as err:
            self.service.removeDbInstance()
            return self.errorResponse(err)
            
