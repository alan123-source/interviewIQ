import logging
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine,text
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()
logger=logging.getLogger(__name__)

DATABASE_URL=os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set")

engine=create_engine(DATABASE_URL)

try:
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    logger.info("Database connection successfully")
except Exception as e:
    logger.error(
        "Database connection failed:%s",e
    )

SessionLocal=sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base=declarative_base()
