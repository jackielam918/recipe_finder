import torch
import torch.nn as nn
from data_munging.data_prep import DataHandler

# https://stackoverflow.com/questions/48962171/how-to-train-glove-algorithm-on-my-own-corpus\


class IngredientEmbeddingModel(nn.Module):
    def __init__(self, input_dim, output_dim):
        """
        :param input_dim: an int, the number of unique inputs
        :param output_dim: an int, the final embedding dimension
        :param alpha: a float: a scaling term
        :param x_max: a int, the maximum value (cutoff) for occurences
        """
        super(IngredientEmbeddingModel, self).__init__()
        self.wi = nn.Embedding(input_dim, output_dim)
        self.wj = nn.Embedding(input_dim, output_dim)
        self.bi = nn.Embedding(input_dim, 1)
        self.bj = nn.Embedding(input_dim, 1)

        # initialize random values
        self.wi.weight.data.uniform_(-1, 1)
        self.wj.weight.data.uniform_(-1, 1)
        self.bi.weight.data.zero_()
        self.bj.weight.data.zero_()

    def forward(self, i, j):
        """
        forward pass for the model

        :param i: index for center token
        :param j: index for outside token
        :return: a float
        """
        w_inside = self.wi.weight[i]
        w_outside = self.wj.weight[j]
        b_inside = self.bi.weight[i].squeeze()
        b_outside = self.bj.weight[i].squeeze()

        return torch.sum(w_inside * w_outside, dim=1) + b_inside + b_outside

