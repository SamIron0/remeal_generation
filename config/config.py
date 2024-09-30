import os
from dotenv import load_dotenv

load_dotenv()

DEEP_INFRA_API_KEY = os.getenv('DEEP_INFRA_API_KEY')
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')