# wikipedia_reader.py
from typing import Any, List
from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document
import wikipedia

class WikipediaReader(BaseReader):
    def load_data(self, pages: List[str], lang: str = "en", **load_kwargs: Any) -> List[Document]:
        results = []
        for page in pages:
            wikipedia.set_lang(lang)
            wiki_page = wikipedia.page(page, **load_kwargs)
            page_content = wiki_page.content
            page_url = wiki_page.url
            document = Document(text=page_content, metadata={'source_url': page_url})
            results.append(document)
        return results
