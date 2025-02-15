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
import os

def get_chain():
    db = get_database()
    llm = ChatGroq(
        model_name="llama3-8b-8192",
        groq_api_key=os.getenv("LANGCHAIN_GROQ"),
        temperature=0
    )
    generate_query = create_sql_query_chain(llm, db, final_prompt)
    execute_query = QuerySQLDataBaseTool(db=db)
    rephrase_answer = answer_prompt | llm | StrOutputParser()
    chain = (
        RunnablePassthrough.assign(table_names_to_use=select_table) |
        RunnablePassthrough.assign(query=generate_query).assign(
            result=itemgetter("query") | execute_query
        )
        | rephrase_answer
    )
    return chain

def invoke_chain(question, messages):
    chain = get_chain()
    history = ChatMessageHistory()
    for message in messages:
        if message["role"] == "user":
            history.add_user_message(message["content"])
        else:
            history.add_ai_message(message["content"])
    response = chain.invoke({"question": question, "top_k": 3, "messages": history.messages})
    return response