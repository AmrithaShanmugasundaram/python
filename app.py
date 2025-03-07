from flask import Flask, request, jsonify
import pandas as pd
import numpy as np

app = Flask(__name__)

# Sample API to process data
@app.route('/process', methods=['POST'])
def process_data():
    data = request.json.get("data", [])
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    df = pd.DataFrame(data)
    df["sum"] = df.sum(axis=1)  # Example operation

    return jsonify(df.to_dict(orient="records"))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
