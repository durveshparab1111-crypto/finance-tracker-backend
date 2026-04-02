from fastapi import FastAPI
from app.database import engine, Base
from app.routers import transactions, users, analytics

app = FastAPI()

# create tables
Base.metadata.create_all(bind=engine)

# include routers
app.include_router(users.router)
app.include_router(transactions.router)
app.include_router(analytics.router)

@app.get("/")
def root():
    return {"message": "Finance Tracker API Running"}