import streamlit as st
import pandas as pd
import pickle
from datetime import datetime

# Load model pipeline
with open('PlaneTicketPricePredcition.pkl', 'rb') as f:
    pipe = pickle.load(f)

st.title("✈️Fight Ticket Price Prediction ")

st.write("Fill the details below to estimate a good buying price for a used car.")

# Input fields
airline = st.text_input("Enter Airline (e.g., IndiGo, Air India, etc.): ")
date_of_Journey = st.date_input("Select Date of Journey:", min_value=datetime.today())

# date_of_Journey = st.text_input("Enter Date of Journey (DD/MM/YYYY): ")

# if date_of_Journey:
#     try:
#         journey_date = datetime.strptime(date_of_Journey, "%d-%m-%Y").date()
#         today = datetime.today().date()

#         if journey_date < today:
#             st.error("Journey date cannot be earlier than today.")
#         else:
#             st.success(f"✅ Journey Date: {journey_date.strftime('%d-%m-%Y')}")
#     except ValueError:
#         st.error("Invalid date format. Please use DD-MM-YYYY.")
        
source = st.text_input("Enter Source city (e.g., Delhi, Kolkata): ")
destination = st.text_input("Enter Destination city (e.g., Mumbai, Bangalore): ")
duration = st.text_input("Enter Duration (e.g., '2h 50m', '50m', '2h'): ")
total_Stops= st.text_input("Enter Total Stops (e.g., 'non-stop', '1 stop', '2 stops'): ")

# Predict button
if st.button("Predict Price"):
    # Prepare input
    columns = ['Airline', 'Date_of_Journey', 'Source', 'Destination', 'Duration','Total_Stops']
    myinput = pd.DataFrame([[airline ,date_of_Journey,source,destination,duration,total_Stops]], columns=columns)
    
    # Prediction
    try:
        result = pipe.predict(myinput)
        st.success(f"You should buy it for ~ ₹ {result[0]} ")
    except Exception as e:
        st.error(f"Prediction failed: {e}")