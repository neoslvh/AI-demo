from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv
import json

# Tải API Key từ file .env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={GEMINI_API_KEY}"

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)  # Cho phép frontend gọi API

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message", "").strip()

    if not user_input:
        return jsonify({"error": "❌ Không có tin nhắn nào được gửi!"}), 400

    payload = {
        "contents": [{"parts": [{"text": user_input}]}]
    }

    try:
        response = requests.post(GEMINI_ENDPOINT, json=payload)
        result = response.json()

        # Debug: In kết quả API ra terminal
        print("📥 API Response:", json.dumps(result, indent=2, ensure_ascii=False))

        if "candidates" in result and len(result["candidates"]) > 0:
            ai_response = result["candidates"][0]["content"]["parts"][0]["text"]
        else:
            ai_response = "⚠️ AI không có phản hồi."

        return jsonify({"response": ai_response})

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"🔴 Lỗi kết nối API: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"⚠️ Lỗi không xác định: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port = port)
