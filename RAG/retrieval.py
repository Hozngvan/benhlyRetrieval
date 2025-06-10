import json
from rank_bm25 import BM25Okapi
from pyvi import ViTokenizer

def load_data():
    # Load preprocessed documents
    with open("preprocessed_documents.json", "r", encoding="utf-8") as f:
        preprocessed_documents = json.load(f)

    # Prepare corpus for BM25
    tokenized_corpus = [data["tokens"] for data in preprocessed_documents.values()]
    bm25 = BM25Okapi(tokenized_corpus)
    doc_ids = list(preprocessed_documents.keys())
    
    return preprocessed_documents, bm25, doc_ids

def preprocess_text(text):
    text = text.lower()
    tokenized = ViTokenizer.tokenize(text)
    return tokenized.split()

def search_symptoms(query, preprocessed_documents, bm25, doc_ids, top_k=10):
    tokenized_query = preprocess_text(query)
    scores = bm25.get_scores(tokenized_query)
    top_indexes = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]

    results = []
    for i in top_indexes:
        if scores[i] > 0:
            doc_id = doc_ids[i]
            results.append({
                "doc_id": doc_id,
                "url": preprocessed_documents[doc_id]["url"],
                "score": scores[i],
                "preview": " ".join(preprocessed_documents[doc_id]["tokens"][:100])
            })
    return results

def main():
    print("🩺 Hệ thống tra cứu triệu chứng bệnh")
    print("=" * 50)
    
    # Load data
    print("\nĐang tải dữ liệu...")
    preprocessed_documents, bm25, doc_ids = load_data()
    print("Đã tải xong!")
    
    while True:
        print("\n" + "=" * 50)
        query = input("\n🔍 Nhập các triệu chứng (hoặc 'q' để thoát): ")
        
        if query.lower() == 'q':
            break
            
        print("\nĐang tìm kiếm...")
        results = search_symptoms(query, preprocessed_documents, bm25, doc_ids)
        
        num_found = sum(1 for r in results if r["score"] > 0)
        if num_found == 0:
            print("\n⚠️ Không tìm thấy kết quả phù hợp.")
            continue
            
        # Display search results
        print("\n📚 Kết quả tìm kiếm:")
        print("-" * 50)
        for r in results:
            if r['score'] > 0:
                print(f"\n📝 {r['doc_id']} (Score: {r['score']:.2f})")
                print(f"🔗 URL: {r['url']}")
                print(f"📄 Preview: {r['preview'].replace('_', ' ')}...")
                print("-" * 50)

if __name__ == "__main__":
    main()
