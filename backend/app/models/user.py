import json
from app.models.database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    surname = db.Column(db.String, nullable=False)
    height = db.Column(db.Integer)
    roster = db.Column(db.String, nullable=False)
    show_info = db.Column(db.Boolean, nullable=False)
    favorites = db.Column(db.String, nullable=False)
    token = db.Column(db.String, unique=True)
    role = db.Column(db.String, nullable=False)

    def __init__(self, email, password, name, surname, role):
        self.email = email
        self.password = password
        self.name = name
        self.surname = surname
        self.height = None
        self.show_info = False
        self.roster = json.dumps([])
        self.favorites = json.dumps({"championships": [], "teams": []})
        self.token = ""
        self.role = role

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def remove_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def to_json(self, token=False):
        if token:
            return {
                'id': self.id,
                'name': self.name,
                "surname": self.surname,
                'email': self.email,
                "height": self.height,
                "show_info": self.show_info,
                "roster": json.loads(self.roster),
                "favorites": json.loads(self.favorites),
                'token': self.token,
                'role': self.role
            }
        else:   
            return {
                'id': self.id,
                'name': self.name,
                "surname": self.surname,
                'email': self.email,
                "height": self.height,
                "show_info": self.show_info,
                "roster": json.loads(self.roster),
                "favorites": json.loads(self.favorites),
                'role': self.role
            }
    
    def get_info(self):
        return {
            'name': self.name,
            "surname": self.surname,
            "height": self.height,
            "show_info": self.show_info
        }