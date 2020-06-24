from utils.database import db
import datetime

class Users(db.Model):
    __tablename__ = 'users'
    #__table_args__ = {"schema": "puzzlegame"}
    #id is gamename here which can be empid or phone number
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(80), nullable=False)
    familyName = db.Column(db.String(80))
    pin = db.Column(db.Integer, nullable=False)

    submissions = db.relationship('Submissions', backref='users', lazy='dynamic')

class Submissions(db.Model):
    __tablename__ = 'submissions'
    #__table_args__ = {"schema": "puzzlegame"}
    userId = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True, nullable=False)
    questionNum = db.Column(db.Integer, nullable=False, primary_key=True)
    isSolved = db.Column(db.Boolean, nullable=False, default=False)
    appearingTime = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    submissionTime = db.Column(db.DateTime, nullable=True)
    submissionCount = db.Column(db.Integer, nullable=False, default=0)

class QuestionSequence(db.Model):
    __tablename__ = 'question_sequence'
    #__table_args__ = {"schema": "puzzlegame"}
    userId = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True, nullable=False)
    sequence = db.Column(db.String(80))

class Leaderboard(db.Model):
    __tablename__ = 'leaderboard'
    #__table_args__ = {"schema": "puzzlegame"}
    userId = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True, nullable=False)
    marks = db.Column(db.Float, nullable=False)

class SubmissionDetails(db.Model):
    __tablename__ = 'submission_details'
    submissionId = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    userId = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    questionNum = db.Column(db.Integer)
    submittedAnswer = db.Column(db.String(80))


db.create_all()
# db.drop_all()

db.session.commit()

