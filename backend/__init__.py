from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from app.models.database import db
from app.models.cache import cache

jwt = JWTManager()
cors = CORS()

app = Flask(__name__)
app.config.from_object('config.Config')

cors.init_app(app)
db.init_app(app)
jwt.init_app(app)
cache.init_app(app)

with app.app_context():
    from app.routes import discover, auth, profile
    app.register_blueprint(auth.auth, url_prefix='/api/v1/auth')
    app.register_blueprint(discover.discover, url_prefix='/api/v1/discover')
    app.register_blueprint(profile.profile, url_prefix='/api/v1/profile')

    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)