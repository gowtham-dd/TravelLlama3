from flask import Flask, render_template, request, jsonify
import os
from constants import google_api_key,GROQ_API_KEY
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_models import ChatOllama
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# LLM setup
# llm = ChatGoogleGenerativeAI(
#     model="gemini-2.5-pro",
#     google_api_key=google_api_key,
#     temperature=0.7
# )

# llm = ChatOllama(
#     model="llama3",
#     temprature=0.7,         # Model name in Ollama (check with `ollama list`)
#     base_url="http://localhost:11434"  # Ollama server URL
# )

groq_api_key = os.environ['GROQ_API_KEY']



llm = ChatGroq(groq_api_key=groq_api_key, model_name="llama-3.1-8b-instant")

# Prompts
first_input_prompt = PromptTemplate(
    input_variables=['name'],
    template="List the top tourist places in {name} with short highlights."
)
second_input_prompt = PromptTemplate(
    input_variables=['place'],
    template="Create a detailed travel plan to visit all {place} in order with timings."
)
third_input_prompt = PromptTemplate(
    input_variables=['plan'],
    template="""
    Based on this plan: {plan}

    1. Give me a detailed flow with transportation (train/flight/bus), timings, and approx cost.
    2. STRICTLY return at the end a JSON object with the key "route".
       - route is an array of objects, each with:
         - "name": landmark or attraction name
         - "city": city name
         - "coords": [latitude, longitude]
    """
)



# Memory
place_memory = ConversationBufferMemory(input_key='name', memory_key='chat_history')
plan_memory = ConversationBufferMemory(input_key='place', memory_key='chat_history')
cost_memory = ConversationBufferMemory(input_key='plan', memory_key='description_history')

# Chains
chain1 = LLMChain(llm=llm, prompt=first_input_prompt, output_key='place', memory=place_memory)
chain2 = LLMChain(llm=llm, prompt=second_input_prompt, output_key='plan', memory=plan_memory)
chain3 = LLMChain(llm=llm, prompt=third_input_prompt, output_key='cost', memory=cost_memory)

parent_chain = SequentialChain(
    chains=[chain1, chain2, chain3],
    input_variables=['name'],
    output_variables=['place', 'plan', 'cost'],
    verbose=True
)

# ---------- ROUTES ----------
@app.route("/")
def index():
    return render_template("index.html")   # 👈 now HTML loads

@app.route("/search", methods=["POST"])
def search():
    data = request.get_json()
    location = data.get("location")

    if not location:
        return jsonify({"error": "Location required"}), 400

    response = parent_chain({"name": location})

    # Extract route JSON
    route_data = []
    import json, re
    try:
        match = re.search(r"\{[\s\S]*\}", response["cost"])  # get JSON block
        if match:
            parsed = json.loads(match.group())
            route_data = parsed.get("route", [])
    except Exception as e:
        print("Failed to parse route:", e)

    return jsonify({
        "place": response.get("place", ""),
        "plan": response.get("plan", ""),
        "cost": response.get("cost", ""),
        "route": route_data
    })

if __name__ == "__main__":
    app.run(debug=True)
