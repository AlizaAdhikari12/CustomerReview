from fastapi import APIRouter

router = APIRouter()

@router.post("/")

def admin():
    print("test")