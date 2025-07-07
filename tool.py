from flask import Flask, request, jsonify, render_template
from langchain_tavily import TavilySearch
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
import os
#from langgraph.checkpoint.memory import MemorySaver


tool = Flask(__name__)

load_dotenv()
search = TavilySearch(
    name="weather_search",
    description="Use this tool to look up current weather in a specific location. Only use it for weather-related questions. Else answer by your own."
)
tools = [search]

model = init_chat_model("gemini-2.0-flash", model_provider="google_genai")


#memory = MemorySaver()
#agent_executor = create_react_agent(model, tools, checkpointer=memory)

'''config = {
    "configurable": {
        "thread_id": "xyc123"  
    }
}'''
agent_executor = create_react_agent(model, tools)


@tool.route("/")
def index():
    return render_template("chatbot.html")


@tool.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    input_message = {"role": "user", "content": user_message}
    
    try:
        final_message = None

        for step in agent_executor.stream(
            {"messages": [input_message]}, config={}, stream_mode="values"
        ):
            final_message = step["messages"][-1] 
            print(final_message)

        if final_message:
            return jsonify({"reply": final_message.content})
        else:
            return jsonify({"reply": "No response received."}), 500

    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}"}), 500

if __name__ == "__main__":
    tool.run(debug=True)
