from flask import Flask
import requests
import threading
import logging
import time

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def query_service2_continuously():
    while True:
        logger.info("Querying service2")
        try:
            response = requests.get('http://service2.default.svc.cluster.local/query_service1')
            response.raise_for_status()
            logger.info(f"Received response from service2: {response.json()}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Request to service2 failed: {e}")
        # Wait for a specified interval before sending the next request
        time.sleep(10)  # Adjust the interval as needed


@app.route('/')
def home():
    return "Service is running", 200


if __name__ == '__main__':
    # Start the background thread that queries service2 continuously
    thread = threading.Thread(target=query_service2_continuously, daemon=True)
    thread.start()

    # Run the Flask application
    app.run(host='0.0.0.0', port=5003)
