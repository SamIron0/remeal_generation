import requests
from config import config
import json
from models.recipe import Recipe
import re
from typing import List


def call_llm_with_json(prompt: str) -> str:
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
                    "content": "You are a professional chef. Reply with only JSON and no other character",
                },
                {"role": "user", "content": prompt},
            ],
            "response_format": {"type": "json_object"},
        },
    )
    response.raise_for_status()
    content = response.json()["choices"][0]["message"]["content"]
    return content


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
                    "content": "You are a helpful assistant.",
                },
                {"role": "user", "content": prompt},
            ],
        },
    )
    response.raise_for_status()
    content = response.json()["choices"][0]["message"]["content"]
    return content


async def generate_recipe(name: dict) -> dict:
    prompt = f"""Generate a unique recipe based on the following parameters:
    Name: {name}
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
    response = call_llm_with_json(prompt)
    cleaned_response = response.strip()
    max_retries = 2
    for attempt in range(max_retries + 1):
        try:
            fixed_response = clean_json_string(cleaned_response)
            return json.loads(fixed_response)
        except json.JSONDecodeError as e:
            if attempt < max_retries:
                print(f"JSON parsing error on attempt {attempt + 1}. Retrying...")
                response = call_llm_with_json(prompt)
                cleaned_response = response.strip()
            else:
                print(f"JSON parsing error after {max_retries + 1} attempts")
                raise


def clean_json_string(s: str) -> str:
    s = re.sub(r"^[^{]*", "", s)
    s = re.sub(r"[^}]*$", "", s)

    s = s.replace("'", '"')

    s = re.sub(r"(\w+)(?=\s*:)", r'"\1"', s)

    s = re.sub(r"\s+", " ", s)

    s = re.sub(r",\s*([}\]])", r"\1", s)

    return s

