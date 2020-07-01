from src.dao.DataAccess import DataAccess
from src.models.model import Users
from src.models.model import QuestionSequence
from src.models.model import Submissions
from src.models.model import SubmissionDetails
from src.models.model import Leaderboard
from src.models.model import Competitions
from src.utils.Constants import CREATED_BY
from src.utils.Constants import TOTAL_QUESTIONS
from src.utils.database import db
from src.utils.Constants import INVALID_PASSWORD_OR_USER_ALREADY_EXISTS
from src.utils.Constants import ALL_QUESTIONS_COMPLETED
from src.utils.Constants import SUCCESS
from src.utils.Constants import TOTAL_QUESTIONS
from src.models.model import Users
from src.models.model import Leaderboard
from src.utils.Constants import SKIP_COUNT
from src.utils.Constants import ANSWERS
from src.utils.Constants import CORRECT_ANSWER
from src.utils.Constants import INVALID_ANSWER
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
            # if(self.hasQuestionBeenSolved(obj)):
            #     data = {}
            #     data["nextQuestion"] = self.getNextQuestion(obj)
            #     # data["giveUp"] = "false"
            #     # data["answer"] = self.answers[int(data["nextQuestion"])]
            #     return self.generateResponseParams("200", "false", data, CORRECT_ANSWER)

            count = self.insertUserAnswer(obj)
            check = self.validateAnswer(obj["questionNum"], obj["answer"])
            AnswerResponse = {}
            if check:
                AnswerResponse["nextQuestion"] = self.selectNextQuestion(obj)
                # AnswerResponse["giveUp"] = "false"
                # AnswerResponse["answer"] = self.answers[int(AnswerResponse["nextQuestion"])]
                self.updateLeaderboardMarks2(obj)
                self.calculateAndUpdateMarks(obj, 10)
                return self.generateResponseParams("200", "false", AnswerResponse, CORRECT_ANSWER)
            AnswerResponse["nextQuestion"] = obj["questionNum"]
            AnswerResponse["giveUp"] = "false"
            AnswerResponse["answer"] = self.answers[int(AnswerResponse["nextQuestion"])]
            if count >= SKIP_COUNT:
                AnswerResponse["giveUp"] = "true"
            return self.generateResponseParams("200", "true", AnswerResponse, INVALID_ANSWER)
        except Exception as err:
            raise Exception(err)

    def hasQuestionBeenSolved(self, obj):
        gamename = obj["gamename"]
        questionNum = obj["questionNum"]
        currQuestion = self.dao.getSubmissionByUserIdAndQuestionNum(gamename, questionNum)
        if currQuestion is None:
            return True
        return currQuestion.isSolved

    def selectNextQuestion(self, obj):
        try:
            gamename = obj["gamename"]
            questionNum = obj["questionNum"]
            questionSequence = self.dao.selectQuestionSequence(gamename).sequence.split(", ")
            length = len(questionSequence) - 1
            pos = questionSequence.index(questionNum)
            if(pos < length):
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

    def getNextQuestion(self, obj):
        try:
            gamename = obj["gamename"]
            questionNum = obj["questionNum"]
            questionSequence = self.dao.selectQuestionSequence(gamename).sequence.split(", ")
            length = len(questionSequence) - 1
            pos = questionSequence.index(questionNum)
            if(pos < length):
                return questionSequence[pos+1]
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
                    data = {}
                    data["questionSequence"] = ["0"]
                    data["gamename"] = gamename
                    data["isAdmin"] = "false"
                    data["answers"] = ANSWERS 
                    return self.generateResponseParams("200", "true", data, INVALID_PASSWORD_OR_USER_ALREADY_EXISTS)
                elif user.isAdmin == True:
                    data = {}
                    data["questionSequence"] = ["0"]
                    data["gamename"] = gamename
                    data["isAdmin"] = "true"
                    data["answers"] = ANSWERS
                    return self.generateResponseParams("200", "true", data, "HELLO ADMIN")

                else:
                    submission = self.dao.getUnsolvedQuestionForAnUser(user.id)
                    data = {}
                    data["answers"] = ANSWERS
                    data["isAdmin"] = "false"
                    data["gamename"] = gamename  
                    if submission is not None:
                        remainingQuestionsLeft = self.getRemainingQuestionsLeft(submission, gamename)
                        data["questionSequence"] = remainingQuestionsLeft
                        return self.generateResponseParams("200", "false", data, SUCCESS)
                    remainingQuestionsLeft = ["11"]
                    data["questionSequence"] = remainingQuestionsLeft   
                    return self.generateResponseParams("200", "false", data, ALL_QUESTIONS_COMPLETED)    
            else:
                shuffledSequence = []
                for i in range (1, TOTAL_QUESTIONS + 2):
                    shuffledSequence.append(i)
                # shuffledSequence = self.shuffleArray(shuffledSequence, 3, 8)

                #create sequence string here
                sequenceString = str(shuffledSequence[0])
                for i in range(1, TOTAL_QUESTIONS + 1):
                    sequenceString += ", " + str(shuffledSequence[i])
                
                #commit to table
                user = Users(id = int(gamename), firstName = data["fname"], familyName = data["lname"], pin = pin)
                self.dao.insert(user)
                # self.dao.commit()

                questionSequence = QuestionSequence(userId = user.id, sequence = sequenceString)
                self.dao.insert(questionSequence)
                # self.dao.commit()

                submission = Submissions(userId = user.id, questionNum = 1)
                self.dao.insert(submission)
                # self.dao.commit()
                
                leaderboard = Leaderboard(userId = user.id)
                self.dao.insert(leaderboard)
                data = {}
                data["answers"] = ANSWERS
                data["isAdmin"] = "false"
                data["gamename"] = gamename
                data["questionSequence"] = sequenceString.split(", ")
                return self.generateResponseParams("200", "false", data, SUCCESS)

        except Exception as err:
            raise Exception(err)
    
    def getRemainingQuestionsLeft(self, submission, gamename):
        unsolvedQuestionNum = submission.questionNum
        questionSequence = self.dao.selectQuestionSequence(gamename).sequence.split(", ")
        pos = questionSequence.index(str(unsolvedQuestionNum))
        remainingQuestionsLeft = []
        for i in range(pos, TOTAL_QUESTIONS):
            remainingQuestionsLeft.append(int(questionSequence[i]))
        remainingQuestionsLeft.append(str(TOTAL_QUESTIONS + 1))
        return remainingQuestionsLeft

    def generateResponseParams(self, httpStatus, hasError, data, message):
        responseParams = {}
        responseParams['responseCode'] = httpStatus
        responseParams['message'] = message
        responseParams['hasError'] = hasError
        responseParams['data'] = data
        return responseParams

    def shuffleArray(self, arr, start, end):
        for i in range(start - 1, end - 1, 1): 
      
            # Pick a random index from 0 to i  
            j = random.randint(i + 1, end - 1)  
    
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

    def getLeaderboard(self, data):

        try:
            users = self.dao.getAllUsersByMarks()
            leaderboard = []

            for user in users:
                userData = {}
                userData["fname"] = user.Users.firstName
                userData["marks"] = user.Leaderboard.marks[0]
                leaderboard.append(userData)
            
            return self.generateResponseParams("200", "false", {"leaderboard" : leaderboard}, SUCCESS)
        except Exception as err:
            raise Exception(err)

    def getSubmissionDetails(self, data):

        try:
            details = self.dao.getLatestSubmissionsDetails()
            submittedAnswers = []

            for detail in details:
                userData = {}
                userData["fname"] = detail.Users.firstName
                userData["questionNum"] = detail.SubmissionDetails.questionNum
                userData["submittedAnswer"] = detail.SubmissionDetails.submittedAnswer
                submittedAnswers.append(userData)
            
            return self.generateResponseParams("200", "false", {"submissionDetails" : submittedAnswers}, SUCCESS)
        except Exception as err:
            raise Exception(err)

    def getSubmissionDetailsAndLeaderboard(self, data):

        try:
            details = self.dao.getLatestSubmissionsDetails()
            submittedAnswers = []

            users = self.dao.getAllUsersByMarks()
            leaderboard = []

            users2 = self.dao.getAllUsersByMarks2()
            leaderboard2 = []

            for detail in details:
                userData = {}
                userData["fname"] = detail.Users.firstName
                userData["questionNum"] = detail.SubmissionDetails.questionNum
                userData["submittedAnswer"] = detail.SubmissionDetails.submittedAnswer
                userData["actualAnswer"] = self.answers[detail.SubmissionDetails.questionNum]
                submittedAnswers.append(userData)

            i = 1
            for user in users:
                userData = {}
                userData["gamename"] = user.Users.id
                userData["fname"] = user.Users.firstName
                userData["marks"] = user.Leaderboard.marks
                userData["rank"] = i
                i = i + 1
                leaderboard.append(userData)

            i = 1
            for user in users2:
                userData = {}
                userData["gamename"] = user.Users.id
                userData["fname"] = user.Users.firstName
                userData["marks"] = user.Leaderboard.marks2
                userData["rank"] = i
                i = i + 1
                leaderboard2.append(userData)
            
            return self.generateResponseParams("200", "false", {"submissionDetails" : submittedAnswers, "leaderboard":leaderboard, "leaderboard2":leaderboard2}, SUCCESS)
        except Exception as err:
            raise Exception(err)

    def updateLeaderboardMarks2(self, data):

        try:
            gamename = int(data["gamename"])
            leaderboard = self.dao.getMarksDetailsOfUser(gamename)
            marks2 = leaderboard.marks2

            existsRowsWithMarks2 = self.dao.getExistsRowWithMarks2(marks2 + 10)
            print(existsRowsWithMarks2)
            if existsRowsWithMarks2 is None:
                leaderboard.milestoneCount = leaderboard.milestoneCount + 1
            leaderboard.marks2 = marks2 + 10
            self.dao.insert(leaderboard)
            
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
