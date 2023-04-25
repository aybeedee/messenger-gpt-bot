import os
from dotenv import load_dotenv
import requests
import time
import ora
import asyncio

load_dotenv()

USER_ID = os.getenv("USER_ID")
PAGE_ID = os.getenv("PAGE_ID")
LATEST_API_VERSION = "v16.0"
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")
CONVERSATION_ID = os.getenv("CONVERSATION_ID")

model = ora.CompletionModel.create(
    system_prompt = 'You are ChatGPT, a large language model trained by OpenAI. Answer as concisely as possible. Mujhse Urdu mei baat karain please',
    description   = 'ChatGPT Openai Language Model',
    name          = 'gpt-3.5')

# init conversation (will give you a conversationId)
init = ora.Completion.create(
    model  = model,
    prompt = 'salam')

print(init.completion.choices[0].text)

async def gptQuery():
    
    response = ora.Completion.create(
        model  = model,
        prompt = prompt,
        includeHistory = True, 
        conversationId = init.id)

    return response.completion.choices[0].text

async def gptQueryAsync():
    
    answer = await asyncio.gather(gptQuery())
    return answer

print("a")
print("b")
asyncio.run(bar())
print("c")
print("d")
print("e")

arguments = {"fields": "messages{message}", "access_token": PAGE_ACCESS_TOKEN}
res = requests.get(f"https://graph.facebook.com/{LATEST_API_VERSION}/{CONVERSATION_ID}",
                params=arguments)

res_json = res.json()

message_count = len(res_json["messages"]["data"])

while(True):

    print("\ncurrent message count = ", message_count)

    time.sleep(5)

    res = requests.get(f"https://graph.facebook.com/{LATEST_API_VERSION}/{CONVERSATION_ID}",
                    params=arguments)
    
    res_json = res.json()

    n = len(res_json["messages"]["data"])

    print("new message count = ", n)

    if (n > message_count):
        print(res_json["messages"]["data"][0]["message"])
        message_count = n

# arguments = {
#     "recipient": f"{{id: {USER_ID}}}", 
#     "messaging_type": "RESPONSE", 
#     "message": f"{{text: \"ok\"}}",
#     "access_token": PAGE_ACCESS_TOKEN
#     }

# r = requests.post(f"https://graph.facebook.com/{LATEST_API_VERSION}/{PAGE_ID}/messages",
#                  params=arguments)

# print(r.json())


#main loop
    #GET message
    #input message to gpt
    #gpt generates answer
    #POST answer


#while(True):
    #make get request
    #set count of messages
    #wait for a while
    #make request again
    #if count of messages has increased
        #store most recent message
        #input to 