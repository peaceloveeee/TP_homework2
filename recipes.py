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

flour = Ingredient("Мука", 500, "г")
print(flour)
print(repr(flour))

same_flour = Ingredient("Мука", 1000, "г")
sugar = Ingredient("Сахар", 500, "г")

print(flour == same_flour)
print(flour == sugar)
    

