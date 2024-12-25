import requests
import asyncio
from config import config
from services.recipe_service import create_recipe
from utils.file_io import read_recipes

async def generate_recipe(recipe_name):
    try:
        recipe = await create_recipe(recipe_name)
        if recipe is None:
            return None

        print(f"Recipe created: {recipe.name}")

        recipe_data = recipe.dict()
        ingestion_result = await ingest_recipe(recipe_data)

        if ingestion_result["success"]:
            print(
                f"Recipe ingested successfully. Recipe ID: {ingestion_result['recipeId']}"
            )
        else:
            print(f"Recipe ingestion failed: {ingestion_result['error']}")

        return recipe
    except Exception as e:
        print(f"Error generating and saving recipe '{recipe_name}': {e}")
        return None


async def ingest_recipe(recipe_data):
    try:
        response = requests.post(config.INGESTION_URL, json=recipe_data)
        response.raise_for_status() 
        return response.json()
    except requests.RequestException as e:
        print(f"Error calling recipe ingestion service: {e}")
        return {"success": False, "error": str(e)}


async def main():
    recipes = read_recipes()
    try:
        for recipe_name in recipes:
            await generate_recipe(recipe_name)

    except KeyboardInterrupt:
        print("\nRecipe generation stopped.")


if __name__ == "__main__":
    asyncio.run(main())
