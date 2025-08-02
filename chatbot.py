from langchain_community.llms import Ollama
import streamlit as st

st.title("LangChain Chatbot with LLaMA via Ollama")

input_text = st.text_input("Ask your query here:")

llm = Ollama(model="llama2")  

if input_text:
    response = llm.invoke(input_text)

    st.subheader("Response:")
    st.write(response)
