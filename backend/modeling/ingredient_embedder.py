import numpy as np
import pandas as pd
import pickle
import torch
from sklearn.metrics.pairwise import cosine_similarity
from data_munging.data_prep import DataHandler
import os
import sys


class IngredientEmbedderWrapper:
    def __init__(self, directory):
        self.directory = directory
        self.ingredient_mapper = None
        self.embeddings = None
        self.model = None
        self.recipe_embeddings = None

        self.load_ingredient_mapper()
        self.load_embeddings()
        self.get_recipe_embeddings()

    def get_recipe_embeddings(self):
        outfile = os.path.join(self.directory, 'recipe_embeddings.pkl')
        if not os.path.exists(outfile):
            corpus = self.load_recipe_corpus()
            corpus.loc[:, 'recipe_embeddings'] = corpus.loc[:, 'recipe'].apply(lambda x: self.query_recipe(x))
            corpus.to_pickle(outfile)
            self.recipe_embeddings = corpus
        else:
            self.recipe_embeddings = pd.read_pickle(outfile)

    def load_embeddings(self):
        embeddings_path = os.path.join(self.directory, 'embeddings.pkl')
        self.embeddings = pickle.load(open(embeddings_path, 'rb'))

    def load_ingredient_mapper(self):
        path = os.path.join(self.directory, 'ingredient_mapper.pkl')
        self.ingredient_mapper = pickle.load(open(path, 'rb'))

    def load_model(self):
        model_path = os.path.join(self.directory, 'model')
        self.model = torch.load(model_path)

    def most_similar_ingredients(self, ingredient, n=1):
        """
        return the n most similar ingredients

        :param ingredient:
        :param n:
        :return:
        """
        embedding = self.query_ingredient_by_name(ingredient)
        scores = cosine_similarity(embedding.reshape(1, -1), self.embeddings)
        sorted_scores = -np.sort(-scores).flatten()[1: 1+n]
        sorted_idxs = np.argsort(-scores).flatten()[1: 1+n]
        return [(self.ingredient_mapper.idx_to_name[idx], s) for s, idx in zip(sorted_scores, sorted_idxs)]

    def query_ingredient_by_name(self, ingredient):
        """
        returns the embedding for an ingredient
        :param ingredient:
        :return:
        """
        idx = self.ingredient_mapper.name_to_idx[ingredient]
        return self.embeddings[idx]

    def query_ingredient_by_id(self, ingredient_id):
        """
        :param ingredient_id:
        :return:
        """
        if ingredient_id not in self.ingredient_mapper.id_to_idx:
            print(f'Ingredient {ingredient_id} not in ingredient mapper', file=sys.stderr)
            return None
        else:
            idx = self.ingredient_mapper.id_to_idx[ingredient_id]
            return self.embeddings[idx]

    def query_recipe(self, recipe, method='id'):
        """
        :param recipe:
        :param method:
        :return:
        """
        if method == 'id':
            return np.mean([self.query_ingredient_by_id(ingredient) for ingredient in recipe], axis=0)

        elif method == 'name':
            return np.mean([self.query_ingredient_by_name(ingredient) for ingredient in recipe], axis=0)

        else:
            raise ValueError(f'invalid method {method}, must be either "id" or "name"')

    def most_similar_recipe(self, recipe, scale, limit=20):
        tmp_df = self.recipe_embeddings.copy()
        recipe_embedding = self.query_recipe(recipe)
        scores = cosine_similarity(recipe_embedding.reshape(1, -1),
                                   np.vstack(tmp_df.loc[:, 'recipe_embeddings'].to_numpy()))
        tmp_df.loc[:, 'similarity'] = scores.flatten()
        filtered_recipes = tmp_df.loc[tmp_df['similarity'] >= scale]
        filtered_recipes_limit = filtered_recipes.sort_values('similarity', ascending=False).head(min(limit, 50))

        embeddings_limit = np.vstack(filtered_recipes_limit['recipe_embeddings'])
        recipe_ids = filtered_recipes_limit['recipeid'].values

        recipe_sims = cosine_similarity(embeddings_limit, embeddings_limit)
        recipe_sims_mask = recipe_sims > 0.9
        similar_recipe_ids = [recipe_ids[mask].tolist() for mask in recipe_sims_mask]
        filtered_recipes_limit['similar_recipe_ids'] = similar_recipe_ids

        filtered_recipes_limit['recipe_difference'] = filtered_recipes_limit.loc[:, 'recipe'].apply(
            lambda x: list(set(x) ^ set(recipe)))

        filtered_recipes_limit['recipe_difference'] = filtered_recipes_limit['recipe_difference'].apply(
            lambda x: [self.ingredient_mapper.id_to_name[i] for i in x]
        )

        filtered_recipes_limit['ingredient_list'] = filtered_recipes_limit['recipe'].apply(
            lambda x: [self.ingredient_mapper.id_to_name[i] for i in x])

        columns = ['recipeid', 'name', 'minutes', 'ingredient_list', 'recipe', 'similarity', 'similar_recipe_ids',
                   'recipe_difference', 'stepslist']
        ret_dict = filtered_recipes_limit.loc[:, columns].head(limit).to_dict('recipeid')
        return ret_dict

    def get_substitute_ingredients(self, ingredients, recipe):
        missing_input_ingredients, missing_recipe_ingredients = self.get_missing_ingredients(ingredients, recipe)
        ingredient_embeddings = np.vstack([self.query_ingredient_by_id(i) for i in missing_input_ingredients])
        recipe_ingredient_embeddings = np.vstack([self.query_ingredient_by_id(i) for i in missing_recipe_ingredients])
        similarities = cosine_similarity(ingredient_embeddings, recipe_ingredient_embeddings)
        ret = []
        for idx, row in enumerate(similarities):
            if np.max(row) > 0.6:
                ingredient_id = missing_input_ingredients[idx]
                missing_ingredient_id = missing_recipe_ingredients[np.argmax(row)]
                ret.append({"name": self.ingredient_mapper.id_to_name[ingredient_id],
                            "substituted_for": self.ingredient_mapper.id_to_name[missing_ingredient_id]})
        return ret

    @staticmethod
    def get_missing_ingredients(ingredients, recipe):
        missing_input_ingredients = set(ingredients) - set(recipe)
        missing_recipe_ingredients = set(recipe) - set(ingredients)
        return list(missing_input_ingredients), list(missing_recipe_ingredients)

    @staticmethod
    def load_recipe_corpus():
        dh = DataHandler()
        corpus = dh.load_default_corpus(full_data=True)
        return corpus


