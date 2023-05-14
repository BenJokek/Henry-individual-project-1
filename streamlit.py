import requests
import streamlit as st

ENDPOINTS = {
    "/movies/month/{month_name}": "month_name",
    "/movies/week/{day_of_week}": "day_of_week",
    "/movies/belongs_to_collection/{franchise}": "franchise",
    "/movies/production_countries/{country}": "country",
    "/movies/production_companies/{producer}": "producer",
    "/movies/return/{movie}": "movie",
    "/movies/recommendation/{title}": "title"
}

with st.form("API Request Form"):
    endpoint = st.selectbox("Choose an endpoint", list(ENDPOINTS.keys()))
    param_name = ENDPOINTS[endpoint]
    param_value = st.text_input(f"Enter the {param_name}")

    params = {param_name: param_value}

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
