from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy import DateTime
from datetime import datetime
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    password_hash = Column(String)
    role = Column(String)

    def __repr__(self):
        return f"User(id={self.id}, name='{self.name}', role='{self.role}')"
    
    created_at = Column(
    DateTime,
    default=datetime.now
)


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)

    filename = Column(String)

    filepath = Column(String)

    role_access = Column(String)

class DocumentChunk(Base):

    __tablename__ = "document_chunks"

    id = Column(Integer, primary_key=True)

    document_id = Column(Integer)

    chunk_text = Column(String)