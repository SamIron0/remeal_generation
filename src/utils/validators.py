from src.models.recipe import Recipe

def validate_recipe(recipe: Recipe):
    if len(recipe.ingredients) < 2:
        raise ValueError('Recipe must have at least 2 ingredients')
    if len(recipe.instructions) < 3:
        raise ValueError('Recipe must have at least 3 instructions')
