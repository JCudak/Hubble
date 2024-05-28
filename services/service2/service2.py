from flask import Flask, jsonify
import requests
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/query_service1', methods=['GET'])
def query_service1():
    logger.info("Querying service1")
    try:
        response = requests.get('http://service1.default.svc.cluster.local/data')
        response.raise_for_status()
        logger.info(f"Received response from service1: {response.json()}")
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        logger.error(f"Request to service1 failed: {e}")
        return jsonify({"error": "Failed to query service1", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
