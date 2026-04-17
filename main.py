from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
import datetime
import logging
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# API keys and endpoints
ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')
ALPHA_VANTAGE_BASE_URL = "https://www.alphavantage.co/query"

@app.route('/get_stock_data', methods=['GET'])
def get_stock_data():
    """
    Fetch stock data from Alpha Vantage API.
    """
    try:
        symbol = request.args.get('symbol')
        if not symbol:
            return jsonify({"error": "Symbol parameter is required"}), 400

        params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": symbol,
            "apikey": ALPHA_VANTAGE_API_KEY
        }

        response = requests.get(ALPHA_VANTAGE_BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

        if "Error Message" in data:
            return jsonify({"error": data["Error Message"]}), 400

        return jsonify(data), 200

    except requests.RequestException as e:
        logging.error(f"Request failed: {e}")
        return jsonify({"error": "Failed to fetch stock data"}), 500
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/place_trade', methods=['POST'])
def place_trade():
    """
    Place a trade based on AI predictions.
    """
    try:
        data = request.get_json()
        symbol = data.get('symbol')
        quantity = data.get('quantity')
        action = data.get('action')

        if not symbol or not quantity or not action:
            return jsonify({"error": "Symbol, quantity, and action are required"}), 400

        # Simulate AI prediction logic
        prediction = predict_market_trend(symbol)

        # Simulate trade execution
        trade_result = execute_trade(symbol, quantity, action, prediction)

        return jsonify({"message": "Trade placed successfully", "trade_result": trade_result}), 200

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return jsonify({"error": "Internal server error"}), 500

def predict_market_trend(symbol):
    """
    Simulate AI prediction of market trend.
    """
    # Placeholder for AI prediction logic
    return "BUY"

def execute_trade(symbol, quantity, action, prediction):
    """
    Simulate trade execution.
    """
    # Placeholder for trade execution logic
    return {
        "symbol": symbol,
        "quantity": quantity,
        "action": action,
        "prediction": prediction,
        "timestamp": datetime.datetime.now().isoformat()
    }

if __name__ == '__main__':
    app.run(debug=True)