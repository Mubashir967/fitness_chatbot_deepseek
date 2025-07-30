# app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from chatbot import get_bot_response
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get("message", "")

    if not user_input:
        return jsonify({"response": "No message received."}), 400

    response = get_bot_response(user_input)
    return jsonify({"response": response})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 4000))  # Use Render-provided port if available
    app.run(host='0.0.0.0', port=port, debug=True)  # Bind to 0.0.0.0 so it's accessible
