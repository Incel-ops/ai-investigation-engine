import os
from dotenv import load_dotenv
from datasets import load_dataset
from llama_index.core import Document
from llama_index.core.node_parser import SentenceSplitter, TokenTextSplitter

load_dotenv()

def load_hotpotqa_data(limit=1000):
    print(f"ვიწყებთ HotpotQA მონაცემების გადმოწერას... ვიღებთ {limit} კითხვას.")
    dataset = load_dataset("hotpotqa/hotpot_qa", "distractor", split="train", streaming=True)

    documents = []
    for i, item in enumerate(dataset):
        if i >= limit:
            break
        # თითო paragraph ცალკე დოკუმენტია, რომ მისი სათაური და ტექსტი არ აირიოს სხვასთან
        for title, sentences in zip(item["context"]["title"], item["context"]["sentences"]):
            text = f"Title: {title}\n" + "".join(sentences)
            documents.append(
                Document(
                    text=text,
                    metadata={
                        "title": title,
                        "question_id": item["id"],
                        "level": item["level"],
                        "type": item["type"],
                    },
                )
            )

    print(f"წარმატებით შეიქმნა {len(documents)} დოკუმენტი (paragraph).")
    return documents

def test_chunking_strategies(documents):
    print("\nსტრატეგია 1: ვჭრით მონაცემებს Sentence Splitter-ით...")
    sentence_splitter = SentenceSplitter(chunk_size=512, chunk_overlap=50)
    nodes_strategy_1 = sentence_splitter.get_nodes_from_documents(documents)
    print(f"[სტრატეგია 1] მივიღეთ {len(nodes_strategy_1)} Chunk (ნაწილი).")

    print("\nსტრატეგია 2: ვჭრით მონაცემებს Token Splitter-ით...")
    token_splitter = TokenTextSplitter(chunk_size=512, chunk_overlap=50)
    nodes_strategy_2 = token_splitter.get_nodes_from_documents(documents)
    print(f"[სტრატეგია 2] მივიღეთ {len(nodes_strategy_2)} Chunk (ნაწილი).")

    return nodes_strategy_1

if __name__ == "__main__":
    docs = load_hotpotqa_data(limit=1000)
    chunks = test_chunking_strategies(docs)
    print("\n✅ მონაცემების ჩამოტვირთვა და დაჭრა წარმატებით დასრულდა!")
