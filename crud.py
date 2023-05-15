from sqlalchemy.orm import Session
from sqlalchemy import extract, func
import models
from datetime import datetime
from typing import Dict
import calendar
from fastapi import HTTPException
from typing import Optional
import math

# Define a function that returns the number of movies released in a given month
def get_movie_count_for_month(db: Session, month_name: str):
    try:
        # Try to parse the month name argument as an English month name
        month_date = datetime.strptime(month_name, "%B")
    except ValueError:
        try:
            # If parsing as an English month name fails, try to parse as a Spanish month name
            spanish_month_names = {
                'enero': 'January',
                'febrero': 'February',
                'marzo': 'March',
                'abril': 'April',
                'mayo': 'May',
                'junio': 'June',
                'julio': 'July',
                'agosto': 'August',
                'septiembre': 'September',
                'octubre': 'October',
                'noviembre': 'November',
                'diciembre': 'December',
            }
            # Map the Spanish month name to its English counterpart
            english_month_name = spanish_month_names[month_name.lower()]
            # Try to parse the English month name
            month_date = datetime.strptime(english_month_name, "%B")
        except KeyError:
            # If parsing as a Spanish month name fails, raise a ValueError
            raise ValueError("Invalid month name")
        
    # Query the database for all movies released in the given month
    num_movies = (
        db.query(models.Movie)
        .filter(extract('month', models.Movie.release_date) == month_date.month)
        .distinct(models.Movie.title)
        .count()
    )
    # Return a dictionary with the month name and movie count
    return {"month_name": month_date.strftime("%B"), "quantity": num_movies}


# Define a function that returns the number of movies released on a given day of the week
def get_movie_count_for_day_of_week(db: Session, day_of_week: str):
    day_mapping = {
        'monday': 0,
        'tuesday': 1,
        'wednesday': 2,
        'thursday': 3,
        'friday': 4,
        'saturday': 5,
        'sunday': 6,
        'lunes': 0,
        'martes': 1,
        'miercoles': 2,
        'jueves': 3,
        'viernes': 4,
        'sabado': 5,
        'domingo': 6
    }
    day_of_week_lower = day_of_week.lower()
    if day_of_week_lower not in day_mapping:
        # If the day_of_week argument is not a valid day of the week, raise a ValueError
        raise ValueError("Invalid day of week")
    day_of_week_int = day_mapping[day_of_week_lower]

    # Query the database for all movies released on the given day of the week
    num_movies = (
        db.query(models.Movie)
        .filter(extract('dow', models.Movie.release_date) == day_of_week_int)
        .distinct(models.Movie.title)
        .count()
    )
    # Return a dictionary with the day of the week name and movie count
    return {"day_of_week": calendar.day_name[day_of_week_int], "quantity": num_movies}

# Define a function to get franchise statistics for a given franchise name
def get_franchise_stats(db: Session, franchise: str) -> Dict:
    # Query the database for all movies belonging to the given franchise
    movies = db.query(models.Movie).filter(func.lower(models.Movie.belongs_to_collection) == func.lower(franchise)).all()
    
    # If there are no movies found for the given franchise name, raise a ValueError
    if not movies:
        raise ValueError(f"Franchise '{franchise}' not found")
    
    # Calculate the number of movies in the franchise, the total revenue of the franchise, and the average revenue per movie
    quantity = len(movies)
    total_revenue = sum(movie.revenue for movie in movies)
    average_revenue = total_revenue / quantity if quantity > 0 else 0
    
    # If the average revenue is not a finite number (e.g. it is NaN or infinity), set it to 0
    if not math.isfinite(average_revenue):
        average_revenue = 0
    # Return a dictionary containing the franchise name, the number of movies in the franchise, the total revenue of the franchise, and the average revenue per movie
    return {'belongs_to_collection': franchise, 'quantity': quantity, 'total_revenue': total_revenue, 'average_revenue': average_revenue}

def get_movies_by_country(db: Session, country: str):
    num_movies = (
            db.query(models.Movie)  # Start a query on the Movie table
            .filter(func.lower(models.Movie.production_countries).contains(func.lower(country)))  # Filter movies produced in the given country
            .distinct(models.Movie.title)  # Only count each movie once, even if it was produced multiple times in the country
            .count()  # Count the number of movies that meet the criteria
        )
    return {'country': country, 'quantity': num_movies}

# Define a function to get movie statistics for a given production company name
# Parameters:
#   - db: a database session object
#   - producer: a string representing the production company name
# Returns:
#   - a dictionary containing statistics for the movies produced by the company
#     - production_companies: the name of the production company
#     - total_revenue: the total revenue of all movies produced by the company
#     - quantity: the number of movies produced by the company
def get_producer_by_name(db: Session, producer: str) -> Optional[Dict]:
    # Query the database to retrieve all movies produced by the given production company
    movies = db.query(models.Movie).filter(func.lower(models.Movie.production_companies) == func.lower(producer)).all()
    
    # If no movies are found, return None
    if not movies:
        return None

    # Calculate the total revenue and quantity of movies produced by the company
    total_profit = sum(movie.revenue for movie in movies)
    quantity = len(movies)
    
    # Return a dictionary containing the movie statistics
    return {'production_companies': producer, 'total_revenue': total_profit, 'quantity': quantity}

# This function queries the database for a movie with a given title.
# It returns a models.Movie object representing the movie.
def get_movie_by_title(db: Session, title: str) -> models.Movie:
    return db.query(models.Movie).filter(func.lower(models.Movie.title) == func.lower(title)).first()
# This function takes a database session and a movie title as input.
# It returns a dictionary with information about the movie's investment,
# revenue, profit, rate of return, and year of release.
def get_movie_return(db: Session, title: str) -> dict:
    # First, query the database for the movie with the given title.
    db_movie = get_movie_by_title(db, title=title)
    if not db_movie:
        # If the movie is not found in the database, raise an HTTPException with status code 404.
        raise HTTPException(status_code=404, detail=f"Movie '{title}' not found")
    # Calculate the investment, revenue, and profit of the movie.
    investment = db_movie.budget
    revenue = db_movie.revenue
    profit = revenue - investment
    # Calculate the rate of return, rounded to 2 decimal places.
    rate_of_return = round((profit / investment) * 100, 2) if investment else 0
    # Return a dictionary with information about the movie.
    return {'movie': title, 'investment': investment, 'profit': profit, 'returns': rate_of_return, 'year': db_movie.release_date.year}

# MODEL:

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# get_recommendations(db: Session, title: str) is a function that takes in a SQLAlchemy database session and a movie title as input, 
# and returns a list of recommended movies. First, it retrieves all movies from the database and converts them to a pandas dataframe. 
# It then performs some data preprocessing, including filling any empty description fields, dropping duplicate movie titles, 
# and limiting the dataframe to the top 500 movies. Next, it computes the cosine similarity matrix using the TfidfVectorizer and linear_kernel 
# functions from the scikit-learn library. It then resets the index of the dataframe and creates a mapping of movie titles to indices. 
# Finally, it gets recommendations for the specified movie by computing the cosine similarity between its description and those of all 
# other movies, and returning the top 5 most similar movies.

# It is limited to 500 movies because the very limited memory in the free server.


def get_recommendations(db: Session, title: str):
    # Retrieve all movies from the database
    movies = db.query(models.Movie).all()
    
    # Convert the movies to a pandas dataframe
    df = pd.DataFrame([m.__dict__ for m in movies])

    # Perform data preprocessing
    df['description'] = df['description'].fillna('') # fill NaN values with an empty string
    df = df.drop_duplicates(subset='title') # remove duplicates based on the 'title' column
    df = df.head(500) # keep only the first 500 movies (for performance reasons)
    print("sample", df["title"].head()) # print a sample of the dataframe
    
    # Compute cosine similarity matrix
    tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 2), min_df=0, stop_words='english')
    tfidf_matrix = tf.fit_transform(df['description'])
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    # Reset index and create mapping of movie titles to indices
    df = df.reset_index() # reset the index to have consecutive integers
    titles = df['title']
    indices = pd.Series(df.index, index=df['title'])

    # Get recommendations for the specified movie
    if title not in indices: # check if the input movie title is in the indices
        return f"Movie not found, try with some of these please: {df['title'].head()}"
    idx = indices[title] # get the index of the input movie title
    sim_scores = list(enumerate(cosine_sim[idx])) # get the cosine similarity scores of the input movie with all other movies
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True) # sort the similarity scores in descending order
    sim_scores = sim_scores[1:6] # keep only the top 5 most similar movies (excluding the input movie)
    movie_indices = [i[0] for i in sim_scores] # get the indices of the most similar movies
    return {'recommended list': titles.iloc[movie_indices].tolist()} # return the titles of the most similar movies
