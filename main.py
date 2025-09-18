import os
from constants import google_api_key
from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain.memory import ConversationBufferMemory

os.environ["GOOGLE_API_KEY"] = google_api_key
st.title("Langchain Demo with Gemini")

input_text = st.text_input("Tourist Place Search")

## Prompt Template 1
first_input_prompt = PromptTemplate(
    input_variables=['name'],
    template="Tell me about the tourist places in {name}"
)

## Memory (make sure input_key matches!)
place_memory = ConversationBufferMemory(input_key='name', memory_key='chat_history')
plan_memory = ConversationBufferMemory(input_key='place', memory_key='chat_history')
cost_memory = ConversationBufferMemory(input_key='plan', memory_key='description_history')

## Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-pro",
    google_api_key=google_api_key,
    temperature=0.7
)

## LLM Chains
chain1 = LLMChain(llm=llm, prompt=first_input_prompt, verbose=True,
                  output_key='place', memory=place_memory)

second_input_prompt = PromptTemplate(
    input_variables=['place'],
    template="Tell me how I can visit all the {place} in an order where to start and end and perfect timing for each place."
)

chain2 = LLMChain(llm=llm, prompt=second_input_prompt, verbose=True,
                  output_key='plan', memory=plan_memory)

third_input_prompt = PromptTemplate(
    input_variables=['plan'],
    template="Give me a detailed flow of {plan} in an order where to start and the train or flight that is available or bus and price ranges and approx cost."
)

chain3 = LLMChain(llm=llm, prompt=third_input_prompt, verbose=True,
                  output_key='cost', memory=cost_memory)

## SequentialChain (returns all outputs)
parent_chain = SequentialChain(
    chains=[chain1, chain2, chain3],
    input_variables=['name'],                   
    output_variables=['place', 'plan', 'cost'],  
    verbose=True
)

if input_text:
    response = parent_chain({'name': input_text})
    st.write("### Tourist Places")
    st.write(response['place'])
    st.write("### Suggested Travel Plan")
    st.write(response['plan'])
    st.write("### Travel Cost & Options")
    st.write(response['cost'])

    with st.expander('Place Name Memory'):
        st.info(place_memory.buffer)
    with st.expander('Plan Memory'):
        st.info(plan_memory.buffer)
    with st.expander('Cost Memory'):
        st.info(cost_memory.buffer)
