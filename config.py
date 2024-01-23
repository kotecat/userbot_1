import os
from dotenv import load_dotenv
import logging


logger = logging.getLogger("CONFIG")


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    logger.error("Подготовьте (Prepare) .env file")
    exit()


class Config:
    API_ID = str(os.getenv("API_ID"))
    API_HASH = str(os.getenv("API_HASH"))
    ME_ID = int(os.getenv("ME_ID"))
