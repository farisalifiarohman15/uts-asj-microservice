from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from minio import Minio
import os
import uuid
import io

ALLOWED_TYPES = ["image/jpeg", "image/png"]
MAX_SIZE = 5 * 1024 * 1024  # 5MB

# Environment variables
DATABASE_URL = os.getenv("DATABASE_URL")
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")
MINIO_ACCESS = os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET = os.getenv("MINIO_SECRET_KEY")
BUCKET_NAME = "photos"

# Database setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    photo_url = Column(String)

Base.metadata.create_all(bind=engine)

# FastAPI app
app = FastAPI(
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <head>
        <title>Web Microservice UTS</title>
        <style>
            body {
                background-color: #4CAF50;
                font-family: Arial;
            }
            .container {
                width: 350px;
                margin: 80px auto;
                background: white;
                padding: 20px;
                border-radius: 5px;
                box-shadow: 0px 0px 10px gray;
            }
            input, button {
                width: 100%;
                padding: 10px;
                margin: 8px 0;
            }
            button {
                background-color: #4CAF50;
                color: white;
                border: none;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h3>Form Input User</h3>
            <form action="/users" method="post" enctype="multipart/form-data">
                <input type="text" name="name" placeholder="Nama" required>
                <input type="email" name="email" placeholder="Email" required>
                <input type="file" name="photo" required>
                <button type="submit">Kirim</button>
            </form>
        </div>
    </body>
    </html>
    """

# MinIO client
minio_client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS,
    secret_key=MINIO_SECRET,
    secure=False
)

# Buat bucket kalau belum ada
if not minio_client.bucket_exists(BUCKET_NAME):
    minio_client.make_bucket(BUCKET_NAME)
@app.post("/users")
async def create_user(
    name: str = Form(...),
    email: str = Form(...),
    photo: UploadFile = File(...)
):
    if "@" not in email:
        raise HTTPException(status_code=400, detail="Email tidak valid")

    contents = await photo.read()

    if len(contents) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File terlalu besar")

    filename = f"{uuid.uuid4()}-{photo.filename}"
    file_data = io.BytesIO(contents)

    # upload ke MinIO
    minio_client.put_object(
        BUCKET_NAME,
        filename,
        file_data,
        length=len(contents),
        content_type=photo.content_type
    )

    photo_url = f"http://{MINIO_ENDPOINT}/{BUCKET_NAME}/{filename}"

    with SessionLocal() as db:
        user = User(name=name, email=email, photo_url=photo_url)
        db.add(user)
        db.commit()

    return RedirectResponse("/", status_code=303)

@app.get("/users")
def get_users():
    with SessionLocal() as db:
        users = db.query(User).all()
        return users

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    with SessionLocal() as db:
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            raise HTTPException(status_code=404, detail="User tidak ditemukan")

        filename = user.photo_url.split("/")[-1]
        minio_client.remove_object(BUCKET_NAME, filename)

        db.delete(user)
        db.commit()

    return {"message": "User berhasil dihapus"}


@app.get("/health")
def health_check():
    return {"status": "ok"}
