from pymongo import MongoClient
import PyPDF2
from kafka import KafkaProducer
import dotenv
import os, json, time

dotenv.load_dotenv()

KAFKA_SERVER = os.getenv("KAFKA_SERVER")
KAFKA_INDEXING_TOPIC = os.getenv("KAFKA_INDEXING_SERVICE_REQUESTS")

class MongoExtractor():
    KAFKA_PRODUCER = KafkaProducer(bootstrap_servers=[KAFKA_SERVER])
    def __init__(self, client: MongoClient, databasName : str, collection : str) -> None:
        self.client = client
        self.database = self.client[databasName]
        self.collection = self.database[collection]

    def extractTextPDF(self, file) -> str:
        text = ""
        reader = PyPDF2.PdfReader(file)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text() or ""
        return text
    
    def storePDF(self, file) -> str:
        text = self.extractTextPDF(file)
        result = self.collection.insert_one(
            {
                "text":text
            }
        )

        kafkaMsg = {
            "RequestType": "ADD",
            "DocumentID": str(result.inserted_id)
        }

        MongoExtractor.KAFKA_PRODUCER.send(topic=KAFKA_INDEXING_TOPIC, value=json.dumps(kafkaMsg).encode())
        
        time.sleep(3)
        
        return str(result.inserted_id)

        