import sqlite3
from functools import wraps
from typing import Optional, Callable, Any
from api.exceptions import IntegrityError, \
    ProgrammingError, OperationalError, NotSupportedError


def exception_handler(function: Callable) -> Any:
    """SQLite Exception wrapper."""
    @wraps(function)
    def wrapper(self, *args, **kwargs) -> None:
        try:
            return function(self, *args, **kwargs)

        except sqlite3.IntegrityError as exception:
            raise IntegrityError(exception)

        except sqlite3.ProgrammingError as exception:
            raise ProgrammingError(exception)

        except sqlite3.OperationalError as exception:
            raise OperationalError(exception)

        except sqlite3.NotSupportedError as exception:
            raise NotSupportedError(exception)

    return wrapper


class DatabaseAPI:
    """Simple SQLite3 wrapper."""

    def __init__(self, path: str):
        self.path = path
        self.connection: Optional[sqlite3.Connection] = None

    @exception_handler
    def connect(self) -> None:
        """Method to connect to database."""
        if not self.connection:
            self.connection = sqlite3.connect(
                self.path,
                check_same_thread=False
            )

    @exception_handler
    def disconnect(self) -> None:
        """Method to disconnect from database."""
        if self.connection:
            self.connection.close()
        self.connection = None

    @exception_handler
    def get_unix_time(self) -> Optional[str]:
        """Method to get current unix time from database."""
        cursor = self.connection.cursor()
        cursor.execute("SELECT strftime('%s', 'now', 'localtime')")
        response = cursor.fetchone()
        cursor.close()

        if response:
            return str(response[0])
        else:
            return None

    @exception_handler
    def create_link_table(self) -> None:
        """Method to create table of links in database."""
        cursor = self.connection.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS links(
            original TEXT UNIQUE NOT NULL PRIMARY KEY,
            shortened TEXT NOT NULL,
            generation_time INTEGER NOT NULL)
        """)
        cursor.close()
        self.connection.commit()

    @exception_handler
    def add_new_short_link(self, original_link: str, shorted_link: str) -> None:
        """Method to add new shorted link to database."""
        cursor = self.connection.cursor()
        cursor.execute(
            "INSERT OR IGNORE INTO links VALUES (?, ?, ?)",
            (original_link, shorted_link, self.get_unix_time())
        )
        cursor.close()
        self.connection.commit()

    @exception_handler
    def get_original_link(self, shorted_link: str) -> Optional[str]:
        """Method to get original link from database."""
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT original FROM links WHERE shortened=?",
            (shorted_link,)
        )
        response = cursor.fetchone()
        cursor.close()

        if response:
            return str(response[0])
        else:
            return None

    @exception_handler
    def delete_outdated_links(self, lifetime: int) -> None:
        """Method to delete outdated links from database."""
        unix_time = self.get_unix_time()
        try:
            border_link_lifetime = int(unix_time) - lifetime
        except ValueError as exception:
            raise NotSupportedError(exception)
        else:
            cursor = self.connection.cursor()
            cursor.execute(
                "DELETE FROM links WHERE generation_time<?",
                (border_link_lifetime,)
            )
            cursor.close()
            self.connection.commit()
