import streamlit as st
from datetime import datetime, timedelta
import pytz  # Import timezone library

# Default constants
DEFAULT_OVER_DURATION = timedelta(minutes=4, seconds=25)  # 4 minutes 25 seconds
DEFAULT_TOTAL_DURATION = timedelta(minutes=85)  # 85 minutes for 20 overs

# Define Guyana's timezone
LOCAL_TIMEZONE = pytz.timezone("America/Guyana")

# App title
st.title("Real-Time Cricket Over Tracker (24-Hour Format)")

# Input: Total overs and start time
st.subheader("Match Setup")
total_overs = st.number_input("Enter the total number of overs in the innings:", min_value=1, value=20)
start_time_str = st.text_input("Enter the start time of the match (HH:MM, 24-hour format):", value="22:00")

# Validate inputs
if start_time_str:
    try:
        start_time = datetime.strptime(start_time_str, "%H:%M")
        start_time = LOCAL_TIMEZONE.localize(start_time)  # Localize start time to the specified timezone
        st.success(f"Start time recorded: {start_time.strftime('%H:%M')} ({LOCAL_TIMEZONE.zone})")
    except ValueError:
        st.error("Invalid time format. Please enter in HH:MM format (24-hour clock).")
        start_time = None
else:
    start_time = None

# Generate over schedule
if start_time:
    st.subheader("Over Completion Schedule")
    over_schedule = []
    for over in range(1, total_overs + 1):
        over_end_time = start_time + (DEFAULT_OVER_DURATION * over)
        over_schedule.append((over, over_end_time))

    # Display checkboxes for each over
    st.subheader("Track Overs in Real-Time")
    completed_overs = []
    for over, end_time in over_schedule:
        is_completed = st.checkbox(f"Over {over} (Ideal End Time: {end_time.strftime('%H:%M:%S')})", key=f"over_{over}")
        completed_overs.append(is_completed)

    # Real-time tracking
    current_time = datetime.now(LOCAL_TIMEZONE)  # Use localized current time
    st.subheader("Real-Time Status")
    st.write(f"Current Time: {current_time.strftime('%H:%M:%S')} ({LOCAL_TIMEZONE.zone})")

    # Calculate "behind/ahead" status
    completed_count = sum(completed_overs)
    ideal_time_for_completed = start_time + (DEFAULT_OVER_DURATION * completed_count)

    if current_time > ideal_time_for_completed:
        time_diff = current_time - ideal_time_for_completed
        minutes, seconds = divmod(time_diff.total_seconds(), 60)
        st.error(f"Behind schedule by: {int(minutes)} minutes and {int(seconds)} seconds.")
    else:
        time_diff = ideal_time_for_completed - current_time
        minutes, seconds = divmod(time_diff.total_seconds(), 60)
        st.success(f"Ahead of schedule by: {int(minutes)} minutes and {int(seconds)} seconds.")

    # Final match end time
    final_time = start_time + (DEFAULT_OVER_DURATION * total_overs)
    st.write(f"Expected Match End Time: {final_time.strftime('%H:%M:%S')} ({LOCAL_TIMEZONE.zone})")

# Reset option
if st.button("Reset"):
    st.experimental_rerun()







