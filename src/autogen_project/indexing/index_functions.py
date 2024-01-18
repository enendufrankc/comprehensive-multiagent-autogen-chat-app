from llama_index import load_index_from_storage, VectorStoreIndex, ServiceContext
from llama_index.node_parser import SimpleNodeParser
from llama_index.text_splitter import get_default_text_splitter
from llama_index import StorageContext
from autogen_project.config.settings import config
from autogen_project.readers.wikipedia_reader import Document
import wikipedia
from typing import Any, List
import json

def load_index(filepath: str):
    storage_context = StorageContext.from_defaults(persist_dir=filepath)
    return load_index_from_storage(storage_context)

def create_wikidocs(wikipage_requests):
    print(f"Preparing to Download:{wikipage_requests}")
    documents = []
    for page_title in wikipage_requests:
        try:
            # Attempt to load the Wikipedia page
            wiki_page = wikipedia.page(page_title)
            page_content = wiki_page.content
            page_url = wiki_page.url
            document = Document(text=page_content, metadata={'source_url': page_url})
            documents.append(document)
        except wikipedia.exceptions.PageError:
            # Handle the case where the page does not exist
            print(f"PageError: The page titled '{page_title}' does not exist on Wikipedia.")
        except wikipedia.exceptions.DisambiguationError as e:
            # Handle the case where the page title is ambiguous
            print(f"DisambiguationError: The page titled '{page_title}' is ambiguous. Possible options: {e.options}")
    print("Finished downloading pages")
    return documents

def index_wikipedia_pages(wikipage_requests):
    print(f"Preparing to index Wikipages: {wikipage_requests}")
    documents = create_wikidocs(wikipage_requests)
    text_splits = get_default_text_splitter(chunk_size=150, chunk_overlap=45)
    parser = SimpleNodeParser.from_defaults(text_splitter=text_splits)
    service_context = ServiceContext.from_defaults(node_parser=parser)
    index =  VectorStoreIndex.from_documents(documents, service_context=service_context, show_progress=False)
    index.storage_context.persist(config.index_path)
    print(f"{wikipage_requests} have been indexed.")
    return "indexed"

def search_and_index_wikipedia(
        hops: list, lang: str = "en", results_limit: int = 2
    ):

    # Set the language for Wikipedia
    wikipedia.set_lang(lang)

    # Initialize an empty list to hold all indexed page titles
    wikipage_requests = []

    # Loop through the identified hops and search for each
    for hop in hops:
        hop_pages = wikipedia.search(hop, results=results_limit)
        print(f"Searching Wikipedia for: {hop} - Found: {hop_pages}")
        wikipage_requests.extend(hop_pages)

    # Index the gathered pages (assuming 'index_wikipedia_pages' is a defined function that you implement)
    index_wikipedia_pages(wikipage_requests)

    return wikipage_requests


def query_wiki_index(hops: List[str], index_path: str = config.index_path, n_results: int = 5): 
    index = load_index(filepath=index_path)
    query_engine = index.as_query_engine(
        response_mode="compact", verbose=True, similarity_top_k=n_results
    )
    
    retrieved_context = {}
    
    # Iterate over each hop in the multihop query
    for hop in hops:
        nodes = query_engine.query(hop).source_nodes
        
        # Process each node found for the current hop
        for node in nodes:
            doc_id = node.node.id_
            doc_text = node.node.text
            doc_source = node.node.metadata.get('source_url', 'No source URL')  # Default value if source_url is not present.
            
            # Append to the list of texts and sources for each doc_id
            if doc_id not in retrieved_context:
                retrieved_context[doc_id] = {'texts': [doc_text], 'sources': [doc_source]}
            else:
                retrieved_context[doc_id]['texts'].append(doc_text)
                retrieved_context[doc_id]['sources'].append(doc_source)

    # Serialise the context for all hops into a JSON file
    file_path = index_path + "retrieved_context.json"
    with open(file_path, 'w') as f:
        json.dump(retrieved_context, f)
    
    return retrieved_context
