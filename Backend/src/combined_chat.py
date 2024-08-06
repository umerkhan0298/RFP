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

def functionality_of_functional_hierarchy(llm, history):
    
    ques = [
    'can you specify which type of app this rfp wants is it web app, mobile app or any other or both',
    'can you specify the user roles based on that app based on the rfp',
    'Now based on that roles write a proper functional hierarchy of each roles, each hierarchy should contain sub sections and each sub sections should contain more sub sections and it should be detailed. Functional heirarchy of specific role might contains all the technicality like login, signup, logout functionality, all the dashboards and many more based on that role.',
    'make it more technical and it should be look like all these information will be add in technical Scope of work containing all the detailed information of each functionality. Make sure the heading should be Functional Hierarchy of specific role and then all the info will be in that and then similarly for all the roles. Make sure the sub sections should contain detailed information and should contain all the functionality and requirements given in the RFP.',
    'Now add a detailed, paragraphic description for each task and its corresponding subtasks until you reach the last subtask. Each description should be detailed and around 100 words or more if needed. Write the description in such a way that should be include in a Scope of Work. There would not be any heading of description, the description will lie under the corresponding heading of sub tasks. The description of last subtask should not be in points, it should be a paragraph.',
    'There should be main headings of the functional hierarchy of specific roles and the functional details of specific roles (specific roles will contain names of all the major roles). The functional hierarchy will contain all the roles and will show the hierarchy and names of all the tasks and their subtasks where the functional details will contain the details of each sub tasks. Make sure do not miss any detail of sub task, if the subtask is written in hierarchy then its details should be there in functional details. The hierarchy of tasks should be like 1, 1.1, 1.1.1 in a proper hierarchichal markdown format'
    ]
    
    for query in ques:
        response, history = ask_bot(llm, history, query)

    return response, history
 
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



