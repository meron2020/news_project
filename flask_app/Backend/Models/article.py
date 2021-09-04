from flask_app.db import db


class Article(db.Model):
    __tablename__ = "articles"

    id = db.Column(db.Integer, primary_key=True)
    newspaper = db.Column(db.String)
    url = db.Column(db.String)
    full_text = db.Colum(db.String)
    topic = db.Colum(db.String)
    title = db.Colum(db.String)
    morphed_title = db.Colum(db.String)
    cluster_id = db.Colum(db.String)

    def __init__(self, newspaper, url, full_text, topic, title, morphed_title, cluster_id):
        self.newspaper = newspaper
        self.url = url
        self.full_text = full_text
        self.topic = topic
        self.title = title
        self.morphed_title = morphed_title
        self.cluster_id = cluster_id

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_url_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first().url

    @classmethod
    def count(cls):
        return cls.query.count()

    @classmethod
    def delete_all(cls):
        return cls.query.delete()

    @classmethod
    def update_cluster_id(cls, _id, cluster_id):
        article = cls.query.filter_by(id=_id).first()
        article.cluster_id = cluster_id
        db.session.commit()
