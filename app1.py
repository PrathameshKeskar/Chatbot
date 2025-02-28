from flask import Flask, render_template, request, jsonify
from chatbot import Chatbot
import os
import json

app = Flask(__name__)

# Initialize the chatbot with pre-loaded documentation
chatbot = Chatbot()

# Route for homepage
@app.route("/")
def home():
    return render_template("index.html")

# API route to handle user queries
@app.route("/ask", methods=["POST"])
def ask():
    query = request.json.get("question", "")
    if not query:
        return jsonify({"error": "No question provided"}), 400

    # Get the chatbot's response for the query
    response = chatbot.get_answer(query)
    return jsonify({"answer": response})

if __name__ == "__main__":
    app.run(debug=True)
