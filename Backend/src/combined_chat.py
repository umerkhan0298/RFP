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
    docs = [Document(page_content=text)]
    combined_doc = "\n".join([doc.page_content for doc in docs])
    return combined_doc


def initialize_chat_history():
    history = InMemoryChatMessageHistory()
    initial_message = (
        "You are a helpful assistant. Your name is GPT Maisters. Your task is to provide the answer from the given document as per the user's prompt."
    )
    history.add_user_message(initial_message)
    return history

def combined_prompt(document_text, user_prompt):
    document_info = f"Document_Info: {document_text}"
    prompt = f"Prompt: {user_prompt}"
    user_input = f'{document_info}\n{prompt}'
    return user_input

def initial_prompt_for_rfp():
    
    prompt = '''
    You are a software company tasked with writing a comprehensive Scope of Work (SOW) document for a software development project based on the given RFP. 
    Give the response of user query accordingly.
    ''' 
    return prompt

def prompt_for_QnA():

    prompt = '''
    You have been provided with an RFP (Request for Proposal) document and a Q/A document containing additional questions and answers from the client regarding the RFP. 
    Give the response of user query accordingly based on RFP and Q/A documents.
    ''' 
    return prompt
    
def prompt_for_Additional_docs():

    prompt = '''
    You have been provided with an RFP (Request for Proposal) document, Q/A documents and some additional documents which are supporting the RFP. 
    Give the response of user query accordingly based on all these documents.
    ''' 
    return prompt

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
    combined_doc = read_pdf(file_path)
    
    
    
    user_input = combined_prompt(combined_doc, user_prompt)
    response, history = ask_bot(llm, history, user_input)
    print("Bot:", response.content)


if __name__ == "__main__":
    main()



