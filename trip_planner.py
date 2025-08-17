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

# --- Create Tabs for Desktop Chart and Mobile List ---
tab1, tab2 = st.tabs(["📊 Timeline Chart", "📋 Trip List"])

# --- Tab 1: The Bubble Chart (Best for Desktop) ---
with tab1:
    fig = px.scatter(
        df, x="Start", y="Type", size="Bubble Size", color="Trip", hover_name="Trip",
        size_max=60
    )
    fig.update_traces(marker={'opacity': 0.7})
    fig.update_layout(
        title="Trip Timeline (Best on Desktop)",
        xaxis_title="Date",
        yaxis_title="Intensity Tier",
        margin=dict(l=20, r=20, t=40, b=20)
    )
    fig.update_xaxes(tickangle=45, nticks=10)
    st.plotly_chart(fig, use_container_width=True)

# --- Tab 2: The Trip List (Ideal for Mobile) ---
with tab2:
    st.subheader("Upcoming Trips")
    # Sort trips by start date to create a clean timeline
    sorted_df = df.sort_values(by="Start")
    for index, row in sorted_df.iterrows():
        with st.container(border=True):
            # Format the date to be readable, e.g., "Sep 06, 2025"
            date_str = row['Start'].strftime("%b %d, %Y")
            st.markdown(f"**{row['Trip']}**")
            st.markdown(f"*{row['Type']}*")
            st.write(f"**When:** {date_str}")
            st.write(f"**Attendees:** {', '.join(row['Attendees'])}")

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
