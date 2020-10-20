import torch
import torch.nn as nn


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

    def weighting_function(self, x):
        """
        a weighting function for scaling the loss

        :param x: numeric
        :return: a float
        """
        return torch.min(x / self.x_max, 1) ** self.alpha

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
