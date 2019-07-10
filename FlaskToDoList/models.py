from app import db


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(40), nullable=False)
    todolist = db.relationship('Lists', backref='ofUser', lazy=True)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username


class Lists(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    poster = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, poster):
        self.poster = poster

    def __repr__(self):
        return '<Posted by %r>' % self.poster


class ToDos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    list_id = db.Column(db.Integer, db.ForeignKey('lists.id'), nullable=False)
    list_message = db.Column(db.String(120))

    def __init__(self, list_message):
        self.list_message = list_message

    def __repr__(self):
        return "<To Do %r>" % self.list_message
