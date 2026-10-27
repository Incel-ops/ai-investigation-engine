from dotenv import load_dotenv
import os
import qdrant_client
from llama_index.core import VectorStoreIndex, StorageContext, Settings
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.embeddings.fastembed import FastEmbedEmbedding
from data_ingestion import load_hotpotqa_data, test_chunking_strategies

load_dotenv()

EMBED_MODEL = "BAAI/bge-small-en-v1.5"  # უნდა ემთხვეოდეს main.py-ს
COLLECTION_NAME = "investigation_engine"


def upload_to_qdrant():
    print("ვუკავშირდებით Qdrant-ს და ვტვირთავთ ემბედინგ მოდელს...")

    Settings.embed_model = FastEmbedEmbedding(model_name=EMBED_MODEL)

    client = qdrant_client.QdrantClient(
        url=os.environ["QDRANT_URL"],
        api_key=os.environ["QDRANT_API_KEY"],
    )

    vector_store = QdrantVectorStore(client=client, collection_name=COLLECTION_NAME)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    docs = load_hotpotqa_data(limit=1000)
    chunks = test_chunking_strategies(docs)

    print(f"\nვიწყებთ {len(chunks)} ნაწილის დაემბედინგებას და ატვირთვას...")

    VectorStoreIndex(
        nodes=chunks,
        storage_context=storage_context,
        show_progress=True,
    )

    print("\n✅ მონაცემები წარმატებით აიტვირთა Qdrant-ში!")


if __name__ == "__main__":
    upload_to_qdrant()
