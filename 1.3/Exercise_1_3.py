def main():
    recipes_list = []
    ingredients_list = []

    def take_recipe():
        name = input("Name of recipe: ")
        cooking_time = int(input("Cooking time: "))
        ingredients = []
        ingredients_entered = False
        counter = 1
        while not ingredients_entered:
            ingredient = input("Ingredient [" + str(counter) + "]: ")
            ingredients.append(ingredient)
            user_done = input("More ingredients? (y/n): ")
            counter += 1
            if user_done == "n":
                ingredients_entered = True
        return {"name": name, "cooking_time": cooking_time, "ingredients": ingredients}

    n = int(input("How many recipes would you like to enter? "))

    for a in range(0, n):
        recipe = take_recipe()
        for ingredient in recipe["ingredients"]:
            if not ingredient in ingredients_list:
                ingredients_list.append(ingredient)
        recipes_list.append(recipe)

    for recipe in recipes_list:
        if recipe["cooking_time"] < 10 and len(recipe["ingredients"]) < 4:
            recipe["difficulty"] = "Easy"
        elif recipe["cooking_time"] < 10 and len(recipe["ingredients"]) >= 4:
            recipe["difficulty"] = "Medium"
        elif recipe["cooking_time"] >= 10 and len(recipe["ingredients"]) < 4:
            recipe["difficulty"] = "Intermediate"
        elif recipe["cooking_time"] >= 10 and len(recipe["ingredients"]) >= 4:
            recipe["difficulty"] = "Hard"
        new_line = "\n \t \t"
        print(
            f"""
            Recipe: {recipe["name"]}
            Cooking Time (min): {recipe["cooking_time"]}
            Ingredients: 
            {new_line.join(f"{ingredient}" for ingredient in recipe["ingredients"])}
            Dificulty: {recipe["difficulty"]}"""
        )

    new_line = "\n"
    sorted_recipes = sorted(ingredients_list)
    print(
        f"""
    Ingredients Available Across All Recipes
    ----------------------------------------
    {new_line.join(ingredient for ingredient in sorted_recipes)}"""
    )


if __name__ == "__main__":
    main()
