import unittest
import tools.db as db
import constants


class TestDB(unittest.TestCase):
    def setUp(self):
        db.close_connection()

    def test_initial_state(self):
        conn = db.get_connection()
        cursor = conn.cursor()

        # check required tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [table[0] for table in cursor.fetchall()]

        self.assertIn("levels", tables)
        self.assertIn("level_times", tables)

        # check tables have correct columns
        cursor.execute("PRAGMA table_info(levels)")
        columns = [column[1] for column in cursor.fetchall()]

        for col in ["id", "name", "data"]:
            self.assertIn(col, columns)

        cursor.execute("PRAGMA table_info(level_times)")
        columns = [column[1] for column in cursor.fetchall()]

        for col in ["id", "level_id", "time", "timestamp"]:
            self.assertIn(col, columns)

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
        self.assertEqual(best_time, -1)
        best_time = db.get_best_time(-1)
        self.assertEqual(best_time, -1) 
        best_time = db.get_best_time(567)
        self.assertEqual(best_time, -1) 

    def test_save_and_load_level(self):
        test_level = constants.TEST_LEVEL_END

        db.save_level("potato", test_level)
        level_id = db.get_level_id("potato")
        level_data = db.load_level_data(level_id)

        self.assertEqual(level_data, test_level)

    def test_save_and_load_level_invalid_input(self):
        level_data = db.load_level_data(9999)

        self.assertEqual(level_data, None)

        db.save_level("potato", [])
        level_id = db.get_level_id("potato")

        self.assertEqual(level_id, None)

        level_data = db.load_level_data(level_id)
        self.assertEqual(level_data, None)

        db.save_level("potato", [[]])
        level_id = db.get_level_id("potato")

        self.assertEqual(level_id, None)

        level_data = db.load_level_data(level_id)
        self.assertEqual(level_data, None)

    def test_get_all_levels(self):
        db.save_level("potato", constants.TEST_LEVEL_END)
        db.save_level("peruna", constants.TEST_LEVEL_END)

        levels = db.get_all_levels()
        level_names = [level[1] for level in levels]

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

        db.save_level("potato", constants.TEST_LEVEL_END)
        db.save_level("peruna", constants.TEST_LEVEL_END)

        self.assertTrue(db.level_name_exists("potato"))
        self.assertTrue(db.level_name_exists("peruna"))
        self.assertFalse(db.level_name_exists("makkaraperunat"))

    def test_delete_level(self):
        db.save_level("potato", constants.TEST_LEVEL_END)
        db.save_level("peruna", constants.TEST_LEVEL_END)

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

    def test_delete_times(self):
        db.save_level("potato", constants.TEST_LEVEL_END)
        db.save_level("peruna", constants.TEST_LEVEL_END)

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
