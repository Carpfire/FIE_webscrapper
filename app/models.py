from sqlalchemy import Boolean, Table, Column, Integer, ForeignKey, String, Date
from sqlalchemy.orm import relationship
from .database import Base


# fencers = Table(
#     'fencers_bouts',
#     Base.metadata,
#     Column('fencers_id', Integer, ForeignKey('fencer.id')), 
#     Column('bout_id', Integer, ForeignKey('bout.id')) 
# )

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
    
    def __repr__(self):
        return f"{self.first_name} {self.last_name}, {self.country}"

class Tournament(Base):
    
    __tablename__ = 'tournament'
    id = Column(Integer, primary_key=True)
    country = Column(String(255))
    city = Column(String(255))
    start_date = Column(Date)
    end_date = Column(Date)
    bouts = relationship('Bout', backref='tournament', lazy='select')
    fencers = relationship('Fencer', secondary=tourn_fen, backref='tournament', lazy='select')
    
    def __repr__(self):
        return f"{self.city},{self.country}:{str(self.start_date)-str(self.end_date)}"


class Bout(Base):

    __tablename__ = 'bout'
    id = Column(Integer, primary_key = True)
    tournament_id = Column(Integer, ForeignKey('tournament.id'))
    fencer_w_score = Column(Integer)
    fencer_l_score = Column(Integer)
    rnd = Column(String(255))
    fencer_win_id = Column(Integer, ForeignKey('fencer.id')) 
    fencer_win = relationship("Fencer", foreign_keys=[fencer_win_id], backref='bout_win')
    fencer_lose_id = Column(Integer, ForeignKey('fencer.id')) 
    fencer_lose = relationship("Fencer", foreign_keys=[fencer_lose_id], backref='bout_lose')
    
    def __repr__(self):
        return f"{''.join([self.fencer_win.first_name, ' ', self.fencer_win.last_name, ' ',  str(self.fencer_w_score)])} to {''.join([self.fencer_lose.first_name, ' ', self.fencer_lose.last_name, ' ', str(self.fencer_l_score)])}"


#Will implement after web scrapping -> database is working

class Touch(Base):
    
    __tablename__ = 'touch'
    bout_id = Column(Integer, ForeignKey('bout.id'))
    id = Column(Integer, primary_key=True)
    point = Column(Integer)
    score = Column(Integer)


