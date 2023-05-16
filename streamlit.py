import requests
import streamlit as st

ENDPOINTS = {
    "/peliculas_mes/{month_name}": "month_name",
    "/peliculas_dia/{day_of_week}": "day_of_week",
    "/franquicia/{franchise}": "franchise",
    "/peliculas_pais/{country}": "country",
    "/productoras/{producer}": "producer",
    "/retorno/{movie}": "movie",
    "/recomendacion/{title}": "title"
}

st.title("Movie API")

# Display dropdown menu to select endpoint
endpoint = st.selectbox("Select an endpoint", list(ENDPOINTS.keys()))

# Display input field for endpoint parameter
param_name = ENDPOINTS[endpoint]
param_value = st.text_input(f"Enter value for {param_name}")

# Display submit button
submit_button = st.button("Submit")

if submit_button:
    # Replace {parameter} with the actual value of the parameter
    url = f"https://henry-individual-project-1.onrender.com{endpoint}"
    url = url.format(**{param_name: param_value})
    
    response = requests.get(url)

    if response.status_code == 200:
        result = response.json()
        st.write(result)
    else:
        st.write("Error: ", response.status_code)
