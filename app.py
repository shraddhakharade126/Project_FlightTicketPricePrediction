import streamlit as st
import pandas as pd
import pickle
from datetime import datetime
import base64



st.title("✈️ Flight Ticket Price Prediction")
st.markdown("*Fill in the flight details to predict ticket price")

# Load model pipeline
with open('PlaneTicketPricePredcitionfinal123.pkl', 'rb') as f:
    pipe = pickle.load(f)

def add_bg_from_local(image_file):
    with open(image_file, "rb") as image:
        encoded_string = base64.b64encode(image.read()).decode()  # ✅ Corrected here
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("data:image/jpg;base64,{encoded_string}");
             background-size: cover;
             background-attachment: fixed;
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

add_bg_from_local('airport23.jpg')  # Replace with your image filename



col1, col2 = st.columns(2)

with col1:
    airline = st.selectbox("Select Airline", ['IndiGo', 'Air India', 'SpiceJet', 'Vistara', 'GoAir', 'Other'])
    source = st.selectbox("Select Source City", ['Delhi', 'Kolkata', 'Chennai', 'Bangalore', 'Mumbai'])

with col2:
    destination = st.selectbox("Select Destination City", ['Delhi', 'Kolkata', 'Chennai', 'Bangalore', 'Mumbai'])
    total_stops = st.selectbox("Total Stops", ['non-stop', '1 stop', '2 stops', '3 stops'])

date_of_Journey = st.date_input("Date of Journey", min_value=datetime.today())
duration = st.text_input("Enter Duration (e.g., '2h 50m', '50m', '2h'):")
from datetime import datetime
def convert_duration(duration_str):
    try:
        parts = duration_str.strip().lower().replace(' ', '').replace('h', ':').replace('m', '').split(':')
        if len(parts) == 2:
            hours, minutes = int(parts[0]), int(parts[1])
        elif 'h' in duration_str:
            hours, minutes = int(parts[0]), 0
        else:
            hours, minutes = 0, int(parts[0])
        return hours * 60 + minutes
    except:
        return 0

duration_mins = convert_duration(duration)

if st.button("Predict Price"):
    try:
        myinput = pd.DataFrame([[airline, date_of_Journey, source, destination, duration_mins, total_stops]],
                               columns=['Airline', 'Date_of_Journey', 'Source', 'Destination', 'Duration', 'Total_Stops'])

        # Optional preprocessing if needed here...

        result = pipe.predict(myinput)
        # Custom color styling using HTML
        st.markdown(
            f"""
            <div style="background-color: rgba(255, 255, 255, 0.1);
                        padding: 10px 18px;
                        border-radius: 12px;
                        display: inline-block;
                        font-size: 22px;
                        font-weight: 600;
                        color: #0a2f5c;
                        box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.15);">
                🧮 Predicted Price: ₹ {result[0]:,.2f}
            </div>
            """,
            unsafe_allow_html=True
        )


    except Exception as e:
        st.error(f"Prediction failed: {e}")