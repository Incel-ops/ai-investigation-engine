import os
from dotenv import load_dotenv
import qdrant_client
from qdrant_client.http import models

load_dotenv()

client = qdrant_client.QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)

collection_name = "investigation_engine"

# ვამოწმებთ არსებობს თუ არა და თუ არადა ვქმნით
collections = client.get_collections().collections
exists = any(c.name == collection_name for c in collections)

if not exists:
    client.create_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE)
    )
    print(f"კოლექცია '{collection_name}' წარმატებით შეიქმნა!")
else:
    print(f"კოლექცია '{collection_name}' უკვე არსებობს.")
