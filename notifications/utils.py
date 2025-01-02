import time

def run_scheduler(client, sleep_time: int = 60):
    while True:
        messages = client.get_messages_to_send()
        if messages:
            for message in messages:
                try:
                    client.send_push_notification(message["message"])
                    client.check_as_sent(message["id"])
                except Exception as e:
                    print(f"Error processing message: {e}")
        time.sleep(sleep_time)