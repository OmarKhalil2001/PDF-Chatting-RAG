from DBManager import vectorEmbeddingsDBManager
import weaviate
from weaviate.connect import ConnectionParams
import dotenv,os

dotenv.load_dotenv()
GEMINI_API = os.getenv("GOOGLE_GEMINI_API")

class weaviateConnector(vectorEmbeddingsDBManager):
    DEFAULT_INDEX_NAME = "raghub"
    def __init__(self, port : str) -> None:
        connectionParameters = ConnectionParams.from_params(
            http_host="weaviate",
            http_port=int(port),
            http_secure=False,
            grpc_host="weaviate",
            grpc_port=50051,
            grpc_secure=False
        )
        self.client = weaviate.WeaviateClient(connection_params = connectionParameters, additional_headers={
            "X-Google-Studio-Api-Key": GEMINI_API
        })
        self.indexName = self.DEFAULT_INDEX_NAME
        self.client.connect()
    
    def setIndexName(self, indexName : str):
        if indexName != None:
            self.indexName = indexName
            
    def getClient(self):
        return self.client
    
    def deleteDocument(self, documentID):
        pass
