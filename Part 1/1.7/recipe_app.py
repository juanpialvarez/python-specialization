import cowsay

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy.types import Integer, String, Enum
from sqlalchemy.orm import sessionmaker
import enum


engine = create_engine("mysql://cf-python:password@localhost/task_database")
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Difficulty(enum.Enum):
    Easy = "Easy"
    Medium = "Medium"
    Intermediate = "Intermediate"
    Hard = "Hard"


class Recipe(Base):
    __tablename__ = "final_recipes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    ingredients = Column(String(255))
    cooking_time = Column(Integer)
    difficulty = Column(Enum(Difficulty))

    def __repr__(self):
        return (
            "<Recipe ID: "
            + str(self.id)
            + "-"
            + self.name
            + "- Difficulty: "
            + self.difficulty.value
            + ">"
        )

    def __str__(self):
        ingredients = self.ingredients.split(", ")
        new_line = "\n \t \t"
        return f"""
            Recipe: {self.name}
            Cooking Time (min): {self.cooking_time}
            Ingredients: 
            {new_line.join(f"- {ingredient}" for ingredient in ingredients)}
            Dificulty: {self.difficulty.value}"""

    def calculate_difficulty(self):
        ingredients = self.ingredients.split(", ")
        if self.cooking_time < 10 and len(ingredients) < 4:
            self.difficulty = "Easy"
        elif self.cooking_time < 10 and len(ingredients) >= 4:
            self.difficulty = "Medium"
        elif self.cooking_time >= 10 and len(ingredients) < 4:
            self.difficulty = "Intermediate"
        elif self.cooking_time >= 10 and len(ingredients) >= 4:
            self.difficulty = "Hard"

    def return_ingredients_as_list(self):
        return self.ingredients.split(", ")


Base.metadata.create_all(engine)


def create_recipe():
    name = input("Name of recipe (max 50 characters): ")
    while len(name) >= 50:
        name = input("Please enter valid name: ")
    cooking_time = input("Cooking time: ")
    while not cooking_time.isnumeric():
        cooking_time = input("Please enter a number: ")
    try:
        cooking_time = int(cooking_time)
    except:
        print("Wrong input")
        return
    ingredients = []
    ingredients_entered = False
    counter = 1
    while True:
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
        if len(ingredients_string) <= 255:
            break
        print("Ingredients must be less than 255 characters")

    recipe = Recipe(
        name=name, ingredients=ingredients_string, cooking_time=cooking_time
    )
    recipe.calculate_difficulty()
    print(recipe.difficulty)
    session.add(recipe)
    session.commit()


def view_recipes():
    all_recipes = session.query(Recipe).all()
    if len(all_recipes) == 0:
        print("No recipes to show")
        return
    for recipe in all_recipes:
        print(recipe)


def search_recipe():
    if session.query(Recipe).count() == 0:
        print("No recipes to show")
        return
    all_ingredients = []
    results = session.query(Recipe).all()
    for result in results:
        ingredients = result.ingredients.split(", ")
        for ingredient in ingredients:
            if ingredient not in all_ingredients:
                all_ingredients.append(ingredient)
    options = []
    for a, ingredient in enumerate(all_ingredients):
        print(f"[{a}] {ingredient}")
        options.append(str(a))
    choice = input("Please choose a numer: ")
    while choice not in options:
        choice = input("Please enter a valid choice: ")
    chosen_ingredient = all_ingredients[int(choice)]
    search_ingredients = (
        session.query(Recipe)
        .filter(Recipe.ingredients.like("%" + chosen_ingredient + "%"))
        .all()
    )
    for recipe in search_ingredients:
        print(recipe)


def update_recipe():
    if session.query(Recipe).count() == 0:
        print("No recipes to show")
        return
    results = session.query(Recipe).with_entities(Recipe.id, Recipe.name).all()
    options = []
    for recipe in results:
        print(f"[{recipe[0]}] {recipe[1]}")
        options.append(str(recipe[0]))
    choice = input("Please choose a numer: ")
    while choice not in options:
        choice = input("Please enter a valid choice: ")
    chosen_recipe = session.query(Recipe).get(int(choice))
    print(chosen_recipe)
    edit_options = ["1", "2", "3"]
    edit_choice = input(
        """
    Which would you like to edit:
    
    [1]: Name
    [2]: Ingredients
    [3]: Cooking Time
    """
    )
    while edit_choice not in edit_options:
        edit_choice = input("Please enter a valid choice: ")

    match edit_choice:
        case "1":
            new_name = input("Please enter new name (max 50 characters): ")
            while len(new_name) >= 50:
                new_name = input("Please enter valid name: ")
            chosen_recipe.name = new_name
            session.commit()
        case "2":
            ingredients = []
            ingredients_entered = False
            counter = 1
            while True:
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
                if len(ingredients_string) <= 255:
                    break
                print("Ingredients must be less than 255 characters")
            chosen_recipe.ingredients = ingredients_string
            chosen_recipe.calculate_difficulty()
            session.commit()
        case "3":
            new_cooking_time = input("Cooking time: ")
            while not new_cooking_time.isnumeric():
                new_cooking_time = input("Please enter a number: ")
            chosen_recipe.cooking_time = int(new_cooking_time)
            chosen_recipe.calculate_difficulty()
            session.commit()


def delete_recipe():
    if session.query(Recipe).count() == 0:
        print("No recipes to show")
        return
    results = session.query(Recipe).with_entities(Recipe.id, Recipe.name).all()
    options = []
    for recipe in results:
        print(f"[{recipe[0]}] {recipe[1]}")
        options.append(str(recipe[0]))
    choice = input("Please choose a numer: ")
    while choice not in options:
        choice = input("Please enter a valid choice: ")
    chosen_recipe = session.query(Recipe).get(int(choice))
    check = input(f"Are you sure you want to delete {chosen_recipe.name}? ")
    while check != "y" and check != "n":
        check = input("Please enter a valid answer (y/n): ")
    if check == "y":
        session.delete(chosen_recipe)
        session.commit()
    else:
        return


def main_menu():
    choice = ""
    while choice != "quit":
        print(
            """
        Pick a choice:
            [1] Create a new recipe
            [2] View all recipes
            [3] Search for a recipe by ingredients
            [4] Update an existing recipe
            [5] Delete a recipe
            Type 'quit' to exit the program
        """
        )
        choice = input("Your choice: ")
        while choice not in ["1", "2", "3", "4", "5", "quit"]:
            choice = input("please enter a valid option: ")
        match choice:
            case "1":
                create_recipe()
                cowsay.cow("Successfully added!")
            case "2":
                view_recipes()
                cowsay.cow("Here are the recipes!")
            case "3":
                search_recipe()
                cowsay.cow("Here's what you searched for!")
            case "4":
                update_recipe()
                cowsay.cow("Successfully updated!")
            case "5":
                delete_recipe()
                cowsay.cow("Successfully deleted!")
            case "quit":
                cowsay.trex("Bye!")
                session.close()
                engine.dispose()


def main():
    cowsay.dragon("Welcome")
    main_menu()


if __name__ == "__main__":
    main()
