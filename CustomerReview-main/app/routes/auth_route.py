from fastapi import APIRouter

router = APIRouter()

@router.post("/")

def auth():
    return {"message": "Auth route working"}