import streamlit as st
from datetime import datetime, timedelta

# Constants
MAX_TIME_PER_OVER = 265  # 4 minutes 25 seconds in seconds

# App title
st.title("Comprehensive Cricket Over Completion Tracker")

# Input: Total overs and start time
st.subheader("Match Setup")
total_overs = st.number_input("Enter the total number of overs in the innings:", min_value=1, value=20)
start_time_str = st.text_input("Enter the start time of the match (HH:MM:SS, 24-hour format):", value="14:00:00")

# Validate inputs
if start_time_str:
    try:
        start_time = datetime.strptime(start_time_str, "%H:%M:%S")
        st.success(f"Start time recorded: {start_time.strftime('%I:%M:%S %p')}")
    except ValueError:
        st.error("Invalid time format. Please enter in HH:MM:SS format (24-hour clock).")
        start_time = None
else:
    start_time = None

# Generate over completion times
if st.button("Generate Over Completion Schedule") and start_time:
    # Calculate completion time for each over
    over_schedule = []
    for over in range(1, total_overs + 1):
        over_end_time = start_time + timedelta(seconds=over * MAX_TIME_PER_OVER)
        over_schedule.append((over, over_end_time.strftime("%I:%M:%S %p")))

    # Display the schedule
    st.subheader("Over Completion Schedule")
    st.write("The following schedule shows when each over should ideally end (HH:MM:SS):")
    for over, time in over_schedule:
        st.write(f"**Over {over}:** Complete by {time}")

# Reset option
if st.button("Reset"):
    st.experimental_rerun()

