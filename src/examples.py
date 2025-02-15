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
        "query": "SELECT * FROM customers WHERE country = 'France' AND creditlimit > 20000;"
    },
    {
        "input": "Get the highest payment amount made by any customer.",
        "query": "SELECT MAX(amount) FROM payments;"
    },
    {
        "input": "Show product details for products in the 'Motorcycles' product line.",
        "query": "SELECT * FROM products WHERE productline = 'Motorcycles';"
    },
    {
        "input": "Retrieve the names of employees who report to employee number 1002.",
        "query": "SELECT firstname, lastname FROM employees WHERE reportsto = 1002;"
    },
    {
        "input": "List all products with a stock quantity less than 7000.",
        "query": "SELECT productname, quantityinstock FROM products WHERE quantityinstock < 7000;"
    },
    {
        "input": "What is the price of '1968 Ford Mustang'?",
        "query": "SELECT buyprice, msrp FROM products WHERE productname = '1968 Ford Mustang' FETCH FIRST 1 ROW ONLY;"   
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
# if __name__ == "__main__":
#     try:
#         example_selector = get_example_selector()
#         test_query = "Find all customers in Germany with high credit limits."
#         retrieved_examples = example_selector.select_examples({"input": test_query})

#         print("✅ Example Selector Initialized Successfully!")
#         print("🔍 Test Query:", test_query)
#         print("📌 Retrieved Similar Examples:")
#         for example in retrieved_examples:
#             print(f" - Input: {example['input']}\n   Query: {example['query']}\n")

#     except Exception as e:
#         print("❌ Error:", str(e))