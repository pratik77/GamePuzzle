from models.model import Users
from models.model import QuestionSequence
from utils.database import db
from models.model import Submissions
from sqlalchemy import and_
from models.model import Users
import datetime


class DataAccess:
    def insert(self, obj):
        try:
            db.session.add(obj)
            db.session.commit()
            return obj
        except Exception as err:
            raise Exception(err)

    def commit(self):
        try:
            db.session.commit()
        except Exception as err:
            raise Exception(err)        

    def getUnsolvedQuestionForAnUser(self, userId):
        try:
            submission = db.session.query(Submissions.questionNum).filter(and_(Submissions.userId == userId, Submissions.isSolved == False)).first()
            return submission

        except Exception as err:
            raise Exception(err)

    def getUserByGameName(self, gamename):
        try:
            user = Users.query.get(int(gamename))
            return user
        except Exception as err:
            raise Exception(err)

    def removeDbInstance(self):
        try:
            db.session.remove()
        except Exception as err:
            raise Exception(err)
    
    def removeDbInstanceAndCommit(self):
        try:
            self.commit()
            self.removeDbInstance()
        except Exception as err:
            raise Exception(err)
    
    def updateSubmittionCountToDB(self,gamename,questionNum):
        try:
            submission = Submissions.query.filter(and_(Submissions.userId == int(gamename),Submissions.questionNum == int(questionNum))).first()
            count = submission.submissionCount
            submission.submissionCount = int(count) + 1
            self.insert(submission)
            return count + 1
        except Exception as err:
            raise Exception(err)

    def updateSolvedAnswerToDB(self,gamename,questionNum):
        try:
            submission = Submissions.query.filter(and_(Submissions.userId == int(gamename),Submissions.questionNum == int(questionNum))).first()
            submission.isSolved = True
            submission.submissionTime = datetime.datetime.now()
            self.insert(submission)
        except Exception as err:
            raise Exception(err)
    
    def selectQuestionSequence(self,gamename):
        try:
            return QuestionSequence.query.get(int(gamename))
        except Exception as err:
            raise Exception(err)
    
    

