from flask import Flask, request, jsonify
from flask_cors import CORS
from chatbot import get_bot_response

app = Flask(__name__)
CORS(app)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    
    try:
        bot_response = get_bot_response(user_message)
        return jsonify({"response": bot_response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Add this to run the app locally (optional for Render, but useful for testing)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000)
