"""
Author:  Richard Baldwin
Date:    /2024
E-mail:  richarb1@umbc.edu
Description: 
    -
Install Info:
      pip install elasticsearch pandas
"""
# imports
from elasticsearch import Elasticsearch
import pandas as pd
import time  # To allow indexing to complete before searching
# constants

# classes

# main function
def main():
    """
    use-----> Main entry for script execution.
    input---> 
    output--> 
    details-> Main function to index data and perform search queries.
    """
    # Setup connection to Elasticsearch on Docker
    es = Elasticsearch(hosts=["localhost:9200"])
    
    indexName = "recipes"
    csvFile = "testdata.csv"

    # Delete and re-create the index to start fresh
    if es.indices.exists(index=indexName):
        es.indices.delete(index=indexName)
    indexDataFromCsv(es, indexName, csvFile)

    # Allow some time for Elasticsearch to index the data
    time.sleep(2)

    # Test the Elasticsearch setup
    testElasticsearch(es, indexName)

# functions
def indexDataFromCsv(es, indexName, csvFile):
    """
    use-----> Index data from a CSV file into Elasticsearch.
    input---> Elasticsearch instance, index name, CSV file path.
    output--> None, indexes data to Elasticsearch.
    details-> This function reads a CSV file and indexes its contents into Elasticsearch with proper mapping.
    """
    # Read data from CSV file
    data = pd.read_csv(csvFile)

    # Define the mapping for the Elasticsearch index
    mapping = {
        "mappings": {
            "properties": {
                "title": {"type": "text"},
                "ingredients": {"type": "text"},
                "directions": {"type": "text"},
                "description": {"type": "text"},
                "keywords": {"type": "keyword"}
            }
        }
    }

    # Create the index with the mapping
    es.indices.create(index=indexName, body=mapping, ignore=400)
    
    # Indexing documents
    for _, row in data.iterrows():
        document = {
            "title": row['title'],
            "ingredients": row.get('ingredients', ''),
            "directions": row.get('directions', ''),
            "description": row['description'],
            "keywords": row.get('keywords', '').split(', ')
        }
        es.index(index=indexName, id=row['id'], document=document)

def searchData(es, indexName, searchText):
    """
    use-----> Perform a search query in Elasticsearch.
    input---> Elasticsearch instance, index name, search text.
    output--> Prints search results.
    details-> This function uses a multi_match query to search across multiple fields.
    """
    # Search query
    searchQuery = {
        "query": {
            "multi_match": {
                "query": searchText,
                "fields": ["title", "ingredients", "description", "directions"]
            }
        }
    }
    res = es.search(index=indexName, query=searchQuery)
    print("Search results:")
    for hit in res['hits']['hits']:
        print(hit['_source'])

def testElasticsearch(es, indexName):
    """
    use-----> Test the functionality of Elasticsearch with example queries.
    input---> Elasticsearch instance, index name.
    output--> Prints results of test queries.
    details-> This function tests various search aspects to verify indexing and search capabilities.
    """
    print("\nTesting Elasticsearch Index...")
    # Example search queries
    testQueries = ["tomato", "pesto", "chocolate"]
    for query in testQueries:
        print(f"\nSearching for '{query}'...")
        searchData(es, indexName, query)

# prebuiltFuncts
if __name__ == "__main__":
    main()
