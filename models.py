from app import db


class Recipe(db.Model):

    __tablename__ = 'recipes'
    recipeid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    
    def __init__(self, name=None):
        self.name = name
