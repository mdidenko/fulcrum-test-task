from config import app, db, SERVER_IP, SERVER_PORT, \
    SERVER_DEBUG_INFO
import logging
import views


if __name__ == '__main__':
    if not db.connect():
        logging.error("- Connection to the"
                      " database isn't established."
                      " Service shut down...")
        raise SystemExit
    else:
        db.create_link_table()
        app.run(
            host=SERVER_IP,
            port=SERVER_PORT,
            debug=SERVER_DEBUG_INFO
        )
        db.disconnect()
