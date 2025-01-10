import json
from app.models.database import db

class RosterMember(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String, nullable=False)
    surname = db.Column(db.String, nullable=False)
    height = db.Column(db.Integer)
    role = db.Column(db.String, nullable=False)
    captain = db.Column(db.Boolean, nullable=False)
    number = db.Column(db.Integer)
    championship_id = db.Column(db.String, nullable=False)
    team_id = db.Column(db.String, nullable=False)

    def __init__(self, name, surname, role, height, championship_id, team_id, captain, number = None):
        self.name = name
        self.surname = surname
        self.height = height
        self.role = role
        self.captain = captain
        self.number = number
        self.championship_id = championship_id
        self.team_id = team_id

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def remove_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            "surname": self.surname,
            "height": self.height,
            "role": self.role,
            "captain": self.captain,
            "number": self.number,
            "championship_id": self.championship_id,
            "team_id": self.team_id
        }
