import autogen
from autogen_project.agents.autogen_agents import user_proxy, analyst, reporter, moderator

class GroupChatManager:
    def __init__(self, llm_config):
        self.groupchat = autogen.GroupChat(
            agents=[user_proxy, analyst, reporter, moderator], 
            messages=[], 
            max_round=20
        )
        self.manager = autogen.GroupChatManager(
            groupchat=self.groupchat, 
            llm_config=llm_config, 
            system_message=''''You should start the workflow by consulting the analyst, 
                                then the reporter and finally the moderator. 
                                If the analyst does not use both the `search_and_index_wikipedia` 
                                and the `query_wiki_index`, you must request that it does.'''
        )
        self.conversation_history = [] 

    def initiate_chat(self, message: str):
        response = self.manager.initiate_chat(self.manager, message=message)
        
        # Capture the conversation history
        # You need to determine how to extract messages from the response or the groupchat object
        # This is a placeholder for where you would append messages to the conversation history
        self.conversation_history.append({"agent_name": "User", "message": message})
        self.conversation_history.append({"agent_name": "System", "message": response})
        
        return self.conversation_history
    
    def get_conversation_history(self):
        return self.conversation_history