from modeling.model_trainer import IngredientEmbedder
from data_munging.data_prep import DataHandler
import matplotlib.pyplot as plt
import numpy as np


def main():
    train_model()


def train_model(alpha=0.75, output_dim=50, x_max=100, epochs=100, lr=0.4, batch_size=4096, train_corpus=None):
    data_handler = DataHandler()
    data_handler.create_co_occurrence_matrix(corpus=train_corpus)
    model = IngredientEmbedder(data_handler=data_handler, alpha=alpha, output_dim=output_dim, x_max=x_max)
    model.fit(epochs=epochs, lr=lr, batch_size=batch_size)
    return model


if __name__ == '__main__':
    EPOCHS = 150
    model = train_model(epochs=EPOCHS)
    fig = plt.figure()
    plt.plot(np.arange(EPOCHS), model.losses)
    plt.title('Average Loss over Training')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.savefig('loss.png')