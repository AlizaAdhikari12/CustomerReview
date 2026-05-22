from fastapi import APIRouter

router = APIRouter()

@router.post("/")

def review():
    return {"message": "Auth route working"}