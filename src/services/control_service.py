import random

class SmartControlSystem:
    def __init__(self):
        self.parameters = {
            'complexity': 'medium',
            'cuisine_style': 'American',
            'dietary_focus': 'balanced',
            'cooking_method': 'any',
            'season': 'any'
        }
        self.complexity_options = ['simple', 'medium', 'complex']
        self.cuisine_styles = ['American']
        self.dietary_focuses = ['balanced', 'low-carb', 'vegetarian', 'vegan', 'keto', 'paleo', 'gluten-free']
        self.cooking_methods = ['baking', 'grilling', 'frying', 'boiling', 'steaming', 'slow-cooking', 'any']

    def adjust_parameters(self):
        # Randomly adjust parameters to create variety
        self.parameters['complexity'] = random.choice(self.complexity_options)
        self.parameters['cuisine_style'] = random.choice(self.cuisine_styles)
        self.parameters['dietary_focus'] = random.choice(self.dietary_focuses)
        self.parameters['cooking_method'] = random.choice(self.cooking_methods)

    def get_parameters(self):
        return self.parameters

    def set_parameter(self, key, value):
        if key in self.parameters:
            self.parameters[key] = value
