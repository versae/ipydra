from ipydra import db

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    nbserver_port = db.Column(db.Integer, unique=True)
    nbserver_pid = db.Column(db.Integer, unique=True)
