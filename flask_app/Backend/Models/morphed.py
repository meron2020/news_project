from flask_app.db import db


class Morphed(db.Model):
    __tablename__ = "morph_cache"

    word = db.Column(db.String)
    morphed_word = db.Column(db.String)

    def __init__(self, word, morphed_word):
        self.word = word
        self.morphed_word = morphed_word

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def delete_all(cls):
        return cls.query.delete()


