import os
from dotenv import load_dotenv
import requests
import time
import ora
import asyncio

#function for gpt query calls and awaiting gpt's response
async def gptQuery(message):
    
    response = ora.Completion.create(
        model  = model,
        prompt = message,
        includeHistory = True,
        conversationId = init.id)

    return response.completion.choices[0].text

#helper function to relay async call for making gpt query
async def gptQueryAsync(message):

    answer = await asyncio.gather(gptQuery(message))
    return answer

#main functionality starts
if __name__ == '__main__':

    #loading environment variables
    load_dotenv()

    USER_ID = os.getenv("USER_ID")
    PAGE_ID = os.getenv("PAGE_ID")
    LATEST_API_VERSION = "v16.0"
    PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")
    CONVERSATION_ID = os.getenv("CONVERSATION_ID")

    #initiating model
    model = ora.CompletionModel.create(
        system_prompt = 'You are ChatGPT, a large language model trained by OpenAI. Answer as concisely as possible. Mujhse Urdu mei baat karain please',
        description   = 'ChatGPT Openai Language Model',
        name          = 'gpt-3.5')

    # init conversation (will give you a conversationId)
    init = ora.Completion.create(
        model  = model,
        prompt = 'salam')

    #logging first gpt response to terminal
    print(init.completion.choices[0].text)

    #arguments
    getArgs = {"fields": "messages{message}", "access_token": PAGE_ACCESS_TOKEN}
    res = requests.get(f"https://graph.facebook.com/{LATEST_API_VERSION}/{CONVERSATION_ID}",
                    params=getArgs)

    res_json = res.json()

    message_count = len(res_json["messages"]["data"])

    while(True):

        print("\ncurrent message count = ", message_count)

        time.sleep(5)

        res = requests.get(f"https://graph.facebook.com/{LATEST_API_VERSION}/{CONVERSATION_ID}",
                        params=getArgs)
        
        res_json = res.json()

        n = len(res_json["messages"]["data"])

        print("new message count = ", n)

        if (n > message_count):

            message_count = n
            message = res_json["messages"]["data"][0]["message"]

            answer = asyncio.run(gptQueryAsync(message))

            postArgs = {
                "recipient": f"{{id: {USER_ID}}}", 
                "messaging_type": "RESPONSE", 
                "message": f"{{text: \"ok\"}}",
                "access_token": PAGE_ACCESS_TOKEN
                }

            res = requests.post(f"https://graph.facebook.com/{LATEST_API_VERSION}/{PAGE_ID}/messages",
                     params=postArgs)

            print(res.json())


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