from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

from app.models.user import User
from app.models.revoked_tokens import RevokedToken
from app.models.roster_member import RosterMember
from app.routes.discover import is_valid_championship, is_valid_team

from werkzeug.security import check_password_hash

import json


profile = Blueprint('profile', __name__)

@profile.get('/')
@jwt_required()
def get_profile():
    if RevokedToken.is_jti_blacklisted(get_jwt()['jti']):
        return jsonify({'status': 'error', 'message': 'Token has been revoked'}), 401
    
    user = User.query.filter_by(email=get_jwt_identity()).first()
    if not user:
        return jsonify({'status': 'error', 'message': 'User not found'}), 404
    
    return jsonify({'status': 'success', 'user': user.to_json(True)}), 200

@profile.get('/info/')
@jwt_required()
def get_info():
    user = User.query.filter_by(email=get_jwt_identity()).first()
    if not user:
        return jsonify({'status': 'error', 'message': 'User not found'}), 404
    
    return jsonify({'status': 'success', 'info': user.get_info()}), 200

@profile.post('/info/')
@jwt_required()
def update_info():
    user = User.query.filter_by(email=get_jwt_identity()).first()
    if not user:
        return jsonify({'status': 'error', 'message': 'User not found'}), 404
    
    data = request.get_json()
    
    updated = False
    if 'name' in data:
        if data['name'] != user.name:
            if type(data['name']) != str:
                return jsonify({'status': 'error', 'message': 'Invalid name'}), 400
            
            if len(data['name']) < 2:
                return jsonify({'status': 'error', 'message': 'Name or surname too short'}), 400
            
            user.name = data['name']
            updated = True
    
    if 'surname' in data:
        if data['surname'] != user.surname:    
            if type(data['surname']) != str:
                return jsonify({'status': 'error', 'message': 'Invalid name'}), 400
            
            if len(data['surname']) < 2:
                return jsonify({'status': 'error', 'message': 'Name or surname too short'}), 400
            
            user.surname = data['surname']
            updated = True
        
    if 'height' in data:
        if type(data['height']) != int:
            return jsonify({'status': 'error', 'message': 'Invalid height'}), 400
        
        if data['height'] != user.height:
            if data['height'] < 0:
                return jsonify({'status': 'error', 'message': 'Invalid height'}), 400
            
            user.height = data['height']
            updated = True
        
                
        
    if 'show_info' in data:
        if data['show_info'] != user.show_info:
            if data['show_info'] not in [True, False]:
                return jsonify({'status': 'error', 'message': 'Invalid show_info'}), 400
            
            user.show_info = data['show_info']
            updated = True

    if not updated:
        return jsonify({'status': 'success', 'message': 'No data to update'}), 200
    
    user.save_to_db()
    return jsonify({'status': 'success', 'message': 'User updated', 'user': user.to_json(True)}), 200

@profile.get('/favorites/')
@jwt_required()
def get_favorites():
    user = User.query.filter_by(email=get_jwt_identity()).first()
    if not user:
        return jsonify({'status': 'error', 'message': 'User not found'}), 404
    
    return jsonify({'status': 'success', 'favorites': json.loads(user.favorites)}), 200

@profile.get('/profile/favorites/championships/')
@jwt_required()
def get_favorites_championships():
    user = User.query.filter_by(email=get_jwt_identity()).first()
    if not user:
        return jsonify({'status': 'error', 'message': 'User not found'}), 404
    
    return jsonify({'status': 'success', 'championships': json.loads(user.favorites)["championships"]}), 200
    

@profile.post('/favorites/championships/')
@jwt_required()
def add_favorite_championships():
    user = User.query.filter_by(email=get_jwt_identity()).first()
    if not user:
        return jsonify({'status': 'error', 'message': 'User not found'}), 404
    
    data = request.get_json()
    if 'championship_id' not in data:
        return jsonify({'status': 'error', 'message': 'Invalid data'}), 400
    
    if type(data['championship_id']) != str:
        return jsonify({'status': 'error', 'message': 'Invalid championship_id'}), 400
        
    favorites = json.loads(user.favorites)
    for favorite in favorites["championships"]:
        if favorite == data['championship_id']:
            return jsonify({'status': 'success', 'message': 'Championship already in favorites'}), 200
    
    if not is_valid_championship(data['championship_id']):
        return jsonify({'status': 'error', 'message': 'Invalid championship_id'}), 404
    
    favorites["championships"].append(data['championship_id'])
    user.favorites = json.dumps(favorites)
    user.save_to_db()
    
    return jsonify({'status': 'success', 'message': 'Championship added to favorites', 'championships': favorites["championships"]}), 200
    
@profile.delete('/favorites/championships/')
@jwt_required()
def remove_favorite_championships():
    user = User.query.filter_by(email=get_jwt_identity()).first()
    if not user:
        return jsonify({'status': 'error', 'message': 'User not found'}), 404
    
    data = request.get_json()
    if 'championship_id' not in data:
        return jsonify({'status': 'error', 'message': 'Invalid data'}), 400
    
    if type(data['championship_id']) != str:
        return jsonify({'status': 'error', 'message': 'Invalid championship_id'}), 400
    
    
    favorites = json.loads(user.favorites)
    for favorite in favorites["championships"]:
        if favorite == data['championship_id']:
            favorites["championships"].remove(favorite)
            user.favorites = json.dumps(favorites)
            user.save_to_db()
            return jsonify({'status': 'success', 'message': 'Championship removed from favorites', 'championships': favorites["championships"]}), 200
        
    return jsonify({'status': 'error', 'message': 'Championship not in favorites'}), 404
    

@profile.get('/favorites/teams/')
@jwt_required()
def get_favorites_teams():
    user = User.query.filter_by(email=get_jwt_identity()).first()
    if not user:
        return jsonify({'status': 'error', 'message': 'User not found'}), 404
    
    return jsonify({'status': 'success', 'teams': json.loads(user.favorites)["teams"]}), 200
    
    
@profile.post('/favorites/teams/')
@jwt_required()
def add_favorite_teams():
    user = User.query.filter_by(email=get_jwt_identity()).first()
    if not user:
        return jsonify({'status': 'error', 'message': 'User not found'}), 404
    
    data = request.get_json()
    if 'championship_id' not in data or 'team_id' not in data:
        return jsonify({'status': 'error', 'message': 'Invalid data'}), 400
    
    if type(data['championship_id']) != str:
        return jsonify({'status': 'error', 'message': 'Invalid championship_id'}), 400
    
    if type(data['team_id']) != str:
        return jsonify({'status': 'error', 'message': 'Invalid team_id'}), 400
           
    if not is_valid_team(data['championship_id'], data['team_id']):
        return jsonify({'status': 'error', 'message': 'Invalid data'}), 404
        
    favorites = json.loads(user.favorites)
    for favorite in favorites["teams"]:
        if favorite["team_id"] == data['team_id']:
            return jsonify({'status': 'success', 'message': 'Team already in favorites'}), 200

    favorites["teams"].append({"team_id": data['team_id'], "championship_id": data['championship_id']})
    user.favorites = json.dumps(favorites)
    user.save_to_db()
    
    return jsonify({'status': 'success', 'message': 'Team added to favorites', 'teams': favorites["teams"]}), 200
    
@profile.delete('/favorites/teams/')
@jwt_required()
def remove_favorite_team():
    user = User.query.filter_by(email=get_jwt_identity()).first()
    if not user:
        return jsonify({'status': 'error', 'message': 'User not found'}), 404
    
    data = request.get_json()
    if 'championship_id' not in data or 'team_id' not in data:
        return jsonify({'status': 'error', 'message': 'Invalid data'}), 400
    
    if type(data['championship_id']) != str:
        return jsonify({'status': 'error', 'message': 'Invalid championship_id'}), 400

    if type(data['team_id']) != str:
        return jsonify({'status': 'error', 'message': 'Invalid team_id'}), 400
    
    
    favorites = json.loads(user.favorites)
    for favorite in favorites["teams"]:
        if favorite['team_id'] == data['team_id']:
            favorites["teams"].remove(favorite)
            user.favorites = json.dumps(favorites)
            user.save_to_db()
            return jsonify({'status': 'success', 'message': 'Team removed from favorites', 'teams': favorites["teams"]}), 200
        
    return jsonify({'status': 'error', 'message': 'Team not in favorites'}), 404


@profile.get('/roster/')
@jwt_required()
def get_roster():
    user = User.query.filter_by(email=get_jwt_identity()).first()
    if not user:
        return jsonify({'status': 'error', 'message': 'User not found'}), 404
    
    return jsonify({'status': 'success', 'roster': json.loads(user.roster)}), 200

@profile.post('/roster/')
@jwt_required()
def add_to_roster():
    user = User.query.filter_by(email=get_jwt_identity()).first()
    if not user:
        return jsonify({'status': 'error', 'message': 'User not found'}), 404
    
    data = request.get_json()
    if 'role' not in data or type(data['role']) != str:
        return jsonify({'status': 'error', 'message': 'Invalid role'}), 400
    
    if data['role'] not in ['B', 'P', 'C', 'O', 'L', 'A', 'VA', 'M', 'D']:
        return jsonify({'status': 'error', 'message': 'Invalid role'}), 400
    
    captain = False
    if 'captain' in data:
        if data['captain'] not in [True, False]:
            return jsonify({'status': 'error', 'message': 'Invalid captain'}), 400
        
        if data['role'] in ['A', 'VA', 'M', 'D'] and data['captain']:
            return jsonify({'status': 'error', 'message': 'This role cannot be a captain'}), 400
        
        captain = data['captain']
    
    if 'championship_id' not in data or 'team_id' not in data:
        return jsonify({'status': 'error', 'message': 'Invalid data'}), 400
    
    if type(data['championship_id']) != str:
        return jsonify({'status': 'error', 'message': 'Invalid championship_id'}), 400

    if type(data['team_id']) != str:
        return jsonify({'status': 'error', 'message': 'Invalid team_id'}), 400

    number = None
    if 'number' in data:
        if type(data['number']) != int:
            return jsonify({'status': 'error', 'message': 'Invalid number'}), 400
        
        if data['role'] in ['A', 'VA', 'M', 'D']:
            return jsonify({'status': 'error', 'message': 'This role does not require a number'}), 400
        number = data['number']
        
    for member in json.loads(user.roster):
        if member['championship_id'] == data['championship_id'] and member['team_id'] == data['team_id']:
            return jsonify({'status': 'error', 'message': 'Member already in this roster'}), 400
    
    member = RosterMember(user.name, user.surname, data['role'], user.height, data['championship_id'], data['team_id'], captain, number)
    member.save_to_db()
    
    roster = json.loads(user.roster)
    roster.append({"id": member.id, "role": data['role'], "captain": captain, "number": number, "championship_id": data['championship_id'], "team_id": data['team_id']})
    
    user.roster = json.dumps(roster)
    user.save_to_db()
    
    return jsonify({'status': 'success', 'message': 'Roster updated', 'roster': roster}), 200

@profile.delete('/roster/')
@jwt_required()
def remove_from_roster():
    user = User.query.filter_by(email=get_jwt_identity()).first()
    if not user:
        return jsonify({'status': 'error', 'message': 'User not found'}), 404
    
    data = request.get_json()
    if 'championship_id' not in data or 'team_id' not in data:
        return jsonify({'status': 'error', 'message': 'Invalid data'}), 400
    
    if type(data['championship_id']) != str:
        return jsonify({'status': 'error', 'message': 'Invalid championship_id'}), 400

    if type(data['team_id']) != str:
        return jsonify({'status': 'error', 'message': 'Invalid team_id'}), 400
    
    roster = json.loads(user.roster)
    for member in roster:
        if member['championship_id'] == data['championship_id'] and member['team_id'] == data['team_id']:
            roster_member = RosterMember.query.filter_by(id=member['id']).first()
            
            if not roster_member:
                return jsonify({'status': 'error', 'message': 'Member not found'}), 404
            
            roster_member.remove_from_db()
            roster.remove(member)
            
            user.roster = json.dumps(roster)
            user.save_to_db()
            
            return jsonify({'status': 'success', 'message': 'Member removed from roster', 'roster': roster}), 200
    
    return jsonify({'status': 'error', 'message': 'Member not in roster'}), 404