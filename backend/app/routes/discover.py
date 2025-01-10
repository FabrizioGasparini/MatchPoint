import requests
from datetime import datetime
from flask import Blueprint, jsonify
from app.models.cache import cache
import json

discover = Blueprint('discover', __name__)

@discover.route('/', methods=['GET'])
@cache.cached()
def committees():
    # fipav_committees = requests.get('http://app.fipavonline.it/api/v1/commettees').json()["data"]["commettees"]["others"]
    
    with open('./app/committees.json', 'r') as f:
        committees = json.load(f)["committees"]
        
    '''
    for committee in fipav_committees:
        committees.append({
            'id': committee["id"],
            'name': committee["nome"],
            'title': committee["title"],
            'address': committee["indirizzo"],
            'email': committee["e_mail"],
            'phone': committee["tel_fax"],
            'logo': committee["image"],
            'region': committee["region-title"]
        })
    '''
    
    return jsonify({'status': 'success', 'committees': committees}), 200

@discover.route('/<string:committee_id>/', methods=['GET'])
@cache.memoize()
def championships(committee_id):  
    try:
        fipav_championships = requests.get(f'http://app.fipavonline.it/api/v1/calendar/{committee_id}').json()["data"]
        if fipav_championships == None or fipav_championships == []:
            return jsonify({'status': 'error', 'message': 'Invalid committee_id'}), 404
    except:
        return jsonify({'status': 'error', 'message': 'Invalid committee_id'}), 404
    
    
    championships = []
    for championship in fipav_championships:
        championships.append({
            'id': championship["id"],
            'parent': championship["parent"],
            'name': championship["title"],
            'title': championship["title-short"],
            'subtitle': championship["sub-title"]
        })
    
    return jsonify({'status': 'success', 'championships': championships}), 200


@discover.route('/<string:any>/<string:championship_id>/', methods=['GET'])
@cache.memoize()
def championship_info(any, championship_id):  
    championship_matches = matches("", championship_id)[0].get_json()["matches"]
    championship_teams = teams("", championship_id)[0].get_json()["teams"]
    championship_standings = standings("", championship_id)[0].get_json()["standings"]
    
    fipav_championship = {'matches': championship_matches, 'teams': championship_teams, 'standings': championship_standings}
    try:
        fipav_matches = requests.get(f'http://app.fipavonline.it/api/v1/calendar/0/{championship_id}').json()["data"]
        if fipav_matches == None or fipav_matches == []:
            return jsonify({'status': 'error', 'message': 'Invalid championship_id'}), 404
    except:
        return jsonify({'status': 'error', 'message': 'Invalid championship_id'}), 404

    fipav_championship["id"] = championship_id
    fipav_championship["name"] = fipav_matches["title"]
    fipav_championship["title"] = fipav_matches["title-short"]
    fipav_championship["subtitle"] = fipav_matches["sub-title"]
    fipav_championship["committee_id"] = fipav_matches["commettee-id"]
    fipav_championship["committee_name"] = fipav_matches["commettee"]
    fipav_championship["committee_title"] = fipav_matches["commettee-short"]
    
    return jsonify({'status': 'success', 'championship': fipav_championship}), 200

@discover.route('/<string:any>/<string:championship_id>/matches', methods=['GET'])
@cache.memoize()
def matches(any, championship_id):
    try:
        fipav_matches = requests.get(f'http://app.fipavonline.it/api/v1/calendar/0/{championship_id}').json()["data"]["matches"]
        if fipav_matches == None or fipav_matches == []:
            return jsonify({'status': 'error', 'message': 'Invalid championship_id'}), 404
    except:
        return jsonify({'status': 'error', 'message': 'Invalid championship_id'}), 404
    
    matches = []
    for match in fipav_matches:
        matches.append({
            'id': match["id"],
            'day': match["day"],   
            'date': match["date"],   
            'time': match["time"],   
            'location': match["stadium"],   
            "lat": match["lat-stadium"],
            "lon": match["lng-stadium"],
            'match_number': match["ng"],   
            "played": match["played"],
            "home_setwin": match["team1-setwin"],
            "away_setwin": match["team2-setwin"],
            "home_points": match["pt_a"],
            "away_points": match["pt_b"],
            "home_team": {
                "id": match["team1"]["id"],
                "name": match["team1"]["title"],
                "society": match["team1"]["nome_societa"],
                "society_id": match["team1"]["cod_aff_societa"],
                "logo": match["team1"]["logo"]
            },
            "away_team": {
                "id": match["team2"]["id"],
                "name": match["team2"]["title"],
                "society": match["team2"]["nome_societa"],
                "society_id": match["team2"]["cod_aff_societa"],
                "logo": match["team2"]["logo"]
            }
        })
    
    return jsonify({'status': 'success', 'matches': matches}), 200

def is_valid_championship(championship_id):
    try:
        fipav_matches = requests.get(f'http://app.fipavonline.it/api/v1/calendar/0/{championship_id}').json()["data"]["matches"]
        if fipav_matches == None or fipav_matches == []:
            return False
    except:
        return False
    
    return True
        
@discover.route('/<string:any>/<string:championship_id>/teams/', methods=['GET'])
@cache.memoize()
def teams(any, championship_id):
    try:
        fipav_matches = requests.get(f'http://app.fipavonline.it/api/v1/calendar/0/{championship_id}').json()["data"]["matches"]
        if fipav_matches == None or fipav_matches == []:
            return jsonify({'status': 'error', 'message': 'Invalid championship_id'}), 404
    except:
        return jsonify({'status': 'error', 'message': 'Invalid championship_id'}), 404
    
    teams = []
    found_teams = []
    for match in fipav_matches:
        if match["team1"]["id"] not in found_teams:
            teams.append({
                "id": match["team1"]["id"],
                "name": match["team1"]["title"],
                "society": match["team1"]["nome_societa"],
                "society_id": match["team1"]["cod_aff_societa"],
                "logo": match["team1"]["logo"]
            })
            found_teams.append(match["team1"]["id"])
            
        if match["team2"]["id"] not in found_teams:
            teams.append({
                "id": match["team2"]["id"],
                "name": match["team2"]["title"],
                "society": match["team2"]["nome_societa"],
                "society_id": match["team2"]["cod_aff_societa"],
                "logo": match["team2"]["logo"]
            })
            found_teams.append(match["team2"]["id"])
    
    return jsonify({'status': 'success', 'teams': teams}), 200


def is_valid_team(championship_id, team_id):
    try:
        fipav_matches = requests.get(f'http://app.fipavonline.it/api/v1/calendar/0/{championship_id}').json()["data"]["matches"]
        if fipav_matches == None or fipav_matches == []:
            return False
    except:
        return False
    
    found_teams = []
    for match in fipav_matches:
        if match["team1"]["id"] not in found_teams:
            found_teams.append(match["team1"]["id"])
        if match["team2"]["id"] not in found_teams:
            found_teams.append(match["team2"]["id"])
            
    return team_id in found_teams
    

@discover.route('/<string:any>/<string:championship_id>/<string:team_id>/', methods=['GET'])
@cache.memoize()
def team(any, championship_id, team_id):
    try:
        fipav_matches = requests.get(f'http://app.fipavonline.it/api/v1/calendar/0/{championship_id}').json()["data"]["matches"]
        if fipav_matches == None or fipav_matches == []:
            return jsonify({'status': 'error', 'message': 'Invalid championship_id'}), 404
    except:
        return jsonify({'status': 'error', 'message': 'Invalid championship_id'}), 404
    
    team_standings = None
    for team in standings("any", championship_id)[0].get_json()["standings"]:
        if team["id"] == team_id:
            team_standings = {
                "lost_games": team["lost_games"],
                "lost_points": team["lost_points"],
                "lost_sets": team["lost_sets"],
                "played": team["played"],
                "points": team["points"],
                "points_ratio": team["points_ratio"],
                "position": team["position"],
                "sets_ratio": team["sets_ratio"],
                "won_games": team["won_games"],
                "won_points": team["won_points"],
                "won_sets": team["won_sets"]
            }
    
    team = None
    matches = []
    for match in fipav_matches:
        if match["team1"]["id"] == team_id or match["team2"]["id"] == team_id:
            matches.append({
                'id': match["id"],
                'day': match["day"],   
                'date': match["date"],   
                'time': match["time"],   
                'location': match["stadium"],   
                "lat": match["lat-stadium"],
                "lon": match["lng-stadium"],
                'match_number': match["ng"],   
                "played": match["played"],
                "home_setwin": match["team1-setwin"],
                "away_setwin": match["team2-setwin"],
                "home_points": match["pt_a"],
                "away_points": match["pt_b"],
                "home_team": {
                    "id": match["team1"]["id"],
                    "name": match["team1"]["title"],
                    "society": match["team1"]["nome_societa"],
                    "society_id": match["team1"]["cod_aff_societa"],
                    "logo": match["team1"]["logo"]
                },
                "away_team": {
                    "id": match["team2"]["id"],
                    "name": match["team2"]["title"],
                    "society": match["team2"]["nome_societa"],
                    "society_id": match["team2"]["cod_aff_societa"],
                    "logo": match["team2"]["logo"]
                }
            })
            if match["team1"]["id"] == team_id:
                team = {
                    "id": match["team1"]["id"],
                    "name": match["team1"]["title"],
                    "society": match["team1"]["nome_societa"],
                    "society_id": match["team1"]["cod_aff_societa"],
                    "logo": match["team1"]["logo"]
                }
            else:
                team = {
                    "id": match["team2"]["id"],
                    "name": match["team2"]["title"],
                    "society": match["team2"]["nome_societa"],
                    "society_id": match["team2"]["cod_aff_societa"],
                    "logo": match["team2"]["logo"]
                }
    
    if team == None or team_standings == None:
        return jsonify({'status': 'error', 'message': 'Invalid team_id'}), 404
    
    return jsonify({'status': 'success', 'team': team, 'matches': matches, 'standings': team_standings}), 200

@discover.route('/<string:any>/<string:championship_id>/standings/', methods=['GET'])
@cache.memoize()
def standings(any, championship_id):
    try:
        fipav_standings = requests.get(f'http://app.fipavonline.it/api/v1/tables/{championship_id}').json()[0]["data"]["teams"]
        if fipav_standings == None or fipav_standings == []:
            return jsonify({'status': 'error', 'message': 'Invalid championship_id'}), 404
    except:
        return jsonify({'status': 'error', 'message': 'Invalid championship_id'}), 404
    
    standings = []
    for team in fipav_standings:
        standings.append({
            "id": team["id"],
            "name": team["title"],
            "logo": team["logo"],
            "played": team["g"],
            "points": team["p"],
            "won_games": team["gv"],
            "lost_games": team["gp"],
            "won_sets": team["sv"],
            "lost_sets": team["sp"],
            "sets_ratio": team["qs"],
            "won_points": team["pf"],
            "lost_points": team["ps"],
            "points_ratio": team["qp"],
            "position": team["pos"],
        })
    
    return jsonify({'status': 'success', 'standings': standings}), 200


@discover.route('/<string:any>/<string:championship_id>/standings/<string:team_id>/', methods=['GET'])
@cache.memoize()
def team_standings(any, championship_id, team_id):
    try:
        fipav_standings = requests.get(f'http://app.fipavonline.it/api/v1/tables/{championship_id}').json()[0]["data"]["teams"]
        if fipav_standings == None or fipav_standings == []:
            return jsonify({'status': 'error', 'message': 'Invalid championship_id'}), 404
    except:
        return jsonify({'status': 'error', 'message': 'Invalid championship_id'}), 404
    
    team_standings = None
    for team in fipav_standings:
        if team["id"] == team_id:
            team_standings = {
                "lost_games": team["gp"],
                "lost_points": team["ps"],
                "lost_sets": team["sp"],
                "played": team["g"],
                "points": team["p"],
                "points_ratio": team["qp"],
                "position": team["pos"],
                "sets_ratio": team["qs"],
                "won_games": team["gv"],
                "won_points": team["pf"],
                "won_sets": team["sv"]
            }
    
    if team_standings == None:
        return jsonify({'status': 'error', 'message': 'Invalid team_id'}), 404
    
    return jsonify({'status': 'success', 'standings': team_standings}), 200

@discover.route('/<string:any>/<string:championship_id>/date/<string:start_date>/<string:end_date>', methods=['GET'])
@cache.memoize()
def date_search(any, championship_id, start_date, end_date):
    try:
        fipav_matches = requests.get(f'http://app.fipavonline.it/api/v1/calendar/0/{championship_id}').json()["data"]["matches"]
        if fipav_matches == None or fipav_matches == []:
            return jsonify({'status': 'error', 'message': 'Invalid championship_id'}), 404
    except:
        return jsonify({'status': 'error', 'message': 'Invalid championship_id'}), 404
    

    print(start_date, end_date)
    matches = []
    for match in fipav_matches:
        match_date = datetime.strptime(match["date"], "%d/%m/%Y")
        if datetime.strptime(start_date, "%d%m%Y") <= match_date <= datetime.strptime(end_date, "%d%m%Y"):
            matches.append({
                'id': match["id"],
                'day': match["day"],   
                'date': match["date"],   
                'time': match["time"],   
                'location': match["stadium"],   
                "lat": match["lat-stadium"],
                "lon": match["lng-stadium"],
                'match_number': match["ng"],   
                "played": match["played"],
                "home_setwin": match["team1-setwin"],
                "away_setwin": match["team2-setwin"],
                "home_points": match["pt_a"],
                "away_points": match["pt_b"],
                "home_team": {
                    "id": match["team1"]["id"],
                    "name": match["team1"]["title"],
                    "society": match["team1"]["nome_societa"],
                    "society_id": match["team1"]["cod_aff_societa"],
                    "logo": match["team1"]["logo"]
                },
                "away_team": {
                    "id": match["team2"]["id"],
                    "name": match["team2"]["title"],
                    "society": match["team2"]["nome_societa"],
                    "society_id": match["team2"]["cod_aff_societa"],
                    "logo": match["team2"]["logo"]
                }
            })
    
    return jsonify({'status': 'success', 'matches': matches}), 200