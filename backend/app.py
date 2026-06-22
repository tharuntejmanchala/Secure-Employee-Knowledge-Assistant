from fastapi import FastAPI,Depends
from schemas import RegisterRequest, LoginRequest
from schemas import QuestionRequest
from fastapi import Depends

from dependencies import get_current_user
from qdrant_client.models import (
    Filter,
    FieldCondition,
    MatchValue
)
import ollama

from sentence_transformers import SentenceTransformer

from qdrant_db import client

from schemas import QuestionRequest

from security import (
    hash_password,
    verify_password,
    create_access_token
)
from database import SessionLocal
from models import User
from role_checker import require_role
from database import engine
from models import Base
from fastapi import UploadFile, File
from dependencies import get_current_user
from database import SessionLocal
from models import Document
app = FastAPI()
from pypdf import PdfReader
from models import DocumentChunk
Base.metadata.create_all(bind=engine)

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

@app.get("/")
def home():
    return {
        "message": "Welcome Tharun!"
    }


@app.get("/about")
def about():
    return {
        "project": "Secure Employee Knowledge Assistant",
        "version": "1.0"
    }


@app.get("/roles")
def roles():
    return {
        "roles": [
            "Employee",
            "Trainer",
            "Manager",
            "HR",
            "CEO"
        ]
    }


@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {
        "user_id": user_id
    }


@app.get("/search")
def search(name: str):
    return {
        "search_term": name
    }


@app.post("/register")
def register(data: RegisterRequest):

    db = SessionLocal()

    hashed_password = hash_password(
        data.password
    )

    new_user = User(
        name=data.name,
        email=data.email,
        password_hash=hashed_password,
        role=data.role
    )

    db.add(new_user)
    db.commit()

    return {
        "message": "User Registered Successfully"
    }


@app.post("/login")
def login(data: LoginRequest):

    db = SessionLocal()

    user = db.query(User).filter(
        User.email == data.email
    ).first()

    if not user:
        return {
            "message": "User not found"
        }

    if not verify_password(
        data.password,
        user.password_hash
    ):
        return {
            "message": "Invalid password"
        }

    token = create_access_token(
        {
            "email": user.email,
            "role": user.role
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@app.get("/profile")
def profile(
    current_user=Depends(get_current_user)
):
    return {
        "message": "Protected Route",
        "user": current_user
    }

@app.get("/manager-dashboard")
def manager_dashboard(
    current_user=Depends(
        require_role("Manager")
    )
):
    return {
        "message": "Welcome Manager",
        "user": current_user
    }

@app.post("/upload-document")
def upload_document(
    current_user=Depends(get_current_user),
    file: UploadFile = File(...)
):

    filepath = f"uploads/{file.filename}"

    with open(filepath, "wb") as f:
        f.write(file.file.read())

    db = SessionLocal()

    document = Document(
        filename=file.filename,
        filepath=filepath,
        role_access=current_user["role"]
    )

    db.add(document)
    db.commit()

    db.refresh(document)

    # PDF Text Extraction

    reader = PdfReader(filepath)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text

    # Chunking

    chunks = []

    chunk_size = 1000

    for i in range(0, len(text), chunk_size):

        chunk = text[i:i + chunk_size]

        chunks.append(chunk)

    # Store Chunks

    for chunk in chunks:

        document_chunk = DocumentChunk(
            document_id=document.id,
            chunk_text=chunk
        )

        db.add(document_chunk)

    db.commit()

    return {
        "message": "File uploaded successfully",
        "document_id": document.id,
        "chunks_created": len(chunks)
    }

@app.get("/documents")
def get_documents(
    current_user=Depends(get_current_user)
):
    db = SessionLocal()

    role_levels = {
        "Employee": 1,
        "Manager": 2,
        "HR": 3,
        "CEO": 4
    }

    current_level = role_levels[
        current_user["role"]
    ]

    documents = db.query(Document).all()

    allowed_documents = []

    for document in documents:

        document_level = role_levels[
            document.role_access
        ]

        if current_level >= document_level:

            allowed_documents.append(
                document.filename
            )

    return {
        "documents": allowed_documents
    }
@app.post("/ask")
def ask_question(
    request: QuestionRequest,
    current_user=Depends(get_current_user)
):

    print("Current User:", current_user)

    user_role = current_user["role"]

    print("User Role:", user_role)

    question = request.question

    query_embedding = model.encode(question)

    results = client.query_points(
        collection_name="document_embeddings",
        query=query_embedding.tolist(),
        limit=3,
        query_filter=Filter(
            must=[
                FieldCondition(
                    key="role_access",
                    match=MatchValue(
                        value=user_role
                    )
                )
            ]
        )
    )

    print("Points Found:", len(results.points))

    if len(results.points) == 0:
        return {
            "answer": "No relevant documents found for your role."
        }

    context = "\n".join(
        point.payload["text"]
        for point in results.points
    )

    prompt = f"""
Answer the question using only the context below.

Context:
{context}

Question:
{question}

Answer:
"""

    response = ollama.chat(
        model="llama3.2:3b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return {
        "answer": response["message"]["content"]
    }