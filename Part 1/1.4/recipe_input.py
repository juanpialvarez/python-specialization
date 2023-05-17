import pickle


def main():
    def calc_difficulty(cooking_time, ingredients):
        if cooking_time < 10 and len(ingredients) < 4:
            difficulty = "Easy"
        elif cooking_time < 10 and len(ingredients) >= 4:
            difficulty = "Medium"
        elif cooking_time >= 10 and len(ingredients) < 4:
            difficulty = "Intermediate"
        elif cooking_time >= 10 and len(ingredients) >= 4:
            difficulty = "Hard"
        return difficulty

    def take_recipe():
        name = input("Name of recipe: ")
        cooking_time = int(input("Cooking time: "))
        ingredients = []
        ingredients_entered = False
        counter = 1
        while not ingredients_entered:
            ingredient = input("Ingredient [" + str(counter) + "]: ")
            ingredients.append(ingredient)
            counter += 1
            user_done = input("More ingredients? (y/n): ")
            while user_done != "y" and user_done != "n":
                user_done = input("Please enter a valid answer (y/n): ")
            if user_done == "n":
                ingredients_entered = True
        difficulty = calc_difficulty(cooking_time, ingredients)
        return {
            "name": name,
            "cooking_time": cooking_time,
            "ingredients": ingredients,
            "difficulty": difficulty,
        }

    def take_recipe_list():
        recipes_list = []
        ingredients_list = []
        n = int(input("How many recipes would you like to enter? "))
        for a in range(0, n):
            print("\n")
            recipe = take_recipe()
            recipes_list.append(recipe)
            for ingredient in recipe["ingredients"]:
                if ingredient not in ingredients_list:
                    ingredients_list.append(ingredient)
        return [recipes_list, ingredients_list]

    try:
        file_name = input("Please enter the file name: ")
        with open(file_name, "rb") as recipes_file:
            data = pickle.load(recipes_file)
    except FileNotFoundError:
        print("\nFile not found")
        recipes_list, ingredients_list = take_recipe_list()
    except:
        print("\nSomething went wrong")
        recipes_list, ingredients_list = take_recipe_list()
    else:
        recipes_list, ingredients_list = data.values()
    finally:
        data = {"recipes_list": recipes_list, "ingredients_list": ingredients_list}
        file_name = input("\nPlease enter a file name: ")

        with open(file_name, "wb") as recipes_data:
            pickle.dump(data, recipes_data)


main()
