import os
from dotenv import load_dotenv
import requests

# requests.get(URL, parameter={key: value}, arguments)


# https://graph.facebook.com/v16.0/t_6194435950612806
# ?
# fields=messages{message}
# &access_token=EAAJ2zxrtrIMBAKWZCPZB20GlbxrJviCLpzQaS61q4sxOrIReKMyMHDWmKn9VM6isbemDmHGUEec9NQEZC3N8s5ZABZBMuxfHX70rBAGFbZBjGyMfFEuUPiX5TM0DwVWnFE1mwzIVMnB3zQ2MqucStUhdoVCZCijCyFyaWVkJz2beS3LkgNncaSX4ORKKl45hTh4rF802vtD6H3aE2OBxLub

load_dotenv()

abc = os.getenv('USER_ID')
print(abc)
