import torch
from modeling.ingredient_embeddings import IngredientEmbeddingModel
from data_munging.data_prep import DataHandler
import torch.optim as optim
import numpy as np
from tqdm import tqdm


class IngredientEmbedder:
    def __init__(self, output_dim=50, alpha=0.75, x_max=20):
        self.output_dim = output_dim
        self.alpha = alpha
        self.x_max = x_max
        self.model = None
        self.data_handler = None
        self.losses = []
        self.device = 'cuda:0' if torch.cuda.is_available() else 'cpu'

    def fit(self, corpus, batch_size=1024, epochs=5, lr=0.05):
        self.fit_co_occurrence(corpus)
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
            for row, col, target in tqdm(self.data_handler.create_batches(batch_size=batch_size)):
                row = row.to(self.device)
                col = col.to(self.device)
                target = target.to(self.device)
                optimizer.zero_grad()
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

    def fit_co_occurrence(self, corpus):
        self.data_handler = DataHandler()
        self.data_handler.create_co_occurrence_matrix(corpus=corpus)
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
        return torch.mean(weight * (y_true - y_pred) ** 2)


