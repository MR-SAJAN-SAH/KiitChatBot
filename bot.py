from flask import Flask, request, jsonify, render_template
from inference import generate_response

app = Flask(__name__)

@app.route("/")
def home():
    """Renders the chatbot UI."""
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    """Handles chat requests and returns AI-generated responses."""
    data = request.json
    user_input = data.get("message", "").strip()

    if not user_input:
        return jsonify({"error": "Empty input!"}), 400

    # Generate response using the existing retrieval + AI pipeline
    response = generate_response(user_input, k=10, temperature=0.7)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)  # Change debug=False for production
