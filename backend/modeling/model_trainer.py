import torch
from modeling.ingredient_embeddings import IngredientEmbeddingModel
import torch.optim as optim
import numpy as np
import pickle
import os
import time


class IngredientEmbedder:
    def __init__(self, data_handler, output_dim=50, alpha=0.75, x_max=20):
        self.input_dim = None
        self.output_dim = output_dim
        self.alpha = alpha
        self.x_max = x_max
        self.model = None
        self.embeddings = None
        self.data_handler = data_handler
        self.ingredient_mapper = data_handler.ingredient_mapper
        self.losses = []
        self.directory = None
        self.device = 'cuda:0' if torch.cuda.is_available() else 'cpu'

    def fit(self, batch_size=1024, epochs=5, lr=0.05, save=True):
        self.input_dim = self.data_handler.unique_values
        self.model = IngredientEmbeddingModel(input_dim=self.input_dim, output_dim=self.output_dim).to(self.device)
        self.train_model(batch_size=batch_size, epochs=epochs, lr=lr)
        if save is True:
            self.package_model()

    def train_model(self, batch_size, epochs, lr):
        batch_losses = []
        optimizer = optim.Adagrad(self.model.parameters(), lr=lr)

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
        self.embeddings = torch.mean(torch.stack([self.model.wi.weight, self.model.wj.weight]), dim=0)

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

    def package_model(self):
        """
        saves all files to load model and perform inference
        :return:
        """
        self.directory = os.path.join(os.path.abspath('outputs'), time.strftime("%d%S%m%y"))
        os.makedirs(self.directory)
        self.save_model(self.directory)
        self.save_ingredient_mapper(self.directory)
        self.save_embeddings(self.directory)

    def save_model(self, directory):
        state_dict_path = os.path.join(directory, 'model_state_dict')
        model_path = os.path.join(directory, 'model')
        torch.save(self.model.state_dict(), state_dict_path)
        torch.save(self.model, model_path)

    def save_embeddings(self, directory):
        path = os.path.join(directory, 'embeddings.pkl')
        with open(path, 'wb') as file:
            pickle.dump(self.embeddings.cpu().detach().numpy(), file)

    def save_ingredient_mapper(self, directory):
        path = os.path.join(directory, 'ingredient_mapper.pkl')
        with open(path, 'wb') as file:
            pickle.dump(self.ingredient_mapper, file)

    def save_data_handler(self, directory):
        path = os.path.join(directory, 'data_handler.pkl')
        with open(path, 'wb') as file:
            pickle.dump(self.data_handler, file)


