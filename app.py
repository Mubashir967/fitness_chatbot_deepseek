from flask import Flask, request, jsonify
from flask_cors import CORS
from chatbot import get_bot_response
import os

app = Flask(__name__)
CORS(app)

# Default GET route for Render testing
@app.route("/", methods=["GET"])
def index():
    return "✅ Fitness Chatbot API is running."

# POST route for chat functionality
@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_input = request.json.get("message")
        if not user_input:
            return jsonify({"error": "No message provided"}), 400

        bot_response = get_bot_response(user_input)
        return jsonify({"response": bot_response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Use the PORT from environment (Render requires this)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
