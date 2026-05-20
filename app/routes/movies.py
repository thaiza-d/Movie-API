from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from ..dependencies import get_db
from ..schemas import MovieCreate, MovieResponse
from ..models import Movie

router = APIRouter()

@router.get("/movie", response_model=list[MovieResponse])
def show(db: Session = Depends(get_db)):
    result = db.query(Movie).all()
    return result

@router.get("/movie/{id}", response_model=MovieResponse)
def show_id(id:int, db: Session = Depends(get_db)):
    result = db.query(Movie).filter(Movie.id == id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Movie not found")
    return result

@router.post("/movie", response_model=MovieResponse)
def create(movie: MovieCreate, db: Session = Depends(get_db)):
    existing = db.query(Movie).filter(Movie.title == movie.title).first()
    if existing:
        raise HTTPException(status_code=409, detail="Conflict")
    new_movie = Movie(
        title = movie.title,
        genre = movie.genre,
        year = movie.year
    )

    db.add(new_movie)
    db.commit()
    db.refresh(new_movie)
    return new_movie

@router.put("/movie/{id}", response_model=MovieResponse)
def update(id:int, movie: MovieCreate, db: Session = Depends(get_db)):
    db_movie = db.query(Movie).filter(Movie.id == id).first()
    if not db_movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    duplicate = db.query(Movie).filter(Movie.title == movie.title, Movie.id != id).first()
    if duplicate:
        raise HTTPException(status_code=409, detail="Conflict")
    db_movie.title = movie.title
    db_movie.genre = movie.genre
    db_movie.year = movie.year

    db.commit()
    db.refresh(db_movie)
    return db_movie

@router.delete("/movie/{id}", status_code=204)
def delete(id: int, db: Session = Depends(get_db)):
    existing = db.query(Movie).filter(Movie.id == id).first()
    if not existing: 
        raise HTTPException(status_code=404, detail="Movie not found")
    db.delete(existing)
    db.commit()
    return