from services.llm_service import generate_recipe
from services.control_service import SmartControlSystem
from models.recipe import Recipe
from services.database_service import generate_recipe_embedding, is_recipe_unique
import numpy as np
from typing import Tuple

async def create_recipe(recipe_name: str) -> Tuple[Recipe, np.ndarray]:
    print(f"Starting to create recipe: {recipe_name}")
    control_system = SmartControlSystem()
    control_system.adjust_parameters()
    parameters = control_system.get_parameters()
    parameters["name"] = recipe_name
    print(f"Adjusted parameters: {parameters}")

    try:
        print("Generating recipe...")
        generated_recipe = await generate_recipe(parameters)
        print(f"Generated recipe: {generated_recipe}")

        recipe = Recipe(**generated_recipe)
        print("Creating embedding...")
        embedding = generate_recipe_embedding(recipe)
        print("Checking if recipe is unique...")
        is_unique = await is_recipe_unique(recipe, embedding)
        if is_unique:
            print(f"Recipe '{recipe.name}' is unique. Returning recipe and embedding.")
            return recipe, embedding
        else:
            print(f"Recipe '{recipe.name}' is too similar to an existing recipe. Skipping.")
            return None, None
    except Exception as e:
        print(f"Error creating recipe: {e}")
        raise
