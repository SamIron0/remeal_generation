from pydantic import BaseModel, validator
from typing import List

class Recipe(BaseModel):
    name: str
    description: str
    ingredients: List[str]
    instructions: List[str]
    cook_time: int
    prep_time: int
    servings: int