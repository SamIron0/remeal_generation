def read_recipes():
    with open('recipes.md', 'r') as file:
        content = file.readlines()
    
    start_index = next((i for i, line in enumerate(content) if '// start here' in line), None)
    
    if start_index is not None:
        recipes = [line.strip() for line in content[start_index + 1:] if line.strip()]
    else:
        recipes = [line.strip() for line in content if line.strip()]
    
    return recipes
