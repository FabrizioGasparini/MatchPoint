import sqlite3
from app.models.database import db

class RevokedToken(db.Model):
    jti = db.Column(db.String)
    _ = db.Column(db.Integer, primary_key=True)

    def __init__(self, jti):
        self.jti = jti

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti=jti).first()
        return bool(query)