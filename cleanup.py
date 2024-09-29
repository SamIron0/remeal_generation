import re
from fuzzywuzzy import fuzz
import itertools

with open("american-recipes.md", "r") as file:
    content = file.read()

recipes = [line.strip() for line in content.split('\n') if line.strip()]

def find_related_recipes(recipes, lower_threshold=71, upper_threshold=79):
    related_pairs = []
    for a, b in itertools.combinations(recipes, 2):
        similarity = fuzz.ratio(a.lower(), b.lower())
        if lower_threshold <= similarity <= upper_threshold:
            related_pairs.append((a, b, similarity))
    return sorted(related_pairs, key=lambda x: x[2], reverse=True)

related_recipes = find_related_recipes(recipes)

for pair in related_recipes:
    recipe1, recipe2, similarity = pair
    print(f"Related recipes (similarity: {similarity}%):")
    print(f"1. {recipe1}")
    print(f"2. {recipe2}")
    
    choice = input("Select recipe(s) (1, 2, or both): ").lower()

    if choice == "1":
        print(f"You selected: {recipe1}")
        recipes.remove(recipe2)
    elif choice == "2":
        print(f"You selected: {recipe2}")
        recipes.remove(recipe1)
    elif choice in ["both", "b"]:
        print(f"You selected both: {recipe1} and {recipe2}")
    else:
        print("Invalid choice. Skipping.")

    print()  

    with open("american-recipes.md", "w") as file:
        for recipe in recipes:
            file.write(f"{recipe}\n")

print("Thank you for using the recipe matcher!")
