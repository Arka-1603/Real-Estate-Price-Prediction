import streamlit as st
import requests

with st.container():
    st.title("Bangalore House Price Prediction")
    
    # Input: Area of the house
    area = st.text_input("Area (Square Feet)", value="1000")

    # Input: Number of BHK
    bhk = st.radio("Select BHK", [1, 2, 3, 4, 5])

    # Input: Number of bathrooms
    bathrooms = st.radio("Select Bathrooms", [1, 2, 3, 4, 5])

    # Dynamically load locations from API
    locations = []
    try:
        response = requests.get("http://127.0.0.1:5000/get_location_names")
        if response.status_code == 200:
            locations = response.json().get("locations", [])
    except Exception as e:
        st.error("Failed to load locations.")

    if not locations:
        st.warning("No locations available. Please check the server.")
    else:
        location = st.selectbox("Select Location", locations)

        # Button to submit the form and get the estimated price
        if st.button("Estimate Price"):
            # Send request to backend API
            url = "http://127.0.0.1:5000/predict_home_price"
            params = {
                "total_sqft": float(area),
                "bhk": bhk,
                "bath": bathrooms,
                "location": location
            }
            response = requests.post(url, json=params)
            
            # Display the result
            if response.status_code == 200:
                estimated_price = response.json().get("estimated_price")
                st.success(f"The estimated price of the house is: ₹ {estimated_price} Lakh")
            else:
                st.error("Error in retrieving the estimated price. Please try again later.")