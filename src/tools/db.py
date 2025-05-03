"""Database functions for the game."""

import json

from sqlalchemy import func

from game.level_data import LevelData
from tools.db_connection import DBConnection
from tools.db_models import Level, LevelTime
from tools.db_utils import run_db_query


def close_connection():
    """Close the database connection."""
    DBConnection.close()


def init_db():
    """Initialize the SQLite database connection to persistent storage.

    This function creates the database and tables if they do not exist.
    If not called, the database will use an in-memory SQLite database.
    """
    DBConnection.init_db()


def get_engine():
    """Get the database engine.

    Returns:
        Engine: The SQLAlchemy engine instance.
    """
    return DBConnection.get_engine()


#### level times ####

def save_level_time(level_id: int, time: float) -> bool:
    """Save the level time for a specific level.

    Args:
        level_id (int): The ID of the level.
        time (float): The time to save.

    Returns:
        bool: True if the time was saved successfully, False otherwise.
    """
    if level_id < 0 or time < 0:
        return False

    def query(session):
        session.add(LevelTime(level_id=level_id, time=time))
        return True

    return run_db_query(query, error_return=False)


def get_best_time(level_id: int) -> float | None:
    """Get the best time for a specific level.

    Args:
        level_id (int): The ID of the level.

    Returns:
        float or None: The best time for the level if it exists, None otherwise.
    """
    if level_id < 0:
        return None

    def query(session):
        return session.query(func.min(LevelTime.time)).filter_by(level_id=level_id).scalar()

    return run_db_query(query)


def get_all_best_times() -> dict[int, float]:
    """Get best times for all levels.

    Returns:
        dict[int, float]: A dictionary mapping level IDs to their best times.
    """
    def query(session):
        results = (
            session.query(LevelTime.level_id, func.min(LevelTime.time))
            .group_by(LevelTime.level_id)
            .all()
        )
        return dict(results)

    return run_db_query(query, error_return={})


def delete_times(level_id: int) -> bool:
    """Delete all times for a specific level.

    Args:
        level_id (int): The ID of the level.

    Returns:
        bool: True if the times were deleted successfully, False otherwise.
    """
    def query(session):
        session.query(LevelTime).filter_by(level_id=level_id).delete()
        return True
    return run_db_query(query, error_return=False)


#### level data ####

def save_level(level_data: LevelData) -> bool:
    """Save level data to the database.

    Updates the level if it already exists, otherwise creates a new entry.

    Args:
        level_data (LevelData): The level data to save.

    Returns:
        bool: True if the level data was saved successfully, False otherwise.
    """
    if not LevelData.is_valid(level_data):
        return False

    if all(len(row) == 0 for row in level_data.data):
        return False

    json_data = json.dumps(level_data.data)

    def query(session):
        exists = session.query(Level).filter_by(name=level_data.name).first()
        if exists:
            exists.data = json_data
        else:
            session.add(Level(name=level_data.name, data=json_data))
        return True

    return run_db_query(query, error_return=False)


def load_level(level_id: int) -> LevelData | None:
    """Load level data from the database.

    Args:
        level_id (int): The ID of the level.

    Returns:
        LevelData or None: The level data if found, None otherwise.
    """
    def query(session):
        level = session.query(Level).filter_by(id=level_id).first()

        if not level:
            return None

        return LevelData.from_db_row((level.id, level.name, level.data))

    return run_db_query(query)


def get_all_levels() -> list[LevelData]:
    """Get all levels from the database.

    Returns:
        list[LevelData]: A list of LevelData objects representing all levels.
    """
    def query(session):
        rows = session.query(Level).order_by(Level.id).all()
        return [LevelData.from_db_row((l.id, l.name, l.data)) for l in rows]

    return run_db_query(query, error_return=[])


def level_name_exists(name: str) -> bool:
    """Check if a level name already exists in the database.

    Args:
        name (str): The name of the level to check.

    Returns:
        bool: True if the level name exists, False otherwise.
    """
    if not name:
        return False

    def query(session):
        result = session.query(Level).filter_by(name=name).first()
        return result is not None

    return run_db_query(query, error_return=False)


def get_level_id(name: str) -> int | None:
    """Get the ID of a level by its name.

    Args:
        name (str): The name of the level.

    Returns:
        int or None: The ID of the level if found, None otherwise.
    """
    if not name:
        return None

    def query(session):
        level_id = session.query(Level.id).filter_by(name=name).scalar()
        return level_id

    return run_db_query(query)


def delete_level(level_id: int) -> bool:
    """Delete a level from the database.

    Deletes the level and all associated times.

    Args:
        level_id (int): The ID of the level to delete.

    Returns:
        bool: True if the level was deleted successfully, False otherwise.
    """
    def query(session):
        session.query(LevelTime).filter_by(level_id=level_id).delete()
        session.query(Level).filter_by(id=level_id).delete()
        return True

    return run_db_query(query, error_return=False)
