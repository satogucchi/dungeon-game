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
        "experience": 0,
        "inventory": []
    }
    
    print(f"\nГерой {player['name']} создан!")
    print(f"HP: {player['hp']}/{player['max_hp']}")
    print(f"Атака: {player['attack']}")
    print(f"Уровень: {player['level']}")
    
    return player


def create_rooms():
    """Создать комнаты подземелья."""
    rooms = {
        "cave": {
            "name": "Тёмная пещера",
            "description": "Вы стоите в тёмной сырой пещере. "
                           "Со стен капает вода. Где-то вдалеке слышен шум.",
            "exits": {"north": "tunnel"},
            "items": ["факел"]
        },
        "tunnel": {
            "name": "Узкий тоннель",
            "description": "Вы в узком каменном тоннеле. "
                           "Стены покрыты мхом. На юг ведёт путь обратно в пещеру.",
            "exits": {"south": "cave"},
            "items": []
        }
    }
    return rooms


def look(room):
    """Осмотреться в комнате."""
    print(f"\n=== {room['name']} ===")
    print(room["description"])
    
    if room["items"]:
        print(f"\nПредметы на полу: {', '.join(room['items'])}")
    
    if room["exits"]:
        exits_str = ", ".join(room["exits"].keys())
        print(f"Выходы: {exits_str}")


def take(item_name, player, room):
    """Подобрать предмет."""
    if item_name in room["items"]:
        room["items"].remove(item_name)
        player["inventory"].append(item_name)
        print(f"\nВы подобрали: {item_name}")
    else:
        print(f"\nЗдесь нет предмета '{item_name}'.")


def show_inventory(player):
    """Показать инвентарь."""
    print("\n=== ИНВЕНТАРЬ ===")
    if player["inventory"]:
        for item in player["inventory"]:
            print(f"- {item}")
    else:
        print("Пусто")


def move(current_room_name, direction, rooms):
    """Переместиться в другую комнату."""
    current_room = rooms[current_room_name]
    
    if direction in current_room["exits"]:
        new_room_name = current_room["exits"][direction]
        return new_room_name
    else:
        print(f"\nТуда нельзя пройти на {direction}.")
        return current_room_name


def game_loop(player, rooms, current_room_name):
    """Основной игровой цикл."""
    look(rooms[current_room_name])
    
    while True:
        command = input("\n> ").strip().lower()
        
        if command == "look":
            look(rooms[current_room_name])
        elif command.startswith("go "):
            direction = command[3:].strip()
            current_room_name = move(current_room_name, direction, rooms)
            look(rooms[current_room_name])
        elif command.startswith("take "):
            item_name = command[5:].strip()
            take(item_name, player, rooms[current_room_name])
        elif command == "inventory" or command == "i":
            show_inventory(player)
        elif command == "quit":
            print("\nДо свидания!")
            break
        else:
            print("Неизвестная команда. Попробуйте 'look', 'go <направление>', 'take <предмет>', 'inventory' или 'quit'.")


def main():
    """Главный цикл игры."""
    while True:
        show_menu()
        choice = input("\nВыберите действие: ").strip()

        if choice == "1":
            player = create_player()
            rooms = create_rooms()
            current_room_name = "cave"
            game_loop(player, rooms, current_room_name)
        elif choice == "2":
            print("\nДо свидания!")
            break
        else:
            print("\nНеверный выбор, попробуйте снова.")


if __name__ == "__main__":
    main()
    