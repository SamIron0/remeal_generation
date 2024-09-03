from src.services.llm_service import generate_recipe
from src.services.control_service import SmartControlSystem
from src.models.recipe import Recipe


async def create_recipe() -> Recipe:
    control_system = SmartControlSystem()
    control_system.adjust_parameters()
    parameters = control_system.get_parameters()

    try:
        generated_recipe = await generate_recipe(parameters)
        recipe = Recipe(**generated_recipe)
        return recipe
    except Exception as e:
        print(f"Error creating recipe: {e}")
        raise
