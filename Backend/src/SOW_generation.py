from dotenv import load_dotenv
import google.generativeai as genai
import os
from langchain_google_genai import ChatGoogleGenerativeAI
import pdfkit
import markdown
from combined_chat import (initialize_chat_history, read_pdf, combined_prompt, 
                           ask_bot, initial_prompt_for_rfp, prompt_for_QnA, 
                           prompt_for_Additional_docs, functionality_of_functional_hierarchy,
                           functionality_of_non_functional, combine_responses, prompt_for_CRD)

import time
# Load environment variables
load_dotenv()
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))


def generate_pdf_from_response(response, output_num):
    # Convert Markdown to HTML
    html = markdown.markdown(response)

    # Convert HTML to PDF
    pdf = pdfkit.from_string(html, False)

    # Save PDF to a file
    with open(f"Output responses/output_{output_num}.pdf", "wb") as file:
        file.write(pdf)


def main():
    history = initialize_chat_history()
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-001", temperature=0)
    combined_doc = ""
    QnA_doc = ""
    additional_doc = ""

    # Asking to upload the RFP 
    while True:
        try:
            print("Bot: Welcome to GPT-Maisters! Kindly upload the RFP document.")
            # file_path = input("User: ").strip()
            file_path = "D:\\Umer Data\\RFP\\Backend\\RFP document\\Sole_power RFP.pdf"
            rfp_doc = read_pdf(file_path)
            user_prompt = initial_prompt_for_rfp()
            user_input = combined_prompt(rfp_doc, user_prompt)
            print("Document uploaded successfully.")   
            break
        except: 
            pass

    # Asking to upload Q/A documents 

    while True:
        try:
            print("Bot: Kindly upload the relevant Q/A documents or write 'next' for the next step.")
            # file_path = input("User: ").strip()
            file_path = 'next'
            if file_path == 'next':
                break
            else:
                try:
                    QnA_doc += read_pdf(file_path)
                    print("Document uploaded successfully.")   
                
                except Exception as e:
                    print(f"Failed to read the PDF document: {e}")
        except:
            pass
    
    if QnA_doc:
        user_prompt = prompt_for_QnA()
        user_input += combined_prompt(QnA_doc, user_prompt)    


    # Asking to upload additional documents 

    while True:
        try:
            print("Bot: Kindly upload the additional documents or write 'next' for the next step.")
            # file_path = input("User: ").strip()
            file_path = 'next'
            if file_path == 'next':
                break
            else:
                try:
                    additional_doc += read_pdf(file_path)
                    print("Document uploaded successfully.")   
                
                except Exception as e:
                    print(f"Failed to read the PDF document: {e}")
        except:
            pass
    
    if additional_doc:
        user_prompt = prompt_for_Additional_docs()
        user_input += combined_prompt(additional_doc, user_prompt)  

    # print(user_input)
    # response, history = ask_bot(llm, history, user_input)
    # print("Bot:", response.content)
    history.add_user_message(user_input)
    
    output_num = 0
    
    start_time = time.time()

    # response, history = functionality_of_functional_hierarchy(llm, history)
    # print("Bot:", response.content)
    # # print("history: ", list(history))
    # functional_req_response = response.content
    # print(time.time() - start_time)

    # history = initialize_chat_history()
    # history.add_user_message(user_input)


    response, history = functionality_of_non_functional(llm, history)
    print("Bot:", response.content)
    # print("history: ", list(history))
    
    print(time.time() - start_time)

    ############### Temporary #############
    
    functional_req_response = read_pdf('D:\\Umer Data\\RFP\\Backend\\src\\Output responses\\D:\Umer Data\RFP\Backend\src\Output responses\Functional_hierarchy_markdown.pdf.pdf')
    history.add_user_message(functional_req_response)

    #######################################
    
    history.add_user_message(functional_req_response)

    response, history = combine_responses(llm, history)
    print("Bot:", response.content)
    # print("history: ", list(history))

    print(time.time() - start_time)


    # Asking to Generating CRD 

    while True:
        try:
            print("Bot: Do you want to generate the CRD as well. Write 'yes' or 'no'.")
            query = input("User: ").strip().lower()
            # query = 'yes'
            if query == 'no':
                break
            elif query == 'yes':
                CRD_prompt = prompt_for_CRD() 
                response, history = ask_bot(llm, history, CRD_prompt)
            else:
                pass
        except:
            pass
    

    # chatting functionality

    while True:
        print("Bot: Enter 'upload' to upload a document, 'ask' to ask a prompt, 'generate' to generate the previous response or 'exit' to quit.")
        action = input("User: ").strip().lower()
        
        # Uploading any document
         
        if action == 'upload':
            print("Enter the file path of the PDF document.")
            file_path = input("User: ").strip()
            
            try:
                combined_doc += read_pdf(file_path)
                print("Document uploaded successfully.")
            
            except Exception as e:
                print(f"Failed to read the PDF document: {e}")


        # asking user query

        elif action == 'ask':
            user_prompt = input("Enter your prompt: ").strip()
            
            if combined_doc:
                user_input = combined_prompt(combined_doc, user_prompt)
                combined_doc = []
            
            else:
                user_input = user_prompt
            response, history = ask_bot(llm, history, user_input)
            print("Bot:", response.content)

        # generating previous response

        elif action == "generate":
            generate_pdf_from_response(response.content, output_num)
            print(f"PDF generated as output_{output_num}.pdf")
            output_num += 1

        # end the conversation

        elif action == 'exit':
            break

        else:
            print("Invalid action. Please enter 'upload', 'ask', or 'exit'.")

if __name__ == "__main__":
    main()
