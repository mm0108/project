from fastapi import FastAPI
from database import Base, engine
from routers import books, board

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(books.router)
app.include_router(board.router)

@app.get("/")
def root():
    return {"message": "Library + Board API Running"}