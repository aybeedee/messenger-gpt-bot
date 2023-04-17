import fbchat
from fbchat import Client
from getpass import getpass

#session = fbchat.Session.login(getpass(), getpass())
#client = fbchat.Client(session = session)
client = fbchat.Client(getpass(), getpass())
name = str(input("Name: "))
user = client.searchForUsers(name)
message = str(input("Message: "))
sent = client.send(fbchat.models.Message(message), user.uid)

if (sent):
    print("Message sent!")

"""import requests

url = ""
x = requests.get(url)

print(x.text)"""