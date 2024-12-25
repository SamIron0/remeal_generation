import os
from dotenv import load_dotenv

load_dotenv()

DEEP_INFRA_API_KEY = os.getenv('DEEP_INFRA_API_KEY')
INGESTION_URL = os.getenv('INGESTION_URL')