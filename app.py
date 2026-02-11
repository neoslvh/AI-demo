from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("Missing GOOGLE_API_KEY (or GEMINI_API_KEY) in .env")

BASE = "https://generativelanguage.googleapis.com/v1beta"
MODELS_URL = f"{BASE}/models"

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)

SELECTED_MODEL = None

def list_models():
    r = requests.get(
        MODELS_URL,
        headers={"X-Goog-Api-Key": API_KEY},
        timeout=15
    )
    if r.status_code != 200:
        raise RuntimeError(f"ListModels failed {r.status_code}: {r.text}")
    return r.json().get("models", [])

def pick_generate_content_model(models):
    candidates = []
    for m in models:
        name = m.get("name")  # "models/xxx"
        methods = m.get("supportedGenerationMethods", []) or []
        if name and "generateContent" in methods:
            candidates.append(name)

    if not candidates:
        raise RuntimeError("No model supports generateContent in this project/key.")

    def score(n: str):
        nlow = n.lower()
        s = 0
        if "gemini" in nlow: s += 10
        if "flash" in nlow: s += 5
        if "pro" in nlow: s += 3
        return -s

    candidates.sort(key=score)
    return candidates[0]

def get_selected_model(force_refresh=False):
    global SELECTED_MODEL
    if SELECTED_MODEL and not force_refresh:
        return SELECTED_MODEL

    models = list_models()
    SELECTED_MODEL = pick_generate_content_model(models)
    print("✅ Using model:", SELECTED_MODEL)
    return SELECTED_MODEL

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    user_input = (data.get("message") or "").strip()
    if not user_input:
        return jsonify({"error": "❌ Không có tin nhắn nào được gửi!"}), 400

    model_name = get_selected_model()
    endpoint = f"{BASE}/{model_name}:generateContent"

    # ✅ System instruction: bắt trả VI + EN rõ ràng
    system_instruction = (
        "Bạn là trợ lý AI song ngữ.\n"
        "Luôn trả lời theo đúng format sau (không thêm phần khác):\n"
        "VI: <câu trả lời tiếng Việt>\n"
        "EN: <English answer>\n"
        "Viết ngắn gọn, rõ ràng, đúng trọng tâm."
    )

    payload = {
        "contents": [
            {"role": "user", "parts": [{"text": user_input}]}
        ],
        "systemInstruction": {
            "parts": [{"text": system_instruction}]
        },
        "generationConfig": {
            "temperature": 0.6,
            "maxOutputTokens": 512
        }
    }

    try:
        r = requests.post(
            endpoint,
            headers={
                "Content-Type": "application/json",
                "X-Goog-Api-Key": API_KEY
            },
            json=payload,
            timeout=20
        )

        # 404 -> refresh model list rồi thử lại 1 lần
        if r.status_code == 404:
            model_name = get_selected_model(force_refresh=True)
            endpoint = f"{BASE}/{model_name}:generateContent"
            r = requests.post(
                endpoint,
                headers={
                    "Content-Type": "application/json",
                    "X-Goog-Api-Key": API_KEY
                },
                json=payload,
                timeout=20
            )

        if r.status_code == 429:
            return jsonify({"error": "⛔ 429: Hết quota / quota = 0. Bật billing hoặc dùng project/key khác."}), 429

        if r.status_code != 200:
            return jsonify({"error": f"🔴 Gemini lỗi {r.status_code}: {r.text}"}), 502

        result = r.json()
        candidates = result.get("candidates") or []
        if not candidates:
            return jsonify({"response": "⚠️ AI không có phản hồi."}), 200

        parts = candidates[0].get("content", {}).get("parts", []) or []
        text = parts[0].get("text") if parts else ""
        text = (text or "").strip()

        # ✅ Nếu model lỡ trả không đúng format, tự vá nhẹ
        if "VI:" not in text or "EN:" not in text:
            text = f"VI: {text}\nEN: {text}"

        return jsonify({"response": text}), 200

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"🔴 Lỗi kết nối API: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    try:
        get_selected_model()
    except Exception as e:
        print("❌ Startup model selection failed:", e)

    app.run(debug=True, host="0.0.0.0", port=port)
