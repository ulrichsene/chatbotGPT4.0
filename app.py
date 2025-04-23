import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
from chatbot import ConfluenceChatbot

if __name__ == "__main__":
    bot = ConfluenceChatbot()
    print("Indexing Confluence pages...")
    bot.index_pages()

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        response = bot.chat(user_input)
        print(f"Bot: {response}")
