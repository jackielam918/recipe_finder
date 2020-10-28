import torch
from modeling.ingredient_embeddings import IngredientEmbeddingModel
from data_munging.data_prep import DataHandler
import torch.optim as optim
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


class IngredientEmbedder:
    def __init__(self, data_handler, output_dim=50, alpha=0.75, x_max=20):
        self.output_dim = output_dim
        self.alpha = alpha
        self.x_max = x_max
        self.model = None
        self.embeddings = None
        self.data_handler = data_handler
        self.ingredient_mapper = data_handler.ingredient_mapper
        self.losses = []
        self.device = 'cuda:0' if torch.cuda.is_available() else 'cpu'

    def fit(self, corpus, batch_size=1024, epochs=5, lr=0.05):
        # self.fit_co_occurrence(corpus)
        input_dim = self.data_handler.unique_values
        self.model = IngredientEmbeddingModel(input_dim=input_dim, output_dim=self.output_dim).to(self.device)
        self.train_model(batch_size=batch_size, epochs=epochs, lr=lr)

    def train_model(self, batch_size, epochs, lr,
                    save_model_path='./ingredient_embedder',
                    save_intermediate=None):
        batch_losses = []
        optimizer = optim.Adagrad(self.model.parameters(), lr=lr)
        save_epoch = True if save_intermediate is not None else False

        for epoch in range(1, epochs+1):
            for row, col, target in self.data_handler.create_batches(batch_size=batch_size):
                row = row.to(self.device)
                col = col.to(self.device)
                target = target.to(self.device)
                self.model.zero_grad()
                x = self.model(row, col)
                loss = self.compute_loss(y_true=target, y_pred=x)
                loss.backward()
                optimizer.step()
                batch_losses.append(loss.item())
            avg_loss = np.mean(batch_losses)
            self.losses.append(avg_loss)
            print(f'Loss for Epoch {epoch}: {avg_loss}')
            if (save_epoch is True) and (epoch % 10 == 0):
                torch.save(self.model.state_dict(), save_intermediate)
        torch.save(self.model.state_dict(), save_model_path)
        torch.save(self.model, f'{save_model_path}_full')
        self.embeddings = torch.mean(torch.stack([self.model.wi.weight, self.model.wj.weight]), dim=0)

    def fit_co_occurrence(self, corpus):
        self.data_handler = DataHandler()
        self.data_handler.create_co_occurrence_matrix(corpus=corpus)
        self.ingredient_mapper = self.data_handler.ingredient_mapper
        print('co-occurrence matrix created')

    def weighting_function(self, x):
        """
        a weighting function for scaling the loss

        :param x: a tensor
        :return: a tensor
        """
        weighted_x = (x / self.x_max) ** self.alpha
        return torch.min(weighted_x, torch.ones_like(weighted_x))

    def compute_loss(self, y_true, y_pred):
        return self.weighted_mse_loss(y_true=torch.log(y_true),
                                      y_pred=y_pred,
                                      weight=self.weighting_function(x=y_true)).to(self.device)

    @staticmethod
    def weighted_mse_loss(y_true, y_pred, weight):
        """
        weighted mean-squared error loss function

        :param y_true: input value
        :param y_pred: target value
        :param weight: a float
        :return:
        """
        return torch.sum(weight * (y_pred - y_true) ** 2)

    def load_model(self, model, data_handler):
        self.data_handler = data_handler
        self.ingredient_mapper = data_handler.ingredient_mapper
        self.model = model
        self.embeddings = torch.mean(torch.stack([self.model.wi.weight, self.model.wj.weight]), dim=0)


    def most_similar_ingredients(self, ingredient, n=1):
        """
        return the n most similar ingredients

        :param ingredient:
        :param n:
        :return:
        """
        self.is_fitted()
        embedding = self.query_ingredient(ingredient)
        scores = cosine_similarity(embedding.reshape(1, -1), self.embeddings.cpu().detach().numpy())
        sorted_scores = -np.sort(-scores).flatten()[1: 1+n]
        sorted_idxs = np.argsort(-scores).flatten()[1: 1+n]
        return [(self.ingredient_mapper.idx_to_name[idx], s) for s, idx in zip(sorted_scores, sorted_idxs)]

    def query_ingredient(self, ingredient):
        """
        returns the embedding for an ingredient
        :param ingredient:
        :return:
        """
        self.is_fitted()
        idx = self.ingredient_mapper.name_to_idx[ingredient]
        return self.embeddings[idx].cpu().detach().numpy()

    def query_recipe(self, recipe):
        """
        :param recipe:
        :return:
        """
        self.is_fitted()
        return np.mean([self.query_ingredient(ingredient) for ingredient in recipe], axis=1)

    def is_fitted(self):
        if self.model is None or self.data_handler is None:
            raise NotImplementedError('Must train or load a model first')

