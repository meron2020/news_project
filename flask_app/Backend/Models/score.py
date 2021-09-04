from flask_app.db import db


class Score(db.Model):
    __tablename__ = "scores"

    first_id = db.Column(db.Integer)
    second_id = db.Column(db.Integer)
    first_title = db.Column(db.String)
    second_title = db.Column(db.String)
    title_score = db.Column(db.Integer)
    text_score = db.Column(db.Integer)
    total_score = db.Column(db.Integer)

    def __init__(self, first_id, second_id, first_title, second_title, title_score, text_score, total_score):
        self.first_id = first_id
        self.second_id = second_id
        self.first_title = first_title
        self.second_title = second_title
        self.title_score = title_score
        self.text_score = text_score
        self.total_score = total_score

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def delete_all(cls):
        return cls.query.delete()
