import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):
    parse = reqparse.RequestParser()
    parse.add_argument('username', type=str, required=True, help="This field cannot be left blank!")
    parse.add_argument('password', type=str, required=True, help="This field cannot be left blank!")

    def post(self):
        data = UserRegister.parse.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "The username '{}' is already being used".format(data['username'])}, 400
        
        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created succesfully!"}, 201
