from models.recipe import Recipe
from services.llm_service import generate_recipe
import numpy as np
from typing import Tuple, List
from transformers import AutoTokenizer, AutoModel
import torch

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
model = AutoModel.from_pretrained("bert-base-uncased")


async def create_recipe(recipe_name: str) -> Tuple[Recipe, np.ndarray, List[str]]:
    print(f"Starting to create recipe: {recipe_name}")

    try:
        print("Generating recipe...")
        generated_recipe = await generate_recipe(recipe_name)
        print(f"Generated recipe: {generated_recipe}")

        recipe = Recipe(**generated_recipe)
        return recipe
    except Exception as e:
        print(f"Error creating recipe: {e}")
        raise
