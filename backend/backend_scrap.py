from modeling.ingredient_embedder import IngredientEmbedderWrapper

model_path = '/home/jackielam/Documents/OMSA/fall_2020/dva/DVA_Project/backend/modeling/outputs/11411120'
model = IngredientEmbedderWrapper(model_path)

# model.most_similar_recipe([28, 103, 321, 1206, 3956, 4848, 5925], 0.5)
x = {"recipe": [9], "ingredients": [8]}
model.get_substitute_ingredients(**x)
