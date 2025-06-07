# app.py
import json
from rank_bm25 import BM25Okapi
from pyvi import ViTokenizer
import streamlit as st

@st.cache_resource
def load_data_and_model():
    # Load dữ liệu đã xử lý
    with open("preprocessed_documents.json", "r", encoding="utf-8") as f:
        preprocessed_documents = json.load(f)

    # Chuẩn bị corpus cho BM25
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
        doc_id = doc_ids[i]
        score = scores[i]
        results.append({
            "doc_id": doc_id,
            "url": preprocessed_documents[doc_id]["url"],
            "score": score,
            "preview": " ".join(preprocessed_documents[doc_id]["tokens"][:50])
        })
    return results

# --- Giao diện Streamlit ---
st.set_page_config(page_title="Tra cứu triệu chứng bệnh", layout="wide")

st.title("🩺 Tra cứu triệu chứng bệnh")

query = st.text_input("🔍 Nhập các triệu chứng bạn đang gặp phải (VD: sốt cao, đau đầu, nổi ban đỏ):")

if query:
    with st.spinner("Đang truy vấn..."):
        preprocessed_documents, bm25, doc_ids = load_data_and_model()
        results = search_symptoms(query, preprocessed_documents, bm25, doc_ids)

        num_found = sum(1 for r in results if r["score"] > 0)
        if num_found == 0:
            st.warning("⚠️ Không tìm thấy kết quả phù hợp.")
        else:
            for r in results:
                if r['score'] > 0:
                    st.markdown(f"### 📝 {r['doc_id']}  (Score: {r['score']:.2f})")
                    st.markdown(f"🔗 [Xem nguồn]({r['url']})")
                    st.write(r['preview'] + "...")
                    st.markdown("---")
