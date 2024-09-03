import asyncio
from supabase import create_client, Client
from src.config import config
from src.models.recipe import Recipe

supabase: Client = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)

async def is_recipe_unique(recipe: Recipe) -> bool:
    # Check if a similar recipe already exists in the database
    similar_recipes = await supabase.table('recipes').select('*').filter('name', 'ilike', f'%{recipe.name}%').execute()
    if similar_recipes.data:
        return False
    return True
