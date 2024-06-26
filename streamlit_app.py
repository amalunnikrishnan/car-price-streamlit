import json
import joblib
import pandas as pd
import streamlit as st
import numpy as np
import requests

options = json.load(open("options.json"))
st.title("Used Car Price Predictor")

# Update this URL to point to your deployed Flask API
url = "https://car-price-flask-api.onrender.com/predict"


def high_end_check(manufacturer):
    if manufacturer.lower() in options["high_end"]:
        return 1
    else:
        return 0


def is_second(owner):
    if owner == "Second":
        return 1
    else:
        return 0


def is_first(owner):
    if owner == "First":
        return 1
    else:
        return 0


def check_fuel_type(fuel):
    if fuel == "Diesel":
        return 1
    else:
        return 0


def check_seller_type(seller):
    if seller == "Individual":
        return 1
    else:
        return 0


def check_trans(transmission):
    if transmission == "Automatic":
        return 1
    else:
        return 0


def predict():
    i = {
        "fuel": check_fuel_type(st.session_state.fuel),
        "seller_type": check_seller_type(st.session_state.seller),
        "transmission": check_trans(st.session_state.transmission),
        "mileage_kmpl": st.session_state.mileage,
        "engine": st.session_state.engine,
        "max_power": st.session_state.power,
        "high_end": high_end_check(st.session_state.manufacturer),
        "km_driven_log": np.log(st.session_state.km),
        "first": is_first(st.session_state.owner),
        "second": is_second(st.session_state.owner),
        "age": 2021 - st.session_state.year
    }
    response = requests.post(url, json=i)
    if response.status_code == 200:
        st.session_state.prediction = response.json()["prediction"]
    else:
        st.session_state.prediction = "Error"



st.selectbox(
    "Manufacturer",
    options=options["manufacturer"],
    placeholder="Select a manufacturer",
    key="manufacturer",
)

st.selectbox(
    "Year",
    options=range(
        options["years"]["min"],
        options["years"]["max"]+1
    ),
    placeholder="Select a year",
    key="year",
)

st.slider(
    "Kilometers driven",
    min_value=options["km"]["min"],
    max_value=options["km"]["max"],
    step=1000,
    format="%dkm",
    key="km",
)

st.slider(
    "Mileage",
    min_value=options["mileage"]["min"],
    max_value=options["mileage"]["max"],
    step=1,
    format="%d kmpl",
    key="mileage",
)

st.selectbox(
    "Fuel Type",
    options=options["fuel_type"],
    key="fuel",
)

st.selectbox(
    "Seller Type",
    options=options["seller_type"],
    key="seller",
)

st.selectbox(
    "Transmission type",
    options=options["transmission"],
    key="transmission",
)

st.selectbox(
    "Owner type",
    options=options["owner_type"],
    key="owner",
)

st.slider(
    "Engine capacity",
    min_value=options["engine"]["min"],
    max_value=options["engine"]["max"],
    step=100,
    format="%dcc",
    key="engine",
)

st.slider(
    "Power",
    min_value=options["power"]["min"],
    max_value=options["power"]["max"],
    step=10,
    key="power",
)

st.button("Predict", on_click=predict)
if "prediction" in st.session_state:
    min_pred = round(st.session_state.prediction * 0.85, 2)
    max_pred = round(st.session_state.prediction * 1.15, 2)
    if st.session_state.prediction == "Error":
        st.error("Error in prediction")
    else:
        st.success(f"Price Evaluation(INR): {min_pred} to {max_pred}")
    
st.text("")
st.text("")
st.text("")
st.markdown("""

#### Project for the Productionalizing ML on Cloud course at Plaksha Tech Leaders Fellowship.

[Based on CarDekho User Car Sales Data for cars manufactured from 1994 to 2020](https://www.kaggle.com/nehalbirla/vehicle-dataset-from-cardekho)
                        
### Git Repositories
- [Streamlit](https://github.com/amalunnikrishnan/car-price-streamlit)
- [Flask API](https://github.com/amalunnikrishnan/car-price-flask-api)
- [Combined](https://github.com/amalunnikrishnan/car-price-predictor)

### Team
- [Amal Nair](https://github.com/amalunnikrishnan)
- [Cefil Joseph Soans](https://github.com/cefiljoseph)
- [Rajat Jacob](https://github.com/RajatJacob)

""")
