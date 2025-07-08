import pandas as pd
import numpy as np
import joblib
import pickle
import streamlit as st
import matplotlib.pyplot as plt


model = joblib.load("pollution_model.pkl")
model_cols = joblib.load("model_columns.pkl")

# Let's create an User interface
st.title("Water Pollutants Predictor")
st.write("Predict the water pollutants based on Year and Station ID")

# User inputs
year_input = st.number_input("Enter Year", min_value=2000, max_value=2100, value=2022)
station_id = st.text_input("Enter Station ID", value='1')

if st.button('Predict'):
    if not station_id:
        st.warning('Please enter the station ID')
    else:
       
        input_df = pd.DataFrame({'year': [year_input], 'id':[station_id]})
        input_encoded = pd.get_dummies(input_df, columns=['id'])

      
        for col in model_cols:
            if col not in input_encoded.columns:
                input_encoded[col] = 0
        input_encoded = input_encoded[model_cols]

      
        predicted_pollutants = model.predict(input_encoded)[0]
        pollutants = ['O2', 'NO3', 'NO2', 'SO4', 'PO4', 'CL']

        st.subheader(f"Predicted pollutant levels for the station '{station_id}' in {year_input}:")
        predicted_values = {}
        for p, val in zip(pollutants, predicted_pollutants):
            st.write(f'**{p} = {val:.2f}**')
            if(p=='O2'):
                if(val>5):
                    st.write("**It has proper levels. >6 mg/L is good for most aquatic life. It's a key indicator of water health.**")
                else:
                    st.write("**Low levels (<5 mg/L) stress or kill aquatic organisms. It's a key indicator of water health.**")
            elif(p=='NO3'):
                if(val>50 and val<10):
                    st.write("**Not good for most aquatic life.Higher causes health risks (e.g., methemoglobinemia).In excess, it promotes algae growth (eutrophication) and can harm aquatic ecosystems and drinking water safety.**")
                else:
                    st.write("**It has proper levels. WHO limit for drinking water nitrate is 10 mg/L nitrate nitrogen or 50 mg/L nitrate.**")
            elif(p=='NO2'):
                if(val>10):
                    st.write("**Toxic to humans and aquatic life; very low allowable limits.Toxic to aquatic organisms, even at low concentrations. Indicates a breakdown in nitrogen processing.**")
                else:
                    st.write("**It should be less tham 10 Mg/L to consume. It has proper levels.**")
            elif(p=='SO4'):
                if(val>250):
                    st.write("**Higher levels cause taste and laxative effects. EPA Secondary Standard.Generally, not harmful in low concentrations but can affect taste and promote corrosion.**")
                else:
                    st.write("**It has proper levels. Generally, not harmful in low concentrations but can affect taste and promote corrosion.**")
            elif(p=='PO4'):
                if(val>0.1):
                    st.write("**Higher levels lead to eutrophication. Aim for low to prevent algal blooms.Excess phosphate leads to algal blooms and eutrophication, causing oxygen depletion and fish kills.**")
                else:
                    st.write("**It has proper levels.**")
            else:
                if(val>250):
                    st.write("**High levels affect taste; aquatic life limits often lower (e.g., <230 mg/L).High chloride concentrations affect drinking water taste and harm freshwater organisms.** ")
                else:
                    st.write("**It has proper levels.**")


# Pollutant ideal proportions (estimated for health/ecosystem balance)
labels = ['O2', 'NO3', 'NO2', 'SO4', 'PO4', 'CL']
sizes = [40, 15, 5, 15, 5, 20]
colors = ['#66c2a5', '#fc8d62', '#8da0cb', '#e78ac3', '#a6d854', '#ffd92f']

fig, ax = plt.subplots()
ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

st.subheader("Ideal Pollutant Proportions for Healthy Water")
st.pyplot(fig)
                
st.markdown("""
    <style>
        .stApp {
            background-image: url("https://i.pinimg.com/736x/97/ac/72/97ac7206f49e25957c5ebb7e07c2525f.jpg");
            background-size: cover;
            background-repeat: repeat;
            background-attachment: fixed;
            font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
           
        }
        .main:before {
            content: "";
            position: fixed;
            top: 0;
            left: 0;
            height: 100%;
            width: 100%;
            background: rgba(255, 255, 255, 0.4);  
            z-index: -1;
        }
        .stButton > button {
            background-color: #009999;
            color: white;
            font-size: 18px;
            padding: 10px;
            border-radius: 10px;
            box-shadow: whitesmoke;
            border-radius: 25%;
        }
        .stwrite{
            box-shadow: whitesmoke;
        }
        .background-image{
            opacity: 75%;
        }
    </style>
""", unsafe_allow_html=True)