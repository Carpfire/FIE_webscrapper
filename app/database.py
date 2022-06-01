from importlib.metadata import MetadataPathFinder
from sqlalchemy import MetaData, create_engine 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
import os


url = "sqlite:///./fencing.db"
engine = create_engine(url, connect_args={"check_same_thread": False})
SessionLocal = Session(engine)
Base = declarative_base()

    



