import streamlit as st
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

# Streamlit App
st.set_page_config(page_title="Chatbot with PDF Upload", layout="wide")

# Initialize chatbot components
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-001", temperature=0)
history = InMemoryChatMessageHistory()

# Sidebar for file upload
st.sidebar.title("Upload PDF")
uploaded_file = st.sidebar.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file:
    pdfreader = PdfReader(uploaded_file)
    text = ''
    for i, page in enumerate(pdfreader.pages):
        content = page.extract_text()
        if content:
            text += content

    docs = [Document(page_content=text)]
    combined_doc = "\n".join([doc.page_content for doc in docs])

    # Display the uploaded document
    st.sidebar.subheader("Uploaded Document")
    st.sidebar.text_area("Document Content", combined_doc, height=300)

    # Create the system prompt template
    template = '''
    Please write a comprehensive summary for the project proposal, ensuring to include detailed information on technology, deadlines, budget, and all other relevant details. The summary should address the following key points:

    Technology involved
    Proposal submission deadline
    Budget details
    Any other relevant information

    Also, please write Scope of work (SOW), ensuring to include detailed information on project objectives, deliverables, tasks, timeline, milestones, technical requirements, budget, resources, stakeholders, and acceptance criteria.

    Also, please write Our Understanding Document (OUD), ensuring to include detailed information on project background, objectives, scope, deliverables, timeline, key assumptions, constraints, risks, responsibilities of each party, and any specific requirements or expectations.

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
    Is there any company that’s already working with them (incumbent)? If there is, please name the company name and the website.
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

    Summary: {text}

    In the end you need to ask from the user something like that If I missed any information or you need an explanation of anything from this RFP document, please ask.
    '''

    prompt = PromptTemplate(
        input_variables=['text'],
        template=template
    )

    # Load the chain with the prompt
    chain = load_summarize_chain(
        llm=llm,
        chain_type="stuff",
        prompt=prompt,
        verbose=False
    )

      # Generate the summary
    summary = chain.invoke(docs)

    # Add the initial summary to the conversation history
    history.add_ai_message(combined_doc)
    # st.session_state.messages = [("Bot", summary['output_text'])]
    # st.session_state.messages.append({"role": "assistant", "content": summary['output_text']})
    st.chat_message("assistant").write(summary['output_text'])
# # Middle section for chatbot interaction
# st.title("Conversational Chatbot")

# if "messages" not in st.session_state:
#     st.session_state.messages = []

def ask_bot(query):
    history.add_user_message(query)
    response = llm.invoke(history.messages)
    history.add_ai_message(response)
    return response

# # Chat input
# query = st.text_input("You: ", key="input_text")
# if st.button("Send"):
#     response = ask_bot(query)

# # Display chat history
# for user, msg in st.session_state.messages:
#     st.text_area(user, msg, height=100, key=f"{user}_{msg}")

# # Left side for chat history
# st.sidebar.title("Chat History")
# for user, msg in st.session_state.messages:
#     st.sidebar.text_area(user, msg, height=50, key=f"history_{user}_{msg}")


# st.title("Conversational Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# # Display chat messages from history on app rerun
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input():
    # Add user message to chat history
    # st.session_state.messages.append({"role": "user", "content": prompt})
    

    # st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    print("user:", prompt)
    response = ask_bot(prompt)
    
    msg = response.content
    print("AI:", msg)
    # st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)