# trip_planner.py
import streamlit as st
import pandas as pd
import plotly.express as px
import datetime

# --- App Configuration ---
st.set_page_config(
    page_title="Our Trip Planner",
    page_icon="🗺️",
    layout="wide"
)

# --- Trip Data with New Intensity Tiers and Simplified Attendees ---
TRIP_DATA = [
    {
        "Trip": "Mount Falcon Loop",
        "Type": "Casual Hiking", # New Category
        "Start": "2025-09-06",
        "End": "2025-09-06",
        "Attendees": ["Dré", "Tracy"],
        "Itinerary": [
            {'Day': 1, 'Time': '9:00 AM', 'Activity': 'Meet at the west trailhead parking lot.'},
            {'Day': 1, 'Time': '9:15 AM', 'Activity': 'Begin the 3-mile loop hike.'},
            {'Day': 1, 'Time': '11:30 AM', 'Activity': 'Finish hike and head to Morrison for lunch.'},
        ]
    },
    {
        "Trip": "Lost Creek Wilderness Intro",
        "Type": "Beginner Backpacking", # New Category
        "Start": "2025-09-20",
        "End": "2025-09-21",
        "Attendees": ["Dré", "Chanty"],
        "Itinerary": [
            {'Day': 1, 'Time': '10:00 AM', 'Activity': 'Meet at the trailhead, check gear.'},
            {'Day': 1, 'Time': '11:00 AM', 'Activity': 'Hike 4 miles to designated campsite.'},
            {'Day': 1, 'Time': '3:00 PM', 'Activity': 'Set up camp, filter water, and relax.'},
            {'Day': 2, 'Time': '9:00 AM', 'Activity': 'Pack up camp and hike back to the trailhead.'},
        ]
    },
    {
        "Trip": "Four Pass Loop",
        "Type": "Intensive Backpacking", # New Category
        "Start": "2026-07-18",
        "End": "2026-07-21",
        "Attendees": ["Dré", "Teresa", "Chanty"],
        "Itinerary": [
            {'Day': 1, 'Time': '8:00 AM', 'Activity': 'Start at Maroon Lake, hike 7 miles over West Maroon Pass.'},
            {'Day': 2, 'Time': '7:00 AM', 'Activity': 'Hike 8 miles over Frigid Air Pass.'},
            {'Day': 3, 'Time': '7:00 AM', 'Activity': 'Hike 7 miles over Trail Rider Pass.'},
            {'Day': 4, 'Time': '6:00 AM', 'Activity': 'Hike 5 miles over Buckskin Pass and return to trailhead.'},
        ]
    }
]

# --- Main App ---
st.title("🗺️ Our Adventure Planner")
st.write("An overview of all the trips we have planned for the next year!")

df = pd.DataFrame(TRIP_DATA)
df['Start'] = pd.to_datetime(df['Start'])
df['End'] = pd.to_datetime(df['End'])
df['Trip Length (Days)'] = (df['End'] - df['Start']).dt.days + 1
df['Participants'] = df['Attendees'].apply(len)
df['Bubble Size'] = df['Trip Length (Days)'] * df['Participants']

# --- Bubble Chart ---
fig = px.scatter(
    df, x="Start", y="Type", size="Bubble Size", color="Trip", hover_name="Trip",
    size_max=60, title="Trip Timeline"
)
fig.update_traces(marker={'opacity': 0.7})
fig.update_layout(xaxis_title="Date", yaxis_title="Intensity Tier")
st.plotly_chart(fig, use_container_width=True)

st.divider()

# --- Combined Trip Details Section ---
st.header("Trip Details")
selected_trip_name = st.selectbox("Select a trip to see its details:", options=df['Trip'])

if selected_trip_name:
    trip = df[df['Trip'] == selected_trip_name].to_dict('records')[0]

    # --- Display Attendees as a list ---
    st.subheader("Attendees")
    attendees = trip['Attendees']
    if attendees:
        # MODIFIED: Displays attendees as a simple bulleted list
        for name in attendees:
            st.markdown(f"- {name}")
    else:
        st.write("No one has signed up yet.")

    st.divider()

    # --- Display Detailed Itinerary as a Table ---
    st.subheader("Itinerary")
    itinerary_items = trip['Itinerary']
    if itinerary_items:
        itinerary_df = pd.DataFrame(itinerary_items)
        st.dataframe(itinerary_df, use_container_width=True, hide_index=True)
    else:
        st.write("No itinerary planned yet.")
