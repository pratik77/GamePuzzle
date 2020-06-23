from service.Services import Services
from utils.Response import Response
from flask_restful import Resource
from flask_restful import Api
from flask import request, json
from utils.Constants import SUCCESS
from utils.database import db

class SubmitAnswer(Resource, Response):
    service = Services()
    def post(self):
        try:
            userAnswer = self.service.submit(request.data)
            return self.response("200", userAnswer["hasError"], userAnswer["data"], userAnswer["message"])
        except Exception as err:
            return self.errorResponse(err)
