from supabase import create_client, Client
from config import config
from models.recipe import Recipe
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from transformers import BertTokenizer, BertModel
import torch

supabase: Client = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)

tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertModel.from_pretrained("bert-base-uncased")


def generate_recipe_embedding(recipe: Recipe) -> np.ndarray:
    print(f"Generating embedding for recipe: {recipe.name}")
    # Combine recipe attributes into a single string
    recipe_text = f"{recipe.name} {recipe.description} {' '.join(recipe.ingredients)} {' '.join(recipe.instructions)}"
    print(f"Combined recipe text: {recipe_text[:100]}...")  # Print first 100 characters

    # Tokenize and encode the recipe text
    inputs = tokenizer(
        recipe_text,
        return_tensors="pt",
        max_length=512,
        truncation=True,
        padding="max_length",
    )
    print(f"Tokenized input shape: {inputs['input_ids'].shape}")

    # Generate embeddings
    print("Generating BERT embeddings...")
    with torch.no_grad():
        outputs = model(**inputs)

    # Use the [CLS] token embedding as the recipe embedding
    embedding = outputs.last_hidden_state[:, 0, :].numpy()[0]
    print(f"Generated embedding shape: {embedding.shape}")

    return embedding


async def is_recipe_unique(recipe: Recipe, new_recipe_embedding: np.ndarray) -> bool:
    print(f"Checking uniqueness for recipe: {recipe.name}")
    # Fetch all recipe embeddings from the database
    result = supabase.table("recipe_vectors").select("recipe_id, embedding").execute()
    existing_embeddings = result.data
    print(f"Fetched {len(existing_embeddings)} existing embeddings from database")

    max_similarity = 0
    most_similar_recipe_id = None
    # Compare the new recipe embedding with existing embeddings
    for existing in existing_embeddings:
        similarity = cosine_similarity([new_recipe_embedding], [existing["embedding"]])[0][0]
        if similarity > max_similarity:
            max_similarity = similarity
            most_similar_recipe_id = existing["recipe_id"]
        if similarity > 0.9:  # Adjust this threshold as needed
            print(f"Recipe '{recipe.name}' is too similar to existing recipe (ID: {existing['recipe_id']}). Similarity: {similarity}")
            return False

    print(f"Recipe '{recipe.name}' is unique. Max similarity: {max_similarity}, Most similar recipe ID: {most_similar_recipe_id}")
    return True


async def save_recipe(recipe: Recipe):
    print(f"Saving recipe: {recipe.name}")
    # Save the recipe to the recipes table
    recipe_data = recipe.dict()

    # Generate and save the recipe embedding
    embedding = generate_recipe_embedding(recipe)
    print(f"Generated embedding for recipe: {recipe.name}")
    
    result = supabase.table("recipe_vectors").insert(
        {"name": recipe_data["name"], "embedding": embedding.tolist()}
    ).execute()
    print(f"Saved recipe vector to database. Result: {result}")

    return result.data[0]['id'] if result.data else None
