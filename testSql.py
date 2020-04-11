from sqlalchemy import Column, Integer, String, create_engine, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


Base = declarative_base()


class Member(Base):
    __tablename__ = 'member'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    discord_id = Column(Integer)
    is_verified = Column(Boolean)
    is_admin = Column(Integer)
    avote = Column(Boolean)


class Poste(Base):
    __tablename__ = 'poste'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    rank = Column(Integer)


class Candidature(Base):
    __tablename__ = 'candidature'
    id = Column(Integer, primary_key=True)
    poste = relationship('Poste')
    member = relationship('Member')
    poste_id = Column(Integer, ForeignKey('poste.id', ondelete="CASCADE"))
    membre_id = Column(Integer, ForeignKey('member.id', ondelete="CASCADE"))


class Vote(Base):
    __tablename__ = 'vote'
    id = Column(Integer, primary_key=True)
    member = relationship('Member')
    poste = relationship('Poste')
    candidat = relationship('Candidature')
    poste_id = Column(Integer, ForeignKey('poste.id', ondelete="CASCADE"))
    member_id = Column(Integer, ForeignKey("member.id", ondelete="CASCADE"))
    candidat_id = Column(Integer, ForeignKey('candidat.id', ondelete="CASCADE"))


class Start(Base):
    __tablename__ = 'start'
    id = Column(Integer, primary_key=True)
    is_started = Column(Boolean)
    poste=relationship("Poste")
    poste_id=Column(Integer, ForeignKey("poste.id", ondelete="CASCADE"))


engine = create_engine('sqlite:///sqlDiscord.db')
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()
plein = session.query(Start).first()
if not plein:
    started = Start(is_started=False, poste_id=-1)
    session.add(started)
    session.commit()
