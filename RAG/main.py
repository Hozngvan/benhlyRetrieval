import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
from retrieval import load_data, search_symptoms

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

@st.cache_resource
def load_model():
    # Initialize Gemini model
    model = genai.GenerativeModel('gemini-1.5-flash')
    return model

def generate_response(query, results, model):
    # Create prompt template
    template = """Bạn là một trợ lý y tế thông minh. Hãy sử dụng thông tin của query và context để xác định bệnh mà người hỏi có thể đang mắc phải. 
    Có thể triệu chứng đó thuộc nhiều hơn một loại bệnh.
    Hãy trả lời ngắn gọn, rõ ràng và dễ hiểu. 
    Context có thể chứa link trang web thông tin chi tiết về bệnh. Hãy liệt kê các link dẫn tới các trang đó.

Câu hỏi: {query}

Thông tin liên quan:
{context}

Hãy trả lời câu hỏi dựa trên thông tin trên."""

    # Format context
    context_text = "\n".join([f"- {r['preview']}" for r in results])
    
    # Create prompt
    prompt = template.format(query=query, context=context_text)
    
    # Generate response
    response = model.generate_content(prompt)
    return response.text

# --- Streamlit Interface ---
st.set_page_config(page_title="Chatbot Tư vấn Y tế", layout="wide")

st.title("🤖 Chatbot Tư vấn Y tế")

# Create two columns
col1, col2 = st.columns([1, 1])

# Initialize session state for chat history and current context
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_context" not in st.session_state:
    st.session_state.current_context = []

# Load data and model
with st.spinner("Đang tải dữ liệu và model..."):
    preprocessed_documents, bm25, doc_ids = load_data()
    model = load_model()

# Chat input
query = st.text_input("🔍 Nhập câu hỏi của bạn về triệu chứng bệnh:")

if query:
    with st.spinner("Đang tìm kiếm và tạo câu trả lời..."):
        # Retrieve relevant context
        results = search_symptoms(query, preprocessed_documents, bm25, doc_ids)
        st.session_state.current_context = results
        
        if not results:
            response = "Xin lỗi, tôi không tìm thấy thông tin phù hợp để trả lời câu hỏi của bạn."
        else:
            # Generate response using the context
            response = generate_response(query, results, model)
        
        # Add to chat history
        st.session_state.messages.append({"role": "user", "content": query})
        st.session_state.messages.append({"role": "assistant", "content": response})

# Display retrieved contexts in left column
with col1:
    st.subheader("📚 Thông tin liên quan")
    if st.session_state.current_context:
        for r in st.session_state.current_context:
            with st.expander(f"📄 {r['doc_id']} (Score: {r['score']:.2f})"):
                st.write(r['preview'].replace("_", " "))
                st.markdown(f"[🔗 Xem nguồn]({r['url']})")
    else:
        st.info("Chưa có thông tin được truy xuất.")

# Display chat history in right column
with col2:
    st.subheader("💬 Lịch sử hội thoại")
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"**Bạn:** {message['content']}")
        else:
            st.markdown(f"**Bot:** {message['content']}")
        st.markdown("---")
