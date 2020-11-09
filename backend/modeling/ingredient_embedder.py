import numpy as np
import pickle
import torch
from sklearn.metrics.pairwise import cosine_similarity
import os


class IngredientEmbedderWrapper:
    def __init__(self, directory):
        self.directory = directory
        self.ingredient_mapper = None
        self.embeddings = None
        self.model = None

        self.load_ingredient_mapper()
        self.load_embeddings()

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
        embedding = self.query_ingredient(ingredient)
        scores = cosine_similarity(embedding.reshape(1, -1), self.embeddings)
        sorted_scores = -np.sort(-scores).flatten()[1: 1+n]
        sorted_idxs = np.argsort(-scores).flatten()[1: 1+n]
        return [(self.ingredient_mapper.idx_to_name[idx], s) for s, idx in zip(sorted_scores, sorted_idxs)]

    def query_ingredient(self, ingredient):
        """
        returns the embedding for an ingredient
        :param ingredient:
        :return:
        """
        idx = self.ingredient_mapper.name_to_idx[ingredient]
        return self.embeddings[idx]

    def query_recipe(self, recipe):
        """
        :param recipe:
        :return:
        """
        return np.mean([self.query_ingredient(ingredient) for ingredient in recipe], axis=0)


