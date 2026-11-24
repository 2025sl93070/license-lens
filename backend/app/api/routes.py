from fastapi import APIRouter, UploadFile, File, HTTPException
from app.modules.parser import parse_dependencies
from app.modules.license_identifier import identify_licenses
from app.modules.policy_engine import evaluate_policy
 
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
    licenses = identify_licenses(dependencies, filename)
    result = evaluate_policy(licenses)
 
    return {
        "filename": filename,
        "total_dependencies": len(dependencies),
        "results": result
    }