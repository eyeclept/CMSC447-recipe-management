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
es = Elasticsearch(
    hosts=["https://localhost:9200"],
    basic_auth=('elastic', 'changeme'),
    ca_certs="./ca.crt",
    verify_certs=False
)

def indexDataFromCsv(es, indexName, csvFile):
    """
    Index data from a CSV file into Elasticsearch.
    """
    data = pd.read_csv(csvFile)
    for _, row in data.iterrows():
        doc = {
            "title": row['title'],
            "ingredients": row['ingredients'],
            "directions": row['directions'],
            "description": row['description'],
            "keywords": row['keywords'].split(', '),
            "timestamp": datetime.now()
        }
        resp = es.index(index=indexName, id=row['id'], document=doc)
        print(resp['result'])

def getDocument(es, indexName, documentId):
    """
    Get a document by its ID.
    """
    resp = es.get(index=indexName, id=documentId)
    print(resp['_source'])

def searchData(es, indexName, searchText):
    """
    Search for documents that match the query.
    """
    searchQuery = {"match": {"text": searchText}}
    resp = es.search(index=indexName, query=searchQuery)
    print("Got %d Hits:" % resp['hits']['total']['value'])
    for hit in resp['hits']['hits']:
        print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])

def updateDocument(es, indexName, documentId, updateFields):
    """
    Update a document by ID with new fields.
    """
    doc = {
        'doc': updateFields
    }
    resp = es.update(index=indexName, id=documentId, doc=doc)
    print(resp['result'])

def refreshIndex(es, indexName):
    """
    Refresh the index to make all operations performed available to search.
    """
    es.indices.refresh(index=indexName)

def deleteDocument(es, indexName, documentId):
    """
    Delete a document by its ID.
    """
    resp = es.delete(index=indexName, id=documentId)
    print(resp['result'])

def main():
    indexName = "recipes"
    csvFile = "testdata.csv"
    documentId = 1  # Example document ID

    # Indexing example
    indexDataFromCsv(es, indexName, csvFile)

    # Refresh index
    refreshIndex(es, indexName)

    # Get document
    getDocument(es, indexName, documentId)

    # Update document
    updateFields = {'text': 'Updated text here...', 'timestamp': datetime.now()}
    updateDocument(es, indexName, documentId, updateFields)

    # Search documents
    searchData(es, indexName, "Updated")

    # Delete document
    deleteDocument(es, indexName, documentId)

if __name__ == "__main__":
    main()
