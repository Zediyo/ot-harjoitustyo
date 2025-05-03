"""Utility for safely running database queries with automatic error handling."""

from sqlalchemy.exc import SQLAlchemyError
from tools.db_connection import DBConnection


def run_db_query(func, error_return=None):
    """Execute a database operation within a managed session context.

    This utility handles session lifecycle (open, commit, rollback, close)
    and catches SQLAlchemy errors. It simplifies calling functions that accept
    a session as their first argument.

    Args:
        func (Callable[[Session], Any]):
            A function that takes a SQLAlchemy session and performs database logic.
        error_return (Any, optional):
            Value to return in case of an exception. Defaults to None.

    Returns:
        Any: The result of the database function if successful; otherwise, `error_return`.
    """
    try:
        with DBConnection.get_session_scope() as session:
            return func(session)
    except SQLAlchemyError:
        return error_return
