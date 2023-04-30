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
        prompt="Reply to me ONLY in Urdu langauge. Don't speak english. Start doing so from the following prompt: How are you?",
        detailed=False,
        include_links=False)
    
    chat = []

    print(response.text)
          
    #arguments for get request
    getArgs = {"fields": "messages{message}", "access_token": PAGE_ACCESS_TOKEN}
    res = requests.get(f"https://graph.facebook.com/{LATEST_API_VERSION}/{CONVERSATION_ID}",
                    params=getArgs)

    #getting current no. of messages in the conversation
    res_json = res.json()

    #new check if recent message is same logic
    latestMessage = res_json["messages"]["data"][0]["message"]

    #old message count logic
    #message_count = len(res_json["messages"]["data"])

    #loop iteration
    i = 1

    #new logic: instead of message count, compare to check if last message in data has changed
    #after a time interval, get request is made, no of messages in the conversation are fetched
    #if they are greater (meaning user typed a new prompt), gpt query is made and answer is posted
    while(True):

        print("-------------------------------------------------------------------")
        print("ITERATION:", i)
        print("\nlatest message = ", latestMessage)

        #time interval to not spam get requests
        time.sleep(5)

        #get request for messages in conversation
        res = requests.get(f"https://graph.facebook.com/{LATEST_API_VERSION}/{CONVERSATION_ID}",
                        params=getArgs)
        
        res_json = res.json()

        #new check if recent message is same logic
        currMessage = res_json["messages"]["data"][0]["message"]

        #old message count logic
        #current no of messages in conversation
        #n = len(res_json["messages"]["data"])

        print("current last message = ", currMessage)

        #if new message has been received
        if (latestMessage != currMessage):

            print("---------------------------ENTERED LOOP----------------------------")

            #gpt query ran
            gptRes = asyncio.run(gptQueryAsync(currMessage))
            answer = gptRes[0]
            print("GPT's Response: ", answer)

            answer = answer.replace('"','')
            answer = answer.replace('\'','')
            answer = answer.replace('\\','')
            answer = answer.replace('/','')

            #set latest message (gpt's response)
            latestMessage = answer

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

            time.sleep(2)

            print("Facebook post response: ", res.json())

        i += 1
        print("-------------------------------------------------------------------")


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