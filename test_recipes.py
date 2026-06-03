from recipes import Ingredient, Recipe, ShoppingList, DietaryRecipe
import pytest

def test_create_ingredient():
    ingred = Ingredient('Соль', 1, 'кг')
    assert ingred.name == 'Соль'
    assert ingred.quantity == 1.0
    assert ingred.unit == 'кг'

def test_line_ingredient():
    ingred = Ingredient('Разрыхлитель', 2, 'г')
    assert str(ingred) == 'Разрыхлитель: 2.0 г'

def test_same_ingredient():
    ingred1 = Ingredient('Разрыхлитель', 3, 'кг')
    ingred2 = Ingredient('Соль', 3, 'кг')
    ingred3 = Ingredient('Соль', 1, 'кг')
    ingred4 = Ingredient('Разрыхлитель', 3, 'г')
    assert ingred2 == ingred3
    assert ingred1 != ingred2
    assert ingred1 != ingred4


def test_create_recipe():
    ingred1 = Ingredient('Разрыхлитель', 3, 'кг')
    ingred2 = Ingredient('Соль', 3, 'кг')
    recipe = Recipe('Вкуснятина', [ingred1, ingred2])
    assert recipe.title == 'Вкуснятина'
    assert recipe.ingredients == [ingred1, ingred2]

def test_add_recipe():
    ingred1 = Ingredient('Разрыхлитель', 3, 'кг')
    recipe = Recipe('венегрет')
    recipe.add_ingredient(ingred1)
    assert len(recipe.ingredients) == 1
    assert recipe.ingredients[0] == ingred1

def test_same_recipe():
    ingred2 = Ingredient('Соль', 3, 'кг')
    ingred3 = Ingredient('Соль', 1, 'кг')
    recipe = Recipe('печенько')
    recipe.add_ingredient(ingred2)
    recipe.add_ingredient(ingred3)
    assert len(recipe.ingredients) == 1
    assert recipe.ingredients[0].quantity == 4.0
    assert recipe.ingredients[0].name == 'Соль'

def test_scale_new_recipe():
    ingred3 = Ingredient('Соль', 1, 'кг')
    recipe = Recipe('кокакола', [ingred3])
    recipe2 = recipe.scale(3)
    assert isinstance(recipe2, Recipe)
    assert recipe2 is not recipe

def test_scale_plus_recipe():
    ingred1 = Ingredient('Разрыхлитель', 3, 'кг')
    ingred3 = Ingredient('Соль', 1, 'кг')
    recipe = Recipe('кокакола', [ingred1, ingred3])
    recipe2 = recipe.scale(3)
    assert recipe2.ingredients[0].quantity == 9.0
    assert recipe2.ingredients[1].quantity == 3.0

def test_scale_same_recipe():
    ingred3 = Ingredient('Соль', 1, 'кг')
    recipe = Recipe('кокакола', [ingred3])
    recipe2 = recipe.scale(3)
    assert recipe2.ingredients[0].name == 'Соль'
    assert recipe2.ingredients[0].quantity == 3.0

def test_scale_bad_ratio_recipe():
    ingred3 = Ingredient('Соль', 1, 'кг')
    recipe = Recipe('кокакола', [ingred3])
    with pytest.raises(ValueError):
        recipe.scale(-3)

def test_len_recipe():
    ingred1 = Ingredient('Разрыхлитель', 3, 'кг')
    ingred2 = Ingredient('Соль', 3, 'кг')
    ingred3 = Ingredient('Соль', 1, 'кг')
    recipe = Recipe('булочка')
    recipe.add_ingredient(ingred1)
    recipe.add_ingredient(ingred2)
    recipe.add_ingredient(ingred3)
    assert len(recipe) == 2


def test_add_recipe_shopping_list():
    ingred3 = Ingredient('Соль', 1, 'кг')
    recipe = Recipe('кокакола', [ingred3])

    list1 = ShoppingList()
    list1.add_recipe(recipe, 2)
    ingreds = list1.get_list()
    assert len(ingreds) == 1
    assert ingreds[0].name == 'Соль'
    assert ingreds[0].quantity == 2.0
    assert ingreds[0].unit == 'кг'

def test_add_recipe_bad_portion_shopping_list():
    ingred3 = Ingredient('Соль', 1, 'кг')
    recipe = Recipe('кокакола', [ingred3])
    list1 = ShoppingList()
    with pytest.raises(ValueError):
        list1.add_recipe(recipe, -1)
    
def test_remove_recipe_shopping_list():
    ingred3 = Ingredient('Соль', 1, 'кг')
    recipe1 = Recipe('кокакола', [ingred3])
    ingred1 = Ingredient('Разрыхлитель', 3, 'кг')
    recipe2 = Recipe('венегрет')
    recipe2.add_ingredient(ingred1)

    list1 = ShoppingList()
    list1.add_recipe(recipe1, 1)
    list1.add_recipe(recipe2, 1)
    list1.remove_recipe('венегрет')
    ingreds = list1.get_list()

    assert len(ingreds) == 1
    assert ingreds[0].name == 'Соль'
    assert ingreds[0].quantity == 1.0
    assert ingreds[0].unit == 'кг'

def test_not_remove_recipe_shopping_list():
    ingred3 = Ingredient('Соль', 1, 'кг')
    recipe1 = Recipe('кокакола', [ingred3])
    list1 = ShoppingList()
    list1.add_recipe(recipe1 , 1)
    list1.remove_recipe('салат')
    ingreds = list1.get_list()

    assert len(ingreds) == 1
    assert ingreds[0].name == 'Соль'
    assert ingreds[0].quantity == 1.0
    assert ingreds[0].unit == 'кг'

def test_get_list_sum_shopping_list():
    ingred3 = Ingredient('Соль', 1, 'кг')
    recipe1 = Recipe('кокакола', [ingred3])
    recipe2 = Recipe('суп', [ingred3])
    list1 = ShoppingList()
    list1.add_recipe(recipe1, 1)
    list1.add_recipe(recipe2, 1)
    ingreds = list1.get_list()

    assert len(ingreds) == 1
    assert ingreds[0].name == 'Соль'
    assert ingreds[0].quantity == 2.0
    assert ingreds[0].unit == 'кг'

def test_get_list_sorted_shopping_list():
    ingred1 = Ingredient('Разрыхлитель', 3, 'кг')
    ingred3 = Ingredient('Соль', 1, 'кг')
    recipe = Recipe('кокакола', [ingred1, ingred3])
    list1 = ShoppingList()
    list1.add_recipe(recipe, 1)
    ingreds = list1.get_list()

    assert [ingred.name for ingred in ingreds] == ['Разрыхлитель', 'Соль']

def test_add_shopping_list():
    ingred3 = Ingredient('Соль', 1, 'кг')
    ingred1 = Ingredient('Разрыхлитель', 3, 'кг')
    recipe1 = Recipe('кокакола', [ingred3])
    recipe2 = Recipe('суп', [ingred1])
    list1 = ShoppingList()
    list2 = ShoppingList()
    list1.add_recipe(recipe1, 1)
    list2.add_recipe(recipe2, 1)
    list3 = list1 + list2

    ingreds = list3.get_list()

    assert len(ingreds) == 2
    assert ingreds[0].name == 'Разрыхлитель'
    assert ingreds[0].quantity == 3.0
    assert ingreds[0].unit == 'кг'

    assert ingreds[1].name == 'Соль'
    assert ingreds[1].quantity == 1.0
    assert ingreds[1].unit == 'кг'

def test_add_same_shopping_list():
    ingred3 = Ingredient('Соль', 1, 'кг')
    ingred1 = Ingredient('Разрыхлитель', 3, 'кг')
    recipe1 = Recipe('кокакола', [ingred3])
    recipe2 = Recipe('суп', [ingred1])
    list1 = ShoppingList()
    list2 = ShoppingList()
    list1.add_recipe(recipe1, 1)
    list2.add_recipe(recipe2, 1)
    list3 = list1 + list2

    ingreds1 = list1.get_list()
    ingreds2 = list2.get_list()
    ingreds3 = list3.get_list()

    assert len(ingreds1) == 1
    assert ingreds1[0] == ingred3

    assert len(ingreds2) == 1
    assert ingreds2[0] == ingred1

    assert len(ingreds3) == 2
    




















    
    


