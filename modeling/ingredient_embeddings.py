import torch
import torch.nn as nn
from data_munging.data_prep import DataHandler

# https://stackoverflow.com/questions/48962171/how-to-train-glove-algorithm-on-my-own-corpus\

class IngredientEmbedder(nn.Module):
    def __init__(self, input_dim, output_dim, alpha=0.75, x_max=100):
        """
        :param input_dim: an int, the number of unique inputs
        :param output_dim: an int, the final embedding dimension
        :param alpha: a float: a scaling term
        :param x_max: a int, the maximum value (cutoff) for occurences
        """
        super(IngredientEmbedder, self).__init__()
        self.wi = nn.Embedding(input_dim, output_dim)
        self.wj = nn.Embedding(input_dim, output_dim)
        self.bi = nn.Embedding(input_dim, 1)
        self.bj = nn.Embedding(input_dim, 1)
        self.x_max = x_max
        self.alpha = alpha

        # initialize random values
        self.wi.weight.data.uniform_(-1, 1)
        self.wj.weight.data.uniform_(-1, 1)
        self.bi.weight.data.zero_()
        self.bj.weight.data.zero_()

    def fit(self, corpus, batch_size=128, epochs=1, lr=0.05):
        """
        :param: corpus: a data to train on
        :param batch_size: an int
        :return:
        """
        data_handler = DataHandler()
        data_handler.create_co_occurence_matrix(corpus=corpus)
        batches = data_handler.gen_batches(batch_size=batch_size)


    def forward(self, i, j):
        """
        forward pass for the model

        :param i: index for center token
        :param j: index for outside token
        :return: a float
        """
        w_inside = self.wi[i]
        w_outside = self.wj[j]
        b_inside = self.bi[i].squeeze()
        b_outside = self.bj[i].squeeze()

        return torch.sum(w_inside * w_outside, dim=1) + b_inside + b_outside

#TODO: move everything but forward pass outside ingredient_embedder class

    def weighting_function(self, x):
        """
        a weighting function for scaling the loss

        :param x: numeric
        :return: a float
        """
        return torch.min(x / self.x_max, 1) ** self.alpha

    def compute_loss(self, y_true, y_pred):
        return self.weighted_mse_loss(y_true=1+torch.log(y_true), y_pred=y_pred, weight=self.weighting_function(y_true))

    @staticmethod
    def weighted_mse_loss(y_true, y_pred, weight):
        """
        weighted mean-squared error loss function

        :param y_true: input value
        :param y_pred: target value
        :param weight: a float
        :return:
        """
        return torch.sum(weight * (y_true - y_pred) ** 2)
