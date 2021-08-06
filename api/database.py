import sqlite3
import logging
from typing import Optional, Union


class DatabaseAPI:
    """Simple SQLite3 wrapper."""

    def __init__(self, path: str):
        self.path = path
        self.connection: Optional[sqlite3.Connection] = None

    def connect(self) -> bool:
        """Method to connect to database."""
        if not self.connection:
            try:
                self.connection = sqlite3.connect(
                    self.path,
                    check_same_thread=False
                )
            except sqlite3.DatabaseError as db_error:
                logging.error(f"{DatabaseAPI.__qualname__}: {db_error}")
                return False

        return True

    def disconnect(self) -> None:
        """Method to disconnect from database."""
        if self.connection:
            try:
                self.connection.close()
            except sqlite3.DatabaseError as db_error:
                logging.error(f"{DatabaseAPI.__qualname__}: {db_error}")

        self.connection = None

    def get_unix_time(self) -> int:
        """Method to get current unix time from database."""
        if self.connection:
            try:
                cursor = self.connection.cursor()
                cursor.execute("SELECT strftime('%s', 'now', 'localtime')")
                response = cursor.fetchone()
                cursor.close()
            except sqlite3.DatabaseError as db_error:
                logging.error(f"{DatabaseAPI.__qualname__}: {db_error}")
            else:
                if response:
                    return int(response[0])

        return 0

    def create_link_table(self) -> bool:
        """Method to create table of links in database."""
        if self.connection:
            try:
                cursor = self.connection.cursor()
                cursor.execute("""CREATE TABLE IF NOT EXISTS links(
                    original TEXT UNIQUE NOT NULL PRIMARY KEY,
                    shortened TEXT NOT NULL,
                    generation_time INTEGER NOT NULL)
                """)

                cursor.close()
                self.connection.commit()
            except sqlite3.DatabaseError as db_error:
                logging.error(f"{DatabaseAPI.__qualname__}: {db_error}")
            else:
                return True

        return False

    def add_new_short_link(self, original_link: str, shorted_link: str) -> bool:
        """Method to add new shorted link to database."""
        if self.connection:
            try:
                cursor = self.connection.cursor()
                cursor.execute(
                    "INSERT OR IGNORE INTO links VALUES (?, ?, ?)",
                    (original_link, shorted_link, self.get_unix_time())
                )

                cursor.close()
                self.connection.commit()
            except sqlite3.DatabaseError as db_error:
                logging.error(f"{DatabaseAPI.__qualname__}: {db_error}")
            else:
                return True

        return False

    def get_original_link(self, shorted_link: str) -> Union[str, bool]:
        """Method to get original link from database."""
        if self.connection:
            try:
                cursor = self.connection.cursor()
                cursor.execute(
                    "SELECT original FROM links WHERE shortened=?",
                    (shorted_link,)
                )
                response = cursor.fetchone()
                cursor.close()
            except sqlite3.DatabaseError as db_error:
                logging.error(f"{DatabaseAPI.__qualname__}: {db_error}")
            else:
                if response:
                    return str(response[0])

        return False

    def delete_outdated_links(self, lifetime: int) -> bool:
        """Method to delete outdated links from database."""
        if self.connection:
            border_link_lifetime = self.get_unix_time() - lifetime
            try:
                cursor = self.connection.cursor()
                cursor.execute(
                    "DELETE FROM links WHERE generation_time<?",
                    (border_link_lifetime,)
                )

                cursor.close()
                self.connection.commit()
            except sqlite3.DatabaseError as db_error:
                logging.error(f"{DatabaseAPI.__qualname__}: {db_error}")
            else:
                return True

        return False
