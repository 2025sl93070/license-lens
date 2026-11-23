from fastapi import APIRouter, UploadFile, File, HTTPException

router = APIRouter()


@router.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    content = await file.read()
    filename = file.filename

    if filename not in ("package.json", "requirements.txt"):
        raise HTTPException(
            status_code=400,
            detail="Only package.json or requirements.txt files are supported"
        )

    return {
        "filename": filename,
        "status": "received",
        "message": "File received successfully. Analysis coming soon."
    }
