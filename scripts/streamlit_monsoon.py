import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# 1. Setup Page Config
st.set_page_config(page_title="Monsoon Onset Guess", layout="wide")

# 2. Mock Rainfall Data (Replace this with your actual timeseries CSV)
@st.cache_data
def get_rainfall_data():
    days = np.arange(1, 151)
    # Simulated rainfall pulse around day 100
    rainfall = np.exp(-((days - 100)**2) / (2 * 15**2)) * 50 + np.random.normal(0, 2, 150)
    return pd.DataFrame({"Day": days, "Rainfall": rainfall})

df_rain = get_rainfall_data()

# 3. Persistent Data Store (In-memory for demo; use a DB/Sheet for production)
if 'guesses' not in st.session_state:
    st.session_state.guesses = []

# --- SIDEBAR: STUDENT INPUT ---
st.sidebar.header("Student Input")
st.sidebar.write("When do you think the monsoon started?")
guess = st.sidebar.number_input("Enter Day Number", min_value=1, max_value=150, value=75)

if st.sidebar.button("Submit Guess"):
    st.session_state.guesses.append(guess)
    st.sidebar.success(f"Guess for Day {guess} recorded!")

# --- MAIN AREA: THE LIVE PLOT ---
st.title("Live Monsoon Onset Guesses")
st.write("The vertical lines represent student responses in real-time.")

# Create the Base Plot
fig = go.Figure()

# Add the Rainfall Time Series
fig.add_trace(go.Scatter(
    x=df_rain["Day"], 
    y=df_rain["Rainfall"],
    mode='lines',
    line=dict(color='royalblue', width=2),
    name='Daily Rainfall'
))

# Overplot the Vertical Lines for Student Guesses
for i, g in enumerate(st.session_state.guesses):
    fig.add_vline(
        x=g, 
        line_width=1, 
        line_dash="dash", 
        line_color="rgba(255, 0, 0, 0.4)" # Semi-transparent red
    )

fig.update_layout(
    xaxis_title="Day of Year",
    yaxis_title="Precipitation (mm/day)",
    hovermode="x"
)

st.plotly_chart(fig, use_container_width=True)

# Auto-refresh logic (optional: keeps the plot updating every few seconds)
st.empty()
