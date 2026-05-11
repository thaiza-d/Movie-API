from pydantic import BaseModel

class MovieCreate(BaseModel):
    title: str
    genre: str
    year: int

class MovieResponse(BaseModel):
    id: int
    title: str
    genre: str
    year: int

    class Config:
        from_attributes = True