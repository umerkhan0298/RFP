from dotenv import load_dotenv
import textwrap
import google.generativeai as genai
import os
from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_core.chat_history import InMemoryChatMessageHistory


load_dotenv()
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

llm = ChatGoogleGenerativeAI(model="gemini-pro")

# result = llm.invoke("how to make tea")

# print(f"Token count: {token_count}")

# with open("response.txt", 'w') as file:
#     for line in result.content:
#         file.write(line)

history = InMemoryChatMessageHistory()

history.add_ai_message("hi Ask me anything about cricket")
# history.add_user_message("which pitch is better")

# history.add_ai_message(llm.invoke(history.messages))
history.add_user_message("what is the size of it")

print(history.messages)
response = llm.invoke(history.messages)
print(response)