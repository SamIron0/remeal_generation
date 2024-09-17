import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from transformers import BertTokenizer, BertModel
# Import the necessary classes and functions
from models.recipe import Recipe
from services.database_service import generate_recipe_embedding, is_recipe_unique

# Initialize BERT model and tokenizer
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertModel.from_pretrained("bert-base-uncased")

# Mock database for storing recipe embeddings
mock_db = []

def mock_is_recipe_unique(recipe: Recipe, new_recipe_embedding: np.ndarray) -> bool:
    global mock_db
    print(f"Checking uniqueness for recipe: {recipe.name}")
    existing_embeddings = mock_db
    print(f"Fetched {len(existing_embeddings)} existing embeddings from mock database")

    max_similarity = 0
    most_similar_recipe_id = None
    for existing in existing_embeddings:
        similarity = cosine_similarity([new_recipe_embedding], [existing["embedding"]])[0][0]
        if similarity > max_similarity:
            max_similarity = similarity
            most_similar_recipe_id = existing["recipe_id"]
        if similarity > 0.9:
            print(f"Recipe '{recipe.name}' is too similar to existing recipe (ID: {existing['recipe_id']}). Similarity: {similarity}")
            return False

    print(f"Recipe '{recipe.name}' is unique. Max similarity: {max_similarity}, Most similar recipe ID: {most_similar_recipe_id}")
    return True

def mock_save_recipe(recipe: Recipe, embedding: np.ndarray):
    global mock_db
    mock_db.append({"recipe_id": len(mock_db) + 1, "embedding": embedding})
    print(f"Saved recipe '{recipe.name}' to mock database")

def generate_test_recipes():
    print("Generating test recipes")
    return [
        Recipe(
            name="Classic Cheeseburger",
            description="A juicy beef patty with melted cheese on a toasted bun",
            ingredients=["beef patty", "cheese", "bun", "lettuce", "tomato"],
            instructions=["Grill the patty", "Add cheese", "Assemble burger"],
            cook_time=15,
            prep_time=10,
            servings=1
        ),
        Recipe(
            name="Bacon Cheeseburger",
            description="A classic cheeseburger with crispy bacon",
            ingredients=["beef patty", "cheese", "bacon", "bun", "lettuce", "tomato"],
            instructions=["Grill the patty", "Add cheese and bacon", "Assemble burger"],
            cook_time=20,
            prep_time=10,
            servings=1
        ),
        Recipe(
            name="Grilled Chicken Salad",
            description="A healthy salad with grilled chicken breast",
            ingredients=["chicken breast", "lettuce", "tomato", "cucumber", "dressing"],
            instructions=["Grill the chicken", "Chop vegetables", "Mix and serve"],
            cook_time=15,
            prep_time=10,
            servings=2
        )
    ]

def run_tests():
    recipes = generate_test_recipes()

    for recipe in recipes:
        print(f"\nTesting recipe: {recipe.name}")
        embedding = generate_recipe_embedding(recipe)
        is_unique = mock_is_recipe_unique(recipe, embedding)
        
        if is_unique:
            mock_save_recipe(recipe, embedding)

if __name__ == "__main__":
    run_tests()
