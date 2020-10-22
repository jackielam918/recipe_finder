from modeling.model_training import IngredientEmbedder
import pandas as pd

corpus = pd.read_pickle('/home/jackielam/Documents/OMSA/fall_2020/dva/DVA_Project/data_munging/data/recipe_data.pkl')

corpus = corpus
model = IngredientEmbedder(alpha=1, output_dim=30)
model.fit(corpus=corpus, epochs=100, lr=0.1, batch_size=2048)
