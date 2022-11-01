import uvicorn , os , sys
from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware , db
from schema import Book as BookSchema
from schema import Author as AuthorSchema
from dotenv import load_dotenv
from models import Book as ModelBook
from models import Author as ModelAuthor

load_dotenv(".env")


app = FastAPI()

app.add_middleware(
    DBSessionMiddleware,db_url=os.environ['DATABASE_URL']
)

@app.get("/")
async def root():
    return {"message": "hello world "}

@app.post("/add-book",response_model=BookSchema)
async def add_book(request: BookSchema):
    db_book = ModelBook(**request.dict())
    db.session.add(db_book)
    db.session.commit()
    db.session.close()
    return request

@app.post("/add-author",response_model=AuthorSchema)
async def add_book(request: AuthorSchema):
    db_author = ModelAuthor(**request.dict())
    db.session.add(db_author)
    db.session.commit()
    db.session.close()
    return request

@app.get("/get-book")
async def get_book():
    book = db.session.query(ModelBook).all()
    return book