"""Первые тесты для игры 'Подземелье'."""
import unittest

from src.player import experience_to_next_level, check_level_up, create_player
from src.utils import calculate_score, difficulty_name


class TestExperience(unittest.TestCase):
    """Тесты формулы опыта."""

    def test_level_1(self):
        """Для 1 уровня нужно 20 опыта."""
        self.assertEqual(experience_to_next_level(1), 20)

    def test_level_5(self):
        """Для 5 уровня нужно 100 опыта."""
        self.assertEqual(experience_to_next_level(5), 100)

    def test_level_10(self):
        """Для 10 уровня нужно 200 опыта."""
        self.assertEqual(experience_to_next_level(10), 200)


class TestCalculateScore(unittest.TestCase):
    """Тесты подсчёта очков для таблицы рекордов."""

    def test_basic_score(self):
        """Базовый подсчёт: убийства*10 + золото + уровень*50."""
        player = {
            "kills": 5,
            "gold": 100,
            "level": 2,
            "victory": False
        }
        # 5*10 + 100 + 2*50 = 50 + 100 + 100 = 250
        self.assertEqual(calculate_score(player), 250)

    def test_victory_bonus(self):
        """Победа добавляет 500 очков."""
        player = {
            "kills": 10,
            "gold": 200,
            "level": 3,
            "victory": True
        }
        # 10*10 + 200 + 3*50 + 500 = 100 + 200 + 150 + 500 = 950
        self.assertEqual(calculate_score(player), 950)

    def test_zero_stats(self):
        """Нулевые характеристики дают 50 очков за 1 уровень."""
        player = {
            "kills": 0,
            "gold": 0,
            "level": 1,
            "victory": False
        }
        # 0 + 0 + 1*50 = 50
        self.assertEqual(calculate_score(player), 50)


class TestCheckLevelUp(unittest.TestCase):
    """Тесты повышения уровня."""

    def test_no_level_up(self):
        """Не хватает опыта — уровень не повышается."""
        player = {
            "level": 1,
            "experience": 10,
            "max_hp": 100,
            "hp": 80,
            "attack": 10,
            "defense": 0
        }
        result = check_level_up(player)
        self.assertFalse(result)
        self.assertEqual(player["level"], 1)

    def test_single_level_up(self):
        """Хватает опыта на один уровень."""
        player = {
            "level": 1,
            "experience": 25,
            "max_hp": 100,
            "hp": 80,
            "attack": 10,
            "defense": 0
        }
        result = check_level_up(player)
        self.assertTrue(result)
        self.assertEqual(player["level"], 2)
        self.assertEqual(player["max_hp"], 120)
        self.assertEqual(player["hp"], 120)  # HP полностью восстановлено
        self.assertEqual(player["attack"], 13)
        self.assertEqual(player["defense"], 1)
        self.assertEqual(player["experience"], 5)  # 25 - 20 = 5

    def test_multiple_level_ups(self):
        """Хватает опыта на несколько уровней сразу."""
        player = {
            "level": 1,
            "experience": 100,
            "max_hp": 100,
            "hp": 50,
            "attack": 10,
            "defense": 0
        }
        result = check_level_up(player)
        self.assertTrue(result)
        # Уровень 1→2: нужно 20, остаётся 80
        # Уровень 2→3: нужно 40, остаётся 40
        # Уровень 3→4: нужно 60, не хватает → стоп на 3
        self.assertEqual(player["level"], 3)
        self.assertEqual(player["experience"], 40)
        self.assertEqual(player["max_hp"], 140)
        self.assertEqual(player["attack"], 16)
        self.assertEqual(player["defense"], 2)


class TestDifficultyName(unittest.TestCase):
    """Тесты отображения сложности."""

    def test_easy(self):
        self.assertEqual(difficulty_name("easy"), "🟢 Легко")

    def test_normal(self):
        self.assertEqual(difficulty_name("normal"), "🟡 Нормально")

    def test_nightmare(self):
        self.assertEqual(difficulty_name("nightmare"), "🔴 Кошмар")

    def test_unknown_defaults_to_normal(self):
        """Неизвестная сложность → Нормально."""
        self.assertEqual(difficulty_name("unknown"), "🟡 Нормально")


if __name__ == "__main__":
    unittest.main()
    