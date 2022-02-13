from db import db

class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    
    items = db.relationship('ItemModel', lazy='dynamic') # using lazy dynamic the items list will not be populate as soon as the store was create. So you need to execute items.all() to update them.

    def __init__(self, name):
        self.name = name
    
    def json(self):
        return {'id':self.id,
                'name': self.name,
                'items': [item.json() for item in self.items.all()]
        }
    
    @classmethod
    def get_all_items(cls):
        return cls.query.all()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first() # SELECT * FROM items WHERE name=name
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        if len(self.items.all()) > 0:
            raise Exception("Storage not empty!")
        db.session.delete(self)
        db.session.commit()