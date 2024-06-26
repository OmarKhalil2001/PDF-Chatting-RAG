# A set for abstract classes used to define and establish the responsibilities of the two types of databases
# used in this part of the project: noSQL and Vector Embeddings Database

from abc import ABC, abstractmethod
from llama_index.core import Document

class DBManager(ABC):
    """
    General Abstraction for Database Managers    
    """
    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def getClient(self):
        """
        return Client object 
        """
        pass 

class documentStoreDBManager(DBManager):
    """
    Type 1 of databases: noSQL, for storing text extracted from different resources
    """
    @abstractmethod
    def getDocumentByID(self, documentID : str) -> Document:
        pass


class vectorEmbeddingsDBManager(DBManager):
    """
    Type 2 of databases: vector embeddings database, for storing vector embeddings of indexed documents used by the LLM
    """
    @abstractmethod
    def deleteDocument(self, documentID):
        """
        Delete Document from vector embeddings database. For some databases, it needs to be done manually. For others, it is done automatically by llamaIndex.
        """
        pass
