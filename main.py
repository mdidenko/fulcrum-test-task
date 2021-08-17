import logging
from api.exceptions import SQLiteWrapperError
from config import app, db, SERVER_IP, SERVER_PORT, \
    SERVER_DEBUG_INFO
import views


if __name__ == '__main__':
    try:
        db.connect()
        db.create_link_table()
        app.run(
            host=SERVER_IP,
            port=SERVER_PORT,
            debug=SERVER_DEBUG_INFO
        )
        db.disconnect()
    except SQLiteWrapperError as exception:
        logging.error(exception)
