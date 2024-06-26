import os, dotenv, threading, json
from RAGSettings import Setup
from mongoConnector import MongoConnector
from weaviateConnector import weaviateConnector
from vectorStoreRAGHUB import weaviateMongoVectorStore
from kafka import KafkaConsumer

dotenv.load_dotenv()
Setup()

# Kafka Setup
KafkaServer = os.getenv("KAFKA_SERVER")
KafkaTopic = os.getenv("KAFKA_INDEXING_SERVICE_REQUESTS")

kafkaConsumer = KafkaConsumer(
    auto_offset_reset="earliest", 
    enable_auto_commit=True,
    bootstrap_servers=[KafkaServer]
)

kafkaConsumer.subscribe(KafkaTopic)

#MongoDB Connection
mongoURI = os.getenv("MONGO_URI")
mongoDBName = os.getenv("MONGO_DB_NAME")
mongoCol = os.getenv("MONGO_COLLECTION")

mongoDB = MongoConnector(mongoURI)

mongoDB.setDatabase(mongoDBName)
mongoDB.setCollection(mongoCol)

#Weaviate Setup
weavPort = os.getenv("WEAVIATE_PORT")
weavCol = os.getenv("WEAVIATE_COLLECTION")

weaviateDB = weaviateConnector(weavPort)
weaviateDB.setIndexName(weavCol)

#Indexing Setup
ThreadsCount = int(os.getenv("THREAD_COUNT"))
vectorStore = weaviateMongoVectorStore(weaviateDB, mongoDB)

Semaphore = threading.Semaphore(ThreadsCount)

def processAddRequest(documentID : str, semaphore : threading.Semaphore, vectorStore : weaviateMongoVectorStore):
    semaphore.acquire()
    try:
        vectorStore.addDocument(documentID)
        print("Success")
    except Exception as e:
        print(e)
    semaphore.release()

def processRemoveRequest(documentID : str, semaphore : threading.Semaphore, vectorStore : weaviateMongoVectorStore):
    semaphore.acquire()
    vectorStore.removeDocument(documentID)
    semaphore.release()


for request in kafkaConsumer:
    requestDic = json.loads(request.value.decode())
    if requestDic["RequestType"] == "ADD":
        requestThread = threading.Thread(
            target=processAddRequest, 
            args=(requestDic["DocumentID"], Semaphore, vectorStore)
            )
        requestThread.start()
    elif requestDic["RequestType"] == "REMOVE":
        requestThread = threading.Thread(
            target=processRemoveRequest, 
            args=(requestDic["DocumentID"], Semaphore, vectorStore)
            )
        requestThread.start()