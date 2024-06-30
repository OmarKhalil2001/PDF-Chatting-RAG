from flask import Flask, request, jsonify
from mongoExtractor import MongoExtractor
from pymongo import MongoClient
import dotenv
import os

dotenv.load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
MONGO_COL = os.getenv("MONGO_COLLECTION")

mongoCl = MongoClient(MONGO_URI)

mongoExtractor = MongoExtractor(mongoCl, MONGO_DB_NAME, MONGO_COL)

app = Flask("Text_Extractor")

@app.route('/api', methods=['POST'])
def receive_file():
    if request.files["file"].headers["Content-Type"] != "application/pdf":
      return jsonify({"MESSAGE":"Only PDF files are supported now. More formats are coming in the future."})
    else:
      try:
        file = request.files["file"]
        id = mongoExtractor.storePDF(file)
        result = {
          "MESSAGE" : id,
          "STATUS": "SUCCESS"
        }
        return jsonify(result)
      except Exception as e:
        result = {
          "MESSAGE" : e,
          "STATUS": "FAILURE"
        }
        return jsonify(result)

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5040)