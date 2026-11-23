from fastapi import APIRouter, UploadFile, File, HTTPException

from app.modules.parser import parse_dependencies
 
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
 
    dependencies = parse_dependencies(content.decode("utf-8"), filename)
 
    return {

        "filename": filename,

        "total_dependencies": len(dependencies),

        "dependencies": dependencies,

        "message": "Dependencies parsed successfully. License analysis coming soon."

    }
 