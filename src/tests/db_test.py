import unittest
import tools.db as db
from sqlalchemy import inspect

from constants import TEST_LEVEL_END_DATA
from game.level_data import LevelData


class TestDB(unittest.TestCase):
    def setUp(self):
        db.close_connection()

    def test_initial_state(self):
        engine = db.get_engine()
        inspector = inspect(engine)

        # check required tables exist
        tables = inspector.get_table_names()

        self.assertIn("levels", tables)
        self.assertIn("level_times", tables)

        # check tables have correct columns
        level_columns = [col["name"]
                         for col in inspector.get_columns("levels")]

        for col in ["id", "name", "data"]:
            self.assertIn(col, level_columns)

        time_columns = [col["name"]
                        for col in inspector.get_columns("level_times")]

        for col in ["id", "level_id", "time"]:
            self.assertIn(col, time_columns)

    def test_save_and_load_level_time(self):
        db.save_level_time(12, 123)
        db.save_level_time(12, 13)
        db.save_level_time(12, 456)
        db.save_level_time(12, 58)

        best_time = db.get_best_time(12)
        self.assertEqual(best_time, 13)

    def test_save_and_load_level_time_invalid_input(self):
        db.save_level_time(-1, 12)
        db.save_level_time(12, -2)

        best_time = db.get_best_time(12)
        self.assertEqual(best_time, None)
        best_time = db.get_best_time(-1)
        self.assertEqual(best_time, None)
        best_time = db.get_best_time(567)
        self.assertEqual(best_time, None)

    def test_save_and_load_level(self):
        to_save = LevelData(-1, "potato", TEST_LEVEL_END_DATA)
        self.assertTrue(LevelData.is_valid(to_save))

        self.assertTrue(db.save_level(to_save))
        level_id = db.get_level_id("potato")
        level_data = db.load_level(level_id)

        self.assertTrue(LevelData.is_valid(level_data))
        self.assertEqual(level_data.data, TEST_LEVEL_END_DATA)

    def test_save_and_load_level_invalid_level_data(self):
        # test random id
        level_data = db.load_level(9999)
        self.assertEqual(level_data, None)

        # try save invalid
        to_save = LevelData(-1, "potato", [])
        self.assertFalse(LevelData.is_valid(to_save))
        self.assertFalse(db.save_level(to_save))

        # test nothing was added
        level_id = db.get_level_id("potato")
        self.assertEqual(level_id, None)

        level_data = db.load_level(level_id)
        self.assertEqual(level_data, None)

    def test_save_and_load_level_valid_but_empty(self):
        # try save valid but empty
        to_save = LevelData(-1, "potato", [[]])
        self.assertTrue(LevelData.is_valid(to_save))
        self.assertFalse(db.save_level(to_save))

        # test nothing was added
        level_id = db.get_level_id("potato")
        self.assertEqual(level_id, None)

        level_data = db.load_level(level_id)
        self.assertEqual(level_data, None)

    def test_get_all_levels(self):
        db.save_level(LevelData(-1, "potato", TEST_LEVEL_END_DATA))
        db.save_level(LevelData(-1, "peruna", TEST_LEVEL_END_DATA))

        levels = db.get_all_levels()

        for level in levels:
            self.assertTrue(LevelData.is_valid(level))

        level_names = [level.name for level in levels]

        self.assertIn("potato", level_names)
        self.assertIn("peruna", level_names)

    def test_get_all_best_times(self):
        best_times = db.get_all_best_times()
        self.assertEqual(len(best_times), 0)

        db.save_level_time(1, 123)
        db.save_level_time(1, 321)
        db.save_level_time(2, 654)
        db.save_level_time(2, 456)
        db.save_level_time(3, 789)
        db.save_level_time(3, 987)

        best_times = db.get_all_best_times()

        best_time1 = best_times.get(1, None)
        best_time2 = best_times.get(2, None)
        best_time3 = best_times.get(3, None)

        self.assertEqual(len(best_times), 3)

        self.assertEqual(best_time1, 123)
        self.assertEqual(best_time2, 456)
        self.assertEqual(best_time3, 789)

    def test_level_name_exists(self):
        self.assertFalse(db.level_name_exists("potato"))
        self.assertFalse(db.level_name_exists("peruna"))
        self.assertFalse(db.level_name_exists("makkaraperunat"))

        db.save_level(LevelData(-1, "potato", TEST_LEVEL_END_DATA))
        db.save_level(LevelData(-1, "peruna", TEST_LEVEL_END_DATA))

        self.assertTrue(db.level_name_exists("potato"))
        self.assertTrue(db.level_name_exists("peruna"))
        self.assertFalse(db.level_name_exists("makkaraperunat"))

    def test_delete_level(self):
        db.save_level(LevelData(-1, "potato", TEST_LEVEL_END_DATA))
        db.save_level(LevelData(-1, "peruna", TEST_LEVEL_END_DATA))
        db.save_level_time(2, 654)
        db.save_level_time(2, 456)
        db.save_level_time(3, 45)
        db.save_level_time(3, 54)

        self.assertTrue(db.level_name_exists("potato"))
        self.assertTrue(db.level_name_exists("peruna"))

        db.delete_level(db.get_level_id("makkaraperunat"))
        db.delete_level(-1)
        db.delete_level(5)

        self.assertTrue(db.level_name_exists("potato"))
        self.assertTrue(db.level_name_exists("peruna"))

        db.delete_level(db.get_level_id("potato"))

        self.assertFalse(db.level_name_exists("potato"))
        self.assertTrue(db.level_name_exists("peruna"))

        db.delete_level(db.get_level_id("peruna"))

        self.assertFalse(db.level_name_exists("potato"))
        self.assertFalse(db.level_name_exists("peruna"))

        times = db.get_all_best_times()
        self.assertEqual(len(times), 0)

    def test_delete_times(self):
        db.save_level(LevelData(-1, "potato", TEST_LEVEL_END_DATA))
        db.save_level(LevelData(-1, "peruna", TEST_LEVEL_END_DATA))

        db.save_level_time(1, 123)
        db.save_level_time(1, 321)
        db.save_level_time(2, 654)
        db.save_level_time(2, 456)

        best_times = db.get_all_best_times()

        best_time1 = best_times.get(1, None)
        best_time2 = best_times.get(2, None)

        self.assertEqual(len(best_times), 2)
        self.assertEqual(best_time1, 123)
        self.assertEqual(best_time2, 456)

        db.delete_times(-1)
        db.delete_times(5)

        best_times = db.get_all_best_times()

        best_time1 = best_times.get(1, None)
        best_time2 = best_times.get(2, None)

        self.assertEqual(len(best_times), 2)
        self.assertEqual(best_time1, 123)
        self.assertEqual(best_time2, 456)

        db.delete_times(1)

        best_times = db.get_all_best_times()

        best_time1 = best_times.get(1, None)
        best_time2 = best_times.get(2, None)

        self.assertEqual(len(best_times), 1)
        self.assertEqual(best_time1, None)
        self.assertEqual(best_time2, 456)

        db.delete_times(2)

        best_times = db.get_all_best_times()
        best_time1 = best_times.get(1, None)
        best_time2 = best_times.get(2, None)

        self.assertEqual(len(best_times), 0)
        self.assertEqual(best_time1, None)
        self.assertEqual(best_time2, None)
