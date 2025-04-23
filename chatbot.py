from langchain_openai import ChatOpenAI
from confluence_client import ConfluenceClient
from embeddings import TextEmbedder
from langchain.schema import HumanMessage
import requests

class ConfluenceChatbot:
    def __init__(self):
        """
        Initializes the ConfluenceChatbot with necessary components:
        - A Confluence client for accessing pages.
        - A text embedder for vectorizing page content.
        - A language model for generating responses.
        """
        self.confluence = ConfluenceClient()
        self.embedder = TextEmbedder()
        self.llm = ChatOpenAI(model_name="gpt-4")

    def index_pages(self):
        """
        Indexes selected Confluence pages by retrieving their content,
        embedding them using a vector store, and storing the associated page IDs.
        """
        page_ids = [9535489, 9601025, 9404548, 9469953, 8945668, 9011202, 9306113]
        texts = []

        for page_id in page_ids:
            try:
                page_content = self.confluence.get_page_content(page_id)
                if page_content.strip():
                    print(f"Indexing page {page_id} ({len(page_content)} chars)")
                    texts.append(page_content)
                else:
                    print(f"Skipping page {page_id} due to empty content.")
            except requests.exceptions.HTTPError as e:
                print(f"Failed to fetch page {page_id}: {e}")

        if not texts:
            print("No valid texts to index.")
            return

        self.embedder.build_faiss_index(texts, page_ids)

    def chat(self, user_query):
        """
        Accepts a user query, retrieves relevant Confluence pages,
        and returns a language model-generated response based on that context.

        Args:
            user_query (str): The user's question or prompt.

        Returns:
            str: The language model's generated response.
        """
        related_pages = self.embedder.search_similar(user_query)
        print(f"Related Page IDs: {related_pages}")

        context_list = []
        for pid in related_pages:
            try:
                content = self.confluence.get_page_content(pid)
                context_list.append(content[:1000])  # Include only first 1000 characters
            except requests.exceptions.HTTPError as e:
                print(f"Error fetching content for page ID {pid}: {e}")
                continue

        context = "\n".join(context_list)
        if len(context) > 6000:
            context = context[:6000] + "...\n[Content truncated]"

        messages = [HumanMessage(content=f"User Query: {user_query}\nContext: {context}")]
        response = self.llm.invoke(messages)

        return response.content
