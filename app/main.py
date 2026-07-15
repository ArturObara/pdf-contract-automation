from fastapi import FastAPI
from app.routers import contracts


app = FastAPI()

app.include_router(contracts.router)

@app.get("/")
async def root():
    return {"message": "API is running!"}