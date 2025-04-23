import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class TextEmbedder:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        """
        Initializes the text embedder with a sentence transformer model and FAISS index.
        
        Args:
            model_name (str): The name of the SentenceTransformer model to use.
        """
        self.model = SentenceTransformer(model_name)
        self.faiss_index = None
        self.page_ids = []

    def get_embedding(self, text):
        """
        Generates a normalized embedding vector for a given piece of text.
        
        Args:
            text (str): Input text to embed.
            
        Returns:
            np.ndarray: The embedding vector.
        """
        return self.model.encode(text, normalize_embeddings=True)

    def add_document(self, text, page_id):
        """
        Adds a single document and its page ID to the FAISS index.
        
        Args:
            text (str): The document text.
            page_id (int): The associated page ID.
        """
        vector = self.get_embedding(text)

        if self.faiss_index is None:
            dimension = vector.shape[0]
            self.faiss_index = faiss.IndexFlatL2(dimension)

        self.faiss_index.add(np.array([vector], dtype=np.float32))
        self.page_ids.append(page_id)

    def build_faiss_index(self, texts, page_ids):
        """
        Builds the FAISS index from a list of texts and their corresponding page IDs.
        
        Args:
            texts (List[str]): A list of document texts.
            page_ids (List[int]): Corresponding page IDs.
        """
        if not texts or not page_ids:
            raise ValueError("No texts or page IDs provided to build the FAISS index.")

        embeddings = self.embed_texts(texts)

        if embeddings.shape[0] != len(page_ids):
            raise ValueError("Mismatch between the number of embeddings and page IDs.")

        dimension = embeddings.shape[1]
        self.faiss_index = faiss.IndexFlatL2(dimension)
        self.faiss_index.add(embeddings)
        self.page_ids = page_ids

        print(f"Indexed {len(page_ids)} pages with corresponding embeddings.")

    def embed_texts(self, texts):
        """
        Embeds a list of texts into vectors.
        
        Args:
            texts (List[str]): A list of strings to embed.
        
        Returns:
            np.ndarray: A 2D array of embeddings.
        """
        return np.array(self.model.encode(texts, normalize_embeddings=True), dtype=np.float32)

    def search_similar(self, query, top_k=5):
        """
        Searches for the top-k most similar indexed documents to the query.
        
        Args:
            query (str): The user query.
            top_k (int): Number of top matches to return.
        
        Returns:
            List[int]: A list of page IDs most similar to the query.
        """
        if self.faiss_index is None:
            raise ValueError("FAISS index is not initialized.")

        query_vector = np.array([self.get_embedding(query)], dtype=np.float32)
        distances, indices = self.faiss_index.search(query_vector, top_k)

        return [self.page_ids[i] for i in indices[0] if i < len(self.page_ids)]
