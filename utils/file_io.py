def read_recipes():
    with open('recipes.md', 'r') as file:
        content = file.readlines()
    
    start_index = next((i for i, line in enumerate(content) if '// start here' in line), None)
    
    if start_index is not None:
        recipes = [line.strip() for line in content[start_index + 1:] if line.strip()]
    else:
        recipes = [line.strip() for line in content if line.strip()]
    
    return recipes
def remove_recipe(recipe):
    with open("recipes.md", "r") as file:
        lines = file.readlines()
    
    with open("recipes.md", "w") as file:
        for line in lines:
            if line.strip() != recipe:
                file.write(line)

def read_checked_pairs():
    try:
        with open("checked_pairs.txt", "r") as file:
            return {(line.split("|")[0], line.split("|")[1]): line.split("|")[2].strip() for line in file}
    except FileNotFoundError:
        return {}

def write_checked_pair(pair, selection):
    with open("checked_pairs.txt", "a") as file:
        file.write(f"{pair[0]}|{pair[1]}|{selection}\n")
