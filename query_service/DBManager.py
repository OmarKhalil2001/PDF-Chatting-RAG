# A set for abstract classes used to define and establish the responsibilities of the two types of databases
# used in this part of the project: noSQL and Vector Embeddings Database

from abc import ABC, abstractmethod
from llama_index.core import Document

#General Abstraction for Database Managers
class DBManager(ABC):
    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def getClient(self):
        pass 

# Type 1 of databases: noSQL, for storing text extracted from different resources
class documentStoreDBManager(DBManager):
    @abstractmethod
    def getDocumentByID(self, documentID : str) -> Document:
        pass

# Type 2 of databases: vector embeddings database, for storing vector embeddings of indexed documents used 
# by the LLM
class vectorEmbeddingsDBManager(DBManager):
    @abstractmethod
    def deleteDocument(self, documentID):
        pass
