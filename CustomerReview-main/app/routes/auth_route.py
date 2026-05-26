from fastapi import APIRouter,HTTPException
from pydantic import BaseModel, EmailStr
from app.create_database import get_connection
from app.auth import hash_password, verify_password, create_access_token


router = APIRouter()


class RegisterRequest(BaseModel):
    fullName : str
    email : EmailStr
    password : str
    role : str = 'User'

class LoginRequest(BaseModel):
    email : EmailStr
    password : str

@router.post("/register")

def register(req : RegisterRequest):
    if req.role not in ['Admin' , "User"]:
        raise HTTPException(status_code = 400, detail ="Invalid role")


    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT Id FROM Users WHERE Email = ?" , (req.email,))
    if cur.fetchone():
        raise HTTPException(status_code = 400, detail = "Email already exists")

    cur.execute(
        "Insert INTO Users (FullName, Email, PasswordHash,Role) VALUES (?,?,?,?)",
        req.fullName
        ,req.email,
        hash_password(req.password),
        req.role
        )

    conn.commit()
    conn.close()
    return {"message" : "User Registered successfully"}



@router.post("/login")
def login(req: LoginRequest):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("Select Id, fullName, Email, PasswordHash, Role FROM  Users WHERE Email = ?", (req.email,))
    user = cur.fetchone()
    conn.close()

    if not user or not verify_password(req.password, user[3] ):
        raise HTTPException(status_code=400, detail = "Invalid email or password")

    token = create_access_token({
            "userId": user[0],
            "fullName": user[1],
            "email": user[2],
            "role": user[4]
    })

    return {
    "access_token": token,
    "token_type": "bearer",
    "message": "success",
    "user": {
        "id": user[0],
        "name": user[1],
        "email": user[2],
        "role": user[4]
    }
  
}
    
def auth():
    return {"message":  "Auth route working"}