"""SQLAlchemy ORM models for the levels and level times."""

from sqlalchemy import Text, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship, mapped_column, Mapped


class Base(DeclarativeBase):
    """Base class for SQLAlchemy ORM models."""


class Level(Base):
    """Model representing a level.

    Attributes:
        id (int): Unique identifier for the level.
        name (str): Name of the level.
        data (str): Level data in string format.
        times (list[LevelTime]): List of level times associated with this level.
    """
    __tablename__ = "levels"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    data: Mapped[str] = mapped_column(Text)

    times: Mapped[list["LevelTime"]] = relationship(back_populates="level")


class LevelTime(Base):
    """Model representing a level time.

    Attributes:
        id (int): Unique identifier for the level time.
        level_id (int): Foreign key referencing the associated level.
        time (float): Time taken to complete the level.
        level (Level): The level associated with this time.
    """
    __tablename__ = "level_times"

    id: Mapped[int] = mapped_column(primary_key=True)
    level_id: Mapped[int] = mapped_column(ForeignKey("levels.id"))
    time: Mapped[float]

    level: Mapped[Level] = relationship(back_populates="times")
