import streamlit as st
from datetime import datetime, timedelta

# Default constants
DEFAULT_OVER_DURATION = timedelta(minutes=4, seconds=25)  # Default: 4 minutes 25 seconds
DEFAULT_TOTAL_DURATION = timedelta(minutes=85)  # Default: 85 minutes for 20 overs

# App title
st.title("Customizable Cricket Over Completion Tracker")

# Input: Total overs and start time
st.subheader("Match Setup")
total_overs = st.number_input("Enter the total number of overs in the innings:", min_value=1, value=20)
start_time_str = st.text_input("Enter the start time of the match (HH:MM, 24-hour format):", value="19:00")

# Allow user to set maximum time per over
st.subheader("Set Maximum Time Allowed per Over")
minutes_per_over = st.number_input("Minutes per over:", min_value=0, max_value=10, value=4, step=1)
seconds_per_over = st.number_input("Seconds per over:", min_value=0, max_value=59, value=25, step=1)

# Calculate time per over
time_per_over = timedelta(minutes=minutes_per_over, seconds=seconds_per_over)

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
    # Calculate the exact match end time
    total_match_duration = time_per_over * total_overs
    match_end_time = start_time + total_match_duration

    # Calculate completion time for each over
    over_schedule = []
    for over in range(1, total_overs + 1):
        over_end_time = start_time + (time_per_over * over)
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

    # Warn if the match duration exceeds 85 minutes
    if total_match_duration > DEFAULT_TOTAL_DURATION:
        st.warning(
            f"The total match duration ({total_match_duration}) exceeds the default allowed duration of 85 minutes."
        )
    elif total_match_duration == DEFAULT_TOTAL_DURATION:
        st.success("The match duration is perfectly aligned with the default 85-minute duration.")
    else:
        st.info(
            f"The total match duration ({total_match_duration}) is shorter than the default allowed duration of 85 minutes."
        )

# Reset option
if st.button("Reset"):
    st.experimental_rerun()











