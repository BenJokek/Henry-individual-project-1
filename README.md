<p align=center><img src=https://d31uz8lwfmyn8g.cloudfront.net/Assets/logo-henry-white-lg.png><p>

# <h1 align=center> **INDIVIDUAL PROJECT Nº1** </h1>

# <h1 align=center>**`Machine Learning Operations (MLOps)`**</h1>

Welcome to the first individual project of the labs stage! On this occasion, I will have to do a job placing myself in the role of a ***MLOps Engineer***.

<hr>  

## Context

Role to develop:
I recently started working as a Data Scientist at a streaming platform aggregation service startup. My first project is to create a recommendation system that hasn't been implemented yet. When examining the available data, I realized that its maturity is very low: it is nested, untransformed, and there are no automated processes for updating new movies or series, among other problems.

I must start from scratch and quickly become a Data Engineer to have an MVP (Minimum Viable Product) ready for next week.

## ETL



## FastAPI

I used the FastAPI framework to create an app with several endpoints. The application communicates with a database using SQLAlchemy to perform various operations on movie data.

## Model

In the FastAPI app it retrieves all movies from a database, performs some data preprocessing on them, and then computes the cosine similarity between their descriptions to get a list of recommended movies for a specified title. It is limited to 500 movies because the very limited memory in the free server.
I could run it with more thans 20000 movies in local (more than 30000 becomes too much for me) and the recommendations seem good. The notebook is available to test.
