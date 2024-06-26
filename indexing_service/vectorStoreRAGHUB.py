from DBManager import documentStoreDBManager, vectorEmbeddingsDBManager
from mongoConnector import MongoConnector
from weaviateConnector import weaviateConnector
from abc import ABC, abstractmethod
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.weaviate import WeaviateVectorStore


class vectorStore(ABC):
    @abstractmethod
    def __init__(self, vectorEmbeddingsDB : vectorEmbeddingsDBManager, documentDB : documentStoreDBManager) -> None:
        pass
    
    @abstractmethod
    def addDocument(self, documentID : str):
        pass

    @abstractmethod
    def removeDocument(self, documentID : str):
        pass

    @abstractmethod
    def getVectorStoreIndex(self):
        pass

class weaviateMongoVectorStore(vectorStore):
    def __init__(self, vectorEmbeddingsDB: weaviateConnector, documentDB: MongoConnector) -> None:
        self.vectorDB = vectorEmbeddingsDB
        self.documentDB = documentDB
        self.vectorStore = WeaviateVectorStore(self.vectorDB.getClient(), index_name= self.vectorDB.indexName)
        self.vectorStoreIndex = VectorStoreIndex.from_vector_store(self.vectorStore)

    def addDocument(self, documentID: str):
        doc = self.documentDB.getDocumentByID(documentID)
        self.vectorStoreIndex.insert(doc)

    def removeDocument(self, documentID: str):
        self.vectorStoreIndex.delete_ref_doc(documentID)

    def getVectorStoreIndex(self) -> VectorStoreIndex:
        return self.vectorStoreIndex
