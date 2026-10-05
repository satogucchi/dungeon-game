def show_menu():
    """Показать главное меню."""
    print("=" * 30)
    print("   ПОДЗЕМЕЛЬЕ")
    print("=" * 30)
    print("1. Новая игра")
    print("2. Выход")
    print("=" * 30)


def create_player():
    """Создать нового персонажа."""
    print("\n=== СОЗДАНИЕ ПЕРСОНАЖА ===")
    name = input("Введите имя героя: ").strip()
    
    if not name:
        name = "Безымянный"
    
    player = {
        "name": name,
        "hp": 100,
        "max_hp": 100,
        "attack": 10,
        "level": 1,
        "experience": 0
    }
    
    print(f"\nГерой {player['name']} создан!")
    print(f"HP: {player['hp']}/{player['max_hp']}")
    print(f"Атака: {player['attack']}")
    print(f"Уровень: {player['level']}")
    
    return player


def main():
    """Главный цикл игры."""
    while True:
        show_menu()
        choice = input("\nВыберите действие: ").strip()

        if choice == "1":
            player = create_player()
            print("\n[Игра пока не реализована]")
            input("Нажмите Enter для продолжения...")
        elif choice == "2":
            print("\nДо свидания!")
            break
        else:
            print("\nНеверный выбор, попробуйте снова.")


if __name__ == "__main__":
    main()
