import requests
import streamlit as st

with st.form("API Request Form"):
    endpoint = st.selectbox("Choose an endpoint", ["/movies/month/{month_name}", "/movies/week/{day_of_week}", "/movies/belongs_to_collection/{franchise}", "/movies/production_countries/{country}", "/movies/production_companies/{producer}", "/movies/return/{movie}", "/movies/recommendation/{title}"])
    if endpoint == "/movies/month/{month_name}":
        month_name = st.text_input("Enter the month name")
        params = {"month_name": month_name}
    elif endpoint == "/movies/week/{day_of_week}":
        day_of_week = st.text_input("Enter the day of the week")
        params = {"day_of_week": day_of_week}
    elif endpoint == "/movies/belongs_to_collection/{franchise}":
        franchise = st.text_input("Enter the franchise name")
        params = {"franchise": franchise}
    elif endpoint == "/movies/production_countries/{country}":
        country = st.text_input("Enter the production country name")
        params = {"country": country}
    elif endpoint == "/movies/production_companies/{producer}":
        producer = st.text_input("Enter the production company name")
        params = {"producer": producer}
    elif endpoint == "/movies/return/{movie}":
        movie = st.text_input("Enter the movie title")
        params = {"movie": movie}
    elif endpoint == "/movies/recommendation/{title}":
        title = st.text_input("Enter the movie title")
        params = {"title": title}

    submit_button = st.form_submit_button(label='Submit')

if submit_button:
    # Replace {parameter} with the actual value of the parameter
    url = "https://henry-individual-project-1.onrender.com" + endpoint
    response = requests.get(url.format(**params))

    if response.status_code == 200:
        result = response.json()
        st.write(result)
    else:
        st.write("Error: ", response.status_code)
