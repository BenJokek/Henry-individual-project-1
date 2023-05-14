## FastAPI

I used the FastAPI framework to create an app with several endpoints. The application communicates with a database using SQLAlchemy to perform various operations on movie data.

## Model

In the FastAPI app it retrieves all movies from a database, performs some data preprocessing on them, and then computes the cosine similarity between their descriptions to get a list of recommended movies for a specified title. It is limited to 500 movies because the very limited memory in the free server.
I could run it with more thans 20000 movies in local (more than 30000 becomes too much I think) and the recommendations seem good. The notebook is available to test.
