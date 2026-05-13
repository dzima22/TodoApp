from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
 
sql_alchemy_database_url='sqlite:///./todosappc.db'

engine=create_engine(sql_alchemy_database_url,connect_args={"check_same_thread":False})

SessionLocal=sessionmaker(autocommit=False, autoflush=False,bind=engine)

Base=declarative_base()

