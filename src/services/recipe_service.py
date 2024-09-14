from services.llm_service import generate_recipe
from services.control_service import SmartControlSystem
from models.recipe import Recipe
from services.database_service import is_recipe_unique

async def create_recipe(recipe_name: str) -> Recipe:
    control_system = SmartControlSystem()
    control_system.adjust_parameters()
    parameters = control_system.get_parameters()
    parameters['name'] = recipe_name

    try:
        generated_recipe = await generate_recipe(parameters)
        
        recipe = Recipe(**generated_recipe)
        is_unique = await is_recipe_unique(recipe)
        if is_unique:
            return recipe
        else:
            print(f"Recipe '{recipe.name}' already exists. Skipping.")
            return None
    except Exception as e:
        print(f"Error creating recipe: {e}")
        raise
