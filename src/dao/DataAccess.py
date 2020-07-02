from src.models.model import Users
from src.models.model import QuestionSequence
from src.utils.database import db
from src.models.model import Submissions
from sqlalchemy import and_
from src.models.model import Users
from src.models.model import Leaderboard
from src.models.model import SubmissionDetails
from src.models.model import Competitions
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
            submission = self.getSubmissionByUserIdAndQuestionNum(gamename, questionNum)
            submission.isSolved = True
            submission.submissionTime = datetime.datetime.now()
            self.insert(submission)
        except Exception as err:
            raise Exception(err)
    
    def getSubmissionByUserIdAndQuestionNum(self, gamename, questionNum):
        return Submissions.query.filter(and_(Submissions.userId == int(gamename),Submissions.questionNum == int(questionNum))).first()

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
    
    def getStartTime(self):
        try:
            competition = Competitions.query.filter(Competitions.isActive == True).first()
            return competition.startTime
        except Exception as err:
            raise Exception(err)

    def getLatestSubmission(self,gamename,questionNum):
        try:
            submission = Submissions.query.filter(and_(Submissions.userId == int(gamename),Submissions.questionNum == int(questionNum))).first()
            return submission
            # Calculating time for appearingTime to submission time
            #if questionNum != 1:
            #    t1 = submission.appearingTime
            #    return (t2 - t1).total_seconds()
            #return (t2 - t1).total_seconds()            
        except Exception as err:
            raise Exception(err)
    
    def updateMarksToDB(self,gamename,marks):
        try:
            leader = Leaderboard.query.get(int(gamename))
            leader.marks = leader.marks + marks
            self.insert(leader)
        except Exception as err:
            raise Exception(err)
    
    def countSolvedAnswer(self):
        try:
            return db.session.query(Submissions.userId, func.count(Submissions.questionNum)).group_by(Submissions.userId).all()
        except Exception as err:
            raise Exception(err)

    def getAllUsersByMarks(self):
        try:
            return db.session.query(Users, Leaderboard).filter(Leaderboard.userId == Users.id).order_by(Leaderboard.marks2.desc(), Leaderboard.milestoneAchieveTime.asc())
        except Exception as err:
            raise Exception(err)

    def getLatestSubmissionsDetails(self):
        try:
            return db.session.query(Users, SubmissionDetails).filter(Users.id == SubmissionDetails.userId).order_by(SubmissionDetails.submissionTime.desc()).limit(30)
        except Exception as err:
            raise Exception(err)

    def getMarksDetailsOfUser(self, gamename):
        try:
            return db.session.query(Leaderboard).filter(Leaderboard.userId == gamename).first()
        except Exception as err:
            raise Exception(err)
    
    def getExistsRowWithMarks2(self, marks):
        try:
            return db.session.query(Leaderboard.userId).filter(Leaderboard.marks2 >= marks).limit(1).first()
        except Exception as err:
            raise Exception(err)

    def getAllUsersByMarks2(self):
        try:
            return db.session.query(Users, Leaderboard).filter(Leaderboard.userId == Users.id).order_by(Leaderboard.marks2.desc(), Leaderboard.marks.asc(), Leaderboard.milestoneAchieveTime.asc())
        except Exception as err:
            raise Exception(err)
    
    def getAllUsers(self):
        try:
            return db.session.query(Users.id).distinct().all()
        except Exception as err:
            raise Exception(err)
    def findandCloseActiveCompetition(self):
        try:
            competition = Competitions.query.filter(Competitions.isActive == True).first()
            competition.isActive = False
            self.insert(competition)
        except Exception as err:
            raise Exception(err)
    
    def getAllUnsolvedSubmissions(self):
        try:
            return db.session.query(Submissions).filter(Submissions.isSolved == False).all()
        except Exception as err:
            raise Exception(err)

        

