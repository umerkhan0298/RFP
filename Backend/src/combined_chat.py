from dotenv import load_dotenv
import google.generativeai as genai
import os
from PyPDF2 import PdfReader
from langchain.docstore.document import Document
from langchain import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain.memory import ConversationBufferMemory
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_google_genai import ChatGoogleGenerativeAI
import pprint

# Load environment variables
load_dotenv()
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

def read_pdf(file_path):
    pdfreader = PdfReader(file_path)
    text = ''
    for i, page in enumerate(pdfreader.pages):
        content = page.extract_text()
        if content:
            text += content
    return text

def initialize_chat_history(combined_doc):
    history = InMemoryChatMessageHistory()
    history.add_ai_message(combined_doc)
    initial_message = (
        "You are a helpful assistant. All the above texts are from an RFP document. Your task is to provide answers based on this RFP document."
    )
    history.add_user_message(initial_message)
    return history

def ask_bot(llm, history, query):
    history.add_user_message(query)
    response = llm.invoke(history.messages)
    history.add_ai_message(response)
    return response, history

def main():
    file_path = 'D:\\Umer Data\\RFP\\Backend\\RFP document\\CYF2405-WELLNESS-rfp.pdf'
    text = read_pdf(file_path)
    
    docs = [Document(page_content=text)]
    combined_doc = "\n".join([doc.page_content for doc in docs])

    # Print the combined document text
    print(combined_doc)

    # Generate the summary
    summary = generate_summary(docs)
    print("Summary of the document:")
    print(summary)

    # Initialize chat history
    history = initialize_chat_history(combined_doc)
    
    # Initialize the LLM
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-001", temperature=0)

    # Interactive conversation with the bot
    print("Bot: How can I assist you further?")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        response, history = ask_bot(llm, history, user_input)
        # print("Bot:", response.content)
        hist = list(history)

        # Extract the latest AI response
        latest_ai_response = hist[0][1][-1].content
        print("Bot:", latest_ai_response)
        
    # Print chat history
    print("Chat History:")
    for message in history.messages:
        print(f"{message.type}: {message.content}")

if __name__ == "__main__":
    main()
