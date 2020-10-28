from modeling.model_training import IngredientEmbedder
from data_munging.data_prep import DataHandler
import pandas as pd

corpus = pd.read_pickle('/home/jackielam/Documents/OMSA/fall_2020/dva/DVA_Project/data_munging/data/recipe_data.pkl')

corpus = corpus
data_handler = DataHandler()
data_handler.create_co_occurrence_matrix(corpus)
model = IngredientEmbedder(data_handler=data_handler, alpha=0.75, output_dim=25, x_max=100)
model.fit(corpus=corpus, epochs=1, lr=0.5, batch_size=2048)
model.most_similar_ingredients('sugar', 5)
