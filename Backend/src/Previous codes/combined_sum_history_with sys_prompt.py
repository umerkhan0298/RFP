from dotenv import load_dotenv
import google.generativeai as genai
import os
from PyPDF2 import PdfReader
from langchain.docstore.document import Document
from langchain import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain.memory import ConversationBufferMemory
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain.memory.buffer import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.llm import LLMChain
from langchain_core.prompts.chat import ChatPromptTemplate

from langchain_core.runnables.passthrough import RunnablePassthrough, RunnableParallel

# Load environment variables
load_dotenv()
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

# Provide the path of the PDF file/files
pdfreader = PdfReader('D:\\Umer Data\\RFP\\Backend\\RFP document\\CYF2405-WELLNESS-rfp.pdf')

# Read text from PDF
text = ''
for i, page in enumerate(pdfreader.pages):
    content = page.extract_text()
    if content:
        text += content

docs = [Document(page_content=text)]
combined_doc = "\n".join([doc.page_content for doc in docs])

print(combined_doc)
# Initialize the LLM
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-001", temperature=0)

# Create the system prompt template
template = '''
Please write a comprehensive summary for the project proposal, ensuring to include detailed information on technology, deadlines, budget, and all other relevant details. The summary should address the following key points:

Technology involved
Proposal submission deadline
Budget details
Any other relevant information

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
print("Summary of the document:")
print(summary)
print("\n\n")

history_prompt = '''
 You are a helpful assistant. 
 The given large text is the information of an Request For Proposal (RFP) document. Your task is to provide answers based on this RFP document.
 Document: {text}
'''


hist_prompt = PromptTemplate(input_variables=['text'],template=history_prompt)

# chain_history_msg = llm | hist_prompt

# chain_history_msg = (
#     {"context": docs, "question": RunnablePassthrough()}
#     | hist_prompt
#     | llm
# )

# retrieval = RunnableParallel(
#     {"context": combined_doc, "question": RunnablePassthrough()}
# )

chain_history_msg = llm | hist_prompt

memory = ConversationBufferMemory(return_messages=True)

memory.chat_memory.add_ai_message(chain_history_msg.invoke(hist_prompt.format(text=docs)))

# Function to handle user queries
def ask_bot(query):
    memory.chat_memory.add_user_message(query)
    response = chain_history_msg.invoke(memory.chat_memory.messages)
    memory.chat_memory.add_ai_message(response)
    return response

# Example conversation
print("Bot: How can I assist you further?")
while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        break
    response = ask_bot(user_input)
    print("Bot:", response)


# memory.chat_memory.add_ai_message("you are a helpful assistant")
# memory = ConversationBufferMemory(return_messages=True)
# memory.chat_memory.add_ai_message(llm.invoke(memory.chat_memory.messages))
# res = memory.chat_memory.add_user_message("hi! my name is umer")
# memory.chat_memory.add_ai_message(llm.invoke(memory.chat_memory.messages))
# res2 = memory.chat_memory.add_user_message("what's my name?")
# # memory.chat_memory.add_ai_message("I am fine, thank you and you?")

print(memory.chat_memory.messages)