from dao.DataAccess import DataAccess
from models.model import Users
from utils.Constants import CREATED_BY
from utils.Constants import SUCCESS
from utils.database import db
#from Services import Services
import os



class Services():
    dao = DataAccess()

    answers = {
                1: "Answer1",
                2: "Answer2",
                3: "Answer3"
    }
    
    def validateAnswer(self, question, answer):
        try:
            if self.answers[int(question)] == answer:
                return True
            else:
                return False
        except Exception as err:
            raise Exception(err)   
        
    def submit(self, obj):
        try: 
            check = self.validateAnswer(obj["questionNum"], obj["answer"])
            responseData = {}
            if check:
                correctAnswer = {}
                correctAnswer["questionNum"] = self.dao.selectNextQuestion(obj["gamename"], obj["questionNum"])
                responseData["hasError"] = "false"
                responseData["message"] = SUCCESS
                responseData["data"] = correctAnswer
                return responseData
            wrongAnswer = {}
            wrongAnswer["questionNum"] = obj["questionNum"]
            responseData["hasError"] = "true"
            responseData["message"] = "Incorrect Answer. Plz try again."
            responseData["data"] = wrongAnswer
            return responseData
        except Exception as err:
            raise Exception(err)

    def checkUser(self,obj):
        try:
            gameName = self.dao.selectGameName(obj)
            return bool(gameName)
        except Exception as err:
            raise Exception(err)

    def insertUser(self,data):
        try:
            fname = data["fname"]
            lname = data["lname"]
            gamename = fname + lname
            user = Users(firstName=fname,familyName=lname,gameName=gamename)
            chk = self.checkUser(user)
            userInfo = {}
            if not chk:
                self.dao.insert(user)
                userInfo["id"] = user.id
                return userInfo
            return {}
        except Exception as err:
            raise Exception(err)
    
    
        