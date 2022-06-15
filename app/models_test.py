from sqlalchemy import Boolean, Table, Column, Integer, ForeignKey, String, Date
from sqlalchemy.orm import relationship
from .database_test import Base



class Fencer(Base):
    __tablename__ = 'fencer'
    id = Column(Integer, primary_key = True)
    name = Column(String)

class Bout(Base):
    __tablename__ = 'bout'
    id = Column(Integer, primary_key = True)
    w_score = Column(Integer)
    l_score = Column(Integer)
    w_fencer_id = Column(Integer, ForeignKey('fencer.id'))
    l_fencer_id = Column(Integer, ForeignKey('fencer.id'))