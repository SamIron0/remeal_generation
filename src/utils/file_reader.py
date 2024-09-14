def read_american_recipes():
    with open('american-recipes.md', 'r') as file:
        recipes = [line.strip().split('. ', 1)[1] for line in file if line.strip()]
    return recipes
