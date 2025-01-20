import time
from datetime import datetime, timezone
def run_scheduler(client, sleep_time: int = 60):
    while True:
        _send_notifications(client)
        time.sleep(sleep_time)

def single_run(client):
    _send_notifications(client)


def _send_notifications(client):
    messages = client.get_messages_to_send()
    if messages:
        for message in messages:
            try:
                client.send_push_notification(message["message"])
                client.check_as_sent(message["id"])
            except Exception as e:
                print(f"Error processing message: {e}")
    else :        
        utc_now = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S %Z')
        print(f"No notifications to send at {utc_now} UTC.")