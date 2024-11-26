import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Constants
MAX_TIME_PER_OVER = 265  # 4 minutes 25 seconds in seconds

# Initialize session state to store data
if 'overs_data' not in st.session_state:
    st.session_state.overs_data = []

if 'interruptions' not in st.session_state:
    st.session_state.interruptions = 0

# App title
st.title("Real-Time Cricket Overrate Tracker")

# Input required overrate
required_rate = st.number_input("Enter required overrate (overs/hour):", min_value=1.0, value=15.0)

# Track overs bowled
st.subheader("Track Overs")
if st.button("Start New Over"):
    st.session_state.overs_data.append({'start_time': datetime.now(), 'end_time': None})

if st.session_state.overs_data and st.session_state.overs_data[-1]['end_time'] is None:
    if st.button("End Over"):
        st.session_state.overs_data[-1]['end_time'] = datetime.now()

# Add interruption
st.subheader("Interruptions")
interruption = st.number_input("Add interruption time (in minutes):", min_value=0, value=0)
if st.button("Add Interruption"):
    st.session_state.interruptions += interruption * 60  # Convert to seconds

# Calculate overrate and time adjustments
if st.session_state.overs_data:
    total_overs = len(st.session_state.overs_data)
    total_time = sum(
        (over['end_time'] - over['start_time']).total_seconds()
        for over in st.session_state.overs_data
        if over['end_time'] is not None
    )

    effective_time = total_time - st.session_state.interruptions
    if effective_time > 0:
        over_rate = (total_overs / (effective_time / 3600))  # Calculate overs/hour
    else:
        over_rate = 0.0

    # Calculate expected time and difference
    expected_time = total_overs * MAX_TIME_PER_OVER  # Total allowed time for the number of overs bowled
    time_diff = effective_time - expected_time  # Positive if over time, negative if ahead

    # Display results
    st.subheader("Results")
    st.write(f"Total Overs Bowled: {total_overs}")
    st.write(f"Total Effective Time: {str(timedelta(seconds=effective_time))}")
    st.write(f"Current Overrate: {over_rate:.2f} overs/hour")

    # Time adjustment display
    if time_diff > 0:
        st.warning(f"The team is behind by {str(timedelta(seconds=abs(time_diff)))} (over the allowed time).")
    else:
        st.success(f"The team is ahead by {str(timedelta(seconds=abs(time_diff)))} (under the allowed time).")

    # Overrate warning
    if over_rate < required_rate:
        st.error("Warning: Overrate is below the required rate!")
    else:
        st.success("Overrate is on track!")
else:
    st.write("No overs tracked yet.")

# Reset data
if st.button("Reset Tracker"):
    st.session_state.overs_data = []
    st.session_state.interruptions = 0
