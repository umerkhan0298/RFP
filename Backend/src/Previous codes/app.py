from flask import Flask, jsonify, request
from flask_cors import CORS
import json
from langchain.docstore.document import Document
from combined_sum_history import generate_summary, ask_bot, initialize_chat_history
app = Flask(__name__)

CORS(app)

@app.route('/doc_summary', methods = ["GET", "POST"])
def doc_summary():
    data = request.get_json()
    print("here")
    docs = [Document(page_content=data['text'])]
    combined_doc = "\n".join([doc.page_content for doc in docs])

    summary = generate_summary(docs)
    history = initialize_chat_history(combined_doc)
    print(history)
    
    return jsonify({'response': summary['output_text'],
                    'history': history.dict()})

@app.route('/chat_response', methods = ["GET", "POST"])
def chat_response():
    data = request.get_json()
    # Initialize the LLM
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-001", temperature=0)

    response, history = ask_bot(llm, data['history'], data['input'])

    return jsonify({'response': response,
                    'history': history})
# @app.route('/', methods = ["GET", "POST"])
# def checking():
#     data = request.get_json()
#     print(data)
#     return 0

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)