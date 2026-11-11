"""Всё про игрока: создание, уровни, предметы, экраны статистики."""
from src.utils import (
    paint, save_highscore, difficulty_name,
    COLOR_RED, COLOR_GREEN, COLOR_YELLOW, COLOR_BLUE, COLOR_BOLD
)


def experience_to_next_level(level):
    """Сколько опыта нужно для следующего уровня."""
    return level * 20


def create_player(difficulty="normal"):
    """Создать нового персонажа."""
    print("\n" + paint("✨ === СОЗДАНИЕ ПЕРСОНАЖА === ✨", COLOR_BOLD + COLOR_MAGENTA if False else COLOR_BOLD + COLOR_GREEN))
    name = input("Введите имя героя: ").strip()

    if not name:
        name = "Безымянный"

    player = {
        "name": name,
        "hp": 100,
        "max_hp": 100,
        "attack": 10,
        "defense": 0,
        "level": 1,
        "experience": 0,
        "gold": 0,
        "kills": 0,
        "victory": False,
        "difficulty": difficulty,
        "inventory": [],
        "equipment": {
            "weapon": None,
            "armor": None
        },
        "quests": {}
    }

    print(f"\n🎉 Герой {player['name']} создан!")
    print(f"❤️  HP: {player['hp']}/{player['max_hp']}")
    print(f"⚔️  Атака: {player['attack']}")
    print(f"🛡️  Защита: {player['defense']}")
    print(f"⭐ Уровень: {player['level']}")
    print(paint(f"💰 Золото: {player['gold']}", COLOR_YELLOW))
    print(paint(f"⚙️  Сложность: {difficulty_name(difficulty)}", COLOR_GREEN))

    print("\n💡 Подсказка: используйте 'go north' чтобы начать путешествие!")
    print("   Введите 'help' для списка всех команд.")
    print("   💡 Совет: используйте 'search' для поиска секретов!")

    return player


def check_level_up(player):
    """Проверить и повысить уровень, если хватает опыта."""
    leveled_up = False
    while player["experience"] >= experience_to_next_level(player["level"]):
        player["experience"] -= experience_to_next_level(player["level"])
        player["level"] += 1
        player["max_hp"] += 20
        player["hp"] = player["max_hp"]
        player["attack"] += 3
        player["defense"] += 1
        leveled_up = True

        print("\n" + paint("🌟" * 15, COLOR_YELLOW))
        print(paint(f"   🎊 НОВЫЙ УРОВЕНЬ: {player['level']}! 🎊", COLOR_BOLD + COLOR_YELLOW))
        print(paint(f"   ❤️  Макс. HP: {player['max_hp']}", COLOR_YELLOW))
        print(paint(f"   ⚔️  Атака: {player['attack']}", COLOR_YELLOW))
        print(paint(f"   🛡️  Защита: {player['defense']}", COLOR_YELLOW))
        print(paint(f"   💚 HP полностью восстановлено!", COLOR_GREEN))
        print(paint("🌟" * 15, COLOR_YELLOW))

    return leveled_up


def use_item(item_name, player):
    """Использовать предмет из инвентаря."""
    if item_name not in player["inventory"]:
        print("\n" + paint(f"❌ У вас нет предмета '{item_name}'.", COLOR_RED))
        return False

    if item_name == "зелье здоровья":
        heal_amount = 30
        old_hp = player["hp"]
        player["hp"] = min(player["hp"] + heal_amount, player["max_hp"])
        healed = player["hp"] - old_hp
        player["inventory"].remove(item_name)
        print("\n" + paint(f"💚 Вы выпили зелье и восстановили {healed} HP!", COLOR_GREEN))
        print(paint(f"   ❤️ Текущее HP: {player['hp']}/{player['max_hp']}", COLOR_GREEN))
        return True
    else:
        print(f"\n❓ Предмет '{item_name}' нельзя использовать.")
        return False


def equip_item(item_name, player, items_db):
    """Экипировать предмет."""
    if item_name not in player["inventory"]:
        print("\n" + paint(f"❌ У вас нет предмета '{item_name}'.", COLOR_RED))
        return

    if item_name not in items_db:
        print(f"\n❓ Предмет '{item_name}' нельзя экипировать.")
        return

    item_data = items_db[item_name]
    item_type = item_data["type"]

    old_item = player["equipment"][item_type]
    if old_item:
        player["inventory"].append(old_item)
        print(f"   🔄 Снято: {old_item}")

    player["equipment"][item_type] = item_name
    player["inventory"].remove(item_name)

    print("\n" + paint(f"✅ Вы экипировали: {item_name}", COLOR_GREEN))
    if item_type == "weapon":
        print(paint(f"   ⚔️ +{item_data['attack_bonus']} к атаке", COLOR_YELLOW))
    elif item_type == "armor":
        print(paint(f"   🛡️ +{item_data['defense_bonus']} к защите", COLOR_BLUE))


def rest(player, room, monsters, items_db):
    """Отдохнуть и восстановить HP."""
    if room["monster"]:
        monster = monsters[room["monster"]]
        print("\n" + paint(f"❌ Нельзя отдыхать! {monster['name']} рядом!", COLOR_RED))
        return False

    if player["hp"] >= player["max_hp"]:
        print("\n❌ Вы полностью здоровы, отдых не нужен.")
        return False

    print("\n😴 Вы присели отдохнуть...")

    if random_chance(30):
        print(paint("⚠️ Вас кто-то потревожил!", COLOR_RED))
        damage = random_damage(3, 7)

        armor_bonus = 0
        if player["equipment"]["armor"] and player["equipment"]["armor"] in items_db:
            armor_bonus = items_db[player["equipment"]["armor"]]["defense_bonus"]
        total_defense = player["defense"] + armor_bonus

        actual_damage = max(1, damage - total_defense)
        player["hp"] -= actual_damage

        if total_defense > 0:
            absorbed = damage - actual_damage
            if absorbed > 0:
                print(paint(f"   🛡️ Защита поглотила {absorbed} урона!", COLOR_BLUE))
        print(paint(f"   💥 Вы получили {actual_damage} урона!", COLOR_RED))
        print(paint(f"   ❤️ HP: {max(0, player['hp'])}/{player['max_hp']}", COLOR_RED))

        if player["hp"] <= 0:
            print("\n" + paint("💀 Вы погибли во время отдыха...", COLOR_BOLD + COLOR_RED))
            return "dead"

        return False

    heal_amount = random_damage(15, 25)
    old_hp = player["hp"]
    player["hp"] = min(player["hp"] + heal_amount, player["max_hp"])
    healed = player["hp"] - old_hp

    print(paint(f"💚 Вы отдохнули и восстановили {healed} HP!", COLOR_GREEN))
    print(paint(f"   ❤️ HP: {player['hp']}/{player['max_hp']}", COLOR_GREEN))
    return True


def random_chance(percent):
    """Вернуть True с шансом percent процентов."""
    import random
    return random.randint(1, 100) <= percent


def random_damage(low, high):
    """Случайное число в диапазоне."""
    import random
    return random.randint(low, high)


def show_inventory(player):
    """Показать инвентарь."""
    print("\n🎒 === ИНВЕНТАРЬ ===")
    print(paint(f"  💰 Золото: {player['gold']}", COLOR_YELLOW))
    print(f"  🗡️  Оружие: {player['equipment']['weapon'] or 'нет'}")
    print(f"  🛡️  Броня: {player['equipment']['armor'] or 'нет'}")
    print("\n  Предметы:")
    if player["inventory"]:
        for item in player["inventory"]:
            print(paint(f"  • {item}", COLOR_GREEN))
    else:
        print("  Пусто")


def show_stats(player, items_db):
    """Показать характеристики героя."""
    needed = experience_to_next_level(player["level"])

    weapon_bonus = 0
    armor_bonus = 0
    if player["equipment"]["weapon"]:
        weapon_bonus = items_db[player["equipment"]["weapon"]]["attack_bonus"]
    if player["equipment"]["armor"]:
        armor_bonus = items_db[player["equipment"]["armor"]]["defense_bonus"]

    total_attack = player["attack"] + weapon_bonus
    total_defense = player["defense"] + armor_bonus

    print("\n📊 === ХАРАКТЕРИСТИКИ ===")
    print(f"  Имя: {player['name']}")
    print(f"  ⚙️  Сложность: {difficulty_name(player.get('difficulty', 'normal'))}")
    print(f"  ⭐ Уровень: {player['level']}")
    print(f"  ✨ Опыт: {player['experience']}/{needed}")
    print(f"  ❤️  HP: {player['hp']}/{player['max_hp']}")
    print(paint(f"  ⚔️  Атака: {total_attack} ({player['attack']} + {weapon_bonus})", COLOR_YELLOW))
    print(paint(f"  🛡️  Защита: {total_defense} ({player['defense']} + {armor_bonus})", COLOR_BLUE))
    print(paint(f"  💰 Золото: {player['gold']}", COLOR_YELLOW))
    print(f"  💀 Убийств: {player['kills']}")
    if player["victory"]:
        print(paint(f"  👑 Подземелье пройдено: ДА", COLOR_BOLD + COLOR_YELLOW))
    print(f"  🗡️  Оружие: {player['equipment']['weapon'] or 'нет'}")
    print(f"  🛡️  Броня: {player['equipment']['armor'] or 'нет'}")


def show_death_stats(player):
    """Показать статистику при смерти."""
    print("\n" + paint("💀" * 20, COLOR_RED))
    print(paint("   ВЫ ПОГИБЛИ В ПОДЗЕМЕЛЬЕ", COLOR_BOLD + COLOR_RED))
    print(paint("💀" * 20, COLOR_RED))
    print(f"\n📊 СТАТИСТИКА ЗА СЕССИЮ:")
    print(f"  Имя: {player['name']}")
    print(f"  Сложность: {difficulty_name(player.get('difficulty', 'normal'))}")
    print(f"  Уровень: {player['level']}")
    print(f"  Убито монстров: {player['kills']}")
    print(paint(f"  Собрано золота: {player['gold']}", COLOR_YELLOW))
    print(paint(f"  Финальный HP: {player['hp']}/{player['max_hp']}", COLOR_RED))

    save_highscore(player)
    print("\n" + paint("🏆 Результат сохранён в таблице рекордов!", COLOR_YELLOW))
    print("\n👋 Спасибо за игру!")


def show_quit_stats(player):
    """Показать статистику при выходе."""
    print(f"\n📊 КРАТКАЯ СТАТИСТИКА:")
    print(f"  Уровень: {player['level']}")
    print(f"  Убито монстров: {player['kills']}")
    print(paint(f"  Золото: {player['gold']}", COLOR_YELLOW))
    if player["victory"]:
        print(paint(f"  👑 Подземелье пройдено: ДА", COLOR_BOLD + COLOR_YELLOW))


def show_victory_screen(player):
    """Показать экран победы после победы над финальным боссом."""
    print("\n" + paint("👑" * 20, COLOR_YELLOW))
    print(paint("   П О Б Е Д А !", COLOR_BOLD + COLOR_YELLOW))
    print(paint("👑" * 20, COLOR_YELLOW))
    print(f"\n   🎉 Герой {player['name']} поверг Короля Скелетов!")
    print("   Подземелье освобождено от древнего зла.")
    print("   Барды будут слагать песни о твоём подвиге!")
    print(f"\n   📊 === СТАТИСТИКА ПРОХОЖДЕНИЯ ===")
    print(f"   ⚙️  Сложность: {difficulty_name(player.get('difficulty', 'normal'))}")
    print(f"   ⭐ Уровень героя: {player['level']}")
    print(f"   💀 Монстров убито: {player['kills']}")
    print(paint(f"   💰 Золота собрано: {player['gold']}", COLOR_YELLOW))
    print(f"   ❤️ Остаток HP: {player['hp']}/{player['max_hp']}")
    print(f"   🎒 Предметов в инвентаре: {len(player['inventory'])}")

    save_highscore(player)
    print("\n" + paint("   🏆 Результат сохранён в таблице рекордов!", COLOR_YELLOW))

    print(f"\n   🎁 Подземелье остаётся открытым для свободной игры:")
    print("   добейте монстров, соберите сокровища или сдайте квесты.")
    print("   Введите 'quit', чтобы завершить поход.")
    print("\n" + paint("👑" * 20, COLOR_YELLOW))