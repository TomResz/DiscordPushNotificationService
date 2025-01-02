from supabase import create_client, Client
from datetime import datetime
import pytz
import requests

class NotificationClient:
    def __init__(self, supabase_url: str, supabase_api_key: str, api_url: str, bot_api_key: str, timezone: str = "Europe/Warsaw"):
        self.supabase: Client = create_client(supabase_url, supabase_api_key)
        self.api_url = api_url
        self.headers = {
            "Authorization": bot_api_key,
            "Content-Type": "application/json"
        }
        self.timezone = pytz.timezone(timezone)
        if not self.__check_configuration():
            print("Fix the configuration issues before proceeding.")
            exit(1)
        if not self.__table_exists("notifications") :
            print("Table 'notifications not exists.'")
            exit(1)

    def __table_exists(self,table_name):
        try:
            response = self.supabase.table(table_name) \
                .select("*").limit(1) \
                    .execute()
            return response.data is not None
        except Exception:
            return False
        
    def __check_configuration(self):
        try:
            if not self.supabase:
                raise ValueError("Supabase client is not initialized.")
            if not self.api_url:
                raise ValueError("API URL is not configured.")
            if "Authorization" not in self.headers or not self.headers["Authorization"]:
                raise ValueError("Bot API key is not set in headers.")
            if not self.timezone:
                raise ValueError("Timezone is not configured.")

            print("Configuration is valid.")
            return True
        except Exception as e:
            print(f"Configuration error: {e}")
            return False

    def get_messages_to_send(self):
        try:
            response = self.supabase.table("notifications") \
                .select("*") \
                .filter("date", "lte", datetime.now(self.timezone)) \
                .filter("was_sent", "eq", False) \
                .execute()
         
            return response.data
        except Exception as e:
            print(f"Error fetching messages: {e}")
            return []
        


    
    def send_push_notification(self, message: str):
        try:
            response = requests.post(self.api_url, json={"content": message}, headers=self.headers)
            if response.status_code == 200:
                print(f"Notification sent: {message}")
            else:
                print(f"Failed to send notification. Status: {response.status_code}, Response: {response.text}")
        except Exception as e:
            print(f"Error sending notification: {e}")


    def check_as_sent(self, message_id):
        try:
            self.supabase.table("notifications") \
                .update({"was_sent": True}) \
                .eq("id", message_id) \
                .execute()
        except Exception as e:
            print(f"Failed to check as sent. Notification with Id={message_id} and error: {e}.")
