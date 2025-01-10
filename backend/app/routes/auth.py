from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, jwt_required

from app.models.user import User
from app.models.revoked_tokens import RevokedToken

from validators import email as validate_email
from werkzeug.security import generate_password_hash, check_password_hash

import json

auth = Blueprint('auth', __name__)

@auth.post('/register/')
def register():
    try:
        data = request.get_json()
        email = data['email']
        password = data['password']
        name = data['name']
        surname = data['surname']
        role = data['role']
    except:
        return jsonify({'status': 'error', 'message': 'Invalid data'}), 400
    
    if len(password) < 6:
        return jsonify({'status': 'error', 'message': 'Password too short'}), 400
    
    if len(name) < 2 or len(surname) < 2:
        return jsonify({'status': 'error', 'message': 'Name or surname too short'}), 400
    
    if role not in ['user', 'admin']:
        return jsonify({'status': 'error', 'message': 'Invalid role'}), 400
    
    if not validate_email(email):
        return jsonify({'status': 'error', 'message': 'Invalid email'}), 400
    
    if User.query.filter_by(email=email).first():
        return jsonify({'status': 'error', 'message': 'Email already registered'}), 400
    
    pass_hash = generate_password_hash(password)
    user = User(email, pass_hash, name, surname, role)
    user.token = create_access_token(identity=user.email)
    user.save_to_db()
    
    return jsonify({'status': 'success', 'message': 'User created', 'user': user.to_json(token=True)}), 201

@auth.post('/login/')
def login():
    try:
        data = request.get_json()
        email = data['email']
        password = data['password']
    except:
        return jsonify({'status': 'error', 'message': 'Invalid data'}), 400
    
    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({'status': 'error', 'message': 'Invalid email or password'}), 400
    
    user.token = create_access_token(identity=user.email)
    user.save_to_db()
    
    return jsonify({'status': 'success', 'message': 'User logged in', 'user': user.to_json(token=True)}), 200

@auth.post('/logout/')
@jwt_required()
def logout():
    user = User.query.filter_by(email=get_jwt_identity()).first()
    if not user:
        return jsonify({'status': 'error', 'message': 'User not found'}), 404
    
    RevokedToken(get_jwt()['jti']).save_to_db()
    
    user.token = ""
    user.save_to_db()
    
    return jsonify({'status': 'success', 'message': 'User logged out'}), 200


@auth.delete('/delete/')
@jwt_required()
def delete():
    try:
        password = request.get_json()['password']
    except:
        return jsonify({'status': 'error', 'message': 'Invalid data'}), 400
    
    user = User.query.filter_by(email=get_jwt_identity()).first()
    if not user:
        return jsonify({'status': 'error', 'message': 'User not found'}), 404
        
    if not check_password_hash(user.password, password):
        return jsonify({'status': 'error', 'message': 'Invalid password'}), 400
    
    RevokedToken(get_jwt()['jti']).save_to_db()
    user.remove_from_db()
    return jsonify({'status': 'success', 'message': 'User deleted'}), 200