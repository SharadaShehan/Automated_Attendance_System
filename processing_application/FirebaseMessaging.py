import firebase_admin
from firebase_admin import credentials, messaging

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

notification_data = {
    "title": "Breaking News!",
    "body": "This is a notification for the 'news' topic.",
    "data": {
        "category": "urgent"
    }
}

topic = "news"  # Replace with your desired topic name
response = messaging.send_to_topic(notification_data, topic)

if response.failure_count > 0:
    print('Error sending message:', response.errors)
else:
    print('Message sent successfully')
