import os
from dotenv import load_dotenv
from notifications import NotificationClient, run_scheduler


load_dotenv()

SUPABASE_URL: str = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY: str = os.getenv("SUPABASE_API_KEY")
API_URL: str = os.getenv("URL")
BOT_API_KEY: str = os.getenv("AUTHORIZATION_HEADER")

client = NotificationClient(
    supabase_url=SUPABASE_URL,
    supabase_api_key=SUPABASE_API_KEY,
    api_url=API_URL,
    bot_api_key=BOT_API_KEY
)

run_scheduler(client)