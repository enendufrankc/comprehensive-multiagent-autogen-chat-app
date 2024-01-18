import autogen
import openai
from autogen_project.utilities.utils import read_json_file  # Import the utility function
import os

class Config:
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.index_path = os.path.join(base_dir, "..", "new_autogen_project", "indexes")
        self.configurations_path = r'C:\Users\LENOVO\1. Projects\AutoGen\new_autogen_tutorial'
        self.api_key = None
        self.model_config = {}

     
    def load_from_json(self):
        file_path = os.path.join(self.configurations_path, "configurations.json")
        data = read_json_file(file_path)  # Use the utility function
        if data and isinstance(data, list) and len(data) > 0:
            self.api_key = data[0]['api_key']
            self.model_config = data[0].get('model', {})
        else:
            raise ValueError("Invalid configuration data")

    def llm_config(self):
        # Define llm_config based on your requirements
        self.llm_config = {
            "functions": [
                {
                    "name": "search_and_index_wikipedia",
                    "description": "Indexes Wikipedia pages based on specified queries for each hop to build a knowledge base for future reference. Use before query_wiki_index.",
                    "parameters": {
                     "type": "object",
                     "properties": {
                          "hops": {
                                "type": "array",
                             "items": {
                                 "type": "string"
                             },
                             "description": "The search queries for identifying relevant Wikipedia pages to index, each corresponding to a hop in the multihop question.",
                         }
                      },
                      "required": ["hops"],
                 },
             },
             {
                "name": "query_wiki_index",
                "description": "Queries the indexed Wikipedia knowledge base to retrieve pertinent information across multiple hops",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "hops": {
                                "type": "array",
                                "items": {
                                    "type": "string"
                                },
                                "description": "The search queries to search the indexed Wikipedia knowledge base for relevant information, each corresponding to a hop in the multihop question.",
                            },
                        },
                        "required": ["hops"],
                    },
                },
            ],
            "config_list": self.model_config,
            "request_timeout": 120,
            "seed": 100,
            "temperature": 0.7
              }

    def llm_config_no_tools(self):
        # llm_config_no_tools excludes the 'functions' key
        self.llm_config_no_tools = {k: v for k, v in self.llm_config.items() if k != 'functions'}


config = Config()
config.load_from_json()

# Set OpenAI key
openai.api_key = config.api_key