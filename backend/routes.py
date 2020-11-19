from models import Ingredient, Recipe
from app import app
from flask import request, jsonify
import json
from modeling.ingredient_embedder import IngredientEmbedderWrapper
import numpy as np
import sys

model_path = '/home/DVA_Project/backend/modeling/outputs/18411120'
model = IngredientEmbedderWrapper(model_path)


@app.route('/')
def home():
    return app.send_static_file('index.html')


@app.route('/api/get-ingredients', methods=['GET'])
def get_ingredients():
    results = Ingredient.query.all()
    return json.dumps([{'id': result.ingredientid, 'name': result.name} for result in results])


@app.route('/api/search-ingredient', methods=['POST'])
def search_ingredients():
    data = request.get_json()
    substring = data['ingredient']
    results = Ingredient.query.filter(Ingredient.name.like(f'{substring}%')).all()
    return json.dumps([{'id': result.ingredientid, 'name': result.name} for result in results])


@app.route('/api/get-recipes', methods=['POST'])
def get_recipes():
    data = request.get_json()
    print(data, file=sys.stderr)
    scale = data['scale']
    ingredients = data['ingredients']
    limit = data.get('limit')
    return json.dumps(model.most_similar_recipe(recipe=ingredients, scale=scale, limit=limit))


# @app.route('/api/substitute-ingredients', methods=['POST'])
# def get_substitute_ingredients():
#     data = request.get_json()
#     ingredients = data['ingredients']
#     recipe = data['recipe']
#     subs = model.get_substitute_ingredients(ingredients, recipe)
#     return json.dumps({'substitutions': subs})

