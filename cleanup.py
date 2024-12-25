from fuzzywuzzy import fuzz
import itertools
from utils.file_io import read_checked_pairs, remove_recipe, write_checked_pair

with open("recipes.md", "r") as file:
    content = file.read()

recipes = [line.strip() for line in content.split("\n") if line.strip()]


def find_related_recipes(recipes, lower_threshold=90, upper_threshold=100):
    related_pairs = []
    for a, b in itertools.combinations(recipes, 2):
        similarity = fuzz.ratio(a.lower(), b.lower())
        if lower_threshold <= similarity <= upper_threshold:
            related_pairs.append((a, b, similarity))
    return sorted(related_pairs, key=lambda x: x[2], reverse=True)


def cleanup():
    related_recipes = find_related_recipes(recipes)
    checked_pairs = read_checked_pairs()
    remaining_pairs = len(related_recipes)
    for pair in related_recipes:
        recipe1, recipe2, similarity = pair
        if similarity == 100:
            remove_recipe(recipe2)
            remaining_pairs -= 1
            if (recipe1, recipe2) not in checked_pairs:
                write_checked_pair((recipe1, recipe2), "1")
            print(f"Removed duplicate recipe: {recipe2}")

        else:
            print(
                f"Related recipes (similarity: {similarity}%) - {remaining_pairs} pair(s) left to review:"
            )
            print(f"1. {recipe1}")
            print(f"2. {recipe2}")
            if (recipe1, recipe2) in checked_pairs:
                selection = checked_pairs[(recipe1, recipe2)]
                if selection == "both":
                    recipes.remove(recipe1)
                    recipes.remove(recipe2)
                    remaining_pairs -= 1
                else:
                    selected_recipe = recipe1 if selection == "1" else recipe2
                    print(f"Previously selected recipe: {selected_recipe}")
                    recipes.remove(selected_recipe)
                    remaining_pairs -= 1
            else:
                choice = input("Select recipe(s) (1, 2, or both): ").lower()
                if choice == "1":
                    remove_recipe(recipe2)
                    remaining_pairs -= 1
                    if (recipe1, recipe2) not in checked_pairs:
                        write_checked_pair((recipe1, recipe2), "1")
                    print(f"You selected: {recipe1}")
                elif choice == "2":
                    remove_recipe(recipe1)
                    remaining_pairs -= 1
                    if (recipe1, recipe2) not in checked_pairs:
                        write_checked_pair((recipe1, recipe2), "2")
                    print(f"You selected: {recipe2}")
                else:
                    remaining_pairs -= 1
                    if (recipe1, recipe2) not in checked_pairs:
                        write_checked_pair((recipe1, recipe2), "both")


print("Starting cleanup process...")
cleanup()
print("Cleanup process completed.")
