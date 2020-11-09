from models import Cleaningredient
from app import app
from flask import request, jsonify
import json
from modeling.ingredient_embedder import IngredientEmbedderWrapper
import numpy as np


model_path = '/home/DVA_project/backend/modeling/outputs/07011120'
model = IngredientEmbedderWrapper(model_path)


@app.route('/')
def home():
    return '<h1>pamplemouse</h1?'


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
    scale = data['scale']
    ingredients = data['ingredients']
    embedding = np.array2string(model.query_recipe(ingredients))
    return jsonify({'embedding': embedding})


