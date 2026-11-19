
import os
from flask import Flask, request, jsonify, send_from_directory
from openai import OpenAI

app = Flask(__name__)

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "")

    if not isinstance(message, str) or not message.strip():
        return jsonify({"error": "Напиши сообщение"}), 400

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return jsonify({"error": "API-ключ ещё не настроен"}), 500

    try:
        client = OpenAI(api_key=api_key)

        response = client.responses.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
            instructions="Ты ULTRA GPT — полезный ИИ-помощник. Отвечай понятно на русском языке.",
            input=message[:6000]
        )

        return jsonify({"answer": response.output_text})

    except Exception:
        app.logger.exception("Ошибка API")
        return jsonify({"error": "Не удалось получить ответ ИИ"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
