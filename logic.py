# Определяем доступные блюда и их ингредиенты
menu = {
    "Яичница": {"Яйца": 2, "Масло": 100},
    "Омлет": {"Яйца": 1, "Молоко": 300, "Масло": 100},
    "Овощной салат": {"Помидор": 1, "Лук репчатый": 1, "Масло": 100},
    "Оладьи": {"Яйца": 1, "Молоко": 100, "Мука": 300, "Масло": 200},
    "Жаренный картофель": {"Картофель": 3, "Масло": 100},
    "Картофельная запеканка": {"Картофель": 3, "Молоко": 100, "Яйцо": 1, "Помидор": 1, "Лук репчатый": 1},
    "Вареная картошка": {"Картофель": 4},
}

# Начальные запасы продуктов
inventory = {
    "Яйца": 3,
    "Лук репчатый": 2,
    "Помидор": 4,
    "Картофель": 4,
    "Мука": 700,
    "Молоко": 800,
    "Масло": 900,
}

def can_prepare(dish):
    """Проверяет, можно ли приготовить блюдо из имеющихся ингредиентов."""
    ingredients = menu[dish]
    for ingredient, amount in ingredients.items():
        if inventory.get(ingredient, 0) < amount:
            return False
    return True

def prepare_dish(dish):
    """Готовит блюдо и уменьшает количество ингредиентов."""
    ingredients = menu[dish]
    for ingredient, amount in ingredients.items():
        inventory[ingredient] -= amount

def ask_meal():

    daily_menu = {}

    for meal in ["завтрак", "обед", "ужин"]:
        print(f"\nЧто хотите на {meal}?")
        available_dishes = [dish for dish in menu.keys() if can_prepare(dish)]

        if not available_dishes:
            print("К сожалению, нет доступных блюд.")
            continue

        print("Доступные блюда:")
        for i, dish in enumerate(available_dishes, start=1):
            print(f"{i}. {dish}")

        choice = int(input("Выберите номер блюда: ")) - 1

        if 0 <= choice < len(available_dishes):
            selected_dish = available_dishes[choice]
            daily_menu[meal] = selected_dish
            prepare_dish(selected_dish)
            print(f"Вы выбрали: {selected_dish}")
        else:
            print("Неверный выбор. Попробуйте снова.")

    return daily_menu

def built_daily_menu():
    daily_menu = ask_meal()

    print("\nВаше меню на день:")
    for meal, dish in daily_menu.items():
        print(f"{meal.capitalize()}: {dish}")


def main():

    built_daily_menu()

if __name__ == "__main__":
    main()