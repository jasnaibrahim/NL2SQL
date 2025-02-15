import os
from dotenv import load_dotenv

load_dotenv()

# Database configuration
db_user = os.getenv("db_user")
db_password = os.getenv("db_password")
db_host = os.getenv("db_host")
db_port=os.getenv("db_port")
db_name = os.getenv("db_name")

# API keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
GROQ_API_KEY = os.getenv("LANGCHAIN_GROQ")