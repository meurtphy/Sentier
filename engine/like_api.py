from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route("/api/like", methods=["POST"])
def handle_like():
    data = request.json
    with open("likes.jsonl", "a") as f:
        f.write(json.dumps(data) + "\n")
    return jsonify({"status": "ok", "message": "Interaction enregistrée"}), 200

if __name__ == "__main__":
    app.run(debug=True)
