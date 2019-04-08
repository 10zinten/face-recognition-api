from api import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(20), unique=True, nullable=False)

    def __repr__(self):
        return f"{self.userid}"

