from fastapi import APIRouter, Path, Query, HTTPException, status,Depends
from fastapi.responses import  JSONResponse
from typing import List
from utils.jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer

from config.database import Session, engine,Base
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder

from middlewares.error_hanlder import ErrorHandler
from middlewares.jwt_bearer import JWTBearer

from services.movie import Movieservice

from schemas.movie import Movie

movie_router = APIRouter()




@movie_router.get("/movies", tags=["movies"],response_model=List[Movie], dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    db = Session()
    # result = db.query(MovieModel).all()
    result = Movieservice(db).get_movies()
    db.close()   # Cerrar la sesión
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@movie_router.get("/movies/{id}", tags=["movies"], response_model=Movie)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    db = Session()
    # movie = db.query(MovieModel).filter(MovieModel.id == id).first()
    movie = Movieservice(db).get_movie(id)
    db.close()   # Cerrar la sesión
    if movie:
        return movie
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")


@movie_router.get("/movies/", tags=["movies"], response_model=List[Movie])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)):
    db = Session()
    # movie = db.query(MovieModel).filter(MovieModel.category == category).all()
    movie = Movieservice(db).get_movies_by_categories(category)
    db.close()   # Cerrar la sesión

    if movie:
        return movie
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")

    # data = [item for item in movies if item ["category"] == category]
    # return JSONResponse(content=data)

@movie_router.post("/movies", tags=["movies"], response_model=dict)
def create_movie(movie: Movie) -> dict:
    db = Session()
    # new_movie = MovieModel(**movie.dict())
    # db.add(new_movie)
    # db.commit()  
    Movieservice(db).create_movie(movie)
    db.close()   # Cerrar la sesión

    # movies.movie_routerend(movie)
    return JSONResponse(content={"message": "Se ha registrado la película"}, status_code=status.HTTP_201_CREATED)

@movie_router.put("/movies/{id}", tags=["movies"], response_model=dict)
def update_movie(id: int, movie: Movie) -> dict:
    db = Session()
    # result = db.query(MovieModel).filter(MovieModel.id == id).first()
    result = Movieservice(db).get_movie(id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
    Movieservice(db).update_movie(id, movie)
    # result.title = movie.title
    # result.overview = movie.overview
    # result.year = movie.year
    # result.rating = movie.rating
    # result.category = movie.category
    # db.commit()
    db.close()
    # for item in movies:
    #     if item["id"] == id:
    #         item.update(movie.dict())
    #         return JSONResponse(content={"message": "Movie updated successfully"}, status_code=status.HTTP_200_OK)
    raise HTTPException(status_code=200, detail={"message":"Se ha modificado la movie"})

@movie_router.delete("/movies/{id}", tags=["movies"], response_model=dict)
def delete_movie(id: int) -> dict:
    db = Session()
    # result = db.query(MovieModel).filter(MovieModel.id == id).first()
    result = Movieservice(db).get_movie(id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
    # db.delete(result)
    # db.commit()
    Movieservice(db).delete_movie(id)
    db.close()
    raise HTTPException(status_code=202, detail="Movie deleted")
