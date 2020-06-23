from models.model import Users
from utils.database import db


class DataAccess:
    def insert(self, obj):
        try:
            db.session.add(obj)
            self.commit()
            return obj
        except Exception as err:
            raise Exception(err)

    def commit(self):
        try:
            db.session.commit()
        except Exception as err:
            raise Exception(err)
    
    def selectGameName(self, obj):
        try:
            gameName = Users.query.filter_by(gameName=obj.gameName).first()
            return gameName
        except Exception as err:
            raise Exception(err)
    
    def selectNextQuestion(self,user, question):
        try:
            return 2
        except Exception as err:
            raise Exception(err)
            
