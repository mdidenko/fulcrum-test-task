import json
import logging
from flask import Flask
from api.database import DatabaseAPI


with open("config.json", "r", encoding="utf-8") as file:
    config = json.loads(file.read())

SERVER_IP = config['server'].get("ip", "127.0.0.1")
SERVER_PORT = config['server'].get("port", 80)
SERVER_DEBUG_INFO = config['server'].get("debug_info", False)
DATABASE_PATH = config['database'].get("path", ":memory:")
LOG_PATH = config['log'].get("path", "app.log")
LINK_LIFETIME = config['link'].get("lifetime_sec", 3600)

app = Flask(__name__)
db = DatabaseAPI(DATABASE_PATH)

logging.basicConfig(
    filename=LOG_PATH,
    filemode='w',
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S"
)
