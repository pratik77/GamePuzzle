#from models.model import Users
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
