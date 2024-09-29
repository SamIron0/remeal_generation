import random
from collections import Counter
from services.database_service import supabase

class DiversityEnforcer:
    def __init__(self):
        self.cuisine_weights = {'american': 1.0}
        self.ingredient_weights = {}
        self.cooking_method_weights = {}

    async def analyze_recent_recipes(self, limit=100):
        recent_recipes = await supabase.table('recipes').select('*').order('created_at', desc=True).limit(limit).execute()
        
        cuisines = Counter()
        ingredients = Counter()
        cooking_methods = Counter()

        for recipe in recent_recipes.data:
            cuisines[recipe['cuisine']] += 1
            ingredients.update(recipe['ingredients'])
            cooking_methods[recipe['cooking_method']] += 1

        total = sum(cuisines.values())
        self.cuisine_weights = {cuisine: 1 - (count / total) for cuisine, count in cuisines.items()}
        self.cuisine_weights['american'] = max(self.cuisine_weights.get('american', 1.0), 0.5)

        self.ingredient_weights = {ingredient: 1 / (count + 1) for ingredient, count in ingredients.items()}
        self.cooking_method_weights = {method: 1 / (count + 1) for method, count in cooking_methods.items()}

    def adjust_generation_params(self, base_params):
        adjusted_params = base_params.copy()
        
        adjusted_params['cuisine'] = 'american'
        adjusted_params['ingredients'] = self.select_diverse_ingredients(base_params.get('ingredients', []))
        adjusted_params['cooking_method'] = self.select_diverse_cooking_method(base_params.get('cooking_method'))

        return adjusted_params

    def select_diverse_ingredients(self, base_ingredients):
        weighted_ingredients = [(ing, self.ingredient_weights.get(ing, 1.0)) for ing in base_ingredients]
        return [ing for ing, _ in sorted(weighted_ingredients, key=lambda x: x[1] * random.random(), reverse=True)[:5]]

    def select_diverse_cooking_method(self, base_method):
        if random.random() < 0.7: 
            return base_method
        return random.choices(list(self.cooking_method_weights.keys()), 
                              weights=list(self.cooking_method_weights.values()))[0]
