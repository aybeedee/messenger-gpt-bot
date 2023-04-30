from gpt4free import you

# simple request with links and details
response = you.Completion.create(
    prompt="Reply to me ONLY in Urdu langauge. Don't speak english. Start doing so from the following prompt: How are you?",
    detailed=False,
    include_links=False, )

print(response.dict())

# {
#     "response": "...",
#     "links": [...],
#     "extra": {...},
#         "slots": {...}
#     }
# }

# chatbot

chat = []

while True:
    prompt = input("You: ")
    if prompt == 'q':
        break
    response = you.Completion.create(
        prompt=prompt,
        chat=chat)

    print("Bot:", response.text)

    chat.append({"question": prompt, "answer": response.text})