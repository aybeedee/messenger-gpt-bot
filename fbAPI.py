import os
from dotenv import load_dotenv
import requests

# requests.get(URL, parameter={key: value}, arguments)


# https://graph.facebook.com/v16.0/t_6194435950612806
# ?
# fields=messages{message}
# &access_token=EAAJ2zxrtrIMBAKWZCPZB20GlbxrJviCLpzQaS61q4sxOrIReKMyMHDWmKn9VM6isbemDmHGUEec9NQEZC3N8s5ZABZBMuxfHX70rBAGFbZBjGyMfFEuUPiX5TM0DwVWnFE1mwzIVMnB3zQ2MqucStUhdoVCZCijCyFyaWVkJz2beS3LkgNncaSX4ORKKl45hTh4rF802vtD6H3aE2OBxLub

load_dotenv()

LATEST_API_VERSION = "v16.0"
PAGE_ACCESS_TOKEN = os.getenv('PAGE_ACCESS_TOKEN')
CONVERSATION_ID = os.getenv('CONVERSATION_ID')


arguments = {"fields": "messages{message}", "access_token": PAGE_ACCESS_TOKEN}
r = requests.get(f"https://graph.facebook.com/{LATEST_API_VERSION}/{CONVERSATION_ID}",
                 params=arguments)

print(r.json())