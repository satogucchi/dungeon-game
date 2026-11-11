"""Точка входа игры «Подземелье»."""
import os

from src.utils import clear_screen, choose_difficulty, show_highscores, paint, COLOR_BOLD, COLOR_CYAN, COLOR_RED
from src.player import (
    create_player, use_item, equip_item, rest,
    show_inventory, show_stats, show_death_stats,
    show_quit_stats, show_victory_screen
)
from src.world import (
    create_rooms, create_monsters, create_items_db, create_npcs,
    save_game, load_game, look, search_room, take, drop_item, move,
    talk_to_npc, show_quests, show_shop, buy_item, sell_item,
    restore_monster_hp
)
from src.combat import attack, flee, monster_counterattack


def show_menu():
    """Показать главное меню."""
    print("\n" + "=" * 40)
    print(paint("       🏰 ПОДЗЕМЕЛЬЕ 🏰", COLOR_BOLD + COLOR_CYAN))
    print("=" * 40)
    print("  1. ⚔️  Новая игра")
    print("  2. 📂 Загрузить игру")
    print("  3. 🏆 Рекорды")
    print("  4. 🚪 Выход")
    print("=" * 40)


def show_help():
    """Показать справку по командам."""
    print("\n" + paint("❓ === ДОСТУПНЫЕ КОМАНДЫ ===", COLOR_BOLD + COLOR_CYAN))
    print("\n  🚶 ПЕРЕМЕЩЕНИЕ:")
    print("    look          — осмотреться")
    print("    go <напр>     — идти (north/south/east/west)")
    print("    search        — искать секреты в комнате")

    print("\n  🎒 ПРЕДМЕТЫ:")
    print("    take <предмет> — подобрать предмет")
    print("    drop <предмет> — выбросить предмет")
    print("    use <предмет>  — использовать предмет")
    print("    equip <предмет> — экипировать оружие/броню")
    print("    inventory / i — показать инвентарь")

    print("\n  ⚔️ БОЙ:")
    print("    attack / a    — атаковать монстра")
    print("    flee          — попытаться сбежать из боя")
    print("    rest          — отдохнуть (восстановить HP)")

    print("\n  🏪 ТОРГОВЛЯ И КВЕСТЫ:")
    print("    shop          — показать магазин (у торговца)")
    print("    buy <предмет> — купить предмет")
    print("    sell <предмет> — продать предмет")
    print("    talk <npc>    — поговорить с NPC")
    print("    quests        — показать активные квесты")

    print("\n  📊 ИНФОРМАЦИЯ:")
    print("    stats         — показать характеристики")
    print("    help          — показать эту справку")

    print("\n  💾 СИСТЕМА:")
    print("    clear / cls   — очистить экран")
    print("    save          — сохранить игру")
    print("    quit          — выйти из игры")
    print("=" * 30)


def game_loop(player, rooms, monsters, items_db, npcs, current_room_name):
    """Основной игровой цикл."""
    look(rooms[current_room_name], monsters, npcs, player)

    while True:
        command = input("\n> ").strip().lower()

        if command == "look":
            look(rooms[current_room_name], monsters, npcs, player)
        elif command == "search":
            search_room(rooms[current_room_name], player)
        elif command.startswith("go "):
            direction = command[3:].strip()
            result = move(current_room_name, direction, rooms, monsters, player)

            if result == "dead":
                show_death_stats(player)
                break

            current_room_name = result
            look(rooms[current_room_name], monsters, npcs, player)
        elif command.startswith("take "):
            item_name = command[5:].strip()
            take(item_name, player, rooms[current_room_name])
        elif command.startswith("drop "):
            item_name = command[5:].strip()
            drop_item(item_name, player, rooms[current_room_name])
        elif command.startswith("use "):
            item_name = command[4:].strip()
            used = use_item(item_name, player)
            if used and rooms[current_room_name]["monster"]:
                monster = monsters[rooms[current_room_name]["monster"]]
                print(paint(f"⏳ Пока вы пили зелье, {monster['name']} атакует!", COLOR_RED))
                result = monster_counterattack(player, monster, items_db)
                if result == "dead":
                    show_death_stats(player)
                    break
        elif command.startswith("equip "):
            item_name = command[6:].strip()
            equip_item(item_name, player, items_db)
        elif command.startswith("talk "):
            npc_key = command[5:].strip()
            room = rooms[current_room_name]
            if room.get("npc") == npc_key:
                talk_to_npc(npc_key, player, npcs)
            else:
                print(f"\n❌ Здесь нет NPC '{npc_key}'.")
        elif command == "quests":
            show_quests(player, npcs)
        elif command == "rest":
            result = rest(player, rooms[current_room_name], monsters, items_db)
            if result == "dead":
                show_death_stats(player)
                break
        elif command in ("attack", "a"):
            was_victory = player["victory"]
            result = attack(player, rooms[current_room_name], monsters, items_db, npcs)
            if result == "dead":
                show_death_stats(player)
                break
            if player["victory"] and not was_victory:
                show_victory_screen(player)
        elif command == "flee":
            result = flee(player, rooms[current_room_name], rooms, monsters, items_db, current_room_name)
            if result == "dead":
                show_death_stats(player)
                break
            elif result != current_room_name:
                current_room_name = result
                look(rooms[current_room_name], monsters, npcs, player)
        elif command == "shop":
            room = rooms[current_room_name]
            if room.get("npc") and room["npc"] in npcs:
                npc = npcs[room["npc"]]
                if "shop" in npc:
                    show_shop(npc, items_db, player)
                else:
                    print("\n❌ У этого NPC нет магазина.")
            else:
                print("\n❌ Здесь нет торговца.")
        elif command.startswith("buy "):
            item_name = command[4:].strip()
            room = rooms[current_room_name]
            if room.get("npc") and room["npc"] in npcs:
                npc = npcs[room["npc"]]
                if "shop" in npc:
                    buy_item(item_name, player, npc, items_db)
                else:
                    print("\n❌ У этого NPC нет магазина.")
            else:
                print("\n❌ Здесь нет торговца.")
        elif command.startswith("sell "):
            item_name = command[5:].strip()
            room = rooms[current_room_name]
            if room.get("npc") and room["npc"] in npcs:
                npc = npcs[room["npc"]]
                sell_item(item_name, player, npc, items_db)
            else:
                print("\n❌ Здесь нет торговца.")
        elif command in ("inventory", "i"):
            show_inventory(player)
        elif command == "stats":
            show_stats(player, items_db)
        elif command in ("clear", "cls"):
            clear_screen()
        elif command == "save":
            save_game(player, rooms, current_room_name)
        elif command == "help":
            show_help()
        elif command == "quit":
            save_game(player, rooms, current_room_name)
            show_quit_stats(player)
            print("\n👋 До свидания!")
            break
        else:
            print(paint("❓ Неизвестная команда. Введите 'help' для списка команд.", COLOR_RED))


def main():
    """Главный цикл игры."""
    # Включаем поддержку ANSI-цветов в консоли Windows
    os.system("")

    while True:
        show_menu()
        choice = input("\nВыберите действие: ").strip()

        if choice == "1":
            difficulty = choose_difficulty()
            player = create_player(difficulty)
            rooms = create_rooms()
            monsters = create_monsters(difficulty)
            items_db = create_items_db()
            npcs = create_npcs()
            current_room_name = "cave"
            game_loop(player, rooms, monsters, items_db, npcs, current_room_name)
        elif choice == "2":
            player, rooms, current_room_name = load_game()
            if player:
                monsters = create_monsters(player.get("difficulty", "normal"))
                restore_monster_hp(rooms, monsters)
                items_db = create_items_db()
                npcs = create_npcs()
                game_loop(player, rooms, monsters, items_db, npcs, current_room_name)
        elif choice == "3":
            show_highscores()
        elif choice == "4":
            print("\n👋 До свидания!")
            break
        else:
            print("\n❌ Неверный выбор, попробуйте снова.")


if __name__ == "__main__":
    main()
    