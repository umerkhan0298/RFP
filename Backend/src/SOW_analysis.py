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
import pdfkit
import markdown
from io import BytesIO


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
    The document should be detailed, shouldn't less than 10,000 words, and below is the example of how your table of content should be. 
    You have to find out if its a mobile app or web app and what information should be given in Functional hierarchy
    Ensure to add or remove necessary components smartly. Include detailed functional hierarchies and descriptions of system components such as user apps, admin panels, mobile apps, web apps, etc. 
    The document should contain subsections and detailed answers with more subsections if necessary.

    1.	Objective
    2.	Executive Summary	
    3.	Functional Hierarchy	
    3.1	Functional Hierarchy of the User App	
    3.2	Functional Hierarchy of the Business Interface	
    3.3	Functional Hierarchy of the Admin Panel	
    4.	Functional Details of User App	
    4.1	Downloading the App	
    4.2	Splash Screen	
    4.3	Login	
    4.3.1	Signup	
    4.3.2	Forgot Password	
    4.4	Side Menu	
    4.5	Dashboard	
    4.5.1	Arrived in Parking Lot	
    4.5.2	Waiting for business to respond	
    4.5.3	Business gives the response	
    4.5.3.1	'Please continue the vicinity now, we are waiting'
    4.5.3.2	'Thank you. Remain in the car until you are contacted'	
    4.5.3.3	'Apologies, your appointment is delayed'	
    4.5.3.4	'Apologies, you do not have an appointment for today'
    4.5.3.5	Custom response	
    4.5.4	Countdown timer ends	
    4.5.5	User ends the session	
    4.5.6	Business ends the session	
    4.6	Push Notifications	
    4.7	My profile	
    4.8	Settings	
    4.8.1	Change password	
    4.8.2	Show Notifications	
    4.8.3	About Us	
    4.8.4	Terms & Conditions	
    4.8.5	Privacy Policy	
    4.9	Logout	
    5.	Business Interface	
    5.1	Sign-up	
    5.1.1	Account Sign-up Email	
    5.2	Login	
    5.3	Dashboard	
    5.4	People Waiting in Queue	
    5.4.1	Give Response to User	
    5.4.2	Alert Notifications	
    5.4.2.1	When user arrives in Parking lot	
    5.4.2.2	When countdown timer is up	
    5.4.2.3	When user clicks: Get an update	
    5.4.2.4	When user ends the session	
    5.4.3	End the Session	
    5.5	Reports	
    5.5.1	Daily	
    5.5.2	Weekly	
    5.5.3	Monthly	
    5.6	Settings	
    5.6.1	Business Profile	
    5.6.2	Change Password	
    5.6.3	Show Notifications	
    5.6.4	Terms & Conditions	
    5.6.5	Privacy Policy	
    5.7	Logout	
    6.	Admin Panel	
    6.1	Change Password	
    6.2	User Management	
    6.3	Business Management	
    6.3.1	Businesses List	
    6.3.2	Business Details	
    6.4	Reports	
    6.4.1	Daily	
    6.4.2	Weekly	
    6.4.3	Monthly	
    6.5	Push Notifications	
    6.6	Logout	
    7.	Compliance	
    8.	Tools & Operating Systems	
    8.1	Design Tools for Mobile App	
    8.2	Operating System & Limitations for Mobile App	
    9.	Roles and Responsibility	
    9.1	Customer's Responsibilities	
    9.2	App Maisters Responsibilities	
    10.	Deliverables	
    11.	Assumptions	
    12.	Warranty and Post Production Support	


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

    user_prompt = initial_prompt_for_rfp()

    user_input = combined_prompt(combined_doc, user_prompt)
    
    response, history = ask_bot(llm, history, user_input)
    print("Bot:", response.content)
  
    # Convert Markdown to HTML
    html = markdown.markdown(response.content)

    # Convert HTML to PDF
    pdf = pdfkit.from_string(html, False)

    # Save PDF to a file
    with open("output.pdf", "wb") as file:
        file.write(pdf)


if __name__ == "__main__":
    main()

