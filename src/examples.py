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
        "input": "List all employees working in the 'New York' office.",
        "query": "SELECT firstName, lastName FROM employees WHERE officeCode = (SELECT officeCode FROM offices WHERE city = 'New York');"
    },
    {
        "input": "Find the total number of customers in France.",
        "query": "SELECT COUNT(*) FROM customers WHERE country = 'France';"
    },
    {
        "input": "Get the total revenue generated from all payments.",
        "query": "SELECT SUM(amount) FROM payments;"
    },
    {
        "input": "Retrieve the names of customers who placed an order in 2024.",
        "query": "SELECT DISTINCT c.customerName FROM customers c JOIN orders o ON c.customerNumber = o.customerNumber WHERE EXTRACT(YEAR FROM o.orderDate) = 2024;"
    },
    {
        "input": "Find the total number of products in stock across all categories.",
        "query": "SELECT SUM(quantityInStock) FROM products;"
    },
    {
        "input": "Show the most expensive product in the database.",
        "query": "SELECT productName, buyPrice FROM products ORDER BY buyPrice DESC LIMIT 1;"
    },
    {
        "input": "Get details of pending orders.",
        "query": "SELECT * FROM orders WHERE status = 'Pending';"
    },
    {
        "input": "List all customers handled by 'Jane Doe'.",
        "query": "SELECT customerName FROM customers WHERE salesRepEmployeeNumber = (SELECT employeeNumber FROM employees WHERE firstName = 'Jane' AND lastName = 'Doe');"
    },
    {
        "input": "Find the top 3 customers with the highest credit limit.",
        "query": "SELECT customerName, creditLimit FROM customers ORDER BY creditLimit DESC LIMIT 3;"
    },
    {
        "input": "Show product details for items in the 'Trains' product line.",
        "query": "SELECT * FROM products WHERE productLine = 'Trains';"
    },
    {
        "input": "Retrieve the total quantity of '1969 Ford Mustang' sold.",
        "query": "SELECT SUM(quantityOrdered) FROM orderdetails WHERE productCode = 'S10_1678';"
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