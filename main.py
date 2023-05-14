# Import the necessary libraries and modules
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from sqlalchemy import func
import calendar
import models, schemas, crud
from database import SessionLocal, engine

# Create the database tables using the metadata of the models module and the engine.
models.Base.metadata.create_all(bind=engine) 

# Create FastAPI instance
app = FastAPI()

# Dependency.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Define an HTTP GET endpoint that maps to the get_movie_count_for_month function
@app.get("/movies/month/{month_name}", response_model=schemas.MovieCountMonth)
async def get_movie_count_for_month(month_name: str, db: Session = Depends(get_db)):
    try:
        # Call the get_movie_count_for_month function with the given month name and database session
        movie_count = crud.get_movie_count_for_month(db, month_name)
    except ValueError:
        # If the get_movie_count_for_month function raises a ValueError, return a 400 Bad Request response with the message "Invalid month name"
        raise HTTPException(status_code=400, detail="Invalid month name")
    # If the function succeeds, return a JSON response with the month name and movie count
    return movie_count

# Define an HTTP GET endpoint that maps to the get_movie_count_for_day_of_week function
@app.get("/movies/week/{day_of_week}", response_model=schemas.MovieCountDayOfWeek)
async def get_movie_count_for_day_of_week(day_of_week: str, db: Session = Depends(get_db)):
    try:
        # Call the get_movie_count_for_day_of_week function with the given day of the week and database session
        movie_count = crud.get_movie_count_for_day_of_week(db, day_of_week)
    except ValueError:
        # If the get_movie_count_for_day_of_week function raises a ValueError, return a 400 Bad Request response with the message "Invalid day of week"
        raise HTTPException(status_code=400, detail="Invalid day of week")
    # If the function succeeds, return a JSON response with the day of the week name and movie count
    return movie_count

# Define an HTTP GET endpoint that maps to the get_franchise_stats function
@app.get("/movies/belongs_to_collection/{franchise}", response_model=schemas.Franchise)
def belongs_to_collection(franchise: str, db: Session = Depends(get_db)):
    try:
        # Call the get_franchise_stats function with the given franchise name and database session
        stats = crud.get_franchise_stats(db, franchise)
    except ValueError as e:
        # If the get_franchise_stats function raises a ValueError, return a 404 Not Found response with the error message
        raise HTTPException(status_code=404, detail=str(e))
    # If the function succeeds, return a JSON response with the franchise statistics
    return stats

@app.get("/movies/production_countries/{country}", response_model=schemas.MovieCountCountry)
async def production_countries(country: str, db: Session = Depends(get_db)):
    # Retrieve the number of movies from the database for the given country
    movie_count = crud.get_movies_by_country(db, country=country)
    # If no movies are found for the given country, raise a 404 exception
    if movie_count['quantity'] == 0:
        raise HTTPException(status_code=404, detail=f"No movies found for {country}")
    # Return the number of movies produced for the given country
    return movie_count

# Define a route for retrieving movie statistics for a given production company name
@app.get("/movies/production_companies/{producer}", response_model=schemas.Producer)
def production_companies(producer: str, db: Session = Depends(get_db)):
    # Call the get_producer_by_name function to retrieve the movie statistics for the given production company
    db_producer = crud.get_producer_by_name(db, producer)
    # If no statistics are found, raise a 404 HTTP exception
    if db_producer is None:
        raise HTTPException(status_code=404, detail=f"Producer '{producer}' not found")
    # Return the movie statistics in a dictionary
    return db_producer

# This route handler takes a movie title and a database session as input.
# It returns a JSON object with information about the movie's return on investment.
@app.get("/movies/return/{movie}", response_model=schemas.Return)
def movie_return(movie: str, db: Session = Depends(get_db)):
    return crud.get_movie_return(db, title=movie)

# Given a movie title, retrieve similar movie recommendations using the cosine similarity method.
@app.get('/movies/recommendation/{title}')
async def get_recommendations(title: str, db: Session = Depends(get_db)):
    recommendations = crud.get_recommendations(db, title)
    return recommendations