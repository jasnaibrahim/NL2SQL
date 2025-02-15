from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_huggingface import HuggingFaceEmbeddings
from qdrant_client import QdrantClient
from langchain_community.vectorstores import Qdrant

def get_example_selector():
    # Initialize Qdrant client
    client = QdrantClient("localhost", port=6333)

    # Load embeddings model
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # Define all example SQL queries
    examples = [
    {
        "input": "List all customers in France with a credit limit over 20,000.",
        "query": "SELECT * FROM customers WHERE country = 'France' AND creditLimit > 20000;"
    },
    {
        "input": "Get the highest payment amount made by any customer.",
        "query": "SELECT MAX(amount) FROM payments;"
    },
    {
        "input": "Show product details for products in the 'Motorcycles' product line.",
        "query": "SELECT * FROM products WHERE productLine = 'Motorcycles';"
    },
    {
        "input": "Retrieve the names of employees who report to employee number 1002.",
        "query": "SELECT firstName, lastName FROM employees WHERE reportsTo = 1002;"
    },
    {
        "input": "List all products with a stock quantity less than 7000.",
        "query": "SELECT productName, quantityInStock FROM products WHERE quantityInStock < 7000;"
    },
    {
     'input':"what is price of `1968 Ford Mustang`",
     "query": "SELECT `buyPrice`, `MSRP` FROM products  WHERE `productName` = '1968 Ford Mustang' LIMIT 1;"   
    }
]


    # Create example selector
    example_selector = SemanticSimilarityExampleSelector.from_examples(
        examples,
        embeddings,
        Qdrant(client=client, collection_name="sql_examples", embeddings=embeddings),
        k=3,  # Adjust 'k' to change how many similar examples are retrieved
        input_keys=["input"]
    )

    return example_selector  