import asyncio
import requests
from services.recipe_service import create_recipe
from utils.file_reader import read_american_recipes

async def generate_and_save_recipe(recipe_name):
    try:
        recipe = await create_recipe(recipe_name)
        if recipe is None:
            return None
        
        print(f"Recipe created: {recipe.name}")
        
        # Convert the recipe object to a dictionary
        recipe_data = recipe.dict()
        
        # Call the recipe ingestion microservice
        ingestion_result = await ingest_recipe(recipe_data)
        
        if ingestion_result['success']:
            print(f"Recipe ingested successfully. Recipe ID: {ingestion_result['recipeId']}")
        else:
            print(f"Recipe ingestion failed: {ingestion_result['error']}")
        
        return recipe
    except Exception as e:
        print(f"Error generating and saving recipe '{recipe_name}': {e}")
        return None

async def ingest_recipe(recipe_data):
    try:
        # Make an HTTP POST request to the Node.js microservice
        response = requests.post('http://localhost:3000/ingest', json=recipe_data)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()
    except requests.RequestException as e:
        print(f"Error calling recipe ingestion service: {e}")
        return {'success': False, 'error': str(e)}

async def main():
    print("Starting recipe generation. Press Ctrl+C to stop.")
    recipes = read_american_recipes()
    try:
        for recipe_name in recipes:
            await generate_and_save_recipe(recipe_name)
          
    except KeyboardInterrupt:
        print("\nRecipe generation stopped.")

if __name__ == "__main__":
    asyncio.run(main())
