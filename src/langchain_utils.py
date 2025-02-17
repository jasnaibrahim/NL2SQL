import os
import logging
from langchain.chains import create_sql_query_chain
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from operator import itemgetter
from database import get_database
from table_details import table_chain as select_table
from prompts import final_prompt, answer_prompt

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Ensure API key is available
GROQ_API_KEY = os.getenv("LANGCHAIN_GROQ")
if not GROQ_API_KEY:
    raise ValueError("LANGCHAIN_GROQ API key is missing. Set it in your environment variables.")

# Initialize Database
db = get_database()
if not db:
    raise ValueError("Database connection failed. Check `get_database()` function.")

# Initialize LLM
llm = ChatGroq(
    model_name="llama3-70b-8192",
    groq_api_key=GROQ_API_KEY,
    temperature=0
)

# Initialize Query Chain (Reuse this across function calls)
generate_query = create_sql_query_chain(llm, db, final_prompt)
execute_query = QuerySQLDataBaseTool(db=db)
rephrase_answer = answer_prompt | llm | StrOutputParser()

# Define Chain
chain = (
    RunnablePassthrough.assign(table_names_to_use=select_table) |
    RunnablePassthrough.assign(query=generate_query).assign(
        result=itemgetter("query") | execute_query
    )
    | rephrase_answer
)

def invoke_chain(question, messages):
    """Handles the question-answering pipeline using LangChain."""
    logging.debug(f"Received question: {question}")
    logging.debug(f"Message history: {messages}")

    history = ChatMessageHistory()
    for message in messages:
        if message["role"] == "user":
            history.add_user_message(message["content"])
        else:
            history.add_ai_message(message["content"])

    try:
        response = chain.invoke({"question": question, "top_k": 3, "messages": history.messages})
        logging.debug(f"Generated response: {response}")
        return response
    except Exception as e:
        logging.error(f"Error in `invoke_chain()`: {str(e)}", exc_info=True)
        return {"error": str(e)}
