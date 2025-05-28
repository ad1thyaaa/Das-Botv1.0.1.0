from flask import Flask, render_template, request, jsonify, session
import dasbot

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # <-- Replace with your own secret key!

DASBOT_VERSION = "1.0.1.0"

@app.route("/")
def home():
    # Pass version to the template
    return render_template("index.html", version=DASBOT_VERSION)

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")

    # Initialize context in session if not present
    if 'context' not in session:
        session['context'] = {
            "awaiting_city": False,
            "awaiting_timezone": False,
            "awaiting_repeat": False
        }

    # Pass the session context to dasbot
    dasbot.context = session['context']

    # Get bot response with current context
    response = dasbot.get_bot_response(user_input)

    # Save updated context back to session
    session['context'] = dasbot.context

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
