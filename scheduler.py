from dotenv import load_dotenv
import os
import requests
import time
from datetime import datetime
from supabase import create_client, Client
import pytz

load_dotenv()

SUPABASE_URL: str = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY: str = os.getenv("SUPABASE_API_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_API_KEY)

API_URL: str = os.getenv("URL")
BOT_API_KEY: str = os.getenv("AUTHORIZATION_HEADER")
HEADERS = {
    "Authorization": BOT_API_KEY,
    "Content-Type": "application/json"
}

polish_tz = pytz.timezone('Europe/Warsaw')


def get_messages_to_send():
    try:
        response = supabase.table("notifications") \
            .select("*") \
            .filter("date", "lte", datetime.now(polish_tz)) \
            .filter("was_sent", "eq", False) \
            .execute()
        
        return response.data
    except Exception as e:
        print(f"Error fetching messages: {e}")
        return []


def send_push_notification(endpoint, message):
    try:
        response = requests.post(endpoint, json={"content": message}, headers=HEADERS)
        if response.status_code == 200:
            print(f"Notification sent: {message}")
        else:
            print(f"Failed to send notification. Status: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print(f"Error sending notification: {e}")


def check_as_sent(id):
    try:
        supabase.table("notifications") \
            .update({"was_sent" : True}) \
            .eq("id", id) \
            .execute()
    except Exception as e:
        print(f"Failed to check as sent. Notification with Id={id} and error: {e}.")

while True:
    messages = get_messages_to_send()

    if messages:
        for message in messages:
            try:
                send_push_notification(endpoint=API_URL, message=message["message"])
                check_as_sent(message["id"])
            except Exception as e:
                print(f"Error processing message: {e}")

    time.sleep(60)
