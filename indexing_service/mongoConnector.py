from DBManager import documentStoreDBManager
from llama_index.core import Document
from pymongo import MongoClient
from bson.objectid import ObjectId


class MongoConnector(documentStoreDBManager):
    def __init__(self, URI: str) -> None:
        self.client = MongoClient(URI)
        self.database = None
        self.collection = None

    def setDatabase(self, database_name : str) -> None:
        self.database = self.client.get_database(database_name)
        self.collection = None

    def setCollection(self, CollectionName)-> None:
        if(self.database is None):
            raise Exception("Database was not set")
        self.collection = self.database.get_collection(CollectionName)
    
    def getClient(self):
        return self.client
    
    def getDocumentByID(self, documentID : str) -> Document:
        if self.database is None:
            raise Exception("Database was not set")
        
        if self.collection is None:
             raise Exception("Collection was not set")
                
        mongo_document = self.collection.find_one(
            {
                "_id": ObjectId(documentID)
            }
        )
        
        if mongo_document == None:
            raise Exception(f"Could not find document with ID: {documentID}.")
        
        # Mongo Schema must include text, tell Essawy
        llamaDocument = Document(
            doc_id = documentID,
            text = mongo_document["text"]
        )

        return llamaDocument
