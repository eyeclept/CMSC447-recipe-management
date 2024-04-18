"""
Author:  Richard Baldwin
Date:    /2024
E-mail:  richarb1@umbc.edu
Description: 
    -
Install Info:
      pip install elasticsearch
"""
# imports
from elasticsearch import Elasticsearch
import pandas as pd
# constants

# classes


# main function
def main():
    """
    use-----> 
    input---> 
    output--> 
    details-> 
    """
    # Setup connection to Elasticsearch on Docker
    es = Elasticsearch(hosts=["localhost:9200"])
    
    indexName = "documents"
    csvFile = "testdata.csv"

    # Index data from CSV
    indexDataFromCsv(es, indexName, csvFile)

    # Example search
    searchText = "example search text"
    searchData(es, indexName, searchText)

# functions
def function():
    """
    use-----> 
    input---> 
    output--> 
    details-> 
    """
    pass
def indexDataFromCsv(es, indexName, csvFile):
    """
    use-----> 
    input---> 
    output--> 
    details-> 
    """
    # Read data from CSV file
    data = pd.read_csv(csvFile)

    # Create the index if it doesn't exist
    if not es.indices.exists(index=indexName):
        es.indices.create(index=indexName, ignore=400)
    
    # Indexing documents
    for _, row in data.iterrows():
        document = {
            "title": row['title'],
            "description": row['description']
        }
        es.index(index=indexName, id=row['id'], document=document)

def searchData(es, indexName, searchText):
    """
    use-----> 
    input---> 
    output--> 
    details-> 
    """
    # Search query
    searchQuery = {
        "query": {
            "multi_match": {
                "query": searchText,
                "fields": ["title", "description"]
            }
        }
    }
    res = es.search(index=indexName, query=searchQuery)
    print("Search results:")
    for hit in res['hits']['hits']:
        print(hit['_source'])

# prebuiltFuncts
if __name__ == "__main__":
    main()

