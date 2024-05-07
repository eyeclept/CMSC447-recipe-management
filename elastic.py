"""
Author:  Richard Baldwin
Date:    /2024
E-mail:  richarb1@umbc.edu
Description: 
    -
Install Info:
      pip install elasticsearch pandas
"""
from datetime import datetime
from elasticsearch import Elasticsearch
import pandas as pd
import time  # To allow indexing to complete before searching

# Setup connection to Elasticsearch on Docker
BASE_ELASTIC_INFO = Elasticsearch(
    hosts=["https://localhost:9200"],
    basic_auth=('elastic', 'changeme'),
    ca_certs="./ca.crt",
    verify_certs=False
)

def indexDataFromCsv(csvFile, indexName = "recipes", es = BASE_ELASTIC_INFO):
    """
    Index data from a CSV file into Elasticsearch.
    This function reads a CSV file and indexes its contents into Elasticsearch with proper mapping.
    Each row in the CSV file is expected to have recipieID, title, ingredients, directions, and link columns.
    """
    # Read data from CSV file
    data = pd.read_csv(csvFile)
    
    # Indexing documents
    for _, row in data.iterrows():
        document = {
            "recipeID": row['#'], 
            "title": row['title'],
            "ingredients": row['ingredients'],
            "directions": row['directions'],
            "link": row['link']
        }
        resp = es.index(index=indexName, id=row['recipeID'], document=document)  # Use recipeID as the document ID
        print(resp['result'])


def getDocument(documentId, indexName = "recipes", es = BASE_ELASTIC_INFO):
    """
    Get a document by its ID.
    """
    resp = es.get(index=indexName, id=documentId)
    print(resp['_source'])

def searchData(searchText, indexName = "recipes", es = BASE_ELASTIC_INFO):
    """
    Search for documents that match the query.
    """
    searchQuery = {"match": {"text": searchText}}
    resp = es.search(index=indexName, query=searchQuery)
    print("Got %d Hits:" % resp['hits']['total']['value'])
    for hit in resp['hits']['hits']:
        print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])

def updateDocument(documentId, updateFields, indexName = "recipes", es = BASE_ELASTIC_INFO):
    """
    Update a document by ID with new fields.
    """
    doc = {
        'doc': updateFields
    }
    resp = es.update(index=indexName, id=documentId, doc=doc)
    print(resp['result'])

def refreshIndex(indexName = "recipes", es = BASE_ELASTIC_INFO):
    """
    Refresh the index to make all operations performed available to search.
    """
    es.indices.refresh(index=indexName)

def deleteDocument(documentId, indexName = "recipes", es = BASE_ELASTIC_INFO):
    """
    Delete a document by its ID.
    """
    resp = es.delete(index=indexName, id=documentId)
    print(resp['result'])

def main():
    csvFile = "testdata.csv"
    documentId = 1  # Example document ID

    # Indexing example
    indexDataFromCsv(csvFile)

    # Refresh index
    refreshIndex()

    # Get document
    getDocument(documentId)

    # Update document
    updateFields = {'title': 'Updated title here...', 'timestamp': datetime.now()}
    updateDocument(documentId, updateFields)

    # Search documents
    searchData("Updated")

    # Delete document
    deleteDocument(documentId)

if __name__ == "__main__":
    main()
