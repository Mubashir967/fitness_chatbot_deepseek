from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv
from chatbot import answer_question, llm


load_dotenv()

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

app = Flask(__name__)
CORS(app)

# Use direct HTTP POST to DeepSeek API
def call_deepseek_api(user_message):
    url = "https://api.deepseek.com/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
    }

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "user", "content": user_message}
        ]
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        data = response.json()
        return data["choices"][0]["message"]["content"]
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "")
        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        response = answer_question(user_message, llm)
        return jsonify({"response": response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
