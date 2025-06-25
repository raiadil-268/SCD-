from flask import Flask, jsonify, request
import json

app = Flask(__name__)

# Load data
def load_data():
    with open("data.json", "r") as file:
        return json.load(file)

# Save data
def save_data(data):
    with open("data.json", "w") as file:
        json.dump(data, file, indent=2)

# Get all players
@app.route("/players", methods=["GET"])
def get_players():
    data = load_data()
    return jsonify(data)

# Add new player
@app.route("/players", methods=["POST"])
def add_player():
    new_player = request.json
    data = load_data()
    data.append(new_player)
    save_data(data)
    return jsonify({"message": "Player added successfully"}), 201

# Get player by name
@app.route("/players/<string:name>", methods=["GET"])
def get_player(name):
    data = load_data()
    for player in data:
        if player["name"].lower() == name.lower():
            return jsonify(player)
    return jsonify({"error": "Player not found"}), 404

# Compare two players
@app.route("/compare", methods=["POST"])
def compare_players():
    req = request.json
    player1_name = req.get("player1")
    player2_name = req.get("player2")
    data = load_data()
    p1 = next((p for p in data if p["name"].lower() == player1_name.lower()), None)
    p2 = next((p for p in data if p["name"].lower() == player2_name.lower()), None)
    if not p1 or not p2:
        return jsonify({"error": "One or both players not found"}), 404

    comparison = {
        "Player 1": p1["name"],
        "Player 2": p2["name"],
        "Higher Runs": p1["name"] if p1["runs"] > p2["runs"] else p2["name"],
        "Better Average": p1["name"] if p1["average"] > p2["average"] else p2["name"]
    }
    return jsonify(comparison)

if __name__ == "__main__":
    app.run(debug=True)
