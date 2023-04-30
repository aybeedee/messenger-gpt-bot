import os
from dotenv import load_dotenv
import requests
import time
import asyncio
from gpt4free import you

#function for gpt query calls and awaiting gpt's response
async def gptQuery(message):

    response = you.Completion.create(
        prompt= message,
        chat=chat)

    answer = response.text 

    chat.append({"question": message, "answer": answer})

    return answer

#helper function to relay async call for making gpt query
async def gptQueryAsync(message):

    answer = await asyncio.gather(gptQuery(message))
    return answer

#main functionality starts
if __name__ == "__main__":

    #loading environment variables
    load_dotenv()

    USER_ID = os.getenv("USER_ID")
    PAGE_ID = os.getenv("PAGE_ID")
    LATEST_API_VERSION = "v16.0"
    PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")
    CONVERSATION_ID = os.getenv("CONVERSATION_ID")

    #initiating model
    response = you.Completion.create(
        prompt="mujhse urdu mei baat karay please",
        detailed=False,
        include_links=False)
    
    chat = []

    #arguments for get request
    getArgs = {"fields": "messages{message}", "access_token": PAGE_ACCESS_TOKEN}
    res = requests.get(f"https://graph.facebook.com/{LATEST_API_VERSION}/{CONVERSATION_ID}",
                    params=getArgs)

    #getting current no. of messages in the conversation
    res_json = res.json()

    message_count = len(res_json["messages"]["data"])

    #after a time interval, get request is made, no of messages in the conversation are fetched
    #if they are greater (meaning user typed a new prompt), gpt query is made and answer is posted
    while(True):

        print("\ncurrent message count = ", message_count)

        #time interval to not spam get requests
        time.sleep(5)

        #get request for messages in conversation
        res = requests.get(f"https://graph.facebook.com/{LATEST_API_VERSION}/{CONVERSATION_ID}",
                        params=getArgs)
        
        res_json = res.json()

        #current no of messages in conversation
        n = len(res_json["messages"]["data"])

        print("new message count = ", n)

        #if new message has been received
        if (n > message_count):

            #message count updated
            message_count = n

            #message extracted
            message = res_json["messages"]["data"][0]["message"]

            #gpt query ran
            answer = asyncio.run(gptQueryAsync(message))

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
            #input to gpt and get answer 