from flask import Flask, request, render_template
import google.generativeai as genai
from dotenv import load_dotenv
import os
from result import result
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage


load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model=genai.GenerativeModel("gemini-2.5-flash")


app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.form['message']
    try:
        prompt_template = ChatPromptTemplate([("system", "You are an expert in Langchain framework. You need to answer the queries realted to this. You need to answer like you are explaining to a person who doesnt know anything about this framework and the answer should always be direct to the point and should be easy to understand. If questions were apart from this framework, remian them that you are a langchain bot so wont be able to answer the query. Give reply if it is about greetings"), MessagesPlaceholder("msgs")])
        messages = [HumanMessage(content=user_message)]
        formatted_prompt = prompt_template.format_prompt(msgs=messages)
        formatted_prompt=formatted_prompt.to_string()
        print(formatted_prompt)
        bot_response=result(formatted_prompt,model)
    except Exception as e:
        bot_response = f"Error: {e}"
    return bot_response

if __name__ == '__main__':
    app.run(debug=True)