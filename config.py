import os
from dotenv import load_dotenv, find_dotenv
from static_data import messages as static

load_dotenv(find_dotenv())


DB_MANAGER = os.getenv("db_manager")
DB_NAME = os.getenv("db_name")
DB_HOST = os.getenv("db_host")
DB_USER = os.getenv("db_user")
DB_PASSWORD = os.getenv("db_password")
DB_PORT = os.getenv("db_port")

TG_TOKEN = os.getenv("tg_token")
TG_ALLOWED_MESSAGES = ["/start"] + static.as_list()
