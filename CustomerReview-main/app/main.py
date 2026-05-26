from fastapi import FastAPI
from app.routes import auth_route, admin_route,review_route

app = FastAPI(
    title = "Customer Review analyzer", 
    description = "Api for customer review submission and AI-based sentiment",
    version = "1.0.0",
    contact={"name":"Development Team"}
)

app.include_router(auth_route.router,
                    prefix='/auth',
                    tags= ["Authentication"])

app.include_router(review_route.router,
                    prefix='/review',
                    tags=["Review"])


app.include_router(admin_route.router,
                    prefix='/admin',
                    tags=['Admin'])


@app.get("/",tags=["Health"])

