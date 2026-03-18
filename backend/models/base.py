import os
from sqlalchemy.orm import declarative_base, sessionmaker, configure_mappers
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

# Base para todos os models
Base = declarative_base()

# URL do banco de dados via .env
DATABASE_URL = os.getenv("DATABASE_URL")

# Engine do SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    echo= False,  # Se quisermos um log do que tá acontecendo ao criar, setamos como true
    future=True
)

# Factory de sessões
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

configure_mappers()