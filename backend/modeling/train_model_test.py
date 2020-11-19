# OLD CODE
from modeling.model_trainer import IngredientEmbedder
from data_munging.data_prep import DataHandler
import pandas as pd
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

corpus = pd.read_pickle('/data_munging/data/recipe_data.pkl')

corpus = corpus
data_handler = DataHandler()
data_handler.create_co_occurrence_matrix(corpus)
model = IngredientEmbedder(data_handler=data_handler, alpha=0.75, output_dim=50, x_max=100)
model.fit(corpus=corpus, epochs=100, lr=0.5, batch_size=4096)
names = [n for n, i in model.most_similar_ingredients('sugar', 20)]

tsne = TSNE(n_components=2)
reduced = tsne.fit_transform(model.embeddings.cpu().detach().numpy())

idxs = [model.ingredient_mapper.name_to_idx[i] for i in names]
reduced_sample = reduced[idxs, :]
y = reduced_sample[:, 1]
z = reduced_sample[:, 0]
n = [model.ingredient_mapper.idx_to_name[i] for i in idxs]

fig, ax = plt.subplots()
ax.scatter(z, y)

for i, txt in enumerate(n):
    ax.annotate(txt, (z[i], y[i]), fontsize=8)

plt.title("t-SNE reduced Embeddings (Random Sample)")
plt.savefig('./embeddings.png')