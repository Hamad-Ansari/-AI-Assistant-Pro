import streamlit as st
from langchain_community.llms import OpenAI
from langchain_community.llms import OpenAI
st.set_page_config(page_title="Quickstart App", layout="centered")

st.title('🦜🔗 Quickstart App')

# Sidebar API key input
openai_api_key = st.sidebar.text_input('OpenAI API Key', type="password")

def generate_response(input_text):
    llm = OpenAI(
        temperature=0.7,
        openai_api_key=openai_api_key
    )
    response = llm.invoke(input_text)
    st.info(response)

# Form UI
with st.form('my_form'):
    text = st.text_area('Enter text:', 'Write something...')
    submitted = st.form_submit_button('Submit')

    if not openai_api_key:
        st.warning('Please enter your OpenAI API key!', icon='⚠')

    elif submitted:
        generate_response(text)
