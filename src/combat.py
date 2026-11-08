"""Боевая система: атака, побег, лут."""
import random

from src.utils import (
    paint,
    COLOR_RED, COLOR_GREEN, COLOR_YELLOW, COLOR_BLUE, COLOR_BOLD
)
from src.player import check_level_up, experience_to_next_level


def drop_loot(monster, player):
    """Выдать лут с монстра."""
    if "loot" not in monster:
        return

    total_gold = 0
    items_dropped = []

    for loot_entry in monster["loot"]:
        if random.randint(1, 100) <= loot_entry["chance"]:
            if loot_entry["item"] == "золото":
                player["gold"] += loot_entry["amount"]
                total_gold += loot_entry["amount"]
            else:
                for _ in range(loot_entry["amount"]):
                    player["inventory"].append(loot_entry["item"])
                    items_dropped.append(loot_entry["item"])

    if total_gold > 0 or items_dropped:
        print("\n🎁 Лут:")
        if total_gold > 0:
            print(paint(f"   💰 +{total_gold} золота", COLOR_YELLOW))
        for item in items_dropped:
            print(paint(f"   📦 +1x {item}", COLOR_GREEN))


def check_quest_progress(player, monster_key, npcs):
    """Проверить прогресс квестов при убийстве монстра."""
    for quest_id, quest_progress in player["quests"].items():
        if quest_progress["completed"]:
            continue

        quest_data = None
        for npc in npcs.values():
            if "quests" in npc and quest_id in npc["quests"]:
                quest_data = npc["quests"][quest_id]
                break

        if quest_data and quest_data["target"] == monster_key:
            quest_progress["progress"] += 1
            print(f"\n📜 Квест '{quest_data['name']}': {quest_progress['progress']}/{quest_data['count']}")

            if quest_progress["progress"] >= quest_data["count"]:
                quest_progress["completed"] = True
                print(paint("   ✅ Квест выполнен! Вернитесь к NPC за наградой.", COLOR_GREEN))


def attack(player, room, monsters, items_db, npcs):
    """Атаковать монстра в комнате."""
    if not room["monster"]:
        print("\n" + paint("❌ Здесь некого атаковать.", COLOR_RED))
        return False

    monster_key = room["monster"]
    monster = monsters[monster_key]

    weapon_bonus = 0
    if player["equipment"]["weapon"] and player["equipment"]["weapon"] in items_db:
        weapon_bonus = items_db[player["equipment"]["weapon"]]["attack_bonus"]

    total_attack = player["attack"] + weapon_bonus

    is_crit = random.randint(1, 100) <= 15
    base_damage = random.randint(total_attack - 2, total_attack + 2)

    if is_crit:
        player_damage = base_damage * 2
        print("\n" + paint(f"💥 КРИТИЧЕСКИЙ УДАР! Вы нанесли {player_damage} урона!", COLOR_BOLD + COLOR_RED))
    else:
        player_damage = max(1, base_damage)
        print(f"\n⚔️ Вы ударили {monster['name']} и нанесли {player_damage} урона.")

    monster["hp"] -= player_damage
    print(paint(f"   {monster['emoji']} HP монстра: {max(0, monster['hp'])}/{monster['max_hp']}", COLOR_RED))

    if monster["hp"] <= 0:
        print("\n" + paint(f"🎉 Вы победили {monster['name']}!", COLOR_BOLD + COLOR_GREEN))

        if monster.get("is_final"):
            print("\n" + paint("👑" * 15, COLOR_YELLOW))
            print(paint("   ФИНАЛЬНЫЙ БОСС ПОВЕРЖЕН!", COLOR_BOLD + COLOR_YELLOW))
            print(paint("   Король Скелетов пал. Подземелье освобождено от зла!", COLOR_YELLOW))
            print(paint("👑" * 15, COLOR_YELLOW))
            player["victory"] = True
        elif monster.get("is_boss"):
            print("\n" + paint("🏆" * 15, COLOR_YELLOW))
            print(paint("   МИНИ-БОСС ПОВЕРЖЕН!", COLOR_BOLD + COLOR_YELLOW))
            print(paint("   Подземелье содрогнулось от вашего удара!", COLOR_YELLOW))
            print(paint("🏆" * 15, COLOR_YELLOW))

        player["experience"] += monster["experience"]
        player["kills"] += 1
        print(paint(f"   ⭐ Получено опыта: {monster['experience']}", COLOR_YELLOW))
        print(f"   ⭐ Всего опыта: {player['experience']}/"
              f"{experience_to_next_level(player['level'])}")

        check_quest_progress(player, monster_key, npcs)

        drop_loot(monster, player)

        room["monster"] = None
        check_level_up(player)
        return True

    armor_bonus = 0
    if player["equipment"]["armor"] and player["equipment"]["armor"] in items_db:
        armor_bonus = items_db[player["equipment"]["armor"]]["defense_bonus"]

    total_defense = player["defense"] + armor_bonus

    raw_monster_damage = random.randint(monster["attack"] - 1, monster["attack"] + 1)
    monster_damage = max(1, raw_monster_damage - total_defense)

    player["hp"] -= monster_damage

    if total_defense > 0:
        absorbed = raw_monster_damage - monster_damage
        if absorbed > 0:
            print("\n" + paint(f"🛡️ Защита поглотила {absorbed} урона!", COLOR_BLUE))
    print(paint(f"🩸 {monster['name']} атакует вас и наносит {monster_damage} урона.", COLOR_RED))
    print(paint(f"   ❤️ Ваше HP: {max(0, player['hp'])}/{player['max_hp']}", COLOR_RED))

    if player["hp"] <= 0:
        return "dead"

    return False


def flee(player, room, rooms, monsters, items_db, current_room_name):
    """Попытаться сбежать из боя."""
    if not room["monster"]:
        print("\n" + paint("❌ Здесь некого бежать — монстра нет.", COLOR_RED))
        return current_room_name

    monster = monsters[room["monster"]]
    print(f"\n🏃 Вы пытаетесь сбежать от {monster['name']}...")

    if random.randint(1, 100) <= 50:
        print(paint("✅ Побег успешен!", COLOR_GREEN))

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
        print(paint("❌ Побег не удался!", COLOR_RED))

        armor_bonus = 0
        if player["equipment"]["armor"] and player["equipment"]["armor"] in items_db:
            armor_bonus = items_db[player["equipment"]["armor"]]["defense_bonus"]

        total_defense = player["defense"] + armor_bonus

        backstab_damage = max(1, monster["attack"] - total_defense)
        player["hp"] -= backstab_damage

        if total_defense > 0:
            print(paint("   🛡️ Защита поглотила часть урона!", COLOR_BLUE))
        print(paint(f"   💥 {monster['name']} бьёт вас в спину и наносит {backstab_damage} урона!", COLOR_RED))
        print(paint(f"   ❤️ Ваше HP: {max(0, player['hp'])}/{player['max_hp']}", COLOR_RED))

        if player["hp"] <= 0:
            return "dead"

        return current_room_name