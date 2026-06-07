from ollama import chat
import json
import os

if os.path.exists("chat_history.json"):
   with open("chat_history.json", "r") as f:
      messages=json.load(f)

else:
  messages=[{
    'role' : 'user',
    'content' : 'you are a DSA teacher'
  }]

while True:
    user=input("YOU: ")

    if(user.lower()=='exit'):
        break
    
      
    if user == "/clear":
        print("DEBUG: CLEAR EXECUTED")
        messages = [
            {
                "role": "system",
                "content": "You are a helpful AI assistant."
            }
        ]

        with open("chat_history.json", "w") as f:
            json.dump(messages, f, indent=4)

        print("BOT: Memory Cleared")

        continue

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

    messages.append({
        "role": "assistant",
        "content": bot_reply
    })

    # History save karo
    with open("chat_history.json", "w") as f:
        json.dump(messages, f, indent=4)



#    ✅ Ollama Integration
# ✅ Conversational Memory
# ✅ System Prompts
# ✅ Real-Time Streaming Responses
# ✅ Persistent Chat Storage (JSON)
# ✅ Memory Reset Commands  