from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain import PromptTemplate
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import CTransformers
from langchain.chains import RetrievalQA
# import chainlit as cl
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
import google.generativeai as genai
import os

DATA_PATH = 'D:\\Umer Data\\RFP\\Backend\\RFP document\\'

load_dotenv()
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


DB_FAISS_PATH = 'faiss_index'
# Use the following given information to answer the user's question. Make sure you answer only related to given information.
# If you don't know the answer, just say that I don't know, don't try to make up an answer.
# You are a helpful assistant and Use the following given information to answer the user's question.
custom_prompt_template = """You are a highly intelligent and insightful language model. Your task is to provide the best possible answer to questions based on a given document. Follow these guidelines:

Accuracy: Ensure your answer is factually correct and directly derived from the document.
Relevance: Focus on the most pertinent information related to the question.
Clarity: Provide answers that are clear, concise, and easy to understand.
Comprehensiveness: Include all necessary details to fully address the question without unnecessary information.
Contextual Awareness: Consider the context within the document to provide the most relevant response.
Adaptability: Understand and respond to both short and detailed questions effectively.
Conversational Tone: Answer in a conversational manner as if you are the document itself. Do not start responses with phrases like "The document states that..."
Context: {context}
Question: {question}

Helpful answer:
"""


# Loading the model
def load_llm():
    model_info = genai.get_model('models/gemini-1.5-flash-001')
    print(model_info.input_token_limit, model_info.output_token_limit)   
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-001",
                             temperature=1)
    # print("tokens",(llm.input_token_limit, llm.output_token_limit))
    return llm


def set_custom_prompt():
    """
    Prompt template for QA retrieval for each vectorstore
    """
    prompt = PromptTemplate(template=custom_prompt_template,
                            input_variables=['context', 'question'])
    return prompt


# Retrieval QA Chain
def retrieval_qa_chain(llm, prompt, db):
    qa_chain = RetrievalQA.from_chain_type(llm=llm,
                                           chain_type='stuff',
                                           retriever=db.as_retriever(search_kwargs={'k': 3}),
                                           return_source_documents=False,
                                           chain_type_kwargs={'prompt': prompt}
                                           )
    return qa_chain


# QA Model Function
def qa_bot(query):
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    db = FAISS.load_local(DB_FAISS_PATH, embeddings, allow_dangerous_deserialization=True)
    # docs = db.similarity_search_with_relevance_scores(query=query, k=3)
    # ret = db.as_retriever(search_kwargs={'k': 2})
    # print("Ret", ret)
    # for i in docs:    
    #     print("similarity\n\n")
    #     print(i)
    llm = load_llm()
    qa_prompt = set_custom_prompt()
    qa = retrieval_qa_chain(llm, qa_prompt, db)

    return qa


# output function
def final_result(query):
    qa_result = qa_bot(query)
    response = qa_result({'query': query})
    return response


# qa_result = qa_bot()
# print(qa_result)
# while True:
#     query = input("ask anything related to pdf\n")
#     print(qa_result)
#     if query == 'q':
#         break
#     # response = qa_result(query, return_only_outputs=True)
#     response = qa_result({'query': query})
#     print(response)


# def update_new_info(query, db):

#     similar = db.similarity_search(query=query, k=2)
#     print("page_content:", similar[0].page_content)
#     df = store_to_df(db)
#     print(df['content'])
#     for i in range(len(df['content'])):
#         if similar[0].page_content in df['content'][i]:
#             print("got it", df['chunk_id'][i])
#             chunk_id = df['chunk_id'][i]

print(final_result("what is the scope of the document"))
# # chainlit code
# @cl.on_chat_start
# async def start():
#     chain = qa_bot()
#     msg = cl.Message(content="Starting the bot...")
#     await msg.send()
#     msg.content = "Hi, Welcome to Banking Bot. What is your query?"
#     await msg.update()
#
#     cl.user_session.set("chain", chain)
#
#
# @cl.on_message
# async def main(message):
#     chain = cl.user_session.get("chain")
#     cb = cl.AsyncLangchainCallbackHandler(
#         stream_final_answer=True, answer_prefix_tokens=["FINAL", "ANSWER"]
#     )
#     # cb.answer_reached = True
#     res = await chain.acall(message, callbacks=[cb])
#     print(res)
#     answer = res["result"]
#     # sources = res["source_documents"]
#     #
#     # if sources:
#     #     answer += f"\nSources:" + str(sources)
#     # else:
#     #     answer += "\nNo sources found"
#
#     await cl.Message(content=answer).send()

def store_to_df(store):
    v_dict = store.docstore._dict
    data_rows = []
    for k in v_dict.keys():
        doc_name = v_dict[k].metadata['source'].split('/')[-1]
        page_number = v_dict[k].metadata['page'] + 1
        content = v_dict[k].page_content
        data_rows.append({"chunk_id": k, "document": doc_name, "page": page_number, "content": content})
    vector_df = pd.DataFrame(data_rows)
    return vector_df
