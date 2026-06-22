# check_documents.py

from database import SessionLocal
from models import Document

db = SessionLocal()

documents = db.query(Document).all()

for document in documents:

    print(
        document.id,
        document.filename,
        document.role_access
    )

db.close()