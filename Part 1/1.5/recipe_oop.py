def main():
    class Recipe:
        all_ingredients = []

        def __update_all_ingredients(self):
            for ingredient in self._ingredients:
                if ingredient not in self.all_ingredients:
                    self.all_ingredients.append(ingredient)

        def __init__(self, name: str, ingredients: list, cooking_time: int):
            self._name = name
            self._ingredients = ingredients
            self.__update_all_ingredients()
            self._cooking_time = cooking_time

        def __calculate_difficulty(self):
            if self.cooking_time < 10 and len(self.ingredients) < 4:
                self._difficulty = "Easy"
            elif self.cooking_time < 10 and len(self.ingredients) >= 4:
                self._difficulty = "Medium"
            elif self.cooking_time >= 10 and len(self.ingredients) < 4:
                self._difficulty = "Intermediate"
            elif self.cooking_time >= 10 and len(self.ingredients) >= 4:
                self._difficulty = "Hard"

        def search_ingredient(self, ingredient):
            return ingredient in self._ingredients

        @property
        def name(self):
            return self._name

        @name.setter
        def name(self, value):
            if isinstance(value, str):
                self._name = value
            else:
                raise ValueError("Value is not a string.")

        @property
        def ingredients(self):
            return self._ingredients

        @ingredients.setter
        def ingredients(self, value):
            if isinstance(value, list):
                self._ingredients = value
                self.__update_all_ingredients()
            else:
                raise ValueError("Value is not a list.")

        @property
        def cooking_time(self):
            return self._cooking_time

        @cooking_time.setter
        def cooking_time(self, value):
            if isinstance(value, int):
                self._cooking_time = value
            else:
                raise ValueError("Value is not an integer.")

        @property
        def difficulty(self):
            self.__calculate_difficulty()
            return self._difficulty

        @difficulty.setter
        def difficulty(self):
            raise AttributeError("Can't access attribute.")

    def recipe_search(data, ingredient):
        print(f"\n{ingredient}: \n")
        for recipe in data:
            if recipe.search_ingredient(ingredient):
                new_line = "\n \t \t"
                print(
                    f"""
                    Recipe: {recipe.name}
                    Cooking Time (min): {recipe.cooking_time}
                    Ingredients: 
                    {new_line.join(f"{ingredient}" for ingredient in recipe.ingredients)}
                    Dificulty: {recipe.difficulty}"""
                )

    tea = Recipe("Tea", ["Tea Leaves", "Sugar", "Water"], 5)
    coffee = Recipe("Coffee", ["Coffee Powder", "Sugar", "Water"], 5)
    cake = Recipe(
        "Cake",
        ["Sugar", "Butter", "Eggs", "Vanilla Essece", "Flour", "Baking Powder", "Milk"],
        50,
    )
    banana_smoothie = Recipe(
        "Banana Smoothie", ["Bananas", "Milk", "Peanut Butter", "Sugar", "Ice Cube"], 5
    )

    recipes_list = [tea, coffee, cake, banana_smoothie]
    ing_list = ["Water", "Sugar", "Bananas"]
    for ing in ing_list:
        recipe_search(recipes_list, ing)


main()

if __name__ == "__main__":
    main()
