from fastapi import APIRouter, UploadFile

router = APIRouter(prefix="/scripts",
                   tags=["scripts"])


@router.post("/upload/")
async def upload_py(file: UploadFile):

    return {"status": 204, "filename": file.filename}
