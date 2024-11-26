import streamlit as st
from datetime import datetime, timedelta

# Constants
OVER_DURATION = timedelta(minutes=4, seconds=25)  # 4 minutes and 25 seconds
TOTAL_MATCH_DURATION = timedelta(minutes=85)  # Total match duration for 20 overs

# App title
st.title("Cricket Over Completion Tracker (Accurate to 85 Minutes)")

# Input: Total overs and start time
st.subheader("Match Setup")
total_overs = st.number_input("Enter the total number of overs in the innings:", min_value=1, value=20)
start_time_str = st.text_input("Enter the start time of the match (HH:MM, 24-hour format):", value="19:00")

# Validate inputs
if start_time_str:
    try:
        start_time = datetime.strptime(start_time_str, "%H:%M")
        st.success(f"Start time recorded: {start_time.strftime('%I:%M %p')}")
    except ValueError:
        st.error("Invalid time format. Please enter in HH:MM format (24-hour clock).")
        start_time = None
else:
    start_time = None

# Generate over completion times
if st.button("Generate Over Completion Schedule") and start_time:
    # Calculate exact end time for the match
    match_end_time = start_time + TOTAL_MATCH_DURATION

    # Calculate completion time for each over
    over_schedule = []
    for over in range(1, total_overs + 1):
        over_end_time = start_time + (OVER_DURATION * over)
        over_schedule.append((over, over_end_time.strftime("%I:%M:%S %p")))

    # Display the schedule
    st.subheader("Over Completion Schedule")
    st.write("The following schedule shows when each over should ideally end (HH:MM:SS):")
    for over, time in over_schedule:
        st.write(f"**Over {over}:** Complete by {time}")

    # Final match timing validation
    st.subheader("Match Timing")
    st.write(f"Match starts at: {start_time.strftime('%I:%M %p')}")
    st.write(f"Match should end by: {match_end_time.strftime('%I:%M:%S %p')}")

    # Check if the final over ends exactly at the expected match end time
    if over_schedule[-1][1] == match_end_time.strftime("%I:%M:%S %p"):
        st.success(f"The match ends correctly at {match_end_time.strftime('%I:%M:%S %p')} after 85 minutes.")
    else:
        st.error(
            f"Timing issue detected! Last over ends at {over_schedule[-1][1]} but should end at {match_end_time.strftime('%I:%M:%S %p')}."
        )

# Reset option
if st.button("Reset"):
    st.experimental_rerun()

