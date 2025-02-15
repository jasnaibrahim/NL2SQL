from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, FewShotChatMessagePromptTemplate, PromptTemplate
from examples import get_example_selector

example_prompt = ChatPromptTemplate.from_messages(
    [
        ("human", "{input}\nSQLQuery:"),
        ("ai", "{query}"),
    ]
)

few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    example_selector=get_example_selector(),
    input_variables=["input", "top_k"],
)
final_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a PostgreSQL expert. Given an input question, create a syntactically correct PostgreSQL query to run. Use standard PostgreSQL functions and syntax.\n\nHere is the relevant table info: {table_info}\n\nBelow are a number of examples of questions and their corresponding SQL queries."),
        few_shot_prompt,
        MessagesPlaceholder(variable_name="messages"),
        ("human", "{input}"),
    ]
)

answer_prompt = PromptTemplate.from_template(
    """Given the following user question, corresponding SQL query, and SQL result, answer the user question.

Question: {question}
SQL Query: {query}
SQL Result: {result}
Answer: """
)
# if __name__ == "__main__":
#     try:
#         # Test final prompt formatting
#         test_input = {
#             "table_info": "Table: customers (id, name, country, creditLimit)",
#             "messages": [],
#             "input": "Get all customers from France.",
#             "top_k": 3
#         }
#         test_final_prompt = final_prompt.format(**test_input)

#         # Test answer prompt formatting
#         test_answer_prompt = answer_prompt.format(
#             question="Who are the customers from France?",
#             query="SELECT * FROM customers WHERE country = 'France';",
#             result="[{'id': 1, 'name': 'John Doe', 'country': 'France'}, {'id': 2, 'name': 'Jane Smith', 'country': 'France'}]"
#         )

#         print("✅ Final Prompt Initialized Successfully!")
#         print("📌 Sample Final Prompt Output:\n", test_final_prompt, "\n")

#         print("✅ Answer Prompt Initialized Successfully!")
#         print("📌 Sample Answer Prompt Output:\n", test_answer_prompt, "\n")

#     except Exception as e:
#         print("❌ Error:", str(e))

