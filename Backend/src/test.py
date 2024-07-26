from combined_chat import initialize_chat_history, read_pdf, combined_prompt, ask_bot, initial_prompt_for_rfp
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.docstore.document import Document

def main():

    history = initialize_chat_history()
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-001", temperature=0)
    combined_doc = ""
    while True:
        try:
            print("Bot: Welcome to GPT-Maisters! Kindly upload the RFP document.")
            file_path = input("User: ").strip()
            rfp_doc = read_pdf(file_path)
            user_prompt = initial_prompt_for_rfp()
            user_input = combined_prompt(rfp_doc, user_prompt)
            break
        except: 
            pass
    try:
        print("Bot: Kindly upload the relevant Q/A document.")
        file_path = input("User: ").strip()
        QnA_doc = read_pdf(file_path)
        user_prompt = prompt_for_QnA()
        user_input += combined_prompt(rfp_doc, user_prompt)
    except:
        pass
    response, history = ask_bot(llm, history, user_input)
    print("Bot:", response.content)
    while True:
        print("Enter 'upload' to upload a document, 'ask' to ask a prompt, or 'exit' to quit.")
        action = input("User: ").strip().lower()

        if action == 'upload':
            print("Enter the file path of the PDF document.")
            file_path = input("User: ").strip()
            
            try:
                combined_doc += read_pdf(file_path)
                print("Document uploaded successfully.")
            
            except Exception as e:
                print(f"Failed to read the PDF document: {e}")

        elif action == 'ask':
            user_prompt = input("Enter your prompt: ").strip()
            
            if combined_doc:
                user_input = combined_prompt(combined_doc, user_prompt)
                combined_doc = []
            
            else:
                user_input = user_prompt
            response, history = ask_bot(llm, history, user_input)
            print("Bot:", response.content)

        elif action == 'exit':
            break

        else:
            print("Invalid action. Please enter 'upload', 'ask', or 'exit'.")

if __name__ == "__main__":
    main()
