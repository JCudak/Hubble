from flask import Flask, jsonify
from pymongo import MongoClient
import random

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


def insert_initial_data():
    """ Function to insert initial data into MongoDB if collection is empty """
    count = collection.count_documents({})
    if count == 1000:
        return

    data_to_insert = []
    for i in range(1000 - count):
        data = {
            'name': f'User {i + 1}',
            'age': random.randint(20, 60),
            'city': 'City Name'
            # Add more fields as needed
        }
        data_to_insert.append(data)

    result = collection.insert_many(data_to_insert)
    print(f"Inserted {len(result.inserted_ids)} documents into 'mycollection'")


if __name__ == '__main__':
    insert_initial_data()
    app.run(host='0.0.0.0', port=5001)
