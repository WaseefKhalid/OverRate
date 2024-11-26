


import streamlit as st
from datetime import datetime, timedelta

# Constants
MAX_TIME_PER_OVER = 265  # 4 minutes and 25 seconds in seconds
TOTAL_MATCH_DURATION = 85 * 60  # Total 85 minutes in seconds for 20 overs

# App title
st.title("Accurate Cricket Over Completion Tracker")

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
    # Calculate completion time for each over
    over_schedule = []
    for over in range(1, total_overs + 1):
        over_end_time = start_time + timedelta(seconds=over * MAX_TIME_PER_OVER)
        over_schedule.append((over, over_end_time.strftime("%I:%M:%S %p")))

    # Calculate the final end time
    final_time = start_time + timedelta(seconds=total_overs * MAX_TIME_PER_OVER)

    # Display the schedule
    st.subheader("Over Completion Schedule")
    st.write("The following schedule shows when each over should ideally end (HH:MM:SS):")
    for over, time in over_schedule:
        st.write(f"**Over {over}:** Complete by {time}")

    # Final match end time
    st.subheader("Match Timing")
    st.write(f"Match starts at: {start_time.strftime('%I:%M %p')}")
    st.write(f"Match should end at: {final_time.strftime('%I:%M:%S %p')}")

    # Validate total match duration
    expected_end_time = start_time + timedelta(seconds=TOTAL_MATCH_DURATION)
    if final_time == expected_end_time:
        st.success(f"The match ends correctly at {final_time.strftime('%I:%M:%S %p')} after 85 minutes.")
    else:
        st.error(f"Timing issue detected! Expected end time is {expected_end_time.strftime('%I:%M:%S %p')}. Please review the calculations.")

# Reset option
if st.button("Reset"):
    st.experimental_rerun()
