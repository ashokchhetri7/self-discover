import streamlit as st
import os
from self_discover import SelfDiscover
from task_example import task1
from dotenv import load_dotenv

# Load the API key from the .env file
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

st.set_page_config(
    page_title="SELF-DISCOVER",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.title("SELF-DISCOVER")


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style.css")



api_key = st.text_input("Enter OpenAI api key ", value=OPENAI_API_KEY)
task = st.text_area("Enter the task example you want to generate a reasoning structure for ", value=task1, height=300)

if st.button("Generate Reasoning Structure"):
    os.environ["OPENAI_API_KEY"] = api_key
    result = SelfDiscover(task)
    result()
    tab1, tab2, tab3, tab4 = st.tabs(["SELECTED_MODULES", "ADAPTED_MODULES", "REASONING_STRUCTURE", "FINAL_OUPTUT"])
    with tab1:
        st.header("SELECTED_MODULES")
        st.write(result.selected_modules)

    with tab2:
        st.header("ADAPTED_MODULES") 
        st.write(result.adapted_modules)

    with tab3:
        st.header("REASONING_STRUCTURE") 
        st.write(result.reasoning_structure)
    
    with tab4:
        st.header("FINAL_OUPTUT")
        st.write(result.solution)

else:
    st.error("Please provide both your API key and a task example.")

