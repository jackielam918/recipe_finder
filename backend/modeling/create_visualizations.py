from sklearn.manifold import TSNE
import matplotlib.pyplot as plt


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