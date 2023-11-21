import time, boto3
import streamlit as st
from langchain.llms import Bedrock
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts.prompt import PromptTemplate

# Setup bedrock
bedrock_runtime = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-1",
)

template = """The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know.

Current conversation:

{history}
Human: {input}
AI Assistant:"""

# St manage cache
@st.cache_resource

# load llm using langchain
def load_llm(selected_model):
    llm = Bedrock(client=bedrock_runtime, model_id=selected_model)
    llm.model_kwargs = {"temperature": 0.7, "max_tokens_to_sample": 8000}

    PROMPT = PromptTemplate(input_variables=["history", "input"], template=template)
    model = ConversationChain(prompt=PROMPT, llm=llm, verbose=True, memory=ConversationBufferMemory())

    return model

# Chatbot using bedrock and langchain. Chat initialisation, historical chat included
def simple_chatbot():
    st.markdown("# Bedrock chatbot ")

    model_selector = {
        "Claude v2": "anthropic.claude-v2",
    }

    selected_model = "anthropic.claude-v2"
    selected_model = st.sidebar.selectbox("Pick a model", model_selector.values())
    model = load_llm(selected_model)

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input with user and assistant prompts
    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        full_response = ""
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            
            result = model.predict(input=prompt)

            # Simulate stream of response with milliseconds delay
            for chunk in result.split():
                full_response += chunk + " "
                time.sleep(0.05)
                # Add a blinking cursor to simulate typing
                message_placeholder.markdown(full_response + "▌")

            message_placeholder.markdown(full_response)

        st.session_state.messages.append({"role": "assistant", "content": full_response})