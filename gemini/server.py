import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow frontend to communicate with backend

# Set up API key
API_KEY = "AIzaSyDuNCt9U-RBn4pNOXS_focEyMH1hmT8q2c"
genai.configure(api_key=API_KEY)

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        user_input = data.get("message", "")

        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(user_input)

        return jsonify({"response": response.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
