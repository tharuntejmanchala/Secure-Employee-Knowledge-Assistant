from fastapi import FastAPI,Depends
from schemas import RegisterRequest, LoginRequest
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

Base.metadata.create_all(bind=engine)

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
    role_access: str,
    file: UploadFile = File(...)
):

    filepath = f"uploads/{file.filename}"

    with open(filepath, "wb") as f:
        f.write(file.file.read())

    db = SessionLocal()

    document = Document(
        filename=file.filename,
        filepath=filepath,
        role_access=role_access
    )

    db.add(document)

    db.commit()

    return {
        "message": "File uploaded successfully"
    }