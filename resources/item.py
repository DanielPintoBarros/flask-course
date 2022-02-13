from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from models.item import ItemModel
from models.store import StoreModel

class Item(Resource):
    parse = reqparse.RequestParser()
    parse.add_argument('price', type=float, required=True, help="This field cannot be left blank!")
    parse.add_argument('store_name', type=str, required=True, help="Every item needs a store!")
    
    def _check_store_name(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.id

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)

        if item:
            return {'item': item.json()}
        return{'message': 'Item not found!'}, 404

    @jwt_required()
    def post(self, name):
        item = ItemModel.find_by_name(name)

        if item is not None:
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parse.parse_args()
        store_id = self._check_store_name(data['store_name'])
        if store_id is None:
            return {'message': 'Store does not exist!'}, 400

        item = ItemModel(name, data['price'], store_id)
        item.save_to_db()
        
        return {'item': item.json()}, 201

    @jwt_required()
    def delete(self, name):
        claims = get_jwt()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': 'Item deleted'}
        return{'message': 'The item "{}" does not existe'.format(name)}, 404
    
    @jwt_required(fresh=True)
    def put(self, name):
        data = Item.parse.parse_args()
        item = ItemModel.find_by_name(name)
        store_id = self._check_store_name(data['store_name'])
        if store_id is None:
            return{'Store send does not exist!'}, 400

        item = ItemModel(name, data['price'], store_id)

        if item:
            item.price = data['price']
            item.store_id= store_id
        else:
            item = ItemModel(name, data['price'], store_id)
        item.save_to_db()
        return {"item": item.json()}


class ItemList(Resource):
    @jwt_required(optional=True, fresh=False)
    def get(self):
        user_id = get_jwt_identity()
        items = ItemModel.get_all_items()
        if user_id:
            return {'items': [item.json() for item in items]}, 200
        return {'items': [item.name for item in items],
                'message': 'More data available if you log in'
        }, 200

