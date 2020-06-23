from service.Services import Services
from utils.Response import Response
from flask_restful import Resource
from flask import request, json
from utils.Constants import SUCCESS

class GenerateGameName(Resource, Response):
    service = Services()
    def post(self):
        try: 
            data = request.data
            # user = self.service.saveUser(data)
            # userInfo = {}
            # userInfo["id"] = user.id
            print(data["fname"])
            userInfo = data
            userInfo["gamename"] = data["fname"] + data["lname"]
            return self.response("200", "false", userInfo, SUCCESS)
        except Exception as err:
            return self.errorResponse(err)