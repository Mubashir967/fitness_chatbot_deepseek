from flask import Flask, request, jsonify
from flask_cors import CORS
from chatbot import get_bot_response  # make sure this function exists in chatbot.py

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "✅ Fitness Chatbot API is running."

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message")
    if not message:
        return jsonify({"error": "No message provided"}), 400

    response = get_bot_response(message)  # This should call your LangChain logic
    return jsonify({"response": response})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
