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
import time
from random import randint
from constants import *

# Setup connection to Elasticsearch on Docker
BASE_ELASTIC_INFO = Elasticsearch(
    hosts=["https://localhost:9200"],
    basic_auth=('elastic', 'ag80tinh5BKN-bBL2s0x'),
    ca_certs="flask/http_ca.crt",
    verify_certs=False
)


def index_data_from_csv(csvFile,
                        indexName="recipes",
                        es=BASE_ELASTIC_INFO,
                        limit=100):
    """
    Index data from a CSV file into Elasticsearch.
    This function reads a CSV file and indexes its contents into Elasticsearch with proper mapping.
    Each row in the CSV file is expected to have recipieID, title, ingredients, directions, and link columns.
    """
    # Read data from CSV file
    data = pd.read_csv(csvFile, nrows=limit)
    # Indexing documents
    ids = []
    for i, row in data.iterrows():
        document = {
            "title": row['title'],
            "ingredients": row['ingredients'],
            "directions": row['directions'],
            "description": "",
            "keywords": []
        }
        es.index(index=indexName, id=i,
                 document=document)  # Use recipeID as the document ID
        ids.append(i)
    return ids


def get_document(documentId, indexName="recipes", es=BASE_ELASTIC_INFO) -> dict:
    """
    Get a document by its ID.

    Raises a NotFoundError if the document does not exist.
    """
    resp = es.get(index=indexName, id=documentId)
    doc = resp['_source']
    doc[RECIPE_ID] = documentId
    return doc


def search_data(searchText, indexName="recipes", es=BASE_ELASTIC_INFO) -> list:
    """
    Search for documents that match the query.

    Returns a list of matching documents.
    """
    searchQuery = {
        "query_string": {
            "query":
                "*" + searchText + "*",
            "fields": [
                "title", "ingredients", "directions", "description", "keywords"
            ]
        }
    }
    resp = es.search(index=indexName, query=searchQuery)
    results = []
    for hit in resp['hits']['hits']:
        doc = hit['_source']
        doc[RECIPE_ID] = hit['_id']
        results.append(doc)
    return results


def insert_document(document,
                    index_name="recipes",
                    es=BASE_ELASTIC_INFO) -> int:
    "Inserts the document and returns it's new _id"
    resp = es.index(index=index_name, document=document)
    return resp['_id']


def update_document(documentId,
                    updateFields,
                    indexName="recipes",
                    es=BASE_ELASTIC_INFO) -> str:
    """
    Update a document by ID with new fields.

    Returns the 'result' field.
    """
    doc = updateFields
    resp = es.update(index=indexName, id=documentId, doc=doc)
    return resp['result']


def refresh_index(indexName="recipes", es=BASE_ELASTIC_INFO):
    """
    Refresh the index to make all operations performed available to search.
    """
    es.indices.refresh(index=indexName)


def delete_document(documentId, indexName="recipes", es=BASE_ELASTIC_INFO) -> str:
    """
    Delete a document by its ID.

    Returns the 'result' field. Raises a NotFoundError if the document does not exist.
    """
    resp = es.delete(index=indexName, id=documentId)
    return resp['result']


def get_random_document(indexName="recipes", es=BASE_ELASTIC_INFO):
    """
    Get a random document from the index.

    Returns the document on success or a dummy recipe on failure
    """
    # this has a very low requirement for 'randomness'
    random_seed = int(time.time()) + randint(1, 1000)
    rand_query = {
        "function_score": {
            "random_score": {
                "seed": random_seed,
                "field": "_seq_no"
            }
        }
    }
    try:
        resp = es.search(index=indexName, query=rand_query, size=1)
        for hit in resp['hits']['hits']:
            doc = hit['_source']
            doc[RECIPE_ID] = hit['_id']
            return doc
    except:
        return {
            RECIPE_ID: "-1",
            "title": "The Empty Recipe",
            "ingredients": ["Backend Dev's Tears"],
            "directions": "Step one: delete all other recipes.",
            "description": "This should never be returned",
            "keywords": ["uh oh"]
        }

def drop_index(index_name="recipes", es=BASE_ELASTIC_INFO):
    print(es.indices.delete(index=index_name))

def main():
    csvFile = "flask/RecipeNLG_dataset.csv"
    documentId = 1  # Example document ID

    # Indexing example
    index_data_from_csv(csvFile, limit=2)

    # Refresh index
    refresh_index()

    # Get document
    print(get_document(documentId))

    # Update document
    updateFields = {'title': 'Updated title here...', 'timestamp': datetime.now()}
    print(update_document(documentId, updateFields))

    get_document(documentId=documentId)
    print("Search result")
    # Search documents
    print(len(search_data("ksajfld;")))

    document = {
            "title": "ex title",
            "ingredients": ["potatoes", "broccoli"],
            "directions": "My very good directions",
            "description": "",
            "keywords": []
        }
    
    new_doc = insert_document(document)

    print(get_document(new_doc))

    # Delete document
    delete_document(new_doc)

    try:
        get_document(new_doc)
    except:
        print("Document was successfully deleted!")

if __name__ == "__main__":
    main()
