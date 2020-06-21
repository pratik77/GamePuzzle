from dao.DataAccess import DataAccess
# from models.model import Users
from utils.Constants import CREATED_BY
from utils.database import db
import os



class Services():
    dao = DataAccess()

    def submit(self, data):
        try: 
            #
            return data
        except Exception as err:
            raise Exception(err)

    
    
    