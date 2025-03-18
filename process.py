import webbrowser
import time
import pyautogui
import urllib.parse
from datetime import datetime
from flask_pymongo import MongoClient
from pymsgbox import alert

from app import app
import logging

# MongoDB Setup
client = MongoClient( HERE REPLACE WITH YOUR MONGODB URI, ssl_cert_reqs=ssl.CERT_NONE)
mongoDB = client['Bulk_Database']
collection = mongoDB['User_info']
collection2 = mongoDB['Detailed']

logging.basicConfig(filename='message_sender.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def send_messages():
    with app.app_context():
        dashboard_users = list(collection2.find())
        url_template = "https://wa.me/{phone_number}?text={message}"

        for user in dashboard_users:
            if user.get('status') == "Pending":
                encoded_message = urllib.parse.quote(user.get('Send_message', ''))
                url = url_template.format(phone_number='+91' + user.get('phoneNumber', ''), message=encoded_message)

                try:
                    webbrowser.open(url)
                    time.sleep(2)
                    pyautogui.click(735, 365)
                    time.sleep(2)
                    pyautogui.press('enter')
                    time.sleep(2)

                    collection2.update_one(
                        {"_id": user['_id']},
                        {
                            "$set": {
                                "status": "Sent",
                                "sent_timestamp": datetime.now()
                            }
                        }
                    )

                    logging.info(f"Message sent to {user.get('phone')} at {datetime.now()}")
                except Exception as e:
                    logging.error(f"Failed to send message to {user.get('phone')}: {str(e)}")
                    alert(f"An error occurred: {str(e)}")
                    continue

        # Close the browser and tabs
        pyautogui.hotkey('command', 'q')
        for _ in dashboard_users:
            pyautogui.hotkey('command', 'w')
        pyautogui.hotkey('command', 'r')


if __name__ == "__main__":
    send_messages()
