import sqlalchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

engine = create_engine('sqlite:///banco.db', echo=True)
Base = declarative_base()

class Pagina(Base):
    __tablename__ = 'paginas'

    id = Column(Integer, primary_key=True)
    link = Column(String)
    titulo = Column(String)
    h1 = Column(String)
    h2 = Column(String)
    h3 = Column(String)
    h4 = Column(String)
    h5 = Column(String)
    h6 = Column(String)
    strong = Column(String)
    negrito = Column(String)

Base.metadata.create_all(engine)