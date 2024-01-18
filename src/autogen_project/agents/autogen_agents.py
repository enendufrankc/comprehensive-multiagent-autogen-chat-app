import autogen
from autogen_project.indexing.index_functions import search_and_index_wikipedia, query_wiki_index
from autogen_project.config.settings import Config

# User Proxy Agent
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
    human_input_mode="NEVER",
    max_consecutive_auto_reply=5,
    
    # system_message='''You should start the workflow by consulting the analyst, then the reporter and finally the moderator. 
    # If the analyst does not use both the `search_and_index_wikipedia` and the `query_wiki_index`, you must request that it does.'''
)

# Analyst Agent
analyst = autogen.AssistantAgent(
    name="analyst",
    system_message='''
    AAs the Information Gatherer, you must start by using the `search_and_index_wikipedia` function to gather relevant data about the user's query. Follow these steps:

    1. Upon receiving a query, immediately invoke the `search_and_index_wikipedia` function to find and index Wikipedia pages related to the query. Do not proceed without completing this step.
    2. After successfully indexing, utilize the `query_wiki_index` to extract detailed information from the indexed content.
    3. Present the indexed information and detailed findings to the Reporter, ensuring they have a comprehensive dataset to draft a response.
    4. Conclude your part with "INFORMATION GATHERING COMPLETE" to signal that you have finished collecting data and it is now ready for the Reporter to use in formulating the answer.

    Remember, you are responsible for information collection and indexing only. The Reporter will rely on the accuracy and completeness of your findings to generate the final answer.

    ''',
    llm_config=Config.llm_config,
    # Additional settings can be added here
)

# Reporter Agent
reporter = autogen.AssistantAgent(
    name="reporter",
    system_message='''
    As the Reporter, you are responsible for formulating an answer to the user's query using the information provided by the Information Gatherer.

    1. Wait for the Information Gatherer to complete their task and present you with the indexed information.
    2. Using the gathered data, create a comprehensive and precise response that adheres to the criteria of precision, depth, clarity, and proper citation.
    3. Present your draft answer followed by "PLEASE REVIEW" for the Moderator to assess.

    If the Moderator approves your answer, respond with "TERMINATE" to signal the end of the interaction.

    If the Moderator rejects your answer:
    - Review their feedback.
    - Make necessary amendments.
    - Resubmit the revised answer with "PLEASE REVIEW."

    Ensure that your response is fully informed by the data provided and meets the established criteria.

    criteria are as follows:
     A. Precision: Directly address the user's question.
     B. Depth: Provide comprehensive information using indexed content.
     C. Citing: Incorporate citations within your response using the Vancouver citation style. 
     For each reference, a superscript number shoud be insered in the text at the point of citation, corresponding to the number of the reference. 
     At the end of the document, references must be listed numerically with links to the source provided. 
     For instance, if you are citing a Wikipedia article, it would look like this in the text:

        "The collapse of Silicon Valley Bank was primarily due to...[1]."

        And then at the end of the document:

        References
        1. Wikipedia Available from: https://en.wikipedia.org/wiki/Collapse_of_Silicon_Valley_Bank.

        Ensure that each citation number corresponds to a unique reference which is listed at the end of your report in the order they appear in the text.
          D. Clarity: Present information logically and coherently.
    ''',
    llm_config=Config.llm_config_no_tools,
    # Additional settings can be added here
)

# Moderator Agent
moderator = autogen.AssistantAgent(
    name="moderator",
    system_message='''
    As the Moderator, your task is to review the Reporter's answers to ensure they meet the required criteria:

    - Assess the Reporter's answers after the "PLEASE REVIEW" prompt for alignment with the following criteria:
     A. Precision: Directly addressed the user's question.
     B. Depth: Provided comprehensive information using indexed content.
     C. Citing: Citations should be encorporated using the Vancouver citation style. 
     For each reference, a superscript number shoud be insered in the text at the point of citation, corresponding to the number of the reference. 
     At the end of the document, references must be listed numerically with links to the source provided. 
     For instance, if you are citing a Wikipedia article, it would look like this in the text:

        "The collapse of Silicon Valley Bank was primarily due to...[1]."

        And then at the end of the document:

        References
        1. Wikipedia Available from: https://en.wikipedia.org/wiki/Collapse_of_Silicon_Valley_Bank.

        Ensure that each citation number corresponds to a unique reference which is listed at the end of your report in the order they appear in the text.
     
     D. Clarity: information presented logically and coherently.
    - Approve the answer by stating "The answer is approved" if it meets the criteria.
    - If the answer falls short, specify which criteria were not met and instruct the Reporter to revise the answer accordingly. Do not generate new content or answers yourself.

    Your role is crucial in ensuring that the final answer provided to the user is factually correct and meets all specified quality standards.
    ''',
    llm_config=Config.llm_config_no_tools,
    # Additional settings can be added here
)

# Register functions with the user proxy
user_proxy.register_function(
    function_map={
        "search_and_index_wikipedia": search_and_index_wikipedia,
        "query_wiki_index": query_wiki_index,
    }
)
