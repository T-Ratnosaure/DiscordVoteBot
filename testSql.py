from sqlalchemy import Column, Integer, String, create_engine, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()


class Member(Base):
    __tablename__ = 'member'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    discord_id = Column(Integer)
    is_verified = Column(Boolean)
    is_admin = Column(Integer)
    avote = Column(Boolean)


class Poste(Base):
    __tablename__ = 'poste'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    rank = Column(Integer)


class Candidature(Base):
    __tablename__ = 'candidature'
    id = Column(Integer, primary_key=True)
    poste_id = relationship(Poste)
    membre_id = relationship(Member)


engine = create_engine('sqlite:///sqlDiscord.db')
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()

prez = Poste(name="Président", rank=0)
prez.add(Poste)
prez.commit()
