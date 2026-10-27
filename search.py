import os
import re
from dotenv import load_dotenv
import qdrant_client
from llama_index.core import VectorStoreIndex, Settings
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.embeddings.fastembed import FastEmbedEmbedding

load_dotenv()

def custom_hybrid_reranker(query, nodes, top_n=3):
    # Custom ალგორითმი: აერთიანებს ვექტორულ (Semantic) და სიტყვიერ (Keyword) ქულებს
    query_words = set(re.findall(r'\w+', query.lower()))
    reranked_results = []
    
    for node in nodes:
        text = node.node.text.lower()
        text_words = set(re.findall(r'\w+', text))
        
        # ვითვლით სიტყვების დამთხვევის (Keyword) ქულას ნორმალიზაციით 0-დან 1-მდე
        keyword_matches = len(query_words.intersection(text_words))
        keyword_score = keyword_matches / max(len(query_words), 1) 
        
        # ვიღებთ ვექტორულ ქულას Qdrant-იდან
        vector_score = node.score if node.score else 0.0
        
        # Hybrid ფორმულა: 70% სემანტიკა, 30% საკვანძო სიტყვები
        final_score = (vector_score * 0.7) + (keyword_score * 0.3)
        
        reranked_results.append({
            "text": node.node.text,
            "vector_score": vector_score,
            "keyword_score": keyword_score,
            "final_score": final_score,
            "metadata": node.node.metadata
        })
        
    # ვალაგებთ კლებადობით საბოლოო ქულის მიხედვით
    reranked_results.sort(key=lambda x: x["final_score"], reverse=True)
    return reranked_results[:top_n]

def run_search():
    Settings.embed_model = FastEmbedEmbedding(model_name="BAAI/bge-small-en-v1.5")
    
    client = qdrant_client.QdrantClient(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY"),
    )
    vector_store = QdrantVectorStore(client=client, collection_name="investigation_engine")
    index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
    
    # ვეძებთ ბაზაში ტოპ 15 რეზულტატს (Retrieval)
    query_engine = index.as_retriever(similarity_top_k=15)
    test_query = "What television series or movie did the actor star in?"
    print(f"ვეძებთ კითხვაზე: '{test_query}'...")
    
    retrieved_nodes = query_engine.retrieve(test_query)
    
    # ვატარებთ ჩვენს Custom Reranker-ში
    final_results = custom_hybrid_reranker(test_query, retrieved_nodes, top_n=3)
    
    print("\nმოძიებული ტოპ 3 შედეგი ჩვენი ალგორითმით:")
    for i, res in enumerate(final_results, 1):
        print(f"\n--- შედეგი {i} (საბოლოო ქულა: {res['final_score']:.3f} | Vector: {res['vector_score']:.3f} | Keyword: {res['keyword_score']:.3f}) ---")
        print(res['text'][:250] + "...") 

if __name__ == "__main__":
    run_search()
