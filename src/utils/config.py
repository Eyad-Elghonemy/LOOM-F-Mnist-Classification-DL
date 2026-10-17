import tensorflow as tf
from dotenv import load_dotenv
from supabase import create_client, Client, ClientOptions
import os

load_dotenv(override=True)

# Get The Variables
APP_NAME = os.getenv("APP_NAME")
VERSION = os.getenv("VERSION")
API_SECRET_KEY = os.getenv("API_SECRET_KEY")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Parent Folder Path
SRC_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Model
MODEL = tf.keras.models.load_model(os.path.join(SRC_FOLDER, 'artifacts', 'model.keras'))

# Class Names
CLASS_NAMES = ['T_shirt', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle_Boot']

# Seconds to wait on Supabase before giving up. Short on purpose: a
# paused/sleeping free-tier project would otherwise hang a request
# for a very long time instead of failing fast.
_SUPABASE_TIMEOUT_SECONDS = 5

# Supabase Client (service_role key -> server-side only, bypasses RLS)
# If the env vars are missing, we don't crash the whole app — logging just gets
# silently skipped (see logger.py). This keeps local dev/testing possible
# without a Supabase project configured. create_client() itself makes no
# network call, so constructing it eagerly is safe even if the project
# happens to be asleep right now -- only the .execute() calls can time out,
# and that's what postgrest_client_timeout bounds.
SUPABASE: Client | None = None
if SUPABASE_URL and SUPABASE_KEY:
    SUPABASE = create_client(
        SUPABASE_URL, SUPABASE_KEY,
        options=ClientOptions(postgrest_client_timeout=_SUPABASE_TIMEOUT_SECONDS),
    )
