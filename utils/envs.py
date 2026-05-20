import os
from dotenv import load_dotenv

load_dotenv()

DISCOR_TOKEN = os.getenv("DISCOR_BOT_TOKEN")
OPEN_ROUTER_API = os.getenv("OPEN_ROUTER_API")
OPEN_ROUTER_MODEL = os.getenv("OPEN_ROUTER_MODEL")