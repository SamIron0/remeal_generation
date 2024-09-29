import asyncio
from services.llm_service import classify_recipe_dietary_restrictions
from models.recipe import Recipe


async def test_classify_recipe_dietary_restrictions():
    vegetarian_recipe = Recipe(
        name="Vegetarian Pasta Primavera",
        description="A delicious and healthy recipe for vegetarian pasta primavera.",
        ingredients=[
            "8 oz pasta",
            "1 cup mixed vegetables",
            "2 tbsp olive oil",
            "2 cloves garlic",
            "1/4 cup grated Parmesan cheese",
            "Salt and pepper to taste",
        ],
        instructions=[
            "Cook pasta according to package instructions.",
            "Sauté vegetables and garlic in olive oil.",
            "Toss cooked pasta with vegetables and Parmesan cheese.",
            "Season with salt and pepper.",
        ],
        cook_time=20,
        prep_time=10,
        servings=2,
    )

    vegan_gf_recipe = Recipe(
        name="Vegan Berry Smoothie",
        description="A delicious and healthy recipe for vegan and gluten-free smoothie.",
        ingredients=[
            "1 cup almond milk",
            "1 banana",
            "1 cup mixed berries",
            "1 tbsp chia seeds",
            "1 tbsp agave nectar",
        ],
        instructions=[
            "Blend all ingredients until smooth.",
            "Pour into a glass and serve immediately.",
        ],
        cook_time=0,
        prep_time=5,
        servings=1,
    )

    caesar_salad_recipe = Recipe(
        name="Classic Caesar Salad",
        description="A traditional Caesar salad with crisp romaine lettuce and creamy dressing.",
        ingredients=[
            "1 head romaine lettuce",
            "1/2 cup Caesar dressing",
            "1/4 cup grated Parmesan cheese",
            "1 cup croutons",
            "2 anchovy fillets, minced (optional)",
            "1 large egg yolk",
            "2 tablespoons lemon juice",
            "1 clove garlic, minced",
        ],
        instructions=[
            "Wash and chop the romaine lettuce.",
            "In a bowl, whisk together egg yolk, lemon juice, garlic, and minced anchovies.",
            "Slowly whisk in olive oil to create the dressing.",
            "Toss lettuce with dressing, Parmesan cheese, and croutons.",
            "Serve immediately.",
        ],
        cook_time=0,
        prep_time=15,
        servings=4,
    )

    caesar_salad_result = await classify_recipe_dietary_restrictions(caesar_salad_recipe)

    print(f"Classic Caesar Salad classifications: {caesar_salad_result}")


if __name__ == "__main__":
    asyncio.run(test_classify_recipe_dietary_restrictions())
