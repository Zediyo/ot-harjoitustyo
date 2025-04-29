""" Contains the LevelData dataclass, representing the level data structure."""

from dataclasses import dataclass
import json


@dataclass
class LevelData:
    """Dataclass representing the level data structure.

    Attributes:
        id (int): The unique identifier for the level.
        name (str): The name of the level.
        data (list[list[int]]): 2D grid data representing the level layout.
    """

    id: int
    name: str
    data: list[list[int]]

    @classmethod
    def from_db_row(cls, row: tuple) -> "LevelData":
        """ Create a LevelData instance from a database row.

        Args:
            row (tuple): A tuple containing (id, name, data) as stored in the database.

        Returns:
            LevelData: A LevelData object.
        """
        level_id, name, data_json = row
        data = json.loads(data_json)
        return cls(id=level_id, name=name, data=data)

    @classmethod
    def is_valid(cls, obj) -> bool:
        """Check if the given data is a valid LevelData object.

        Args:
            data (any): The data to check.

        Returns:
            bool: True if the data is a valid LevelData object, False otherwise.
        """
        return (
            isinstance(obj, LevelData) and
            isinstance(obj.id, int) and
            isinstance(obj.name, str) and obj.name.strip() != "" and
            isinstance(obj.data, list) and
            len(obj.data) > 0 and
            all(
                isinstance(row, list) and all(isinstance(cell, int)
                                              for cell in row)
                for row in obj.data
            )
        )
