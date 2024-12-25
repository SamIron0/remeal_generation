from models.recipe import Recipe
from services.llm_service import generate_recipe
import numpy as np
from typing import Tuple, List

async def create_recipe(recipe_name: str) -> Tuple[Recipe, np.ndarray, List[str]]:
    try:
        generated_recipe = await generate_recipe(recipe_name)
        recipe = Recipe(**generated_recipe)
        return recipe
    except Exception as e:
        print(f"Error creating recipe: {e}")
        raise
