import pandas as pd
import numpy as np
from itertools import permutations
import scipy.sparse
from sklearn.utils import shuffle
import torch
from tqdm import trange
from dotenv import load_dotenv
import psycopg2
import os
import pathlib


np.random.seed(2020)


class DataHandler:
    def __init__(self):
        """
        - creates co-occurence matrix for data
        -
        """
        self.co_occurrence_matrix = None
        self.ingredient_mapper = None
        self.unique_values = None

    def create_batches(self, batch_size, negative_sample_ratio=0.3):
        """
        generates batches for training model

        :param batch_size:
        :return:
        """
        if self.co_occurrence_matrix is None:
            raise NotImplementedError('Must create co-occurrence matrix first')

        row, col = self.co_occurrence_matrix.nonzero()
        non_zero_size = self.co_occurrence_matrix.nnz

        negative_sample_size = int(np.floor((negative_sample_ratio / (1 - negative_sample_ratio)) * non_zero_size))
        zero_row, zero_col = shuffle(*np.where(self.co_occurrence_matrix.todense() == 0))

        row = np.concatenate((row, zero_row[:negative_sample_size]))
        col = np.concatenate((col, zero_col[:negative_sample_size]))

        total_size = non_zero_size + negative_sample_size
        row_rand, col_rand = shuffle(row, col)

        for idx in trange(0, total_size, batch_size):
            i, j = row_rand[idx: idx+batch_size], col_rand[idx: idx+batch_size],
            yield torch.LongTensor(i), torch.LongTensor(j), torch.FloatTensor(self.co_occurrence_matrix[i, j])

    def create_co_occurrence_matrix(self, corpus=None):
        """
        :param corpus: a 2-d array, each row is a recipe and each entry is an ingredient id
        :return:
        """
        if self.ingredient_mapper is None:
            self.fit_ingredient_mapper()

        if corpus is None:
            corpus = self.load_default_corpus()

        n = self.ingredient_mapper.ingredient_count
        a = np.zeros((n, n))
        print('creating co-occurrence matrix')
        for recipe in corpus:
            ingredient_idxs = self.ingredient_mapper.recipe_to_idxs(recipe)
            permutes = list(permutations(ingredient_idxs, 2))
            for m, n in permutes:
                a[m, n] += 1
        self.co_occurrence_matrix = scipy.sparse.csr_matrix(a)
        self.unique_values = self.co_occurrence_matrix.shape[0]
        print('co-occurrence matrix created')

    def fit_ingredient_mapper(self):
        """
        :return:
        """
        ingredient_mapper = IngredientMapper()
        ingredient_mapper.fit()
        self.ingredient_mapper = ingredient_mapper

    @staticmethod
    def load_default_corpus(full_data=False):
        parent_path = pathlib.Path(__file__).parent.absolute()
        load_dotenv(os.path.join(parent_path, '.env'))
        conn = psycopg2.connect(
            host=os.environ['DBHOST'],
            database=os.environ['DBNAME'],
            user=os.environ['DBUSER'],
            password=os.environ['DBPASS']
        )
        print('loading corpus...')
        if full_data is True:
            with open(os.path.join(parent_path, 'sql/load_full_recipe_data.sql'), 'r') as query:
                corpus = pd.read_sql(query.read(), conn)
        else:
            with open(os.path.join(parent_path, 'sql/load_recipes.sql'), 'r') as query:
                corpus = pd.read_sql(query.read(), conn)
                corpus = corpus['recipe']
        conn.close()
        print('corpus loaded')
        return corpus


class IngredientMapper:
    def __init__(self):
        """
        handles all mapping ingredients
        """
        self.name_to_id = None
        self.name_to_idx = None
        self.idx_to_id = None
        self.idx_to_name = None
        self.id_to_idx = None
        self.id_to_name = None
        self.ingredient_count = None
        self.fitted = False

    def fit(self):
        """
        update when DB created using flat file for now
        :return:
        """
        load_dotenv('../data_munging/.env')
        conn = psycopg2.connect(
                    host=os.environ['DBHOST'],
                    database=os.environ['DBNAME'],
                    user=os.environ['DBUSER'],
                    password=os.environ['DBPASS']
        )
        with open('../data_munging/sql/load_ingredients.sql', 'r') as query:
            df = pd.read_sql(query.read(), conn)
        conn.close()
        df.loc[:, 'idx'] = list(range(len(df)))

        self.ingredient_count = len(df)

        name_dict = df.set_index('name').to_dict()
        self.name_to_id = name_dict['ingredient_id']
        self.name_to_idx = name_dict['idx']

        idx_dict = df.set_index('idx').to_dict()
        self.idx_to_id = idx_dict['ingredient_id']
        self.idx_to_name = idx_dict['name']

        id_dict = df.set_index('ingredient_id').to_dict()
        self.id_to_idx = id_dict['idx']
        self.id_to_name = id_dict['name']

        self.fitted = True

    def recipe_to_idxs(self, recipe):
        if self.fitted is False:
            raise NotImplementedError('Mapper is not fitted')
        return [self.id_to_idx[i] for i in recipe]


