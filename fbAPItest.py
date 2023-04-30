import os
from dotenv import load_dotenv
import requests
import time
import asyncio
from gpt4free import you


#main functionality starts
if __name__ == "__main__":

    #loading environment variables
    load_dotenv()

    USER_ID = os.getenv("USER_ID")
    PAGE_ID = os.getenv("PAGE_ID")
    LATEST_API_VERSION = "v16.0"
    PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")
    CONVERSATION_ID = os.getenv("CONVERSATION_ID")

    l = ['apple "hitt" the fan']
    answer = l[0]
    answer = answer.strip('"')
    #post request arguments set
    postArgs = {
        "recipient": f"{{id: {USER_ID}}}", 
        "messaging_type": "RESPONSE", 
        #"message": f"{{text: \"ok\"}}",
        "message": f"{{text: \"{answer}\"}}",
        "access_token": PAGE_ACCESS_TOKEN
        }

    res = requests.post(f"https://graph.facebook.com/{LATEST_API_VERSION}/{PAGE_ID}/messages",
                params=postArgs)
    
    print(res.json())

