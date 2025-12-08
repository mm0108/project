from pydantic import BaseModel

class BookBase(BaseModel):
    title: str
    author: str
    year: int

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
    is_available: bool

    class Config:
        orm_mode = True

class PostBase(BaseModel):
    title: str
    content: str

class Post(PostBase):
    id: int
    class Config:
        from_attributes = True