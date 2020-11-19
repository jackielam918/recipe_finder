select recipeid, name, minutes, ingredientidlist recipe, cleaningredientnamelist, stepslist
from recipes
where iscomplete = TRUE
