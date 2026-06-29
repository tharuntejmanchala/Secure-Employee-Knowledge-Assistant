from http.client import HTTPException
from urllib import response
from urllib import response
from fastapi import HTTPException
from fastapi import FastAPI,Depends
from schemas import RegisterRequest, LoginRequest
from schemas import QuestionRequest
from fastapi import Depends
from fastapi.middleware.cors import CORSMiddleware
from qdrant_client.models import PointStruct
from dependencies import get_current_user
import os
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
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
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

    # Check if email already exists
    existing_user = db.query(User).filter(
        User.email == data.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered."
        )

    # Security check for privileged roles
    if data.role == "Manager":
        if data.admin_code != "MANAGER123":
            raise HTTPException(
                status_code=403,
                detail="Invalid Manager registration code."
            )

    elif data.role == "HR":
        if data.admin_code != "HR123":
            raise HTTPException(
                status_code=403,
                detail="Invalid HR registration code."
            )

    elif data.role == "CEO":
        if data.admin_code != "CEO123":
            raise HTTPException(
                status_code=403,
                detail="Invalid CEO registration code."
            )

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
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if not verify_password(
        data.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid password"
        )
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

    # Store Document
    document = Document(
        filename=file.filename,
        filepath=filepath,
        role_access=current_user["role"]
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    # Save values before session closes
    document_id = document.id
    document_role = document.role_access

    # PDF Text Extraction
    try:
        reader = PdfReader(filepath)
    except Exception:
        db.close()
        raise HTTPException(
            status_code=400,
            detail="Invalid PDF file"
        )

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text

    # Chunking

    chunks = []

    chunk_size = 1000

    for i in range(0, len(text), chunk_size):

        chunks.append(
            text[i:i + chunk_size]
        )

    # Store Chunks + Generate Embeddings

    points = []

    for chunk in chunks:

        document_chunk = DocumentChunk(
            document_id=document_id,
            chunk_text=chunk
        )

        db.add(document_chunk)

        # Generates chunk ID without commit
        db.flush()

        embedding = model.encode(chunk)

        point = PointStruct(

            id=document_chunk.id,

            vector=embedding.tolist(),

            payload={

                "chunk_id": document_chunk.id,

                "document_id": document_id,

                "role_access": document_role,

                "text": chunk

            }

        )

        points.append(point)

    # Save chunks to PostgreSQL
    db.commit()

    # Store vectors in Qdrant
    client.upsert(

        collection_name="document_embeddings",

        points=points

    )

    db.close()

    return {

        "message": "File uploaded successfully",

        "document_id": document_id,

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

    if not question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )

    role_levels = {
        "Employee": 1,
        "Manager": 2,
        "HR": 3,
        "CEO": 4
    }

    current_level = role_levels[user_role]

    query_embedding = model.encode(question)

    results = client.query_points(
        collection_name="document_embeddings",
        query=query_embedding.tolist(),
        limit=20
    )

    print("Points Found:", len(results.points))

    allowed_points = []

    for point in results.points:

        document_role = point.payload["role_access"]

        document_level = role_levels[document_role]

        if current_level >= document_level:

            allowed_points.append(point)

    if len(allowed_points) == 0:

        return {
            "answer": "No relevant documents found for your role."
        }

    context = "\n".join(

        point.payload["text"]

        for point in allowed_points[:8]

    )

    prompt = f"""
You are an Enterprise Knowledge Assistant.

Your job is to answer ONLY from the provided context.

Rules:
- If the answer exists in the context, answer it clearly.
- Do not make up information.
- If the context does not contain the answer, reply:
  "The uploaded documents do not contain enough information to answer this question."


Context:
{context}

Question:
{question}

Answer:
"""
    print("\n========== PROMPT ==========")
    print(prompt)
    print("========== END PROMPT ==========\n")

    response = ollama.chat(
        model="llama3.2:3b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    answer = response["message"]["content"]

    return {

        "question": question,

        "role": user_role,

        "chunks_retrieved": len(allowed_points[:3]),

        "answer": answer

    }

@app.get("/stats")
def stats():

    db = SessionLocal()

    users = db.query(User).count()

    documents = db.query(Document).count()

    chunks = db.query(DocumentChunk).count()

    db.close()

    return {
        "users": users,
        "documents": documents,
        "chunks": chunks
    }


@app.get("/")
def home():
    return {
        "message": "Secure Employee Knowledge Assistant Running"
    }

@app.get("/me")
def get_me(
    current_user=Depends(get_current_user)
):

    db = SessionLocal()

    user = db.query(User).filter(
        User.email == current_user["email"]
    ).first()

    db.close()

    return {

        "name": user.name,

        "email": user.email,

        "role": user.role,

        "joined_on": user.created_at.strftime("%d %b %Y")

    }


@app.delete("/documents/{filename}")
def delete_document(
    filename: str,
    current_user=Depends(get_current_user)
):

    db = SessionLocal()

    document = db.query(Document).filter(
        Document.filename == filename
    ).first()

    if not document:

        db.close()

        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    # Allow only owner role or CEO
    if (
        document.role_access != current_user["role"]
        and current_user["role"] != "CEO"
    ):

        db.close()

        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    # Delete file
    if os.path.exists(document.filepath):
        os.remove(document.filepath)

    # Get chunk ids
    chunks = db.query(DocumentChunk).filter(
        DocumentChunk.document_id == document.id
    ).all()

    chunk_ids = [chunk.id for chunk in chunks]

    # Delete from Qdrant
    if chunk_ids:

        client.delete(

            collection_name="document_embeddings",

            points_selector=chunk_ids

        )

    # Delete chunks
    db.query(DocumentChunk).filter(
        DocumentChunk.document_id == document.id
    ).delete()

    # Delete document
    db.delete(document)

    db.commit()

    db.close()

    return {

        "message": "Document deleted successfully"

    }