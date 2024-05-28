from flask import Flask, jsonify
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

# Update MongoDB connection to use the service name created by Helm
client = MongoClient("mongodb://suu:suu@mongo-mongodb-headless:27017/suu_db")
db = client.suu_db
collection = db.mycollection

def serialize_document(document):
    """ Helper function to convert MongoDB document to JSON serializable format """
    if '_id' in document:
        document['_id'] = str(document['_id'])
    return document

@app.route('/data', methods=['GET'])
def get_data():
    data = collection.find_one()  # Fetch the first document
    if data:
        data = serialize_document(data)  # Convert ObjectId to string
    return jsonify(data), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
