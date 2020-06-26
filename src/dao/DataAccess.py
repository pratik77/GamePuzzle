from models.model import Users
from models.model import QuestionSequence
from utils.database import db
from models.model import Submissions
from sqlalchemy import and_
from models.model import Users
from models.model import Leaderboard
from models.model import Competitions
from sqlalchemy import func
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

    #delete all rows
    def delete(self,obj):
        try:
            db.session.query(obj).delete()
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

    def updateSolvedQuestionToDB(self,gamename,questionNum):
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

    def getScore(self,gamename):
        try:
            leader = Leaderboard.query.get(int(gamename))
            return leader.marks
        except Exception as err:
            raise Exception(err)
    
    def getTime(self,gamename,questionNum):
        try:
            submission = Submissions.query.filter(and_(Submissions.userId == int(gamename),Submissions.questionNum == int(questionNum))).first()
            t2 = submission.submissionTime
            if questionNum != 1:
                t1 = submission.appearingTime
                return (t2 - t1).total_seconds()
            competition = Competitions.query.filter(Competitions.isActive == True).first()
            t1 = competition.startTime
            return (t2 - t1).total_seconds()            
        except Exception as err:
            raise Exception(err)
    
    def updateMarksToDB(self,gamename,marks):
        try:
            leader = Leaderboard.query.get(int(gamename))
            leader.marks = marks
            self.insert(leader)
        except Exception as err:
            raise Exception(err)
    
    def countSolvedAnswer(self):
        try:
            return db.session.query(Submissions.userId, func.count(Submissions.questionNum)).group_by(Submissions.userId).all()
        except Exception as err:
            raise Exception(err)

        

    
    
    

