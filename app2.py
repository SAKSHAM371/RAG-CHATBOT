from ollama import chat

messages=[{
    'role' : 'user',
    'content' : 'you are a DSA teacher'
}]

while True:
    user=input("YOU: ")

    if(user.lower()=='exit'):
        break

    messages.append({
        'role' : 'user',
        'content' : user
    })

    stream = chat(
        model='llama3',
        messages=messages,
        stream=True
    )
    # khaali string use krenge taaki poora explanation aa jaaye 
    print("BOT: ",end="")
  
    bot_reply = ""
    # loop chla hai jbtk poora explanation khtm na ho jata   
    for chunk in stream:
      content = chunk['message']['content']
    # flush true mtlb message turant aate hi display kr dega screen pr
      print(content, end="", flush=True)

      bot_reply += content

print()