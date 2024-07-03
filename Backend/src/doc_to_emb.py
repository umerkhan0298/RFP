import urllib
import warnings

warnings.filterwarnings("ignore")
from pathlib import Path as p
from pprint import pprint
import pandas as pd
from langchain import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
from PyPDF2 import PdfReader
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma, FAISS
from dotenv import load_dotenv
import google.generativeai as genai
import os
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings

load_dotenv()
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))



def get_pdf_text(pdf):
    loader = PyPDFLoader(pdf)
    pages = loader.load()
    return pages

def get_text_chunks(pages):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_documents(pages)
    # print("chunks")
    # print(chunks)
    return chunks


def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    vector_store = FAISS.from_documents(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")
    return vector_store
    # db = Chroma.from_documents(text_chunks, embeddings)
    # db = Chroma.from_documents(text_chunks, embeddings, persist_directory= "chroma_db")
    # db.persist()
    # return db


def get_conversational_chain():

    prompt_template = """
    Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in
    provided context just say, "The document does't contain this information", don't provide the wrong answer\n\n
    Context:\n {context}?\n
    Question: \n{question}\n

    Answer:
    """

    model = ChatGoogleGenerativeAI(model="gemini-1.5-flash-001",
                             temperature=0.2)

    prompt = PromptTemplate(template = prompt_template, input_variables = ["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

    return chain



def user_input(user_question, vector_store):
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    
    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    docs = new_db.similarity_search_with_relevance_scores(user_question)

    # new_db = Chroma("chroma_db", embeddings)
    # new_db = Chroma(vector_store, embeddings)
    # docs = new_db.similarity_search_with_score(user_question)

    # new_db = Chroma(vector_store, embeddings)
    # retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 3})
    # docs = new_db.get_relevant_documents(user_question)
    for i in docs:
        print("docs")
        print(i)
    # chain = get_conversational_chain()

    
    # response = chain(
    #     {"input_documents":docs, "question": user_question}, 
    #     return_only_outputs=True)

    # print("response", response)



def main():
    
    pdf_file = "D:\\Umer Data\\RFP\\Backend\\RFP document\\CYF2405-WELLNESS-rfp.pdf"
    text = get_pdf_text(pdf_file)
    print("text done", len(text))
    
    text_chunks = get_text_chunks(text)
    print("chunks done", len(text_chunks))

    vector_store = get_vector_store(text_chunks)
    print("database done")
    user_question = "what's PROPOSAL DELIVERY"
    user_input(user_question, vector_store)
    print("finally done")

if __name__ == "__main__":
    main()