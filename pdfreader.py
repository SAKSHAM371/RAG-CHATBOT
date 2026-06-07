from ollama import chat
import json
import os
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

reader = PdfReader("FRONTENDRESUME.pdf")

text = ""

for page in reader.pages:
    extracted = page.extract_text()

    if extracted:
        text += extracted + "\n"

print("Total Characters:", len(text))

def chunk_text(text, chunk_size=400, overlap=100):

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunks.append(text[start:end])

        start += chunk_size - overlap

    return chunks


chunks = chunk_text(text)

print("Total Chunks:", len(chunks))

print("Loading Embedding Model...")

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

embeddings = model.encode(
    chunks,
    normalize_embeddings=True
)

print("Embedding Dimension:", embeddings.shape[1])

dimension = embeddings.shape[1]

# Cosine Similarity
index = faiss.IndexFlatIP(dimension)

index.add(
    np.array(embeddings).astype("float32")
)

print("Vectors Stored:", index.ntotal)

if os.path.exists("chat_history.json"):

    with open("chat_history.json", "r") as f:
        messages = json.load(f)

else:
    messages = []

while True:

    user = input("\nYOU: ")

    if user.lower() == "exit":
        break

    if user.lower() == "/clear":

        messages = []

        with open("chat_history.json", "w") as f:
            json.dump(messages, f, indent=4)

        print("BOT: Memory Cleared")
        continue

    query_embedding = model.encode(
        [user],
        normalize_embeddings=True
    )
    D, I = index.search(
        np.array(query_embedding).astype("float32"),
        k=3
    )

    retrieved_text = ""

    for idx in I[0]:
        retrieved_text += chunks[idx]
        retrieved_text += "\n\n"

    prompt = f"""
You are a helpful AI assistant.

Answer ONLY from the provided context.

Rules:
1. Do not make up information.
2. If answer is not present in context, say:
   "I could not find that information in the PDF."
3. Keep answers concise.

CONTEXT:
{retrieved_text}

QUESTION:
{user}
"""
    messages.append({
        "role": "user",
        "content": user
    })

    stream = chat(
        model="llama3",
        messages=[
            {
                "role": "system",
                "content": "Answer only from provided context."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        stream=True
    )

    print("BOT: ", end="")

    bot_reply = ""

    for chunk in stream:

        content = chunk["message"]["content"]

        print(content, end="", flush=True)

        bot_reply += content

    print()

    messages.append({
        "role": "assistant",
        "content": bot_reply
    })

    with open("chat_history.json", "w") as f:
        json.dump(messages, f, indent=4)

print("\nGoodbye!")