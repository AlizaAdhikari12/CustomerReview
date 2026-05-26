from fastapi import APIRouter, Depends
from app.create_database import get_connection
from app.dependencies import require_admin

router = APIRouter()

@router.get("/reviews")

def all_reviews(admin: dict = Depends(require_admin)):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT r.Id, u.FullName, u.Email , r.CustomerName, r.ReviewText, r.Sentiment, r.Score, r.Keywords, r.Category, r.AiSummary
        FROM CustomerReviews r 
        INNER JOIN Users u ON r.UserID = u.Id
        ORDER BY r.Id DESC
        """
    )
    rows = cur.fetchall()
    columns = [c[0] for c in cur.description]
    print(columns)
    conn.close()

    return(
        [dict(zip(columns,row)) for row in rows ]
    )

@router.get("/dashboard")
def dashboard(admin : dict = Depends(require_admin)):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT Sentiment,
        COUNT(*) TotalReviews,
        AVG(Score) AverageScore from CustomerReviews
        GROUP BY Sentiment
        """
    )
    rows = cur.fetchall()
    sentiment = ([dict(zip([c[0] for c in cur.description],row))] for row in rows)

    cur.execute("""
    SELECT Category,
    COUNT(*) AS Total
    FROM CustomerReviews
    GROUP BY Category
    """)
    rows = cur.fetchall()
    category = ([dict(zip([c[0] for c in cur.description],row))] for row in rows)
    
    conn.close()
    return{
        "sentimentSummary" : sentiment,
        "CategorySummary": category
    }
