from ollama import chat 

messages=[{
    'role' : 'user',
    'content' : "you are a helpful DSA Teacher"
}]

while True:
    user=input("YOU:")

    if(user.lower()=="exit"):
        break

    messages.append({
        'role' : 'user',
        'content' : user
    })

    response = chat(
        model='llama3',
        messages=messages
    )

    bot_reply= response['message']['content']

    print("BOT: ", bot_reply)

    messages.append({
        'role' : 'assistant',
        'content' : bot_reply
    })