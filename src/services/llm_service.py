import requests
from config import config
import json
from services.diversity_enforcer import DiversityEnforcer
import re

# diversity_enforcer = DiversityEnforcer()


def call_llm(prompt: str) -> str:
    response = requests.post(
        "https://api.deepinfra.com/v1/openai/chat/completions",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {config.DEEP_INFRA_API_KEY}",
        },
        json={
            "model": "meta-llama/Meta-Llama-3.1-70B-Instruct",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a professional chef specializing in American cuisine. Reply with only JSON and no other character",
                },
                {"role": "user", "content": prompt},
            ],
            "response_format": {"type": "json_object"},
        },
    )
    response.raise_for_status()
    content = response.json()["choices"][0]["message"]["content"]
    return content


async def generate_recipe(parameters: dict) -> dict:
    prompt = f"""Generate a unique recipe based on the following parameters:
    Name: {parameters['name']}
    Do not include optional ingredients! Include measurement wherever possible
    Return only a JSON object with the following structure, :
    {{
        "name": "Recipe Name",
        "description": "Brief description",
        "ingredients": ["ingredient 1", "ingredient 2", ...],
        "instructions": ["step 1", "step 2", ...],
        "cook_time": number (in minutes),
        "prep_time": number (in minutes),
        "servings": number,
    }}."""
    response = call_llm(prompt)
    cleaned_response = response.strip()

    try:
        fixed_response = clean_json_string(cleaned_response)
        return json.loads(fixed_response)
    except json.JSONDecodeError as e:
        print(f"JSON parsing error")
        raise


def clean_json_string(s: str) -> str:
    # Remove any leading/trailing non-JSON characters
    s = re.sub(r"^[^{]*", "", s)
    s = re.sub(r"[^}]*$", "", s)

    # Replace single quotes with double quotes
    s = s.replace("'", '"')

    # Ensure property names are in double quotes
    s = re.sub(r"(\w+)(?=\s*:)", r'"\1"', s)

    # Remove any newlines and extra spaces
    s = re.sub(r"\s+", " ", s)

    # Remove any trailing commas before closing braces or brackets
    s = re.sub(r",\s*([}\]])", r"\1", s)

    return s
