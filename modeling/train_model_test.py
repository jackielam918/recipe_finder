from modeling.model_training import IngredientEmbedder
import pandas as pd

corpus = pd.read_pickle('/home/jackielam/Documents/OMSA/fall_2020/dva/DVA_Project/data_munging/data/recipe_data.pkl')

corpus = corpus
model = IngredientEmbedder(alpha=0.75, output_dim=30, x_max=75)
model.fit(corpus=corpus, epochs=100, lr=0.5, batch_size=2048)
