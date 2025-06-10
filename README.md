# benhlyRetrieval - Hệ thống Tư vấn Y tế Thông minh

Đồ án CS419 - Truy xuất thông tin

## Giới thiệu

benhlyRetrieval là một hệ thống tư vấn y tế thông minh, kết hợp giữa kỹ thuật truy xuất thông tin (BM25) và mô hình ngôn ngữ lớn (Gemini) để cung cấp thông tin y tế chính xác và hữu ích cho người dùng.

### Tính năng chính

- 🔍 Tìm kiếm thông tin bệnh dựa trên triệu chứng
- 🤖 Tư vấn y tế thông minh sử dụng Gemini AI
- 📚 Hiển thị các nguồn thông tin liên quan
- 💬 Giao diện chat thân thiện với người dùng

## Cài đặt

### Yêu cầu hệ thống

- Python 3.8 trở lên
- pip (Python package manager)

### Các bước cài đặt

1. Clone repository:

```bash
git clone https://github.com/your-username/benhlyRetrieval.git
cd benhlyRetrieval
```

2. Tạo và kích hoạt môi trường ảo:

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

3. Cài đặt các thư viện cần thiết:

```bash
pip install -r requirements.txt
```

4. Tạo file .env và thêm API key:

```
GOOGLE_API_KEY=your_gemini_api_key_here
```

## Sử dụng

### Chạy ứng dụng

1. Khởi động ứng dụng Streamlit:

```bash
streamlit run RAG/main.py
```

2. Mở trình duyệt và truy cập địa chỉ được hiển thị (thường là http://localhost:8501)

### Cách sử dụng

1. Nhập câu hỏi về triệu chứng bệnh vào ô tìm kiếm
2. Hệ thống sẽ:
   - Tìm kiếm thông tin liên quan từ cơ sở dữ liệu
   - Hiển thị các kết quả tìm kiếm ở cột bên trái
   - Tạo câu trả lời thông minh dựa trên thông tin tìm được
   - Hiển thị lịch sử hội thoại ở cột bên phải

### Ví dụ câu hỏi

- "Tôi bị sốt cao và đau đầu, có thể là bệnh gì?"
- "Triệu chứng ho khan và khó thở là dấu hiệu của bệnh gì?"
- "Đau bụng dưới bên phải kèm sốt nhẹ là bệnh gì?"

## Cấu trúc dự án

```
benhlyRetrieval/
├── RAG/
│   ├── main.py           # Giao diện Streamlit và xử lý chính
│   └── retrieval.py      # Module truy xuất thông tin
├── preprocessed_documents.json  # Dữ liệu đã xử lý
├── requirements.txt      # Danh sách thư viện
└── README.md            # Tài liệu hướng dẫn
```

## Công nghệ sử dụng

- **Streamlit**: Xây dựng giao diện người dùng
- **BM25**: Thuật toán truy xuất thông tin
- **Gemini AI**: Mô hình ngôn ngữ lớn cho việc tạo câu trả lời
- **PyVi**: Xử lý ngôn ngữ tiếng Việt

## Đóng góp

Mọi đóng góp đều được hoan nghênh! Vui lòng tạo issue hoặc pull request để đóng góp.

## Giấy phép

Dự án này được phát hành dưới giấy phép MIT.
