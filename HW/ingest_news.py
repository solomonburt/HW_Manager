import pandas as pd
import chromadb
import os

# Setup paths
csv_path = "data/news.csv"  # Ensure your csv is in a 'data' folder
db_path = "news_db_storage"

# Load data
if not os.path.exists(csv_path):
    print(f"Error: {csv_path} not found. Please place news.csv in the data folder.")
else:
    df = pd.read_csv(csv_path)
    
    # Initialize ChromaDB
    client = chromadb.PersistentClient(path=db_path)
    
    # Create collection
    collection = client.get_or_create_collection(name="news_monitor")

    # Prep data for indexing
    documents = df['Document'].tolist()
    # Metadata helps the LLM with context and allows for specific company filtering
    metadatas = df[['company_name', 'Date', 'URL']].to_dict('records')
    ids = [f"news_{i}" for i in range(len(df))]

    # Add to database
    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )

    print(f"Successfully indexed {len(df)} articles to {db_path}")
