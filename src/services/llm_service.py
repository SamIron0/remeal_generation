import requests
from src.config import config
import json
from src.services.diversity_enforcer import DiversityEnforcer

diversity_enforcer = DiversityEnforcer()

def call_llm(prompt: str) -> str:
    response = requests.post(
        "https://api.deepinfra.com/v1/openai/chat/completions",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {config.DEEP_INFRA_API_KEY}"
        },
        json={
            "model": "meta-llama/Meta-Llama-3.1-70B-Instruct",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            "response_format": { "type": "json_object" }
        }
    )
    response.raise_for_status()
    return response.json()['choices'][0]['message']['content']

async def generate_recipe(parameters: dict) -> dict:
    await diversity_enforcer.analyze_recent_recipes()
    adjusted_params = diversity_enforcer.adjust_generation_params(parameters)

    prompt = f"""Generate a unique American recipe based on the following parameters:
    Complexity: {adjusted_params['complexity']}
    Cuisine Style: American
    Dietary Focus: {adjusted_params['dietary_focus']}
    Cooking Method: {adjusted_params['cooking_method']}
    Season: {adjusted_params['season']}
    Ingredients to include: {', '.join(adjusted_params['ingredients'])}
    Return a JSON object with the following structure:
    {{
        "name": "Recipe Name",
        "description": "Brief description",
        "ingredients": ["ingredient 1", "ingredient 2", ...],
        "instructions": ["step 1", "step 2", ...],
        "cook_time": number (in minutes),
        "prep_time": number (in minutes),
        "servings": number,
        "cuisine": "American",
        "dietary_tags": ["tag1", "tag2", ...]
    }}"""

    response = call_llm(prompt)
    return json.loads(response)
