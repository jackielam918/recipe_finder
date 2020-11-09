from modeling.model_trainer import IngredientEmbedder
from data_munging.data_prep import DataHandler

def main():
    train_model()

def train_model(alpha=0.75, output_dim=50, x_max=100, epochs=100, lr=0.5, batch_size=4096, corpus=None):
    data_handler = DataHandler()
    data_handler.create_co_occurrence_matrix(corpus=corpus)
    model = IngredientEmbedder(data_handler=data_handler, alpha=alpha, output_dim=output_dim, x_max=x_max)
    model.fit(epochs=epochs, lr=lr, batch_size=batch_size)


if __name__ == '__main__':
    train_model()