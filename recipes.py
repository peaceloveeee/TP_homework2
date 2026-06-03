class Ingredient:
    def __init__(self, name: str, quantity: float, unit: str):
        self.name = name
        self.quantity = quantity
        self.unit = unit

    @property
    def quantity(self):
        return self._quantity
    
    @quantity.setter
    def quantity(self, val):
        val = float(val)
        if val <= 0:
            raise ValueError("Количество должно быть положительным")
        self._quantity = val
        
    def __str__(self):
        return f"{self.name}: {self.quantity} {self.unit}"
    
    def __repr__(self):
        return f"Ingredient('{self.name}', {self.quantity}, '{self.unit}')"

    def __eq__(self, other):
        if not(isinstance(other, Ingredient)):
            return False
        return self.name == other.name and self.unit == other.unit


class Recipe:
    def __init__(self, title: str, ingredients=None):
        self.title = title
        if ingredients is None:
            self.ingredients = []
        else:
            self.ingredients = ingredients

    def add_ingredient(self, ingredient):
        for el in self.ingredients:
            if el == ingredient:
                el.quantity += ingredient.quantity
                return
        self.ingredients.append(ingredient)
    
    @staticmethod
    def is_valid_ratio(ratio):
        return (isinstance(ratio, (int, float)) and ratio > 0)
    
    def scale(self, ratio: float):
        if not(self.is_valid_ratio(ratio)):
            raise ValueError("Ожидалось положительное число")
        new_ingredients = []
        for el in self.ingredients:
            new_ingredients.append(Ingredient(el.name, el.quantity * ratio, el.unit))
        return Recipe(self.title, new_ingredients)
        
    def __len__(self):
        return len(self.ingredients)
    
    def __str__(self):
        return f"{self.title}: {', '.join(str(el) for el in self.ingredients)}"
    

class ShoppingList:
    def __init__(self):
        self._items = []
    
    def add_recipe(self, recipe, portions):
        if portions <= 0:
            raise ValueError("Количество порций должно быть положительным")
        recipe2 = recipe.scale(portions)
        for el in recipe2.ingredients:
            self._items.append((el, recipe2.title))
    
    def remove_recipe(self, title):
        new_items = []
        for el in self._items:
            if el[1] != title:
                new_items.append(el)
        self._items = new_items
        return
    
    def get_list(self):
        shops = {}
        for ingred, title in self._items:
            key = (ingred.name, ingred.unit)
            if key in shops.keys():
                shops[key] += ingred.quantity
            else:
                shops[key] = ingred.quantity
        rez = []
        for key, quantity in shops.items():
            rez.append(Ingredient(key[0], quantity, key[1]))
        rez.sort(key=lambda x: x.name)
        return rez


    def __add__(self, other):
        list2 = ShoppingList()
        list2._items = self._items + other._items
        return list2


class DietaryRecipe(Recipe):
    def __init__(self, title, diet_type, ingredients=None):
        super().__init__(title, ingredients)
        self.diet_type = diet_type
    
    def scale(self, ratio: float):
        recipe2 = super().scale(ratio)
        return DietaryRecipe(recipe2.title, self.diet_type, recipe2.ingredients)
    
    def __str__(self):
        s1 = super().__str__()
        return f"[{self.diet_type}] {s1}"
    