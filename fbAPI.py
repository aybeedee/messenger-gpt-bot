import os
from dotenv import load_dotenv
import requests

# requests.get(URL, parameter={key: value}, arguments)

load_dotenv()

LATEST_API_VERSION = "v16.0"
PAGE_ACCESS_TOKEN = os.getenv('PAGE_ACCESS_TOKEN')
CONVERSATION_ID = os.getenv('CONVERSATION_ID')


arguments = {"fields": "messages{message}", "access_token": PAGE_ACCESS_TOKEN}
r = requests.get(f"https://graph.facebook.com/{LATEST_API_VERSION}/{CONVERSATION_ID}",
                 params=arguments)

print(r.json())