from fastapi import FastAPI
from app.database import engine, Base
from app.routers import contracts


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(contracts.router)

@app.get("/")
async def root():
    return {"message": "API umów fotowoltaicznych działa!"}