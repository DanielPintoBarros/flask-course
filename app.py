import os
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from db import db
from security import authenticate, identity

from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','sqlite:///data.db').replace('postgres:/', 'postgresql:/')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #Turning off flask modification tracker to not consume resources. SQLAlchemy has its on tracker
app.secret_key = 'jose'
api = Api(app)

#app.config['JWT_AUTH_URL_RULE'] = '/auth'
#app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800) # config JWT to expire within half an hour
#app.config['JWT_AUTH_USERNAME_KEY'] = 'email' # config JWT auth key name to be 'email' instead of default 'username'

jwt = JWT(app, authenticate, identity)

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
@app.route('/')
def home():
    return("API running!")

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)




######################################
# customize JWT auth response, include user_id in response body
#from flask import jsonify
#from flask_jwt import JWT
#from security import authenticate, identity as identity_function
#jwt = JWT(app, authenticate, identity_function)
#@jwt.auth_response_handler
#def customized_response_handler(access_token, identity):
#    return jsonify({
#        'access_token': access_token.decode('utf-8'),
#        'user_id': identity.id
#    })
######################################

######################################
# customize JWT auth response, include user_id in response body
#from flask import jsonify
#from flask_jwt import JWT
#from security import authenticate, identity as identity_function
#jwt = JWT(app, authenticate, identity_function)
#@jwt.error_handler
#def customized_error_handler(error):
#   return jsonify({
#       'message': error.description,
#       'code': error.status_code
#   }), error.status_code
######################################

######################################
#from flask_jwt import jwt_required, current_identity
#class User(Resource):
#   @jwt_required()
#   def get(self): # view all users
#        user = current_identity
#       # then implement admin auth method
######################################