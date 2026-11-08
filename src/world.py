"""Мир игры: комнаты, монстры, NPC, магазин, сохранения."""
import json
import os
import random

from src.utils import (
    paint,
    COLOR_RED, COLOR_GREEN, COLOR_YELLOW, COLOR_BLUE,
    COLOR_MAGENTA, COLOR_CYAN, COLOR_BOLD
)
from src.player import check_level_up


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
        "серебряный кинжал": {
            "type": "weapon",
            "attack_bonus": 7,
            "description": "Острый кинжал из чистого серебра",
            "price": 80,
            "sell_price": 35
        },
        "дубина тролля": {
            "type": "weapon",
            "attack_bonus": 8,
            "description": "Тяжёлая дубина из цельного ствола дерева",
            "price": 100,
            "sell_price": 45
        },
        "меч короля скелетов": {
            "type": "weapon",
            "attack_bonus": 10,
            "description": "Проклятый клинок бывшего властителя подземелья",
            "sell_price": 60
        },
        "кожаная броня": {
            "type": "armor",
            "defense_bonus": 2,
            "description": "Простая кожаная куртка",
            "price": 30,
            "sell_price": 12
        },
        "щит стражника": {
            "type": "armor",
            "defense_bonus": 4,
            "description": "Прочный щит с гербом",
            "price": 60,
            "sell_price": 25
        },
        "кольцо защиты": {
            "type": "armor",
            "defense_bonus": 3,
            "description": "Магическое кольцо, усиливающее защиту",
            "price": 50,
            "sell_price": 20
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
        },
        "железный ключ": {
            "type": "key",
            "description": "Старый железный ключ",
            "sell_price": 10
        },
        "золотая корона": {
            "type": "treasure",
            "description": "Древняя корона, усыпанная камнями",
            "sell_price": 100
        },
        "древний амулет": {
            "type": "treasure",
            "description": "Таинственный амулет с мерцающим камнем",
            "sell_price": 50
        }
    }
    return items


def create_monsters(difficulty="normal"):
    """Создать шаблоны монстров с учётом сложности."""
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
                {"item": "зелье здоровья", "amount": 1, "chance": 40}
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
                {"item": "кожаная броня", "amount": 1, "chance": 15},
                {"item": "зелье здоровья", "amount": 1, "chance": 40}
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
                {"item": "зелье здоровья", "amount": 1, "chance": 40},
                {"item": "ржавый меч", "amount": 1, "chance": 20}
            ]
        },
        "troll": {
            "name": "Пещерный тролль",
            "hp": 80,
            "max_hp": 80,
            "attack": 14,
            "experience": 80,
            "emoji": "🧌",
            "is_boss": True,
            "loot": [
                {"item": "золото", "amount": 50, "chance": 100},
                {"item": "зелье здоровья", "amount": 1, "chance": 60},
                {"item": "дубина тролля", "amount": 1, "chance": 40}
            ]
        },
        "skeleton_king": {
            "name": "Король Скелетов",
            "hp": 120,
            "max_hp": 120,
            "attack": 18,
            "experience": 150,
            "emoji": "☠️",
            "is_boss": True,
            "is_final": True,
            "loot": [
                {"item": "золото", "amount": 100, "chance": 100},
                {"item": "зелье здоровья", "amount": 2, "chance": 100},
                {"item": "меч короля скелетов", "amount": 1, "chance": 50}
            ]
        }
    }

    # Множители сложности
    if difficulty == "easy":
        hp_mult, atk_mult, exp_mult, gold_mult = 0.7, 0.7, 1.0, 1.2
    elif difficulty == "nightmare":
        hp_mult, atk_mult, exp_mult, gold_mult = 1.5, 1.4, 1.3, 1.5
    else:
        return monsters

    for monster in monsters.values():
        monster["hp"] = max(1, int(monster["hp"] * hp_mult))
        monster["max_hp"] = monster["hp"]
        monster["attack"] = max(1, int(monster["attack"] * atk_mult))
        monster["experience"] = max(1, int(monster["experience"] * exp_mult))
        for loot_entry in monster["loot"]:
            if loot_entry["item"] == "золото":
                loot_entry["amount"] = max(1, int(loot_entry["amount"] * gold_mult))

    return monsters


def create_rooms():
    """Создать комнаты подземелья."""
    rooms = {
        "cave": {
            "name": "Тёмная пещера",
            "description": "Вы стоите в тёмной сырой пещере. Со стен капает вода.",
            "exits": {"north": "tunnel"},
            "items": ["факел"],
            "monster": None,
            "npc": None,
            "secret_exit": {"east": "secret_chamber"}
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
            "exits": {"west": "tunnel", "north": "bone_crypt", "south": "dark_lake"},
            "items": [],
            "monster": "slime",
            "npc": None
        },
        "goblin_camp": {
            "name": "Лагерь гоблинов",
            "description": "Грязная стоянка с остатками еды и сломанным оружием. Воняет.",
            "exits": {"east": "tunnel", "south": "armory"},
            "items": ["ржавый нож"],
            "monster": "goblin",
            "npc": None
        },
        "bone_crypt": {
            "name": "Костяная крипта",
            "description": "Холодное помещение, усыпанное костями. В центре стоит саркофаг.",
            "exits": {"south": "spider_nest", "north": "throne_room"},
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
        },
        "dark_lake": {
            "name": "Тёмное озеро",
            "description": "Подземное озеро с чёрной водой. От воды веет холодом и опасностью.",
            "exits": {"north": "spider_nest", "east": "troll_lair"},
            "items": ["железный ключ"],
            "monster": None,
            "npc": None
        },
        "armory": {
            "name": "Оружейная",
            "description": "Заброшенная оружейная. На стенах висят ржавые доспехи и сломанное оружие.",
            "exits": {"north": "goblin_camp"},
            "items": ["щит стражника"],
            "monster": None,
            "npc": None,
            "secret_exit": {"east": "treasury"}
        },
        "throne_room": {
            "name": "Тронный зал",
            "description": "Величественный зал с троном из костей. Здесь пахнет древней магией.",
            "exits": {"south": "bone_crypt"},
            "items": ["золотая корона"],
            "monster": "skeleton_king",
            "npc": None,
            "locked": True
        },
        "secret_chamber": {
            "name": "Тайная комната",
            "description": "Маленькая скрытая комната, освещённая магическим светом. Здесь пахнет древними заклинаниями.",
            "exits": {"west": "cave"},
            "items": ["кольцо защиты", "зелье здоровья"],
            "monster": None,
            "npc": None
        },
        "treasury": {
            "name": "Сокровищница",
            "description": "Комната, набитая сундуками с сокровищами. Золото блестит в свете факелов.",
            "exits": {"west": "armory"},
            "items": ["серебряный кинжал", "золотая корона"],
            "monster": None,
            "npc": None
        },
        "troll_lair": {
            "name": "Логово тролля",
            "description": "Огромная пещера, заваленная костями и валунами. В центре храпит огромное существо.",
            "exits": {"west": "dark_lake"},
            "items": [],
            "monster": "troll",
            "npc": None
        }
    }
    return rooms


def create_npcs():
    """Создать NPC с квестами."""
    npcs = {
        "merchant": {
            "name": "Торговец Гаррет",
            "emoji": "🧙",
            "dialogue": "Приветствую, путник! Я покупаю и продаю товары.",
            "shop": ["зелье здоровья", "ржавый нож", "кожаная броня", "ржавый меч", "щит стражника"],
            "quests": {
                "rat_hunter": {
                    "name": "Охотник на крыс",
                    "description": "Крысы в тоннеле мешают мне спать. Убей 3 гигантских крыс.",
                    "target": "rat",
                    "count": 3,
                    "reward_gold": 50,
                    "reward_exp": 30,
                    "dialogue_accept": "Отлично! Крысы находятся в узком тоннеле на юге отсюда.",
                    "dialogue_complete": "Спасибо! Теперь я могу спокойно спать. Вот твоя награда."
                }
            }
        }
    }
    return npcs


def save_game(player, rooms, current_room_name):
    """Сохранить игру в файл."""
    os.makedirs("saves", exist_ok=True)
    save_data = {
        "player": player,
        "rooms": rooms,
        "current_room": current_room_name,
        "save_version": 2
    }
    with open("saves/savegame.json", "w", encoding="utf-8") as f:
        json.dump(save_data, f, ensure_ascii=False, indent=2)
    print("\n" + paint("💾 Игра сохранена!", COLOR_GREEN))


def load_game():
    """Загрузить игру из файла."""
    if not os.path.exists("saves/savegame.json"):
        print("\n" + paint("❌ Сохранение не найдено!", COLOR_RED))
        return None, None, None
    with open("saves/savegame.json", "r", encoding="utf-8") as f:
        save_data = json.load(f)

    # Миграция старых сейвов (игрок)
    if "gold" not in save_data["player"]:
        save_data["player"]["gold"] = 0
    if "equipment" not in save_data["player"]:
        save_data["player"]["equipment"] = {"weapon": None, "armor": None}
    if "defense" not in save_data["player"]:
        save_data["player"]["defense"] = 0
    if "kills" not in save_data["player"]:
        save_data["player"]["kills"] = 0
    if "victory" not in save_data["player"]:
        save_data["player"]["victory"] = False
    if "difficulty" not in save_data["player"]:
        save_data["player"]["difficulty"] = "normal"
    if "quests" not in save_data["player"]:
        save_data["player"]["quests"] = {}

    # Миграция комнат
    for room_key in save_data["rooms"]:
        if "npc" not in save_data["rooms"][room_key]:
            save_data["rooms"][room_key]["npc"] = None
        if "locked" not in save_data["rooms"][room_key]:
            save_data["rooms"][room_key]["locked"] = False
        if "secret_exit" not in save_data["rooms"][room_key]:
            save_data["rooms"][room_key]["secret_exit"] = None

    # Добавляем новые комнаты и новые выходы из старых комнат
    new_rooms = create_rooms()
    for room_key, room_data in new_rooms.items():
        if room_key not in save_data["rooms"]:
            save_data["rooms"][room_key] = room_data
        else:
            for direction, target in room_data["exits"].items():
                if direction not in save_data["rooms"][room_key]["exits"]:
                    save_data["rooms"][room_key]["exits"][direction] = target

    # Миграция на версию 2: финальный босс в Тронном зале (только для старых сейвов)
    if save_data.get("save_version", 1) < 2:
        throne = save_data["rooms"].get("throne_room")
        if throne is not None and throne.get("monster") is None:
            throne["monster"] = "skeleton_king"

    print("\n" + paint("📂 Игра загружена!", COLOR_GREEN))
    return save_data["player"], save_data["rooms"], save_data["current_room"]


def look(room, monsters, npcs, player):
    """Осмотреться в комнате."""
    print(f"\n📍 === {paint(room['name'], COLOR_BOLD + COLOR_BLUE)} ===")
    print(room["description"])

    if room.get("locked"):
        print("\n" + paint("🔒 Эта комната заперта! Нужен ключ.", COLOR_RED))

    if room["monster"]:
        monster = monsters[room["monster"]]
        if monster.get("is_final"):
            line = (f"☠️ ФИНАЛЬНЫЙ БОСС: {monster['emoji']} {monster['name']}!! "
                    f"(HP: {monster['hp']}/{monster['max_hp']})")
            print("\n" + paint(line, COLOR_BOLD + COLOR_RED))
            print(paint("   ☠️ Сильнейший враг подземелья! Запаситесь зельями!", COLOR_RED))
        elif monster.get("is_boss"):
            line = (f"⚠️ МИНИ-БОСС: {monster['emoji']} {monster['name']}! "
                    f"(HP: {monster['hp']}/{monster['max_hp']})")
            print("\n" + paint(line, COLOR_BOLD + COLOR_RED))
            print(paint("   ☠️ Это очень опасный противник! Подготовьтесь перед боем.", COLOR_RED))
        else:
            line = (f"{monster['emoji']} Здесь находится {monster['name']}! "
                    f"(HP: {monster['hp']}/{monster['max_hp']})")
            print("\n" + paint(line, COLOR_RED))

    if room.get("npc"):
        npc = npcs[room["npc"]]
        print("\n" + paint(f"{npc['emoji']} Здесь находится {npc['name']}.", COLOR_MAGENTA))
        print(paint(f"   💬 \"{npc['dialogue']}\"", COLOR_MAGENTA))
        print(f"   💡 Используйте 'talk {room['npc']}' для диалога.")

    if room["items"]:
        items_str = ", ".join(room["items"])
        print("\n" + paint(f"🎒 Предметы на полу: {items_str}", COLOR_GREEN))

    if room["exits"]:
        exits_str = ", ".join(room["exits"].keys())
        print(paint(f"🚪 Выходы: {exits_str}", COLOR_CYAN))

    if room.get("secret_exit") and not room.get("secret_found"):
        print("\n💡 Вы чувствуете, что здесь есть что-то скрытое... Попробуйте 'search'.")

    hp_percent = (player["hp"] / player["max_hp"]) * 100
    if hp_percent <= 30:
        print("\n" + paint(f"⚠️ ВНИМАНИЕ: Низкий уровень HP ({player['hp']}/{player['max_hp']})!", COLOR_BOLD + COLOR_RED))
        print(paint("   Используйте 'use зелье здоровья' или 'rest' для восстановления.", COLOR_RED))


def search_room(room, player):
    """Искать секреты в комнате."""
    print("\n🔍 Вы внимательно осматриваете комнату...")

    if room.get("secret_exit") and not room.get("secret_found"):
        room["secret_found"] = True
        secret_dir = list(room["secret_exit"].keys())[0]
        secret_room = room["secret_exit"][secret_dir]

        room["exits"][secret_dir] = secret_room

        print("\n" + paint(f"✨ Вы обнаружили секретный проход на {secret_dir}!", COLOR_BOLD + COLOR_MAGENTA))
        print(paint(f"   🚪 Новый выход добавлен: {secret_dir}", COLOR_MAGENTA))
        return True
    else:
        messages = [
            "Вы ничего не нашли.",
            "Только пыль и камни.",
            "Ничего подозрительного.",
            "Стены кажутся обычными."
        ]
        print(f"   🌫️ {random.choice(messages)}")
        return False


def take(item_name, player, room):
    """Подобрать предмет."""
    if item_name in room["items"]:
        room["items"].remove(item_name)
        player["inventory"].append(item_name)
        print("\n" + paint(f"✅ Вы подобрали: {item_name}", COLOR_GREEN))
    else:
        print("\n" + paint(f"❌ Здесь нет предмета '{item_name}'.", COLOR_RED))


def drop_item(item_name, player, room):
    """Выбросить предмет из инвентаря."""
    if item_name not in player["inventory"]:
        print("\n" + paint(f"❌ У вас нет предмета '{item_name}'.", COLOR_RED))
        return

    player["inventory"].remove(item_name)
    room["items"].append(item_name)
    print(f"\n🗑️ Вы выбросили: {item_name}")


def trigger_random_event(player):
    """Случайное событие при переходе (15% шанс)."""
    if random.randint(1, 100) > 15:
        return

    event_roll = random.randint(1, 100)

    print("\n" + paint("✨" * 20, COLOR_MAGENTA))

    if event_roll <= 20:
        gold_found = random.randint(8, 20)
        player["gold"] += gold_found
        print(paint(f"💰 Вы нашли {gold_found} золота в трещине стены!", COLOR_YELLOW))

    elif event_roll <= 35:
        trap_damage = random.randint(5, 12)
        player["hp"] -= trap_damage
        print(paint(f"⚠️ Вы наступили на скрытую ловушку и получили {trap_damage} урона!", COLOR_RED))
        print(paint(f"   ❤️ HP: {max(0, player['hp'])}/{player['max_hp']}", COLOR_RED))

        if player["hp"] <= 0:
            print("\n" + paint("💀 Вы погибли от ловушки...", COLOR_BOLD + COLOR_RED))
            return "dead"

    elif event_roll <= 50:
        player["inventory"].append("зелье здоровья")
        print(paint("🧪 Вы обнаружили тайник с зельем здоровья!", COLOR_GREEN))

    elif event_roll <= 65:
        heal_amount = random.randint(15, 30)
        old_hp = player["hp"]
        player["hp"] = min(player["hp"] + heal_amount, player["max_hp"])
        healed = player["hp"] - old_hp
        print(paint(f"✨ Таинственная сила исцелила вас на {healed} HP!", COLOR_GREEN))
        print(paint(f"   ❤️ HP: {player['hp']}/{player['max_hp']}", COLOR_GREEN))

    elif event_roll <= 75:
        items_found = ["кость", "паутина", "древний амулет"]
        found_item = random.choice(items_found)
        player["inventory"].append(found_item)
        print(paint(f"📦 Вы нашли {found_item} среди обломков!", COLOR_GREEN))

    elif event_roll <= 85:
        messages = [
            "👻 Перед вами появился призрак древнего воина...",
            "👻 Тень мелькнула в углу комнаты...",
            "👻 Вы услышали шёпот из прошлого..."
        ]
        print(paint(random.choice(messages), COLOR_MAGENTA))
        print("   ...но он исчез так же быстро, как появился.")

    elif event_roll <= 95:
        fall_damage = random.randint(2, 5)
        player["hp"] -= fall_damage
        print(paint(f"🕳️ Вы провалились в яму и получили {fall_damage} урона!", COLOR_RED))
        print(paint(f"   ❤️ HP: {max(0, player['hp'])}/{player['max_hp']}", COLOR_RED))

        if player["hp"] <= 0:
            print("\n" + paint("💀 Вы погибли от падения...", COLOR_BOLD + COLOR_RED))
            return "dead"

    else:
        messages = [
            "Вы слышите странный шум вдалеке...",
            "Капля воды падает вам на голову.",
            "Вы чувствуете чей-то взгляд на спине...",
            "Стены словно шепчут что-то...",
            "Летучая мышь пролетела мимо!",
            "Старая свеча внезапно зажглась в нише.",
            "🌫️ Туман сгущается вокруг вас..."
        ]
        print(paint(f"🌫️ {random.choice(messages)}", COLOR_CYAN))

    print(paint("✨" * 20, COLOR_MAGENTA))
    return None


def move(current_room_name, direction, rooms, monsters, player):
    """Переместиться в другую комнату."""
    current_room = rooms[current_room_name]
    if direction in current_room["exits"]:
        new_room_name = current_room["exits"][direction]
        new_room = rooms[new_room_name]

        if new_room.get("locked"):
            if "железный ключ" in player["inventory"]:
                print("\n" + paint("🔑 Вы использовали железный ключ и открыли дверь!", COLOR_GREEN))
                player["inventory"].remove("железный ключ")
                new_room["locked"] = False
            else:
                print("\n" + paint("🔒 Дверь заперта! Нужен железный ключ.", COLOR_RED))
                return current_room_name

        event_result = trigger_random_event(player)
        if event_result == "dead":
            return "dead"

        return new_room_name
    else:
        print("\n" + paint(f"❌ Туда нельзя пройти на {direction}.", COLOR_RED))
        return current_room_name


def talk_to_npc(npc_key, player, npcs):
    """Поговорить с NPC."""
    if npc_key not in npcs:
        print("\n" + paint("❌ NPC не найден.", COLOR_RED))
        return

    npc = npcs[npc_key]
    print("\n" + paint(f"{npc['emoji']} {npc['name']}: \"{npc['dialogue']}\"", COLOR_MAGENTA))

    if "quests" in npc:
        for quest_id, quest_data in npc["quests"].items():
            if quest_id not in player["quests"]:
                print("\n" + paint(f"📜 Доступен квест: {quest_data['name']}", COLOR_BOLD + COLOR_MAGENTA))
                print(f"   {quest_data['description']}")
                print(paint(f"   Награда: {quest_data['reward_gold']} золота, {quest_data['reward_exp']} опыта", COLOR_YELLOW))
                accept = input("\nПринять квест? (да/нет): ").strip().lower()
                if accept == "да":
                    player["quests"][quest_id] = {
                        "progress": 0,
                        "completed": False
                    }
                    print("\n" + paint(f"✅ Квест принят! {quest_data['dialogue_accept']}", COLOR_GREEN))
                else:
                    print("\n❌ Квест отклонён.")
            else:
                quest_progress = player["quests"][quest_id]
                if quest_progress["completed"]:
                    print("\n" + paint(f"✅ Квест '{quest_data['name']}' уже выполнен!", COLOR_GREEN))
                    print(f"   {quest_data['dialogue_complete']}")
                    if not quest_progress.get("rewarded"):
                        player["gold"] += quest_data["reward_gold"]
                        player["experience"] += quest_data["reward_exp"]
                        quest_progress["rewarded"] = True
                        print(paint(f"   💰 +{quest_data['reward_gold']} золота", COLOR_YELLOW))
                        print(paint(f"   ⭐ +{quest_data['reward_exp']} опыта", COLOR_YELLOW))
                        check_level_up(player)
                else:
                    print(f"\n📜 Квест в процессе: {quest_data['name']}")
                    print(f"   Прогресс: {quest_progress['progress']}/{quest_data['count']}")


def show_quests(player, npcs):
    """Показать активные квесты."""
    print("\n" + paint("📜 === АКТИВНЫЕ КВЕСТЫ ===", COLOR_BOLD + COLOR_MAGENTA))

    if not player["quests"]:
        print("  Нет активных квестов.")
        print("  Поговорите с NPC, чтобы получить задания.")
        return

    for quest_id, quest_progress in player["quests"].items():
        quest_data = None
        for npc in npcs.values():
            if "quests" in npc and quest_id in npc["quests"]:
                quest_data = npc["quests"][quest_id]
                break

        if quest_data:
            status = "✅ ВЫПОЛНЕН" if quest_progress["completed"] else "⏳ В ПРОЦЕССЕ"
            print(f"\n  {status} — {quest_data['name']}")
            print(f"  {quest_data['description']}")
            print(f"  Прогресс: {quest_progress['progress']}/{quest_data['count']}")
            if quest_progress["completed"] and not quest_progress.get("rewarded"):
                print(paint(f"  💡 Вернитесь к NPC за наградой!", COLOR_YELLOW))


def show_shop(npc, items_db, player):
    """Показать магазин торговца."""
    print("\n" + paint(f"🏪 === МАГАЗИН {npc['name'].upper()} ===", COLOR_BOLD + COLOR_YELLOW))
    print(paint(f"💰 Ваше золото: {player['gold']}", COLOR_YELLOW))

    print("\n  📦 ПОКУПКА:")
    for item_name in npc["shop"]:
        if item_name in items_db:
            item = items_db[item_name]
            price = item.get("price", 0)
            print(f"  • {item_name} — {price} золота")
            if item["type"] == "weapon":
                print(paint(f"    ⚔️ +{item['attack_bonus']} к атаке", COLOR_YELLOW))
            elif item["type"] == "armor":
                print(paint(f"    🛡️ +{item['defense_bonus']} к защите", COLOR_BLUE))
            elif item["type"] == "consumable":
                print(paint(f"    💚 Восстанавливает {item['heal_amount']} HP", COLOR_GREEN))

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
        print("\n" + paint(f"❌ Торговец не продаёт '{item_name}'.", COLOR_RED))
        return

    if item_name not in items_db:
        print(f"\n❌ Предмет '{item_name}' не найден в базе.")
        return

    item = items_db[item_name]
    price = item.get("price", 0)

    if player["gold"] < price:
        print("\n" + paint(f"❌ Недостаточно золота! Нужно {price}, у вас {player['gold']}.", COLOR_RED))
        return

    player["gold"] -= price
    player["inventory"].append(item_name)
    print("\n" + paint(f"✅ Вы купили {item_name} за {price} золота!", COLOR_GREEN))
    print(paint(f"   💰 Осталось золота: {player['gold']}", COLOR_YELLOW))


def sell_item(item_name, player, npc, items_db):
    """Продать предмет торговцу."""
    if not player["inventory"]:
        print("\n" + paint("❌ Ваш инвентарь пуст.", COLOR_RED))
        return

    if item_name not in player["inventory"]:
        print("\n" + paint(f"❌ У вас нет предмета '{item_name}'.", COLOR_RED))
        return

    if item_name not in items_db or "sell_price" not in items_db[item_name]:
        print(f"\n❌ Торговец не покупает '{item_name}'.")
        return

    sell_price = items_db[item_name]["sell_price"]
    player["inventory"].remove(item_name)
    player["gold"] += sell_price

    print("\n" + paint(f"✅ Вы продали {item_name} за {sell_price} золота!", COLOR_GREEN))
    print(paint(f"   💰 Теперь у вас: {player['gold']} золота", COLOR_YELLOW))