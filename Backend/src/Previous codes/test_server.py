from test import read_pdf, generate_summary
from langchain.docstore.document import Document
import requests

file_path = 'D:\\Umer Data\\RFP\\Backend\\RFP document\\CYF2405-WELLNESS-rfp.pdf'
text = read_pdf(file_path)
data = {'text':text}

response = requests.post("http://127.0.0.1:5000/doc_summary", json=data)
response = response.json()
print(response['response'])
print(response['history'])
