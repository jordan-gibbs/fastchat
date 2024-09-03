import streamlit as st
from openai import OpenAI

client = OpenAI()

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-mini"

# Initialize chat history
if "messages2" not in st.session_state:
    st.session_state.messages2 = []

def main():
    st.set_page_config(
        page_title="FastChat",
        page_icon="⚡",
        layout="wide"
    )

    with open("style.css") as css:
        st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)

    hide_streamlit_style = """
            <style>
            #root > div:nth-child(1) > div > div > div > div > section > div {padding-top: 0rem;}
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    st.title("FastChat ⚡")
    st.subheader("Fastest AI Chat in the West")

    # clear_state = st.sidebar.button("New Chat")
    # if clear_state:
    #     st.session_state.messages2 = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages2:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input(placeholder="Chat with the AI:"):
        # Add user message to chat history
        st.session_state.messages2.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages2
                ] + [{"role": "user", "content": f"{prompt}"}],
                stream=True,
            )
            response = st.write_stream(stream)
        st.session_state.messages2.append({"role": "assistant", "content": response})

    else:
        # Display chat history if no new input
        for message in st.session_state.messages2:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])



if __name__ == "__main__":
    main()
