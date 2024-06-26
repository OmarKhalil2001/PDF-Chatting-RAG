import os, dotenv, threading, json
from RAGSettings import Setup
from weaviateConnector import weaviateConnector
from Query import Query
from queryHandler import weaviateQueryHandler
from kafka import KafkaConsumer, KafkaProducer


dotenv.load_dotenv()
Setup()

# Kafka Setup
KafkaServer = os.getenv("KAFKA_SERVER")
KafkaRequestsTopic = os.getenv("KAFKA_QUERY_SERVICE_REQUESTS")
KafkaResponseTopic = os.getenv("KAFKA_QUERY_SERVICE_RESPONSE")

kafkaConsumer = KafkaConsumer(
    auto_offset_reset="earliest", 
    enable_auto_commit=True,
    bootstrap_servers=[KafkaServer]
)

kafkaConsumer.subscribe(KafkaRequestsTopic)

kafkaProducer = KafkaProducer(bootstrap_servers=[KafkaServer])

#Weaviate Setup
weavPort = os.getenv("WEAVIATE_PORT")
weavCol = os.getenv("WEAVIATE_COLLECTION")

weaviateDB = weaviateConnector(weavPort)
weaviateDB.setIndexName(weavCol)
# for item in weaviateDB.client.collections.get("RAGHUB").iterator():
#     print(item)
#Query Setup
ThreadsCount = int(os.getenv("THREAD_COUNT"))

queryHandler = weaviateQueryHandler(weaviateDB)
Semaphore = threading.Semaphore(ThreadsCount)

def processQuery(RequestValue, queryHandler : weaviateQueryHandler, semaphore: threading.Semaphore, kafkaProd : KafkaProducer):
    semaphore.acquire()
    print("started")
    queryObj = Query(RequestValue)
    queryResponse = queryHandler.answer(queryObj)
    queryResponseJSON = json.dumps(queryResponse)
    print(queryResponseJSON)
    kafkaProd.send(KafkaResponseTopic, queryResponseJSON.encode())
    semaphore.release()

for request in kafkaConsumer:
    requestThread = threading.Thread(target=processQuery, args=(request.value, queryHandler, Semaphore, kafkaProducer))
    requestThread.start()

