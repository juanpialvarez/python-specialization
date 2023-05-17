import mysql.connector
import cowsay


def calc_difficulty(cooking_time, ingredients):
    if cooking_time < 10 and len(ingredients) < 4:
        return "Easy"
    elif cooking_time < 10 and len(ingredients) >= 4:
        return "Medium"
    elif cooking_time >= 10 and len(ingredients) < 4:
        return "Intermediate"
    elif cooking_time >= 10 and len(ingredients) >= 4:
        return "Hard"


def create_recipe(conn, cursor):
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
    ingredients_string = ", ".join(ingredients)
    query = "INSERT INTO Recipes (name, ingredients, cooking_time, difficulty) VALUES (%s, %s, %s, %s)"
    val = (name, ingredients_string, cooking_time, difficulty)
    cursor.execute(query, val)
    conn.commit()


def search_recipe(conn, cursor):
    cursor.execute(
        """SELECT ingredients
FROM Recipes"""
    )
    results = cursor.fetchall()
    if len(results) == 0:
        print("No recipes")
        return
    all_ingredients = []
    for result in results:
        ingredients = result[0].split(", ")
        for ingredient in ingredients:
            if ingredient not in all_ingredients:
                all_ingredients.append(ingredient)
    print("Available ingredients: \n")
    possible_choices = []
    for a, ingredient in enumerate(all_ingredients):
        print(f"{a} {ingredient}")
        possible_choices.append(f"{a}")
    choice = input("Your choice: ")
    while choice not in possible_choices:
        input("Please enter valud choice: ")
    chosen_ingredient = all_ingredients[int(choice)]
    query = "SELECT * FROM Recipes WHERE ingredients LIKE %s"
    val = (f"%{chosen_ingredient}%",)
    cursor.execute(query, val)
    searched_recipes = cursor.fetchall()
    for row in searched_recipes:
        print(
            f"""
        ID: {row[0]}
        Name: { row[1]}
        Ingredients: { row[2]}
        Cooking Time: { row[3]}
        Difficulty: { row[4]}
        """
        )


def update_recipe(conn, cursor):
    cursor.execute(
        """SELECT id, name
FROM Recipes"""
    )
    results = cursor.fetchall()
    if len(results) == 0:
        print("No recipes")
        return
    possible_choices = []
    for result in results:
        print(f"ID:[{result[0]}] {result[1]}")
        possible_choices.append(str(result[0]))
    choice = input("Please enter a redipe ID: ")
    while choice not in possible_choices:
        input("Please enter valud choice: ")
    possible_updates = ["1", "2", "3"]
    choice_update = input(
        f"""
    Please choose an update:
    [1] Name
    [2] Cooking Time
    [3] Ingredients
    """
    )
    while choice_update not in possible_updates:
        choice_update = input("Please enter valud choice (1, 2, or 3): ")
    match choice_update:
        case "1":
            new_value = input("Enter new name: ")
            cursor.execute(
                "UPDATE Recipes SET name = %s  WHERE id = %s", (new_value, choice)
            )
        case "2":
            new_value = input("Enter new cooking time: ")
            cursor.execute(
                f"UPDATE Recipes SET cooking_time = {new_value} WHERE id = {choice}"
            )
            conn.commit()
            cursor.execute(f"SELECT ingredients FROM Recipes WHERE id = {choice}")
            result = cursor.fetchall()
            difficulty = calc_difficulty(int(new_value), result[0][0].split(", "))
            cursor.execute(
                "UPDATE Recipes SET difficulty = %s WHERE id = %s", (difficulty, choice)
            )
            conn.commit()
        case "3":
            print("Enter new ingredients:")
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
            ingredients_string = ", ".join(ingredients)
            cursor.execute(
                "UPDATE Recipes SET ingredients = %s WHERE id = %s",
                (ingredients_string, choice),
            )
            conn.commit()
            cursor.execute(f"SELECT cooking_time FROM Recipes WHERE id = {choice}")
            result = cursor.fetchall()
            difficulty = calc_difficulty(int(result[0][0]), ingredients)
            cursor.execute(
                "UPDATE Recipes SET difficulty = %s WHERE id = %s", (difficulty, choice)
            )
            conn.commit()


def delete_recipe(conn, cursor):
    cursor.execute(
        """SELECT id, name
FROM Recipes"""
    )
    results = cursor.fetchall()
    if len(results) == 0:
        print("No recipes")
        return
    possible_choices = []
    for result in results:
        print(f"ID:[{result[0]}] {result[1]}")
        possible_choices.append(str(result[0]))
    choice = input("Please enter a redipe ID: ")
    while choice not in possible_choices:
        input("Please enter valud choice: ")
    cursor.execute(f"DELETE FROM Recipes WHERE id = {choice}")
    conn.commit()


def main_menu(conn, cursor):
    choice = ""
    while choice != "quit":
        print(
            """
        Pick a choice:
            [1] Create a new recipe
            [2] Search for a recipe by ingredients
            [3] Update an existing recipe
            [4] Delete a recipe
            Type 'quit' to exit the program
        """
        )
        choice = input("Your choice: ")
        while choice not in ["1", "2", "3", "4", "quit"]:
            choice = input("please enter a valid option: ")
        match choice:
            case "1":
                create_recipe(conn, cursor)
                cowsay.cow("Successfully added!")
            case "2":
                search_recipe(conn, cursor)
                cowsay.cow("Search successful!")
            case "3":
                update_recipe(conn, cursor)
                cowsay.cow("Successfully updated!")
            case "4":
                delete_recipe(conn, cursor)
                cowsay.cow("Successfully deleted!")
            case "quit":
                cowsay.trex("Bye!")
                conn.close()


def main():
    conn = mysql.connector.connect(
        host="localhost", user="cf-python", passwd="password"
    )

    cursor = conn.cursor()

    cursor.execute("CREATE DATABASE IF NOT EXISTS task_database")
    cursor.execute("USE task_database")
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS Recipes(
        id INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(50),
        ingredients VARCHAR(255),
        cooking_time INT,
        difficulty VARCHAR(20),
        CHECK(difficulty = "Easy" OR difficulty = "Medium" OR difficulty = "Intermediate" OR difficulty = "Hard")
    )"""
    )
    cowsay.dragon("Welcome")
    main_menu(conn, cursor)


if __name__ == "__main__":
    main()
