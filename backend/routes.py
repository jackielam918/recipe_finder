from models import Cleaningredient
from app import app
from flask import jsonify, request
import json


@app.route('/')
def home():
    return 'pamplemouse'


@app.route('/api/hello', methods=['POST'])
def hello():
    return 'hello'


@app.route('/api/get-ingredients', methods=['GET'])
def get_ingredients():
    results = Cleaningredient.query.all()
    return json.dumps([{'id': result.cleaningredientid, 'name': result.name} for result in results])


@app.route('/api/search-ingredient', methods=['POST'])
def search_ingredients():
    data = request.get_json()
    substring = data['ingredient']
    results = Cleaningredient.query.filter(Cleaningredient.name.like(f'{substring}%')).all()
    return json.dumps([{'id': result.cleaningredientid, 'name': result.name} for result in results])


@app.route('/api/get-recipes', methods=['POST'])
def get_recipes():
    data = request.get_json()
    ingredients = data['ingredients']
    scale = data['scale']
