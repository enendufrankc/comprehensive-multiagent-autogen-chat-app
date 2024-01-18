import streamlit as st
from autogen_project.chat_manager.group_chat_manager import GroupChatManager
from autogen_project.config.settings import config  # Ensure correct import path

# Initialize the GroupChatManager
chat_manager = GroupChatManager(config.llm_config)

def main():
    st.title("AutoGen Interaction Simulator")

    user_input = st.text_area("Enter your message:", "")

    if st.button("Send"):
        if user_input:
            # Send the input to the GroupChatManager and get the conversation history
            conversation_history = chat_manager.initiate_chat(user_input)
            
            # Display each interaction in the conversation history
        for interaction in conversation_history:
            st.write(f"{interaction['agent_name']}: {interaction['message']}")

        if "TERMINATE" in user_input:
            st.write("Chat terminated by the reporter.")
            st.stop()
            
if __name__ == "__main__":
    main()
