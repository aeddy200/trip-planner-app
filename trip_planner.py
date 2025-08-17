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

# --- Trip Data ---
TRIP_DATA = [
    {
        "Trip": "Mount Falcon Loop", "Type": "Casual Hiking", "Start": "2025-09-06", "End": "2025-09-06",
        "Attendees": ["Dré", "Tracy"],
        "Itinerary": [
            {'Day': 1, 'Time': '9:00 AM', 'Activity': 'Meet at the west trailhead parking lot.'},
            {'Day': 1, 'Time': '9:15 AM', 'Activity': 'Begin the 3-mile loop hike.'},
            {'Day': 1, 'Time': '11:30 AM', 'Activity': 'Finish hike and head to Morrison for lunch.'},
        ]
    },
    {
        "Trip": "Lost Creek Wilderness Intro", "Type": "Beginner Backpacking", "Start": "2025-09-20", "End": "2025-09-21",
        "Attendees": ["Dré", "Chanty"],
        "Itinerary": [
            {'Day': 1, 'Time': '10:00 AM', 'Activity': 'Meet at the trailhead, check gear.'},
            {'Day': 1, 'Time': '11:00 AM', 'Activity': 'Hike 4 miles to designated campsite.'},
            {'Day': 1, 'Time': '3:00 PM', 'Activity': 'Set up camp, filter water, and relax.'},
            {'Day': 2, 'Time': '9:00 AM', 'Activity': 'Pack up camp and hike back to the trailhead.'},
        ]
    },
    {
        "Trip": "Four Pass Loop", "Type": "Intensive Backpacking", "Start": "2026-07-18", "End": "2026-07-21",
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

# --- Vertical Bubble Chart (Mobile-Friendly) ---
st.header("Trip Timeline")
fig = px.scatter(
    df,
    x="Type",          # Trip types are now on the horizontal axis
    y="Start",         # Dates are now on the vertical axis
    size="Bubble Size",
    color="Trip",
    hover_name="Trip",
    size_max=60
)

# Re-orient the y-axis so that the earliest date is at the top
fig.update_yaxes(autorange="reversed")

fig.update_layout(
    xaxis_title="Intensity Tier",
    yaxis_title="Date",
    # Set a fixed height to ensure it's scrollable and not squished
    height=600,
    margin=dict(l=20, r=20, t=40, b=20)
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# --- Combined Trip Details Section ---
st.header("Trip Details")
selected_trip_name = st.selectbox("Select a trip to see its details:", options=df['Trip'])

if selected_trip_name:
    trip = df[df['Trip'] == selected_trip_name].to_dict('records')[0]

    st.subheader("Attendees")
    if trip['Attendees']:
        for name in trip['Attendees']:
            st.markdown(f"- {name}")
    else:
        st.write("No one has signed up yet.")

    st.divider()

    st.subheader("Itinerary")
    itinerary_items = trip['Itinerary']
    if itinerary_items:
        for item in itinerary_items:
            with st.container(border=True):
                st.markdown(f"**Day {item['Day']} at {item['Time']}**")
                st.write(item['Activity'])
    else:
        st.write("No itinerary planned yet.")
