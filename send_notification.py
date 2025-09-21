import firebase_admin
from firebase_admin import credentials, messaging
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # directory of the current file
cred_path = os.path.join(BASE_DIR, 'cloud_messaging_credentials.json')

# Initialize the Firebase Admin SDK (run once)
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)

def send_broadcast_message(topic: str, title: str, body: str):
    """
    Send a broadcast message to all devices subscribed to a given FCM topic.

    Args:
        topic (str): The FCM topic name (without '/topics/').
        title (str): Notification title.
        body (str): Notification body text.
    """
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body
        ),
        topic=topic
    )

    try:
        response = messaging.send(message)
        print(f"✅ Successfully sent message to topic '{topic}': {response}")
    except Exception as e:
        print(f"❌ Error sending message to topic '{topic}': {e}")



