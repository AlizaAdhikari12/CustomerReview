from fastapi import APIRouter, Depends
import json
from pydantic import BaseModel
from app.create_database import get_connection
from app.dependencies import get_currentuser
from app.ai_analyzer import analyze_review


router = APIRouter()


class ReviewReport(BaseModel):
    CustomerName : str
    ReviewText : str

@router.post("/")
def submit_review(req : ReviewReport, current_user : dict = Depends(get_currentuser)):
    result = analyze_review(req.ReviewText)
    print(result)
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO CustomerReviews
    (UserID,
    CustomerName,
    ReviewText,
    Sentiment,
    Score,
    Keywords,
    Category,
    AiSummary)
    VALUES
    (?,?,?,?,?,?,?,?)
    """,
    current_user['userId'],
    req.CustomerName,
    req.ReviewText,
    result['sentiment'],
    result["score"],
    json.dumps(result["keywords"]),
    result["category"],
    result["summary"]
    )
    conn.commit()
    conn.close()

    return {
        "message": "Review submitted and analyzed",
        "analysis" : result
    }



class viewReport(BaseModel):
    CustomerName : str

@router.get("/my")
def my_review(current_user: dict = Depends(get_currentuser)):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT Id, 
        CustomerName,
        ReviewText,
        Sentiment,
        Score,
        Keywords,
        Category,
        AiSummary

        FROM CustomerReviews
        
        WHERE UserId = ? ORDER BY ID DESC
        """,
        current_user['userId']
    )
    rows = cur.fetchall()
    conn.close()

    return{
        "message": "Test sucessful",
        "reviews":dict(zip([c[0] for c in cur.description],row) for row in rows)
    }


def review():
    return {"message": "Auth route working"}