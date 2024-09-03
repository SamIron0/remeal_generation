import asyncio
from src.services.recipe_service import create_recipe


async def generate_and_save_recipe():
    try:
        recipe = await create_recipe()
        print("Recipe generated and saved:", recipe)
        return recipe
    except Exception as e:
        print(f"Error generating and saving recipe: {e}")
        raise


async def main():
    print("Starting recipe generation. Press Ctrl+C to stop.")
    try:
        await generate_and_save_recipe()
    except KeyboardInterrupt:
        print("\nRecipe generation failed.")


if __name__ == "__main__":
    asyncio.run(main())
