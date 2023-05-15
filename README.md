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

First I import the dirty data from the datasets directory. Then I clean it. Finally I export it as a ".csv" file in order to use it later in the model to test the recommendation system. Also I upload it to my PostgreSQL database hosted in Render (create your own here: https://dashboard.render.com/new/database) so I can use it with my API. The connection uses the credentials saved in a ".env" file that must be created with the data as in the ".env.example".

## DEA

The DEA uses ydata_profiling, dataprep, sweetviz, autoviz, missingno and wordcloud to analyse the data from the ETL.

## FastAPI

I used the FastAPI framework to create an app with several endpoints. The application communicates with my PostgreSQL database using SQLAlchemy to perform various operations on movie data. I host the API in Render (the same website where I created the database) and also there I can configure the enviroment variables with the database credentials. That's the only configuration I need in order to connect the database, the code itself do the rest. Also important when creating the "Web Service" server in Render, in order to be able to use the API, I have to configure the settings so the "Build Command" is "pip install -r requirements.txt" and the "Start Command" is "uvicorn main:app --host 0.0.0.0 --port 10000". Here is the importance of having a environment in our project so we can add the dependencies with "pip freeze > requirements.txt" so the server use that file to install everything needed (https://github.com/HX-FNegrete/render-fastapi-tutorial).

## Model - Movie Description Based Recommender

The model will look for similarity between movies. This is known as Content Based Filtering/Recommender because I will be using movie metadata to build it. It will be based on movie "Overviews" and "Taglines". Also, I will be using a subset of all the movies available due to limiting computing power.

The FastAPI app retrieves all movies from my PostgreSQL database, performs some data preprocessing on them, and then computes the cosine similarity between their descriptions to get a list of recommended movies for a specified title. It is limited to 500 movies because the very limited memory in the free server.
I could run it with more thans 20000 movies in local (more than 30000 becomes too much for me) and the recommendations seem good. The notebook is available to test.
