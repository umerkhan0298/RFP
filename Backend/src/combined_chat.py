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
    I need you to write a comprehensive Scope of Work (SOW) document for a Given RFP document. The SOW should cover the following sections:

    1. Overview:

    A brief description of the project, its goals, and objectives.
    The target audience for the project (e.g., public users, staff, specific demographics).
    The purpose and benefits of the project.
    2. Objective:

    Clearly state the main goal of the project and its significance.
    Mention any specific challenges or limitations the project aims to address.
    Outline the intended outcome of the project and its impact.
    3. Functional Requirements:

    User Interface:
    Describe the overall design principles and user experience expectations (e.g., modern, responsive, accessible).
    Outline specific UI elements and features, including:
    Display font size and customization options.
    Dynamic section boxes, their functionality, and editing capabilities.
    Multiple-language translation support (including search and results).
    SMS sharing feature (including the user interface).
    A notification center for alerting users (including alert types and criteria).
    Other Functional Requirements:
    List any additional functionality that needs to be included in the system, beyond the user interface.
    4. Non-Functional Requirements:

    Application Configuration and Development Framework:
    Specify the hosting environment (e.g., IIS, on-premise).
    Outline the development stack (e.g., ASP.NET, SQL Server).
    Mention any specific technologies or libraries to be used.
    Compliance:
    Indicate any relevant compliance standards the project needs to meet (e.g., ADA WCAG, HIPAA).
    Security:
    Discuss security measures, including:
    Immutable logs of user access and changes.
    Data encryption and access control.
    Mobile SDK Development:
    Indicate the need for a mobile SDK and its functionality.
    Clarify the development approach and any support required.
    CI/CD Pipelines:
    Describe the Continuous Integration and Continuous Deployment pipeline.
    Outline the process for updating Al weight files, firmware files, and deploying new Al models.
    5. Assumptions:

    List any assumptions or pre-existing conditions that are essential for the project's successful completion.
    Clarify how any unaddressed assumptions or changes in scope will be handled.
    6. Warranty and Postproduction Support:

    Outline the warranty period and support agreement.
    Specify the support channels available (e.g., email, phone).
    Clarify the support availability (e.g., working hours).
    Mention any specific support limitations or exclusions.
    7. Project Timeline and Budget:

    Include a timeline for the project, breaking down key milestones and deliverables.
    Provide a budget breakdown for the project, including estimated costs for development, testing, deployment, and ongoing maintenance.
    8. Additional Information:

    Include any other relevant information or details that are not covered in the previous sections.

    Also, please write a detailed critical review document that addresses the following 27 questions related to the project proposal:

    Is it a new app or an existing app?
    Is this a federal, state, local, or school RFP?
    Is this a small business or is 8a set aside?
    Is there agency preference for any IDIQ Contract Vehicle?
    What is the high-level SOW/summary?
    Is it relevant to us and can we do this on our own?
    What government agency is this proposal for? Please name the agency.
    What is the proposal submission deadline?
    What are the requirements for submission? Please list all of them.
    Are there any obvious show-stoppers?
    Have we contacted the contracting officer? Who is he/she? Name/Email/Phone number?
    What is the length of the contract?
    Do we have two weeks to work on this?
    Is there any company that's already working with them (incumbent)? If there is, please name the company name and the website.
    Is the incumbent also bidding for this opportunity?
    Is it a buy option (Off the shelf) or a build (Custom Development)?
    Will the application be hosted on Cloud or on the client premise?
    How many client references are required in the proposal and what should be their qualification?
    How do we submit the proposal? Email? Bid website? Sealed Proposal? (Add email, links, or address)? How many copies?
    Is there a budget defined in the proposal? If yes, what is the budget or details for costing/pricing?
    Are there any compliances required for this opportunity?
    Is there a pre-proposal conference date and link? Please provide the date and time for it.
    Is the Q&A pre-proposal conference mandatory?
    What is the questionnaire submission deadline?
    Please attach Q&A responses for the opportunity.
    Is the information clear to the business analyst?
    Is there any requirement that has to be clarified from the agency by our BA?

    ''' 
    return prompt

def prompt_for_QnA():

    prompt = '''
    You have been provided with an RFP (Request for Proposal) document and a Q/A document containing additional questions and answers from the client regarding the RFP. 
    Generate the SOW and CRD based on the previous instructions while keeping these Questions and Answers with client in mind.

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



