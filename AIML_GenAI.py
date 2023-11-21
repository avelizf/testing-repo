import streamlit as st

import pages.scripts.AIML_GAI_chat as AIML_GAI_chat
import pages.scripts.AIML_GAI_txt2img as AIML_GAI_txt2img
import pages.scripts.AIML_GAI_DC_Prompt as AIML_GAI_DC_Prompt
import pages.scripts.AIML_GAI_DC_RAG as AIML_GAI_DC_RAG
import pages.scripts.AIML_Repo2Wiki as AIML_Repo2Wiki





st.set_page_config(page_title="Toolbox", page_icon="🛠️")
st.sidebar.markdown("# GenAI demos")


# Demo 1
# Chatbot using bedrock and langchain. Chat initialisation, historical chat included
def simple_chatbot():
    AIML_GAI_chat.simple_chatbot()

# Demo 2
# Text to image demo
def text_to_image():
    AIML_GAI_txt2img.text_to_image()

# Demo 3
# Document chatbot using prompt context as input - No RAG
def prompting_docchat():
    AIML_GAI_DC_Prompt.prompting_docchat()

# Demo 4
# Document chatbot using RAG (embeddings + FAISS)
def rag_docchat():
    AIML_GAI_DC_RAG.rag_DocChat()

# Demo 5
# Generate MD wiki from linkedin repo
def repo_wiki_gen():
    AIML_Repo2Wiki.repo_to_wiki()
    

page_names_to_funcs = {
    "[PROMPT] Chatbot": simple_chatbot,
    "[PROMPT] Image Generator": text_to_image,
    "[PROMPT] Wiki Generator": repo_wiki_gen,
    "[PROMPT] DocChat Context": prompting_docchat,
    "[RAG] DocChat RAG": rag_docchat,
}

selected_page = st.sidebar.selectbox("Select a demo", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()