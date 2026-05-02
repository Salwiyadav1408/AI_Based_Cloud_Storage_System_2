from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from routes.auth import router as auth_router
from routes.files import router as files_router

# ================= CREATE APP =================
app = FastAPI()

# ================= CORS MIDDLEWARE =================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ================= ENSURE UPLOAD FOLDER EXISTS =================
UPLOAD_DIR = "uploads"

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# ================= SERVE FILES =================
app.mount("/storage", StaticFiles(directory="storage"), name="storage")

# ================= REGISTER ROUTES =================
app.include_router(auth_router)
app.include_router(files_router)

# ================= ROOT =================
@app.get("/")
def root():
    return {"message": "AI Vault Backend Running 🚀"}