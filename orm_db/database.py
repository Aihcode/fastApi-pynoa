import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

# SQLALCHEMY_DATABASE_URL = os.getenv("DB_URL")
# SQLALCHEMY_DATABASE_URL = os.getenv("DB_URL")
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://%s:%s@%s:%s/%s" % (os.getenv("DB_USER"), os.getenv("DB_PASSWORD"), os.getenv("DB_HOST"), os.getenv("DB_PORT"), os.getenv("DB_NAME"))
engine = create_engine(url=SQLALCHEMY_DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()