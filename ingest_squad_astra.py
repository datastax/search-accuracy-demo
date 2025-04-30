import os
from langchain_astradb.vectorstores import AstraDBVectorStore
from langchain.schema import Document
import json
import csv
from uuid import uuid4

# Environment variables for Astra DB connection
ASTRA_DB_APPLICATION_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
ASTRA_DB_API_ENDPOINT = os.getenv("ASTRA_DB_API_ENDPOINT")

# Maximum character length per document (approximating < 512 tokens)
MAX_CHAR_LENGTH = 1000

# Function to split text into chunks
def split_text(text, max_length):
    chunks = []
    while len(text) > max_length:
        # Find a suitable split point (preferably at a sentence boundary)
        split_point = text.rfind('.', 0, max_length)
        if split_point == -1 or split_point < max_length // 2:
            split_point = max_length
        chunks.append(text[:split_point])
        text = text[split_point:].strip()
    if text:
        chunks.append(text)
    return chunks

# Function to process CSV file
def process_csv_file(file_content):
    documents = []
    csv_reader = csv.DictReader(file_content.splitlines())
    for row in csv_reader:
        content = f"Question: {row['question']} Answer: {row['answer']}"
        # Split content if it exceeds MAX_CHAR_LENGTH
        content_chunks = split_text(content, MAX_CHAR_LENGTH)
        for i, chunk in enumerate(content_chunks):
            doc = Document(
                page_content=chunk,
                metadata={
                    "source": "qa_pairs.csv",
                    "id": str(uuid4()),
                    "chunk_index": i,
                    "original_question": row['question'][:100]  # Truncated for metadata
                }
            )
            documents.append(doc)
    return documents

# Function to process JSON file
def process_json_file(file_content):
    documents = []
    data = json.loads(file_content)
    for i, text in enumerate(data):
        # Split text if it exceeds MAX_CHAR_LENGTH
        text_chunks = split_text(text, MAX_CHAR_LENGTH)
        for j, chunk in enumerate(text_chunks):
            doc = Document(
                page_content=chunk,
                metadata={
                    "source": "squad_docs.json",
                    "id": str(uuid4()),
                    "index": i,
                    "chunk_index": j
                }
            )
            documents.append(doc)
    return documents

# Main function to ingest data into Astra DB
def ingest_to_astra_db():
    # Initialize Astra DB clients for each collection
    qa_pairs_vstore = AstraDBVectorStore(
        collection_name="qa_pairs",
        token=ASTRA_DB_APPLICATION_TOKEN,
        api_endpoint=ASTRA_DB_API_ENDPOINT,
        autodetect_collection=True,
    )
    
    # Initialize Astra DB client for squad_docs collection
    squad_docs_vstore = AstraDBVectorStore(
        collection_name="squad_docs",
        token=ASTRA_DB_APPLICATION_TOKEN,
        api_endpoint=ASTRA_DB_API_ENDPOINT,
        autodetect_collection=True,
    )

    # Sample file contents (in practice, read from actual files)
    with open("qa_pairs.csv", "r") as f:
        csv_content = f.read()
    with open("squad_docs.json", "r") as f:
        json_content = f.read()

    # Process files
    qa_documents = process_csv_file(csv_content)
    squad_documents = process_json_file(json_content)

    # Ingest documents into respective collections
    qa_pairs_vstore.add_documents(qa_documents)
    squad_docs_vstore.add_documents(squad_documents)

    print("Successfully ingested documents into Astra DB collections: qa_pairs and squad_docs")

if __name__ == "__main__":
    ingest_to_astra_db()
