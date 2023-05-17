import pickle


def main():
    def display_recipe(recipe):
        new_line = "\n \t \t"
        print(
            f"""
                Recipe: {recipe["name"]}
                Cooking Time (min): {recipe["cooking_time"]}
                Ingredients: 
                {new_line.join(f"{ingredient}" for ingredient in recipe["ingredients"])}
                Dificulty: {recipe["difficulty"]}"""
        )

    def search_ingredients(data):
        recipes_list, ingredients_list = data.values()
        for a, ingredient in enumerate(ingredients_list):
            print(f"[{a}] {ingredient}")
        try:
            ingredient_searched = ingredients_list[
                int(input("Pick a number from the ingredient list: "))
            ]
        except ValueError:
            print("Value not a number")
        except IndexError:
            print("Value outside the range of recipes")
        else:
            for recipe in recipes_list:
                if ingredient_searched in recipe["ingredients"]:
                    display_recipe(recipe)

    file_name = input("Please enter a file name: ")
    try:
        with open(file_name, "rb") as recipes_file:
            data = pickle.load(recipes_file)
    except FileNotFoundError:
        print("Flie does not exist")
    else:
        search_ingredients(data)


if __name__ == "__main__":
    main()
