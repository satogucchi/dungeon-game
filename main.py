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
        "defense": 0,  # НОВОЕ: базовая защита
        "level": 1,
        "experience": 0,
        "gold": 0,
        "inventory": [],
        "equipment": {
            "weapon": None,
            "armor": None
        }
    }

    print(f"\n🎉 Герой {player['name']} создан!")
    print(f"❤️  HP: {player['hp']}/{player['max_hp']}")
    print(f"⚔️  Атака: {player['attack']}")
    print(f"🛡️  Защита: {player['defense']}")
    print(f"⭐ Уровень: {player['level']}")
    print(f"💰 Золото: {player['gold']}")
    print(f"🛡️  Экипировка: нет")

    return player


def experience_to_next_level(level):
    """Сколько опыта нужно для следующего уровня."""
    return level * 20


def check_level_up(player):
    """Проверить и повысить уровень, если хватает опыта."""
    leveled_up = False
    while player["experience"] >= experience_to_next_level(player["level"]):
        player["experience"] -= experience_to_next_level(player["level"])
        player["level"] += 1
        player["max_hp"] += 20
        player["hp"] = player["max_hp"]
        player["attack"] += 3
        player["defense"] += 1  # НОВОЕ: +1 защита за уровень
        leveled_up = True

        print("\n" + "🌟" * 15)
        print(f"   🎊 НОВЫЙ УРОВЕНЬ: {player['level']}! 🎊")
        print(f"   ❤️  Макс. HP: {player['max_hp']}")
        print(f"   ⚔️  Атака: {player['attack']}")
        print(f"   🛡️  Защита: {player['defense']}")
        print(f"   💚 HP полностью восстановлено!")
        print("🌟" * 15)

    return leveled_up


def create_items_db():
    """База данных предметов с характеристиками."""
    items = {
        "ржавый нож": {
            "type": "weapon",
            "attack_bonus": 3,
            "description": "Старый нож с зазубринами",
            "price": 20,
            "sell_price": 8
        },
        "ржавый меч": {
            "type": "weapon",
            "attack_bonus": 5,
            "description": "Тяжёлый меч, покрытый ржавчиной",
            "price": 40,
            "sell_price": 15
        },
        "кожаная броня": {
            "type": "armor",
            "defense_bonus": 2,
            "description": "Простая кожаная куртка",
            "price": 30,
            "sell_price": 12
        },
        "зелье здоровья": {
            "type": "consumable",
            "heal_amount": 30,
            "description": "Восстанавливает 30 HP",
            "price": 15,
            "sell_price": 5
        },
        "кость": {
            "type": "junk",
            "description": "Обычная кость",
            "sell_price": 2
        },
        "паутина": {
            "type": "junk",
            "description": "Липкая паутина",
            "sell_price": 3
        },
        "факел": {
            "type": "junk",
            "description": "Горящий факел",
            "sell_price": 1
        }
    }
    return items


def create_monsters():
    """Создать шаблоны монстров с балансом и лутом."""
    monsters = {
        "rat": {
            "name": "Гигантская крыса",
            "hp": 20,
            "max_hp": 20,
            "attack": 5,
            "experience": 10,
            "emoji": "🐀",
            "loot": [
                {"item": "золото", "amount": 5, "chance": 70},
                {"item": "кость", "amount": 1, "chance": 30}
            ]
        },
        "spider": {
            "name": "Пещерный паук",
            "hp": 35,
            "max_hp": 35,
            "attack": 8,
            "experience": 20,
            "emoji": "🕷️",
            "loot": [
                {"item": "золото", "amount": 10, "chance": 60},
                {"item": "паутина", "amount": 1, "chance": 40}
            ]
        },
        "slime": {
            "name": "Кислотный слизень",
            "hp": 45,
            "max_hp": 45,
            "attack": 4,
            "experience": 25,
            "emoji": "🟢",
            "loot": [
                {"item": "золото", "amount": 8, "chance": 80},
                {"item": "зелье здоровья", "amount": 1, "chance": 20}
            ]
        },
        "goblin": {
            "name": "Гоблин-разбойник",
            "hp": 28,
            "max_hp": 28,
            "attack": 12,
            "experience": 30,
            "emoji": "👺",
            "loot": [
                {"item": "золото", "amount": 15, "chance": 90},
                {"item": "ржавый нож", "amount": 1, "chance": 25},
                {"item": "кожаная броня", "amount": 1, "chance": 15}
            ]
        },
        "skeleton": {
            "name": "Древний скелет",
            "hp": 50,
            "max_hp": 50,
            "attack": 10,
            "experience": 45,
            "emoji": "💀",
            "loot": [
                {"item": "золото", "amount": 25, "chance": 100},
                {"item": "кость", "amount": 2, "chance": 50},
                {"item": "зелье здоровья", "amount": 1, "chance": 30},
                {"item": "ржавый меч", "amount": 1, "chance": 20}
            ]
        }
    }
    return monsters


def create_rooms():
    """Создать комнаты подземелья с новыми локациями."""
    rooms = {
        "cave": {
            "name": "Тёмная пещера",
            "description": "Вы стоите в тёмной сырой пещере. Со стен капает вода.",
            "exits": {"north": "tunnel"},
            "items": ["факел"],
            "monster": None,
            "npc": None
        },
        "tunnel": {
            "name": "Узкий тоннель",
            "description": "Стены покрыты мхом. Слышны странные звуки со всех сторон.",
            "exits": {"south": "cave", "east": "spider_nest", "west": "goblin_camp", "north": "merchant_room"},
            "items": [],
            "monster": "rat",
            "npc": None
        },
        "spider_nest": {
            "name": "Паучье гнездо",
            "description": "Всё затянуто паутиной. В углу колышется липкая масса.",
            "exits": {"west": "tunnel", "north": "bone_crypt"},
            "items": [],
            "monster": "slime",
            "npc": None
        },
        "goblin_camp": {
            "name": "Лагерь гоблинов",
            "description": "Грязная стоянка с остатками еды и сломанным оружием. Воняет.",
            "exits": {"east": "tunnel"},
            "items": ["ржавый нож"],
            "monster": "goblin",
            "npc": None
        },
        "bone_crypt": {
            "name": "Костяная крипта",
            "description": "Холодное помещение, усыпанное костями. В центре стоит саркофаг.",
            "exits": {"south": "spider_nest"},
            "items": [],
            "monster": "skeleton",
            "npc": None
        },
        "merchant_room": {
            "name": "Лавка торговца",
            "description": "Маленькая комната с прилавком. За ним стоит пожилой торговец.",
            "exits": {"south": "tunnel"},
            "items": [],
            "monster": None,
            "npc": "merchant"
        }
    }
    return rooms


def create_npcs():
    """Создать NPC."""
    npcs = {
        "merchant": {
            "name": "Торговец Гаррет",
            "emoji": "🧙",
            "dialogue": "Приветствую, путник! Я покупаю и продаю товары.",
            "shop": ["зелье здоровья", "ржавый нож", "кожаная броня", "ржавый меч"]
        }
    }
    return npcs


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
    
    # Миграция старых сейвов
    if "gold" not in save_data["player"]:
        save_data["player"]["gold"] = 0
    if "equipment" not in save_data["player"]:
        save_data["player"]["equipment"] = {"weapon": None, "armor": None}
    if "defense" not in save_data["player"]:  # НОВОЕ
        save_data["player"]["defense"] = 0
    
    # Миграция комнат: добавляем поле npc, если его нет
    for room_key in save_data["rooms"]:
        if "npc" not in save_data["rooms"][room_key]:
            save_data["rooms"][room_key]["npc"] = None
    
    print("\n📂 Игра загружена!")
    return save_data["player"], save_data["rooms"], save_data["current_room"]


def look(room, monsters, npcs):
    """Осмотреться в комнате."""
    print(f"\n📍 === {room['name']} ===")
    print(room["description"])

    if room["monster"]:
        monster = monsters[room["monster"]]
        print(f"\n{monster['emoji']} Здесь находится {monster['name']}! "
              f"(HP: {monster['hp']}/{monster['max_hp']})")

    if room.get("npc"):
        npc = npcs[room["npc"]]
        print(f"\n{npc['emoji']} Здесь находится {npc['name']}.")
        print(f"   💬 \"{npc['dialogue']}\"")

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


def use_item(item_name, player):
    """Использовать предмет из инвентаря."""
    if item_name not in player["inventory"]:
        print(f"\n❌ У вас нет предмета '{item_name}'.")
        return

    if item_name == "зелье здоровья":
        heal_amount = 30
        old_hp = player["hp"]
        player["hp"] = min(player["hp"] + heal_amount, player["max_hp"])
        healed = player["hp"] - old_hp
        player["inventory"].remove(item_name)
        print(f"\n💚 Вы выпили зелье и восстановили {healed} HP!")
        print(f"   ❤️ Текущее HP: {player['hp']}/{player['max_hp']}")
    else:
        print(f"\n❓ Предмет '{item_name}' нельзя использовать.")


def equip_item(item_name, player, items_db):
    """Экипировать предмет."""
    if item_name not in player["inventory"]:
        print(f"\n❌ У вас нет предмета '{item_name}'.")
        return
    
    if item_name not in items_db:
        print(f"\n❓ Предмет '{item_name}' нельзя экипировать.")
        return
    
    item_data = items_db[item_name]
    item_type = item_data["type"]
    
    # Снимаем старую экипировку этого типа (если есть)
    old_item = player["equipment"][item_type]
    if old_item:
        player["inventory"].append(old_item)
        print(f"   🔄 Снято: {old_item}")
    
    # Надеваем новый предмет
    player["equipment"][item_type] = item_name
    player["inventory"].remove(item_name)
    
    print(f"\n✅ Вы экипировали: {item_name}")
    if item_type == "weapon":
        print(f"   ⚔️ +{item_data['attack_bonus']} к атаке")
    elif item_type == "armor":
        print(f"   🛡️ +{item_data['defense_bonus']} к защите")


def show_shop(npc, items_db, player):
    """Показать магазин торговца."""
    print(f"\n🏪 === МАГАЗИН {npc['name'].upper()} ===")
    print(f"💰 Ваше золото: {player['gold']}\n")
    
    print("  📦 ПОКУПКА:")
    for item_name in npc["shop"]:
        if item_name in items_db:
            item = items_db[item_name]
            price = item.get("price", 0)
            print(f"  • {item_name} — {price} золота")
            if item["type"] == "weapon":
                print(f"    ⚔️ +{item['attack_bonus']} к атаке")
            elif item["type"] == "armor":
                print(f"    🛡️ +{item['defense_bonus']} к защите")
            elif item["type"] == "consumable":
                print(f"    💚 Восстанавливает {item['heal_amount']} HP")
    
    print("\n  💸 ПРОДАЖА (ваши предметы):")
    sellable_items = {}
    for item_name in player["inventory"]:
        if item_name in items_db and "sell_price" in items_db[item_name]:
            if item_name not in sellable_items:
                sellable_items[item_name] = {"count": 0, "price": items_db[item_name]["sell_price"]}
            sellable_items[item_name]["count"] += 1
    
    if sellable_items:
        for item_name, data in sellable_items.items():
            print(f"  • {item_name} x{data['count']} — {data['price']} золота за шт.")
    else:
        print("  Нет предметов для продажи.")
    
    print("\n  Команды: buy <предмет>, sell <предмет>")


def buy_item(item_name, player, npc, items_db):
    """Купить предмет у торговца."""
    if item_name not in npc["shop"]:
        print(f"\n❌ Торговец не продаёт '{item_name}'.")
        return
    
    if item_name not in items_db:
        print(f"\n❌ Предмет '{item_name}' не найден в базе.")
        return
    
    item = items_db[item_name]
    price = item.get("price", 0)
    
    if player["gold"] < price:
        print(f"\n❌ Недостаточно золота! Нужно {price}, у вас {player['gold']}.")
        return
    
    player["gold"] -= price
    player["inventory"].append(item_name)
    print(f"\n✅ Вы купили {item_name} за {price} золота!")
    print(f"   💰 Осталось золота: {player['gold']}")


def sell_item(item_name, player, npc, items_db):
    """Продать предмет торговцу."""
    if item_name not in player["inventory"]:
        print(f"\n❌ У вас нет предмета '{item_name}'.")
        return
    
    if item_name not in items_db or "sell_price" not in items_db[item_name]:
        print(f"\n❌ Торговец не покупает '{item_name}'.")
        return
    
    sell_price = items_db[item_name]["sell_price"]
    player["inventory"].remove(item_name)
    player["gold"] += sell_price
    
    print(f"\n✅ Вы продали {item_name} за {sell_price} золота!")
    print(f"   💰 Теперь у вас: {player['gold']} золота")


def show_inventory(player):
    """Показать инвентарь."""
    print("\n🎒 === ИНВЕНТАРЬ ===")
    print(f"  💰 Золото: {player['gold']}")
    print(f"  🗡️  Оружие: {player['equipment']['weapon'] or 'нет'}")
    print(f"  🛡️  Броня: {player['equipment']['armor'] or 'нет'}")
    print("\n  Предметы:")
    if player["inventory"]:
        for item in player["inventory"]:
            print(f"  • {item}")
    else:
        print("  Пусто")


def show_stats(player, items_db):
    """Показать характеристики героя."""
    needed = experience_to_next_level(player["level"])
    
    # Бонусы от экипировки
    weapon_bonus = 0
    armor_bonus = 0
    if player["equipment"]["weapon"]:
        weapon_bonus = items_db[player["equipment"]["weapon"]]["attack_bonus"]
    if player["equipment"]["armor"]:
        armor_bonus = items_db[player["equipment"]["armor"]]["defense_bonus"]
    
    total_attack = player["attack"] + weapon_bonus
    total_defense = player["defense"] + armor_bonus  # НОВОЕ: общая защита
    
    print("\n📊 === ХАРАКТЕРИСТИКИ ===")
    print(f"  Имя: {player['name']}")
    print(f"  ⭐ Уровень: {player['level']}")
    print(f"  ✨ Опыт: {player['experience']}/{needed}")
    print(f"  ❤️  HP: {player['hp']}/{player['max_hp']}")
    print(f"  ⚔️  Атака: {total_attack} ({player['attack']} + {weapon_bonus})")
    print(f"  🛡️  Защита: {total_defense} ({player['defense']} + {armor_bonus})")
    print(f"  💰 Золото: {player['gold']}")
    print(f"  🗡️  Оружие: {player['equipment']['weapon'] or 'нет'}")
    print(f"  🛡️  Броня: {player['equipment']['armor'] or 'нет'}")


def show_help():
    """Показать справку по командам."""
    print("\n❓ === ДОСТУПНЫЕ КОМАНДЫ ===")
    print("  look          — осмотреться")
    print("  go <напр>     — идти (north/south/east/west)")
    print("  take <предмет> — подобрать предмет")
    print("  use <предмет>  — использовать предмет")
    print("  equip <предмет> — экипировать оружие/броню")
    print("  attack / a    — атаковать монстра")
    print("  flee          — попытаться сбежать из боя")
    print("  shop          — показать магазин (у торговца)")
    print("  buy <предмет> — купить предмет")
    print("  sell <предмет> — продать предмет")
    print("  inventory / i — показать инвентарь")
    print("  stats         — показать характеристики")
    print("  save          — сохранить игру")
    print("  help          — показать эту справку")
    print("  quit          — выйти из игры")
    print("=" * 30)


def drop_loot(monster, player):
    """Выдать лут с монстра."""
    if "loot" not in monster:
        return
    
    print("\n🎁 Лут:")
    for loot_entry in monster["loot"]:
        if random.randint(1, 100) <= loot_entry["chance"]:
            if loot_entry["item"] == "золото":
                player["gold"] += loot_entry["amount"]
                print(f"   💰 +{loot_entry['amount']} золота")
            else:
                # Для предметов добавляем несколько копий, если amount > 1
                for _ in range(loot_entry["amount"]):
                    player["inventory"].append(loot_entry["item"])
                print(f"   📦 +{loot_entry['amount']}x {loot_entry['item']}")


def attack(player, room, monsters, items_db):
    """Атаковать монстра в комнате."""
    if not room["monster"]:
        print("\n❌ Здесь некого атаковать.")
        return False

    monster_key = room["monster"]
    monster = monsters[monster_key]

    # Бонус от оружия
    weapon_bonus = 0
    if player["equipment"]["weapon"] and player["equipment"]["weapon"] in items_db:
        weapon_bonus = items_db[player["equipment"]["weapon"]]["attack_bonus"]

    total_attack = player["attack"] + weapon_bonus
    
    # --- ЛОГИКА КРИТИЧЕСКОГО УДАРА ---
    is_crit = random.randint(1, 100) <= 15  # 15% шанс крита
    base_damage = random.randint(total_attack - 2, total_attack + 2)
    
    if is_crit:
        player_damage = base_damage * 2
        print(f"\n💥 КРИТИЧЕСКИЙ УДАР! Вы нанесли {player_damage} урона!")
    else:
        player_damage = max(1, base_damage)
        print(f"\n⚔️ Вы ударили {monster['name']} и нанесли {player_damage} урона.")
    # ----------------------------------

    monster["hp"] -= player_damage
    print(f"   {monster['emoji']} HP монстра: {max(0, monster['hp'])}/{monster['max_hp']}")

    if monster["hp"] <= 0:
        print(f"\n🎉 Вы победили {monster['name']}!")
        player["experience"] += monster["experience"]
        print(f"   ⭐ Получено опыта: {monster['experience']}")
        print(f"   ⭐ Всего опыта: {player['experience']}/"
              f"{experience_to_next_level(player['level'])}")
        
        # Выдаём лут
        drop_loot(monster, player)
        
        room["monster"] = None
        check_level_up(player)
        return True

    # --- ОТВЕТНЫЙ УДАР МОНСТРА С УЧЁТОМ БРОНИ ---
    armor_bonus = 0
    if player["equipment"]["armor"] and player["equipment"]["armor"] in items_db:
        armor_bonus = items_db[player["equipment"]["armor"]]["defense_bonus"]

    total_defense = player["defense"] + armor_bonus  # НОВОЕ: общая защита

    raw_monster_damage = random.randint(monster["attack"] - 1, monster["attack"] + 1)
    monster_damage = max(1, raw_monster_damage - total_defense)  # Защита снижает урон
    
    player["hp"] -= monster_damage
    
    if total_defense > 0:
        absorbed = raw_monster_damage - monster_damage
        if absorbed > 0:
            print(f"\n🛡️ Защита поглотила {absorbed} урона!")
    print(f"🩸 {monster['name']} атакует вас и наносит {monster_damage} урона.")
    print(f"   ❤️ Ваше HP: {max(0, player['hp'])}/{player['max_hp']}")
    # -------------------------------------------

    if player["hp"] <= 0:
        print("\n💀 Вы погибли...")
        return "dead"

    return False


def flee(player, room, rooms, monsters, items_db, current_room_name):
    """Попытаться сбежать из боя."""
    if not room["monster"]:
        print("\n❌ Здесь некого бежать — монстра нет.")
        return current_room_name

    monster = monsters[room["monster"]]
    print(f"\n🏃 Вы пытаетесь сбежать от {monster['name']}...")

    # Шанс побега 50%
    if random.randint(1, 100) <= 50:
        print("✅ Побег успешен!")
        
        # Выбираем случайную доступную комнату для побега
        exits = list(room["exits"].keys())
        if exits:
            escape_direction = random.choice(exits)
            new_room_name = room["exits"][escape_direction]
            print(f"   Вы убегаете в направлении: {escape_direction}")
            return new_room_name
        else:
            print("   ❌ Но вам некуда бежать! Вы заперты.")
            return current_room_name
    else:
        print("❌ Побег не удался!")
        
        # Урон в спину тоже снижается защитой
        armor_bonus = 0
        if player["equipment"]["armor"] and player["equipment"]["armor"] in items_db:
            armor_bonus = items_db[player["equipment"]["armor"]]["defense_bonus"]
        
        total_defense = player["defense"] + armor_bonus  # НОВОЕ
        
        backstab_damage = max(1, monster["attack"] - total_defense)
        player["hp"] -= backstab_damage
        
        if total_defense > 0:
            print(f"   🛡️ Защита поглотила часть урона!")
        print(f"   💥 {monster['name']} бьёт вас в спину и наносит {backstab_damage} урона!")
        print(f"   ❤️ Ваше HP: {max(0, player['hp'])}/{player['max_hp']}")
        
        if player["hp"] <= 0:
            print("\n💀 Вы погибли...")
            return "dead"
        
        return current_room_name


def move(current_room_name, direction, rooms, monsters):
    """Переместиться в другую комнату."""
    current_room = rooms[current_room_name]
    if direction in current_room["exits"]:
        return current_room["exits"][direction]
    else:
        print(f"\n❌ Туда нельзя пройти на {direction}.")
        return current_room_name


def game_loop(player, rooms, monsters, items_db, npcs, current_room_name):
    """Основной игровой цикл."""
    look(rooms[current_room_name], monsters, npcs)

    while True:
        command = input("\n> ").strip().lower()

        if command == "look":
            look(rooms[current_room_name], monsters, npcs)
        elif command.startswith("go "):
            direction = command[3:].strip()
            current_room_name = move(current_room_name, direction, rooms, monsters)
            look(rooms[current_room_name], monsters, npcs)
        elif command.startswith("take "):
            item_name = command[5:].strip()
            take(item_name, player, rooms[current_room_name])
        elif command.startswith("use "):
            item_name = command[4:].strip()
            use_item(item_name, player)
        elif command.startswith("equip "):
            item_name = command[6:].strip()
            equip_item(item_name, player, items_db)
        elif command in ("attack", "a"):
            result = attack(player, rooms[current_room_name], monsters, items_db)
            if result == "dead":
                print("\n👋 Игра окончена.")
                break
        elif command == "flee":
            result = flee(player, rooms[current_room_name], rooms, monsters, items_db, current_room_name)
            if result == "dead":
                print("\n👋 Игра окончена.")
                break
            elif result != current_room_name:
                current_room_name = result
                look(rooms[current_room_name], monsters, npcs)
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
            items_db = create_items_db()
            npcs = create_npcs()
            current_room_name = "cave"
            game_loop(player, rooms, monsters, items_db, npcs, current_room_name)
        elif choice == "2":
            player, rooms, current_room_name = load_game()
            if player:
                monsters = create_monsters()
                items_db = create_items_db()
                npcs = create_npcs()
                game_loop(player, rooms, monsters, items_db, npcs, current_room_name)
        elif choice == "3":
            print("\n👋 До свидания!")
            break
        else:
            print("\n❌ Неверный выбор, попробуйте снова.")


if __name__ == "__main__":
    main()