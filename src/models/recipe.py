from pydantic import BaseModel, validator
from typing import List
from src.utils.validators import validate_recipe

class Recipe(BaseModel):
    name: str
    description: str
    ingredients: List[str]
    instructions: List[str]
    cook_time: int
    prep_time: int
    servings: int

    @validator('*')
    def validate_fields(cls, v):
        validate_recipe(cls)
        return v
