import json
import pandas as pd
import streamlit as st
import numpy as np
import requests

options = json.load(open("options.json"))
st.header("Car prediction predictor")

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
    print(response.text)
    if response.status_code == 200:
        st.session_state.prediction = response.json()["prediction"]
    else:
        st.session_state.prediction = "Error"


st.selectbox(
    "Manufacturer",
    options=options["manufacturer"],
    placeholder="Select a manufacturer",
    key="manufacturer",
    on_change=predict
)

st.selectbox(
    "Year",
    options=range(
        options["years"]["min"],
        options["years"]["max"]+1
    ),
    placeholder="Select a year",
    key="year",
    on_change=predict
)

st.slider(
    "Kilometers driven",
    min_value=options["km"]["min"],
    max_value=options["km"]["max"],
    step=1000,
    format="%dkm",
    key="km",
    on_change=predict
)

st.slider(
    "Mileage",
    min_value=options["mileage"]["min"],
    max_value=options["mileage"]["max"],
    step=1,
    format="%d kmpl",
    key="mileage",
    on_change=predict
)

st.selectbox(
    "Fuel Type",
    options=options["fuel_type"],
    key="fuel",
    on_change=predict
)

st.selectbox(
    "Seller Type",
    options=options["seller_type"],
    key="seller",
    on_change=predict
)

st.selectbox(
    "Transmission type",
    options=options["transmission"],
    key="transmission",
    on_change=predict
)

st.selectbox(
    "Owner type",
    options=options["owner_type"],
    key="owner",
    on_change=predict
)

st.slider(
    "Engine capacity",
    min_value=options["engine"]["min"],
    max_value=options["engine"]["max"],
    step=100,
    format="%dcc",
    key="engine",
    on_change=predict
)

st.slider(
    "Power",
    min_value=options["power"]["min"],
    max_value=options["power"]["max"],
    step=10,
    key="power",
    on_change=predict
)

predict()
st.success(f"prediction: {st.session_state.prediction}")
