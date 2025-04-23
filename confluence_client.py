import os
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv(dotenv_path=".env")

print("Base URL:", os.getenv("CONFLUENCE_BASE_URL"))
print("User Email:", os.getenv("CONFLUENCE_USER_EMAIL"))
print("API Token:", os.getenv("CONFLUENCE_API_TOKEN")[:5] + "*")

class ConfluenceClient:
    """
    A client for interacting with the Confluence REST API to fetch and search content.
    """

    def __init__(self):
        """
        Initializes the Confluence client with authentication credentials
        from environment variables.
        """
        self.base_url = os.getenv("CONFLUENCE_BASE_URL")
        self.auth = (os.getenv("CONFLUENCE_USER_EMAIL"), os.getenv("CONFLUENCE_API_TOKEN"))

        if not self.base_url or not all(self.auth):
            raise ValueError("Missing required environment variables. Check your .env file.")

    def get_page_content(self, page_id):
        """
        Retrieves the content of a Confluence page by its ID.

        Args:
            page_id (int or str): The ID of the page to retrieve.

        Returns:
            str: The HTML content of the page, or None if not found or an error occurs.
        """
        try:
            url = f"{self.base_url}/rest/api/content/{page_id}?expand=body.storage"
            response = requests.get(url, auth=self.auth)
            response.raise_for_status()
            return response.json()["body"]["storage"]["value"]
        except requests.exceptions.HTTPError as err:
            if err.response.status_code == 404:
                print(f"Page ID {page_id} not found.")
            else:
                print(f"Error fetching content for page ID {page_id}: {err}")
            return None
        except KeyError:
            print(f"Unexpected response structure for page ID {page_id}.")
            return None

    def search_pages(self, query="space=GP", limit=5):
        """
        Searches Confluence pages using a CQL query.

        Args:
            query (str): The CQL query string. Defaults to "space=GP".
            limit (int): The number of results to return.

        Returns:
            List[str]: A list of page IDs matching the query.
        """
        cql_query = query if query else "space=GP"
        url = f"{self.base_url}/rest/api/content/search"
        params = {"cql": cql_query, "limit": limit}

        response = requests.get(url, auth=self.auth, params=params)
        print(f"Requesting: {response.url}")
        print(f"Response: {response.status_code} - {response.text}")

        response.raise_for_status()
        return [page["id"] for page in response.json().get("results", [])]
