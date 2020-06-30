from dao.DataAccess import DataAccess
from models.model import Users
from models.model import QuestionSequence
from models.model import Submissions
from models.model import SubmissionDetails
from models.model import Leaderboard
from models.model import Competitions
from utils.Constants import CREATED_BY
from utils.Constants import TOTAL_QUESTIONS
from utils.database import db
from utils.Constants import INVALID_PASSWORD_OR_USER_ALREADY_EXISTS
from utils.Constants import ALL_QUESTIONS_COMPLETED
from utils.Constants import SUCCESS
from utils.Constants import SKIP_COUNT
from utils.Constants import ANSWERS
import os, random
import datetime



class Services():
    dao = DataAccess()

    answers = ANSWERS
    
    def validateAnswer(self, question, answer):
        try:
            if self.answers[int(question)] == answer.casefold():
                return True
            else:
                return False
        except Exception as err:
            raise Exception(err)   
        
    def submit(self, obj):
        try: 
            count = self.insertUserAnswer(obj)
            check = self.validateAnswer(obj["questionNum"], obj["answer"])
            AnswerResponse = {}
            if check:
                AnswerResponse["nextQuestion"] = self.selectNextQuestion(obj)
                AnswerResponse["giveUp"] = "false"
                self.calculateAndUpdateMarks(obj, 10)
                return self.generateResponseParams("200", "false", AnswerResponse, SUCCESS)
            AnswerResponse["nextQuestion"] = obj["questionNum"]
            AnswerResponse["giveUp"] = "false"
            if count >= SKIP_COUNT:
                AnswerResponse["giveUp"] = "true"
            return self.generateResponseParams("200", "true", AnswerResponse, "Incorrect Answer. Plz try again.")
        except Exception as err:
            raise Exception(err)

    def selectNextQuestion(self, obj):
        try:
            gamename = obj["gamename"]
            questionNum = obj["questionNum"]
            questionSequence = self.dao.selectQuestionSequence(gamename).sequence.split(", ")
            length = len(questionSequence) - 1
            pos = questionSequence.index(questionNum)
            if( pos < length ):
                self.dao.updateSolvedQuestionToDB(gamename,questionNum)
                nextQuestion = Submissions(userId = int(gamename),questionNum = int(questionSequence[pos+1]), appearingTime = datetime.datetime.now())
                self.dao.insert(nextQuestion)
                return questionSequence[pos+1]
            else:
                self.dao.updateSolvedQuestionToDB(gamename,questionNum)
                nextQuestion = Submissions(userId=int(gamename),questionNum=TOTAL_QUESTIONS + 1)
                self.dao.updateSolvedQuestionToDB(gamename,questionNum)
                return str(TOTAL_QUESTIONS + 1)
        except Exception as err:
            raise Exception(err)   

    def insertUserAnswer(self,obj):
        try:
            gamename = int(obj["gamename"])
            questionNum = int(obj["questionNum"])
            answer = obj["answer"]
            userAnswer = SubmissionDetails(userId=gamename,questionNum=questionNum,submittedAnswer=answer)
            self.dao.insert(userAnswer)
            return self.dao.updateSubmittionCountToDB(gamename,questionNum)
        except Exception as err:
            raise Exception(err)

    def userGameplayData(self, data):
        try:

            gamename = data["gamename"]
            pin = data["pin"]
            user  = self.dao.getUserByGameName(gamename)
            if user is not None:
                dbPin = user.pin
                if dbPin != int(pin):
                    return self.generateResponseParams("200", "true", {"nextQuestion" : "0", "gamename":gamename, "isAdmin":"false"}, INVALID_PASSWORD_OR_USER_ALREADY_EXISTS)
                elif user.isAdmin == True:
                    return self.generateResponseParams("200", "true", {"nextQuestion" : "0", "gamename":gamename, "isAdmin":"true"}, "HELLO ADMIN")

                else:
                    submission = self.dao.getUnsolvedQuestionForAnUser(user.id)
                    if submission is not None:
                        questionNum = submission.questionNum
                        return self.generateResponseParams("200", "false", {"nextQuestion" : questionNum, "gamename":gamename, "isAdmin":"false"}, SUCCESS)
                    questionNum = TOTAL_QUESTIONS + 1    
                    return self.generateResponseParams("200", "false", {"nextQuestion" : questionNum, "gamename":gamename, "isAdmin":"false"}, ALL_QUESTIONS_COMPLETED)    
            else:
                sequence = [1, 2, 3]
                shuffledSequence = []
                for i in range (4, TOTAL_QUESTIONS + 1):
                    shuffledSequence.append(i)
                shuffledSequence = self.shuffleArray(shuffledSequence)

                #create sequence string here
                sequence += shuffledSequence
                sequenceString = str(sequence[0])
                for i in range(1, TOTAL_QUESTIONS):
                    sequenceString += ", " + str(sequence[i])
                
                #commit to table
                user = Users(id = int(gamename), firstName = data["fname"], familyName = data["lname"], pin = pin)
                self.dao.insert(user)
                leaderboard = Leaderboard(userId = int(gamename))
                self.dao.insert(leaderboard)
                self.dao.commit()
                questionSequence = QuestionSequence(userId = user.id, sequence = sequenceString)
                self.dao.insert(questionSequence)
                self.dao.commit()

                submission = Submissions(userId = user.id, questionNum = 1)
                self.dao.insert(submission)
                self.dao.commit()
                    
                return self.generateResponseParams("200", "false", {"nextQuestion" : "1", "gamename":gamename, "isAdmin":"false"}, SUCCESS)

        except Exception as err:
            raise Exception(err)
    
    
    def generateResponseParams(self, httpStatus, hasError, data, message):
        responseParams = {}
        responseParams['responseCode'] = httpStatus
        responseParams['message'] = message
        responseParams['hasError'] = hasError
        responseParams['data'] = data
        return responseParams

    def shuffleArray(self, arr):
        for i in range(len(arr)-1, 0, -1): 
      
            # Pick a random index from 0 to i  
            j = random.randint(0, i + 1)  
    
            # Swap arr[i] with the element at random index  
            arr[i], arr[j] = arr[j], arr[i]
        return arr

    def removeDbInstance(self):
        try:
            self.dao.removeDbInstance()
        except Exception as err:
            raise Exception(err)
    
    def removeDbInstanceAndCommit(self):
        try:
            self.dao.removeDbInstanceAndCommit()
        except Exception as err:
            raise Exception(err)
    
    def giveUp(self, obj):
        try:
            AnswerResponse = {}
            AnswerResponse["nextQuestion"] = self.selectNextQuestion(obj)
            AnswerResponse["giveUp"] = "false"
            self.calculateAndUpdateMarks(obj, 0)
            return self.generateResponseParams("200", "false", AnswerResponse, SUCCESS)
        except Exception as err:
            raise Exception(err)
    
    def calculateAndUpdateMarks(self, obj, score):
        try:
            gamename = int(obj["gamename"])
            questionNum = int(obj["questionNum"])
            marks = self.dao.getScore(gamename) + score - (self.dao.getTime(gamename,questionNum) * 0.0166667)
            self.dao.updateMarksToDB(gamename,marks)
        except Exception as err:
            raise Exception(err)

    def startCompetition(self):
        try:
            self.dao.delete(Competitions)
            self.dao.delete(Submissions)
            self.dao.delete(SubmissionDetails)
            self.dao.delete(Leaderboard)
            self.dao.delete(QuestionSequence)
            self.dao.delete(Users)
            competition = Competitions(startTime=datetime.datetime.now(), isActive=True)
            self.dao.insert(competition)
            return self.generateResponseParams("200", "false", {"Status" : "GameStarted"}, SUCCESS)
        except Exception as err:
            raise Exception(err)