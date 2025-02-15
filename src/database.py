from sqlalchemy import create_engine
from langchain_community.utilities.sql_database import SQLDatabase
from config import db_user, db_password, db_host,db_port, db_name

def get_database():
    try:
        engine = create_engine(f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")
        db = SQLDatabase(engine)
        return db
    except Exception as e:
        print(f"Database connection failed: {str(e)}")
        exit()


    