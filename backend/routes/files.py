from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import FileResponse

import os
import shutil
from datetime import datetime

from database.db import files_collection
from services.ai_pipeline import classify_file
from utils.security import verify_token

router = APIRouter()


# ================= UPLOAD =================
@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    user=Depends(verify_token)
):
    try:
        email = user["email"]

        # temp upload
        os.makedirs("uploads", exist_ok=True)
        temp_path = os.path.join("uploads", file.filename)

        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 🔥 AI classification
        result, folder = classify_file(temp_path)
        folder = folder.lower().replace(" ", "_")

        allowed_folders = ["selfies", "resumes", "documents", "others"]
        if folder not in allowed_folders:
            folder = "others"

        # final storage
        final_dir = f"storage/{email}/{folder}"
        os.makedirs(final_dir, exist_ok=True)

        final_path = os.path.join(final_dir, file.filename)
        shutil.move(temp_path, final_path)

        file_size = os.path.getsize(final_path)

        # save in DB
        files_collection.insert_one({
            "email": email,
            "filename": file.filename,
            "classification": result,
            "folder": folder,
            "size_bytes": file_size,
            "path": final_path,
            "uploaded_at": datetime.utcnow()
        })

        # 🔥 IMPORTANT FIX
        return {
            "filename": file.filename,
            "classification": result,
            "folder": folder,
            "filepath": final_path  # ✅ FIXED
        }

    except Exception as e:
        print("UPLOAD ERROR:", e)
        return {"error": str(e)}


# ================= GET FILES =================
@router.get("/files")
def get_files(user=Depends(verify_token)):
    email = user["email"]

    results = files_collection.find({"email": email})

    return [
        {
            "filename": f["filename"],
            "classification": f.get("classification"),
            "folder": f.get("folder"),
            "size_bytes": f.get("size_bytes"),
            "uploaded_at": str(f.get("uploaded_at")),
            "filepath": f.get("path")  # ✅ IMPORTANT
        }
        for f in results
    ]


# ================= DELETE =================
@router.delete("/delete/{filename}")
def delete_file(filename: str, user=Depends(verify_token)):
    email = user["email"]

    files_collection.delete_one({
        "email": email,
        "filename": filename
    })

    user_folder = f"storage/{email}"

    for root, _, files in os.walk(user_folder):
        if filename in files:
            os.remove(os.path.join(root, filename))
            return {"message": "Deleted successfully"}

    return {"message": "File not found"}


# ================= DOWNLOAD =================
@router.get("/download/{filename}")
def download_file(filename: str, user=Depends(verify_token)):
    email = user["email"]
    user_folder = f"storage/{email}"

    for root, _, files in os.walk(user_folder):
        if filename in files:
            path = os.path.join(root, filename)

            return FileResponse(
                path=path,
                filename=filename,
                media_type="application/octet-stream"
            )

    raise HTTPException(status_code=404, detail="File not found")