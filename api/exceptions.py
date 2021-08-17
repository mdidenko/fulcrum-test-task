class SQLiteWrapperError(Exception):
    """SQLite base exception class."""
    __slots__ = ()


class IntegrityError(SQLiteWrapperError):
    """
    Exception raised when the relational integrity of the database is
    affected, e.g. a foreign key check fails.
    """


class ProgrammingError(SQLiteWrapperError):
    """
    Exception raised for programming errors,
    e.g. table not found or already exists, syntax error in the SQL
    statement, wrong number of parameters specified, etc.
    """


class OperationalError(SQLiteWrapperError):
    """
    Exception raised for errors that are related to the database’s
    operation and not necessarily under the control of the programmer,
    e.g. an unexpected disconnect occurs, the data source name isn't found,
    a transaction could not be processed, etc.
    """


class NotSupportedError(SQLiteWrapperError):
    """
    Exception raised in case a method or database API was used which isn't
    supported by the database, e.g. calling the rollback() method on a
    connection that does not support transaction or has transactions
    turned off.
    """
