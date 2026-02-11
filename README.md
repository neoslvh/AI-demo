# 🤖 AI Demo – Gemini + Flask Chat App

A simple AI chat web application built with Flask and Google Gemini API.
The app supports real-time chat, automatic model detection, and bilingual responses (Vietnamese + English).

🚀 Features

🔥 Google Gemini API integration

🧠 Auto-detect available Gemini model

🌐 REST API backend (Flask)

💬 Modern chat UI

🌍 Bilingual responses (VI / EN)

🛡 Secure API key via .env

⚡ Handles 404 model errors & 429 quota errors

🏗 Tech Stack

Python 3.10+

Flask

Google Generative Language API (Gemini)

HTML + CSS (Custom Chat UI)

dotenv

requests

📂 Project Structure
AI-demo/
│
├── app.py
├── templates/
│   └── index.html
├── static/
│   └── style.css
├── .env (not included)
├── .gitignore
└── README.md

⚙ Installation
1️⃣ Clone repository
git clone https://github.com/neoslvh/AI-demo.git
cd AI-demo

2️⃣ Create virtual environment
python -m venv venv


Activate:

Windows:

venv\Scripts\activate


Mac/Linux:

source venv/bin/activate

3️⃣ Install dependencies
pip install -r requirements.txt


If no requirements.txt yet:

pip install flask flask-cors requests python-dotenv

🔑 Setup API Key

Create .env file:

GOOGLE_API_KEY=your_api_key_here


⚠️ Do NOT commit .env to GitHub.

▶ Run Application
python app.py


Open browser:

http://127.0.0.1:5000

🧠 How It Works

The app automatically calls /v1beta/models

Selects a model that supports generateContent

Sends user message to Gemini API

Returns formatted response (Vietnamese + English)

⚠️ Common Errors
404 NOT_FOUND

Model not available → Auto detection handles this.

429 RESOURCE_EXHAUSTED

Quota exceeded → Enable billing or use new project.

🔐 Security Notes

API key stored in .env

.env ignored via .gitignore

No API key exposed in frontend

📌 Future Improvements

Add streaming response

Add conversation memory

Add Docker deployment

Improve UI animations

📜 License

MIT License

==========================================================

# 🤖 AI Demo – Ứng dụng Chat với Gemini + Flask

Ứng dụng chat AI đơn giản được xây dựng bằng Flask và Google Gemini API.
Hệ thống hỗ trợ trò chuyện thời gian thực, tự động phát hiện model Gemini phù hợp và trả lời song ngữ (Tiếng Việt + Tiếng Anh).

🚀 Tính năng chính

🔥 Tích hợp Google Gemini API

🧠 Tự động phát hiện model Gemini khả dụng

🌐 Backend REST API bằng Flask

💬 Giao diện chat hiện đại

🌍 Trả lời song ngữ (VI / EN)

🛡 Bảo mật API Key bằng .env

⚡ Xử lý lỗi 404 (model) và 429 (quota)

🏗 Công nghệ sử dụng

Python 3.10+

Flask

Google Generative Language API (Gemini)

HTML + CSS (Giao diện chat tùy chỉnh)

python-dotenv

requests

📂 Cấu trúc dự án
AI-demo/
│
├── app.py
├── templates/
│   └── index.html
├── static/
│   └── style.css
├── .env (không được push lên GitHub)
├── .gitignore
└── README.md

⚙ Hướng dẫn cài đặt
1️⃣ Clone repository
git clone https://github.com/neoslvh/AI-demo.git
cd AI-demo

2️⃣ Tạo môi trường ảo
python -m venv venv


Kích hoạt:

Windows:

venv\Scripts\activate


Mac/Linux:

source venv/bin/activate

3️⃣ Cài đặt thư viện

Nếu có file requirements.txt:

pip install -r requirements.txt


Nếu chưa có:

pip install flask flask-cors requests python-dotenv

🔑 Cấu hình API Key

Tạo file .env trong thư mục gốc:

GOOGLE_API_KEY=your_api_key_here


⚠️ Không được push file .env lên GitHub.

▶ Chạy ứng dụng
python app.py


Mở trình duyệt tại:

http://127.0.0.1:5000

🧠 Cách hoạt động

Ứng dụng gọi API /v1beta/models để lấy danh sách model khả dụng

Tự động chọn model hỗ trợ generateContent

Gửi nội dung người dùng tới Gemini API

Nhận và hiển thị phản hồi song ngữ

⚠️ Lỗi thường gặp
404 NOT_FOUND

Model không tồn tại → hệ thống tự động chọn lại model phù hợp.

429 RESOURCE_EXHAUSTED

Hết quota → cần bật Billing hoặc tạo project/API key mới.

🔐 Lưu ý bảo mật

API key được lưu trong .env

.env đã được thêm vào .gitignore

Không lộ API key ở frontend

📌 Hướng phát triển trong tương lai

Thêm tính năng streaming phản hồi

Lưu lịch sử hội thoại

Triển khai bằng Docker

Cải thiện animation giao diện

📜 Giấy phép

MIT License
