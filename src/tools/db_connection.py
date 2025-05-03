"""Database connection and session management for SQLAlchemy."""

import json
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

import constants
from tools.db_models import Base, Level


class DBConnection:
    """Singleton class for managing the database connection and session."""

    _engine = None

    @classmethod
    def init_db(cls, add_test_level=False):
        """Initialize the database connection and create tables.

        Args:
            add_test_level (bool): If True, adds a test level to the database.
        """
        if cls._engine:
            cls._engine.dispose()

        cls._engine = create_engine("sqlite:///data.db")
        Base.metadata.create_all(bind=cls._engine)

        if add_test_level:
            cls._add_test_level()

    @classmethod
    def init_memory_db(cls):
        """Initialize an in-memory SQLite database for testing."""
        if cls._engine:
            cls._engine.dispose()

        cls._engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(bind=cls._engine)

        cls._add_test_level()

    @classmethod
    def get_engine(cls):
        """Get the database engine.

        If the engine is not initialized, it initializes a memory database.
        This is useful for testing purposes.

        Returns:
            Engine: The SQLAlchemy engine instance.
        """
        if cls._engine is None:
            cls.init_memory_db()
        return cls._engine

    @classmethod
    def get_session(cls):
        """Get a new session for database operations.

        If the engine is not initialized, it initializes a memory database.
        This is useful for testing purposes.

        Returns:
            Session: A new SQLAlchemy session instance.
        """
        engine = cls.get_engine()
        return Session(engine)

    @classmethod
    @contextmanager
    def get_session_scope(cls):
        """Provide a transactional scope around a series of operations.

        Handles session lifecycle (open, commit, rollback, close) and catches errors.
        Useful for ensuring that all operations within context are treated as a single transaction.

        Yields:
            Session: A SQLAlchemy session instance for the context.
        """
        session = cls.get_session()
        try:
            yield session
            session.commit()
        except SQLAlchemyError:
            session.rollback()
        finally:
            session.close()

    @classmethod
    def _add_test_level(cls):
        """Add a test level to the database if it doesn't exist."""
        with cls.get_session_scope() as session:
            exists = session.query(Level).filter_by(
                name="test_level").first()
            if not exists:
                session.add(Level(
                    name="test_level",
                    data=json.dumps(constants.TEST_LEVEL_DATA)
                ))

    @classmethod
    def close(cls):
        """Close the database connection."""
        if cls._engine:
            cls._engine.dispose()
            cls._engine = None
