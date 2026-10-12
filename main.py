import json
import os
import random


def show_menu():
    """Показать главное меню."""
    print("\n" + "=" * 40)
    print("       🏰 ПОДЗЕМЕЛЬЕ 🏰")
    print("=" * 40)
    print("  1. ⚔️  Новая игра")
    print("  2. 📂 Загрузить игру")
    print("  3. 🚪 Выход")
    print("=" * 40)


def create_player():
    """Создать нового персонажа."""
    print("\n✨ === СОЗДАНИЕ ПЕРСОНАЖА === ✨")
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

    print(f"\n🎉 Герой {player['name']} создан!")
    print(f"❤️  HP: {player['hp']}/{player['max_hp']}")
    print(f"⚔️  Атака: {player['attack']}")
    print(f"⭐ Уровень: {player['level']}")

    return player


def create_monsters():
    """Создать шаблоны монстров."""
    monsters = {
        "rat": {
            "name": "Гигантская крыса",
            "hp": 20,
            "max_hp": 20,
            "attack": 5,
            "experience": 10,
            "emoji": "🐀"
        }
    }
    return monsters


def create_rooms():
    """Создать комнаты подземелья."""
    rooms = {
        "cave": {
            "name": "Тёмная пещера",
            "description": "Вы стоите в тёмной сырой пещере. "
                           "Со стен капает вода. Где-то вдалеке слышен шум.",
            "exits": {"north": "tunnel"},
            "items": ["факел"],
            "monster": None
        },
        "tunnel": {
            "name": "Узкий тоннель",
            "description": "Вы в узком каменном тоннеле. "
                           "Стены покрыты мхом. На юг ведёт путь обратно в пещеру.",
            "exits": {"south": "cave"},
            "items": [],
            "monster": "rat"
        }
    }
    return rooms


def save_game(player, rooms, current_room_name):
    """Сохранить игру в файл."""
    os.makedirs("saves", exist_ok=True)

    save_data = {
        "player": player,
        "rooms": rooms,
        "current_room": current_room_name
    }

    with open("saves/savegame.json", "w", encoding="utf-8") as f:
        json.dump(save_data, f, ensure_ascii=False, indent=2)

    print("\n💾 Игра сохранена!")


def load_game():
    """Загрузить игру из файла."""
    if not os.path.exists("saves/savegame.json"):
        print("\n❌ Сохранение не найдено!")
        return None, None, None

    with open("saves/savegame.json", "r", encoding="utf-8") as f:
        save_data = json.load(f)

    print("\n📂 Игра загружена!")
    return save_data["player"], save_data["rooms"], save_data["current_room"]


def look(room, monsters):
    """Осмотреться в комнате."""
    print(f"\n📍 === {room['name']} ===")
    print(room["description"])

    if room["monster"]:
        monster = monsters[room["monster"]]
        print(f"\n{monster['emoji']} Здесь находится {monster['name']}! "
              f"(HP: {monster['hp']}/{monster['max_hp']})")

    if room["items"]:
        print(f"\n🎒 Предметы на полу: {', '.join(room['items'])}")

    if room["exits"]:
        exits_str = ", ".join(room["exits"].keys())
        print(f"🚪 Выходы: {exits_str}")


def take(item_name, player, room):
    """Подобрать предмет."""
    if item_name in room["items"]:
        room["items"].remove(item_name)
        player["inventory"].append(item_name)
        print(f"\n✅ Вы подобрали: {item_name}")
    else:
        print(f"\n❌ Здесь нет предмета '{item_name}'.")


def show_inventory(player):
    """Показать инвентарь."""
    print("\n🎒 === ИНВЕНТАРЬ ===")
    if player["inventory"]:
        for item in player["inventory"]:
            print(f"  • {item}")
    else:
        print("  Пусто")


def show_help():
    """Показать справку по командам."""
    print("\n❓ === ДОСТУПНЫЕ КОМАНДЫ ===")
    print("  look          — осмотреться")
    print("  go <напр>     — идти (north/south/east/west)")
    print("  take <предмет> — подобрать предмет")
    print("  attack / a    — атаковать монстра")
    print("  inventory / i — показать инвентарь")
    print("  save          — сохранить игру")
    print("  help          — показать эту справку")
    print("  quit          — выйти из игры")
    print("=" * 30)


def attack(player, room, monsters):
    """Атаковать монстра в комнате."""
    if not room["monster"]:
        print("\n❌ Здесь некого атаковать.")
        return False

    monster_key = room["monster"]
    monster = monsters[monster_key]

    # Урон игрока по монстру (с небольшим разбросом)
    player_damage = random.randint(player["attack"] - 2, player["attack"] + 2)
    player_damage = max(1, player_damage)
    monster["hp"] -= player_damage
    print(f"\n⚔️ Вы ударили {monster['name']} и нанесли {player_damage} урона!")
    print(f"   {monster['emoji']} HP монстра: {max(0, monster['hp'])}/{monster['max_hp']}")

    # Проверка смерти монстра
    if monster["hp"] <= 0:
        print(f"\n🎉 Вы победили {monster['name']}!")
        player["experience"] += monster["experience"]
        print(f"   ⭐ Получено опыта: {monster['experience']}")
        print(f"   ⭐ Всего опыта: {player['experience']}")
        room["monster"] = None
        return True

    # Ответный удар монстра
    monster_damage = random.randint(monster["attack"] - 1, monster["attack"] + 1)
    monster_damage = max(1, monster_damage)
    player["hp"] -= monster_damage
    print(f"\n💥 {monster['name']} атакует вас и наносит {monster_damage} урона!")
    print(f"   ❤️ Ваше HP: {max(0, player['hp'])}/{player['max_hp']}")

    # Проверка смерти игрока
    if player["hp"] <= 0:
        print("\n💀 Вы погибли...")
        return "dead"

    return False


def move(current_room_name, direction, rooms, monsters):
    """Переместиться в другую комнату."""
    current_room = rooms[current_room_name]

    if direction in current_room["exits"]:
        new_room_name = current_room["exits"][direction]
        return new_room_name
    else:
        print(f"\n❌ Туда нельзя пройти на {direction}.")
        return current_room_name


def game_loop(player, rooms, monsters, current_room_name):
    """Основной игровой цикл."""
    look(rooms[current_room_name], monsters)

    while True:
        command = input("\n> ").strip().lower()

        if command == "look":
            look(rooms[current_room_name], monsters)
        elif command.startswith("go "):
            direction = command[3:].strip()
            current_room_name = move(current_room_name, direction, rooms, monsters)
            look(rooms[current_room_name], monsters)
        elif command.startswith("take "):
            item_name = command[5:].strip()
            take(item_name, player, rooms[current_room_name])
        elif command in ("attack", "a"):
            result = attack(player, rooms[current_room_name], monsters)
            if result == "dead":
                print("\n👋 Игра окончена.")
                break
        elif command in ("inventory", "i"):
            show_inventory(player)
        elif command == "save":
            save_game(player, rooms, current_room_name)
        elif command == "help":
            show_help()
        elif command == "quit":
            save_game(player, rooms, current_room_name)
            print("\n👋 До свидания!")
            break
        else:
            print("❓ Неизвестная команда. Введите 'help' для списка команд.")


def main():
    """Главный цикл игры."""
    while True:
        show_menu()
        choice = input("\nВыберите действие: ").strip()

        if choice == "1":
            player = create_player()
            rooms = create_rooms()
            monsters = create_monsters()
            current_room_name = "cave"
            game_loop(player, rooms, monsters, current_room_name)
        elif choice == "2":
            player, rooms, current_room_name = load_game()
            if player:
                monsters = create_monsters()
                game_loop(player, rooms, monsters, current_room_name)
        elif choice == "3":
            print("\n👋 До свидания!")
            break
        else:
            print("\n❌ Неверный выбор, попробуйте снова.")


if __name__ == "__main__":
    main()
    