from abc import ABC, abstractmethod
from Query import Query
from weaviateConnector import weaviateConnector    
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.weaviate import WeaviateVectorStore

class queryHandler(ABC):
    @abstractmethod
    def __init__(self, vectorDBClient : any) -> None:
        pass
    
    @abstractmethod
    def answer(self, queryObj : Query) -> dict[str, str]:
        pass

class weaviateQueryHandler(queryHandler):
    def __init__(self, vectorDBClient: weaviateConnector) -> None:
        self.vectorStore = WeaviateVectorStore(vectorDBClient.getClient(), index_name= vectorDBClient.indexName)
        self.vectorStoreIndex = VectorStoreIndex.from_vector_store(self.vectorStore)
    
    def answer(self, queryObj: Query) -> dict[str, str]:
        engine = self.vectorStoreIndex.as_query_engine(filters = queryObj.getDocumentFilters())
        queryResponse = engine.query(queryObj.getQueryText())

        responsePacket = {
            "queryID" : queryObj.getQueryID(),
            "queryAnswer" : queryResponse.response
        }

        return responsePacket

