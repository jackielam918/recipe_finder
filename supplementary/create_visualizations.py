from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from modeling.ingredient_embedder import IngredientEmbedderWrapper


model_path = '/modeling/outputs/19321120'
model = IngredientEmbedderWrapper(model_path)

names = [n for n, _ in model.most_similar_ingredients('vanilla', 3)]
names.extend([n for n, _ in model.most_similar_ingredients('pork', 5)])
names.extend([n for n, _ in model.most_similar_ingredients('celery', 3)])

tsne = TSNE(n_components=2)
reduced = tsne.fit_transform(model.embeddings)

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
plt.savefig('./new_embeddings.png')