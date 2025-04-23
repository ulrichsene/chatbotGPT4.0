# Confluence Chatbot

A chat interface for querying Confluence pages using OpenAI's GPT model and LangChain. This chatbot indexes specific Confluence pages and provides intelligent, context-aware responses using semantic search powered by FAISS and Sentence Transformers. I specifically sourced data from Gonzaga's public website for this project.

---

## Features

- Semantic search over Confluence content using FAISS
- Intelligent responses via OpenAI GPT-4 and LangChain
- Page indexing from Confluence REST API
- Environment-based authentication and easy config
- Interactive command-line chat loop

---

## Requirements

Install dependencies using:

```bash
pip install -r requirements.txt
```
To run chatbot in terminal: 
```bash
python app.py
