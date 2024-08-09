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
    You are a software company named App Maisters tasked with writing a comprehensive Scope of Work (SOW) document for a software development project based on the given RFP. 
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
    'Now add a detailed description for each task and its corresponding subtasks until you reach the last subtask. Each description should be detailed and around 100 words or more if needed. Write the description in such a way that should be include in a Scope of Work. There would not be any heading of description, the description will lie under the corresponding heading of sub tasks.',
    'There should be main headings of the functional hierarchy of specific roles and the functional details of specific roles (specific roles will contain names of all the major roles). The functional hierarchy will contain all the roles and will show the hierarchy and names of all the tasks and their subtasks where the functional details will contain the details of each sub tasks. Make sure do not miss any detail of sub task, if the subtask is written in hierarchy then its details and heading should be there in functional details with same hierarchichal format. The hierarchy of tasks should be like 1, 1.1, 1.1.1 in a proper hierarchichal markdown format',
    'In functional details make sure every tasks contain summary section and every sub tasks should contain a summary section where it will be a summary of the detail description. The name of heading will be summary and description of sepcific task or sub task',
    'Generate the same response again but make sure this time functional hierarchy contains all the headings which is included in the functional details also make sure do not miss any heading in functional hierarchy. Also generate in proper markdown format.'
    ]
    
    for query in ques:
        response, history = ask_bot(llm, history, query)
        print("query: ", query)

    return response, history
 

def functionality_of_non_functional(llm, history):
    
    ques = [
    '''
    write a proper SOW while keeping all the above document in mind and specially it should be based on the given RFP. Each heading must be more than 100 words. The table of content should be like that.
    1. Overview
    2. Executive summary
    3. all the non functional headings
    4. Reports
    5. Complaince
    6. Tools and Operating Systems
    7. Roles and Responsibility
    8. Deliverables
    9. Assumptions
    10. HIPPA- PHI COMPLIANCE DATA ENCRYPTION (if asked in RFP or any other)

    Note: All the headings will be written based on the given RFP. Make sure the non functional requirement contains multiple headings and sub sections and each subsections should contain around 100 words). Don't add extra Table of content from your side other than the above given table of content, just make these headings detailed as much as you can.
    The executive summary should contain the how we will make this app.
    '''
    ]
    
    for query in ques:
        response, history = ask_bot(llm, history, query)

    return response, history

def combine_responses(llm, history):
    
    ques = [
    '''
    Now add this Functional hierarchy and functional details in this SOW. Make sure both Functional hierarchy and functional details heading will be add as it is you don't need to update this.
    Just add these headings after executive summary and all the remaining content will be same.
    The document should be in proper Markdown format.
    Also must add the table of content at the start as well for the below content. Make sure the table contains each content including Functional hierarchy (each sections and subsections) with their numbers like 1, 1.1,1.1.1 etc.
    '''
    ]
    
    for query in ques:
        response, history = ask_bot(llm, history, query)

    return response, history

def prompt_for_CRD():

    prompt = '''
    
    please write a detailed critical review document based on the given RFP that addresses the following 27 questions related to the project proposal:

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



