""" Contains the EndScreenData dataclass, representing the end screen data structure."""

from dataclasses import dataclass
from game.level_data import LevelData
from game.timer import Timer


@dataclass
class EndScreenData:
    """Dataclass representing the end screen data structure.

    Attributes:
        level (LevelData): The level data from the last completed level.
        timer (Timer): The timer from the last completed level.
    """

    level: LevelData
    timer: Timer

    @classmethod
    def is_valid(cls, data) -> bool:
        """Check if the given data is a valid EndScreenData object.

        Args:
            data (any): The data to check.

        Returns:
            bool: True if the data is a valid EndScreenData object, False otherwise.
        """
        return (
            isinstance(data, cls) and
            LevelData.is_valid(data.level) and
            isinstance(data.timer, Timer)
        )
