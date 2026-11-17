"""Утилиты: цвета, сложность, таблица рекордов."""
import json
import os


# ANSI-цвета для терминала
COLOR_RED = "\033[91m"
COLOR_GREEN = "\033[92m"
COLOR_YELLOW = "\033[93m"
COLOR_BLUE = "\033[94m"
COLOR_MAGENTA = "\033[95m"
COLOR_CYAN = "\033[96m"
COLOR_BOLD = "\033[1m"
COLOR_RESET = "\033[0m"


def paint(text, color):
    """Обернуть текст в ANSI-цвет для терминала."""
    return color + text + COLOR_RESET


def clear_screen():
    """Очистить экран."""
    os.system('cls' if os.name == 'nt' else 'clear')
    print("🧹 Экран очищен.")


def difficulty_name(difficulty):
    """Красивое название сложности."""
    names = {
        "easy": "🟢 Легко",
        "normal": "🟡 Нормально",
        "nightmare": "🔴 Кошмар"
    }
    return names.get(difficulty, "🟡 Нормально")


def choose_difficulty():
    """Выбрать сложность игры."""
    print("\n" + paint("⚙️ === ВЫБОР СЛОЖНОСТИ ===", COLOR_BOLD + COLOR_CYAN))
    print(paint("  1. 🟢 Легко — монстры слабее, больше золота", COLOR_GREEN))
    print("  2. 🟡 Нормально — сбалансированная игра")
    print(paint("  3. 🔴 Кошмар — монстры сильнее, больше опыта и золота", COLOR_RED))
    choice = input("\nВаш выбор (1/2/3): ").strip()
    if choice == "1":
        return "easy"
    elif choice == "3":
        return "nightmare"
    return "normal"


def calculate_score(player):
    """Посчитать очки забега для таблицы рекордов."""
    score = player["kills"] * 10 + player["gold"] + player["level"] * 50
    if player["victory"]:
        score += 500
    return score


def save_highscore(player):
    """Сохранить забег в таблицу рекордов (топ-10)."""
    os.makedirs("saves", exist_ok=True)
    path = "saves/highscores.json"

    entries = []
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            entries = json.load(f)

    entries.append({
        "name": player["name"],
        "level": player["level"],
        "kills": player["kills"],
        "gold": player["gold"],
        "victory": player["victory"],
        "difficulty": player.get("difficulty", "normal"),
        "score": calculate_score(player)
    })

    entries.sort(key=lambda entry: entry["score"], reverse=True)
    entries = entries[:10]

    with open(path, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)


def show_highscores():
    """Показать таблицу рекордов."""
    path = "saves/highscores.json"
    print("\n" + paint("🏆 === ТАБЛИЦА РЕКОРДОВ ===", COLOR_BOLD + COLOR_YELLOW))

    entries = []
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            entries = json.load(f)

    if not entries:
        print("  Таблица пуста. Станьте первым героем!")
        return

    medals = ["🥇", "🥈", "🥉"]
    for i, entry in enumerate(entries):
        if i < 3:
            place = medals[i]
        else:
            place = f"{i + 1}."
        victory_mark = " 👑" if entry["victory"] else ""
        score_str = paint(f"{entry['score']} очков", COLOR_YELLOW)
        print(f"  {place} {entry['name']} — {score_str}{victory_mark}")
        diff = difficulty_name(entry.get("difficulty", "normal"))
        print(f"     Уровень {entry['level']}, убийств: {entry['kills']}, "
              f"золото: {entry['gold']}, сложность: {diff}")

def create_achievements():
    """База данных достижений."""
    return {
        "first_blood": {"emoji": "🩸", "name": "Первая кровь", "description": "Убейте первого монстра"},
        "monster_slayer": {"emoji": "⚔️", "name": "Охотник на монстров", "description": "Убейте 15 монстров"},
        "rich": {"emoji": "💰", "name": "Богач", "description": "Накопите 200 золота одновременно"},
        "veteran": {"emoji": "🎖️", "name": "Ветеран", "description": "Достигните 5 уровня"},
        "victor": {"emoji": "👑", "name": "Победитель подземелья", "description": "Повергните Короля Скелетов"},
        "nightmare_victor": {"emoji": "🔥", "name": "Победитель Кошмара", "description": "Пройдите игру на сложности 'Кошмар'"},
        "secret_finder": {"emoji": "🕵️", "name": "Искатель тайн", "description": "Найдите 2 секретных прохода"},
        "trap_master": {"emoji": "🛠️", "name": "Мастер ловушек", "description": "Обезвредьте 2 ловушки"},
        "quest_hero": {"emoji": "📜", "name": "Герой квестов", "description": "Выполните 2 квеста"},
        "collector": {"emoji": "🎒", "name": "Коллекционер", "description": "Держите 8 предметов в инвентаре одновременно"},
    }


def check_achievements(player):
    """Проверить достижения и показать вновь открытые."""
    achievements = create_achievements()
    rewarded_quests = sum(1 for q in player["quests"].values() if q.get("rewarded"))

    conditions = {
        "first_blood": player["kills"] >= 1,
        "monster_slayer": player["kills"] >= 15,
        "rich": player["gold"] >= 200,
        "veteran": player["level"] >= 5,
        "victor": player["victory"],
        "nightmare_victor": player["victory"] and player.get("difficulty") == "nightmare",
        "secret_finder": player.get("secrets_found", 0) >= 2,
        "trap_master": player.get("traps_disarmed", 0) >= 2,
        "quest_hero": rewarded_quests >= 2,
        "collector": len(player["inventory"]) >= 8,
    }

    for ach_id, unlocked in conditions.items():
        if unlocked and ach_id not in player["achievements"]:
            player["achievements"].append(ach_id)
            ach = achievements[ach_id]
            print("\n" + paint("🏅" * 15, COLOR_YELLOW))
            print(paint(f"   ДОСТИЖЕНИЕ ОТКРЫТО: {ach['emoji']} {ach['name']}!", COLOR_BOLD + COLOR_YELLOW))
            print(paint(f"   {ach['description']}", COLOR_YELLOW))
            print(paint("🏅" * 15, COLOR_YELLOW))


def show_achievements(player):
    """Показать все достижения."""
    achievements = create_achievements()
    print("\n" + paint("🏅 === ДОСТИЖЕНИЯ ===", COLOR_BOLD + COLOR_YELLOW))
    for ach_id, ach in achievements.items():
        if ach_id in player["achievements"]:
            print(paint(f"  ✅ {ach['emoji']} {ach['name']} — {ach['description']}", COLOR_GREEN))
        else:
            print(f"  🔒 {ach['emoji']} {ach['name']} — {ach['description']}")
    print(f"\n  Открыто: {len(player['achievements'])}/{len(achievements)}")
