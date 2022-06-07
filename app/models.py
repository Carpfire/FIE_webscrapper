from sqlalchemy import Boolean, Table, Column, Integer, ForeignKey, String, Date
from sqlalchemy.orm import relationship
from .database import Base


fencers = Table(
    'fencers_bouts',
    Base.metadata,
    Column('fencers_id', Integer, ForeignKey('fencer.id')), 
    Column('bout_id', Integer, ForeignKey('bout.id')) 
)

tourn_fen = Table(
    'fencers_tournament',
    Base.metadata, 
    Column('fencer_id', Integer, ForeignKey('fencer.id')),
    Column('tournament_id', Integer, ForeignKey('tournament.id'))
)



class Fencer(Base):

    __tablename__ = 'fencer'
    id = Column(Integer, primary_key = True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    country = Column(String(255))



class Tournament(Base):
    
    __tablename__ = 'tournament'
    id = Column(Integer, primary_key=True)
    country = Column(String(255))
    city = Column(String(255))
    start_date = Column(Date)
    end_date = Column(Date)
    bouts = relationship('Bout', backref='tournament', lazy='select')
    fencers = relationship('Fencer', secondary=tourn_fen, backref='tournament', lazy='select')



class Bout(Base):

    __tablename__ = 'bout'
    id = Column(Integer, primary_key = True)
    tournament_id = Column(Integer, ForeignKey('tournament.id'))
    fencer_w_score = Column(Integer)
    fencer_l_score = Column(Integer)
    rnd = Column(String)
    fencer_win =  relationship('Fencer', secondary=fencers, backref='bouts', lazy='select')
    fencer_lose = relationship('Fencer', secondary=fencers, backref='bouts', lazy='select')



#Will implement after web scrapping -> database is working

class Touch(Base):
    
    __tablename__ = 'touch'
    bout_id = Column(Integer, ForeignKey('bout.id'))
    id = Column(Integer, primary_key=True)
    point = Column(Integer)
    score = Column(Integer)


