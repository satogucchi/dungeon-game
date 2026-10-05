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


def create_room():
    """Создать первую комнату."""
    room = {
        "name": "Тёмная пещера",
        "description": "Вы стоите в тёмной сырой пещере. "
                       "Со стен капает вода. Где-то вдалеке слышен шум.",
        "exits": {}
    }
    return room


def look(room):
    """Осмотреться в комнате."""
    print(f"\n=== {room['name']} ===")
    print(room["description"])


def game_loop(player, room):
    """Основной игровой цикл."""
    look(room)
    
    while True:
        command = input("\n> ").strip().lower()
        
        if command == "look":
            look(room)
        elif command == "quit":
            print("\nДо свидания!")
            break
        else:
            print("Неизвестная команда. Попробуйте 'look' или 'quit'.")


def main():
    """Главный цикл игры."""
    while True:
        show_menu()
        choice = input("\nВыберите действие: ").strip()

        if choice == "1":
            player = create_player()
            room = create_room()
            game_loop(player, room)
        elif choice == "2":
            print("\nДо свидания!")
            break
        else:
            print("\nНеверный выбор, попробуйте снова.")


if __name__ == "__main__":
    main()
    