import os
from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from blocklist import BLOCKLIST
from db import db

from resources.user import UserLogin, UserRegister, User, TokenRefresh, UserLogout
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','sqlite:///data.db').replace('postgres:/', 'postgresql:/')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #Turning off flask modification tracker to not consume resources. SQLAlchemy has its on tracker
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLOCKLIST_ENABLED'] = True
app.config['JWT_BLOCKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.secret_key = 'jose'

api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWTManager(app) # Do not create /auth

@jwt.additional_claims_loader
def add_claims_to_jwt(identity): # Add others parameters to token
    if identity == 1: #Should retrive from db
        return {'is_admin': True}
    return {'is_admin': False}

@jwt.expired_token_loader
def expired_token_callback(decripted_header, decrypted_body):
    return jsonify({
        'description': 'The token has expired.',
        'error': 'token_expired'
    }), 401

@jwt.invalid_token_loader # when the token is not a actual jwt
def invalid_token_callback(error):
    return jsonify({
        'description': 'Signature verification failed',
        'error': 'invalid_token'
    }), 401

@jwt.unauthorized_loader # when they dont send a jwt
def missing_token_callback(error):
    return jsonify({
        'description': 'Request does not contain an access token',
        'error': 'authorization_required'
    }), 401

@jwt.needs_fresh_token_loader # call when they dont send a fresh token
def token_not_fresh_callback(decripted_header, decrypted_body):
    return jsonify({
        'description': 'The token is not fresh',
        'error': 'fresh_token_required'
    }), 401

@jwt.revoked_token_loader #when someone logout end the token cant be valid anymore
def revoke_token_callback(decripted_header, decrypted_body):
    return jsonify({
        'description': 'The token has been revoked',
        'error': 'token_revoked'
    }), 401

@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(decripted_header, decrypted_body):
    return decrypted_body['sub'] in BLOCKLIST

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(UserLogout, '/logout')
@app.route('/')
def home():
    return("API running!")

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)