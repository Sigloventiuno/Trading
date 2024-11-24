from flask import Flask, jsonify, request, render_template
import random

app = Flask(__name__)

# Game data
player_data = {
    "balance": 100,
    "inventory": {"Gold": 0, "Silver": 0, "Platinum": 0},
    "market_prices": {
        "Gold": random.randint(50, 100),
        "Silver": random.randint(20, 50),
        "Platinum": random.randint(100, 200),
    }
}

# Helper Functions
def generate_market_prices():
    """Generates new random market prices for items."""
    return {
        "Gold": random.randint(50, 100),
        "Silver": random.randint(20, 50),
        "Platinum": random.randint(100, 200),
    }


@app.route("/")
def index():
    """Serve the main HTML page."""
    return render_template("index.html")


@app.route("/api/market", methods=["GET"])
def get_market():
    """Get current market prices."""
    return jsonify(player_data["market_prices"])


@app.route("/api/player", methods=["GET"])
def get_player_data():
    """Get player balance and inventory."""
    return jsonify(
        {
            "balance": player_data["balance"],
            "inventory": player_data["inventory"],
        }
    )


@app.route("/api/buy", methods=["POST"])
def buy_item():
    """Buy items from the market."""
    data = request.json
    item = data.get("item")
    quantity = data.get("quantity")

    if item not in player_data["market_prices"]:
        return jsonify({"error": "Invalid item!"}), 400

    cost = player_data["market_prices"][item] * quantity
    if cost > player_data["balance"]:
        return jsonify({"error": "Not enough balance!"}), 400

    # Update balance and inventory
    player_data["balance"] -= cost
    player_data["inventory"][item] += quantity
    return jsonify({"success": f"Bought {quantity} {item}(s) for ${cost}."})


@app.route("/api/sell", methods=["POST"])
def sell_item():
    """Sell items to the market."""
    data = request.json
    item = data.get("item")
    quantity = data.get("quantity")

    if item not in player_data["inventory"]:
        return jsonify({"error": "Invalid item!"}), 400

    if quantity > player_data["inventory"][item]:
        return jsonify({"error": "Not enough items in inventory!"}), 400

    # Update balance and inventory
    revenue = player_data["market_prices"][item] * quantity
    player_data["balance"] += revenue
    player_data["inventory"][item] -= quantity
    return jsonify({"success": f"Sold {quantity} {item}(s) for ${revenue}."})


@app.route("/api/refresh", methods=["POST"])
def refresh_market():
    """Refresh the market prices."""
    player_data["market_prices"] = generate_market_prices()
    return jsonify({"success": "Market prices refreshed!"})


if __name__ == "__main__":
    app.run(debug=True)
