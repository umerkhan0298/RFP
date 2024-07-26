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


def initialize_chat_history():
    history = InMemoryChatMessageHistory()
    initial_message = (
        "You are a helpful assistant. Your task is to give the answer from the given document as per the user's prompt."
    )
    history.add_user_message(initial_message)
    return history

def ask_bot(llm, history, query):
    history.add_user_message(query)    
    response = llm.invoke(history.messages)
    history.add_ai_message(response)
    return response, history

def main():
    # Initialize chat history
    history = initialize_chat_history()
    
    # Initialize the LLM
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-001", temperature=0)
    
    file_path = 'D:\\Umer Data\\RFP\\Backend\\RFP document\\CYF2405-WELLNESS-rfp.pdf'
    text = read_pdf(file_path)
    
    docs = [Document(page_content=text)]
    combined_doc = "\n".join([doc.page_content for doc in docs])

    msg1 = combined_doc
    # prompt = "Prompt: What's the deadline?"
    # user_input = f'{msg}\n{prompt}'
    # response, history = ask_bot(llm, history, user_input)
    # print("Bot:", response.content)

    
    file_path = 'D:\\Umer Data\\RFP\\Backend\\RFP document\\CRD_test_ques.pdf'
    text = read_pdf(file_path)
    
    docs = [Document(page_content=text)]
    combined_doc = "\n".join([doc.page_content for doc in docs])

    msg = combined_doc
    prompt = "Prompt: give all the answers of this questions"
    user_input = f'{msg1}\n{msg}\n{prompt}'
    response, history = ask_bot(llm, history, user_input)
    print("Bot:", response.content)
    

    # file_path = 'D:\\Umer Data\\RFP\\Backend\\RFP document\\CYF2405-WELLNESS-rfp.pdf'
    # text = read_pdf(file_path)
    
    # docs = [Document(page_content=text)]
    # combined_doc = "\n".join([doc.page_content for doc in docs])

    # msg = combined_doc
    # prompt = "Prompt: What's the deadline?"
    # user_input = f'{msg}\n{prompt}'
    # response, history = ask_bot(llm, history, user_input)
    # print("Bot:", response.content)

    
    # file_path = 'D:\\Umer Data\\RFP\\Backend\\RFP document\\CRD_test_ques.pdf'
    # text = read_pdf(file_path)
    
    # docs = [Document(page_content=text)]
    # combined_doc = "\n".join([doc.page_content for doc in docs])

    # msg = combined_doc
    # prompt = "Prompt: give all the answers of this questions"
    # user_input = f'{msg}\n{prompt}'
    # response, history = ask_bot(llm, history, user_input)
    # print("Bot:", response.content)
    
    
    
    
    
    # msg = "Document_Info: My name is Umer Khan. I am an AI Engineer from LN Technologies"
    # prompt = "Prompt: Who is Umer"
    # user_input = f'{msg}\n{prompt}'
    # response, history = ask_bot(llm, history, user_input)
    # print("Bot:", response.content)
    
    
    # while True:
    #     user_input = input("You: ")
    #     if user_input.lower() in ["exit", "quit"]:
    #         break
    #     response, history = ask_bot(llm, history, user_input)
    #     # print("Bot:", response.content)
    #     hist = list(history)

    #     # Extract the latest AI response
    #     latest_ai_response = hist[0][1][-1].content
    #     print("Bot:", latest_ai_response)
        
    # # Print chat history
    # print("Chat History:")
    # for message in history.messages:
    #     print(f"{message.type}: {message.content}")

if __name__ == "__main__":
    main()



