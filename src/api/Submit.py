from src.service.Services import Services
from utils.Response import Response
from flask_restful import Resource
from flask import request, json
from utils.Constants import SUCCESS

class Submit(Resource, Response):
    service = Services()
    def post(self):
        try: 
            data = request.data
            user = self.service.saveUser(data)
            userInfo = {}
            userInfo["id"] = user.id
            return self.response("200", "false", userInfo, SUCCESS)
        except Exception as err:
            return self.errorResponse(err)