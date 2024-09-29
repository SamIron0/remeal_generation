def read_american_recipes():
    with open('american-recipes.md', 'r') as file:
        recipes = [line.strip() for line in file if line.strip()]
    return recipes
