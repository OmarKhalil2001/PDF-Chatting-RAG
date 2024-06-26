import json
from llama_index.core.vector_stores import ExactMatchFilter, MetadataFilters


class Query:
    def __init__(self, queryDetails : bytes) -> None:
        self.queryDetails = json.loads(queryDetails.decode())
        
        if self.queryDetails.get("queryID", None) == None:
            raise Exception("No document ID provided")
        elif self.queryDetails.get("queryText", "") == "":
            raise Exception("Query text was empty")
        elif self.queryDetails.get("Documents", None) == None:
            raise Exception("Missing document filters")

        self.queryID = self.queryDetails["queryID"]
        self.queryText = self.queryDetails["queryText"]
        self.documentFilters =  self.queryDetails["Documents"]
    
    def getQueryID(self):
        return self.queryID
    
    def getQueryText(self):
        return self.queryText
    
    def getDocumentFilters(self):
        filters = MetadataFilters(
            filters = [
                ExactMatchFilter(key = "ref_doc_id", value = document) for document in self.documentFilters
            ]
        )
        return filters