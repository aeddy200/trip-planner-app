# trip_planner.py
import streamlit as st
import pandas as pd
import plotly.express as px
import datetime

# --- App Configuration & Data ---
st.set_page_config(page_title="Our Trip Planner", page_icon="🗺️", layout="wide")
TRIP_DATA = [
    {
        "Trip": "Mount Falcon Loop", "Type": "Casual Hiking", "Start": "2025-09-06", "End": "2025-09-06",
        "Attendees": ["Dré", "Tracy"],
        "Itinerary": [{'Day': 1, 'Time': '9:00 AM', 'Activity': 'Meet at the west trailhead parking lot.'}]
    },
    {
        "Trip": "Lost Creek Wilderness Intro", "Type": "Beginner Backpacking", "Start": "2025-09-20", "End": "2025-09-21",
        "Attendees": ["Dré", "Chanty"],
        "Itinerary": [{'Day': 1, 'Time': '10:00 AM', 'Activity': 'Meet at the trailhead, check gear.'}]
    },
    {
        "Trip": "Four Pass Loop", "Type": "Intensive Backpacking", "Start": "2026-07-18", "End": "2026-07-21",
        "Attendees": ["Dré", "Teresa", "Chanty"],
        "Itinerary": [{'Day': 1, 'Time': '8:00 AM', 'Activity': 'Start at Maroon Lake, hike 7 miles.'}]
    }
]

# --- Main App Logic ---
st.markdown("<h1 style='font-size: 24px;'>🗺️ Our Adventure Planner</h1>", unsafe_allow_html=True)

df = pd.DataFrame(TRIP_DATA)
df['Start'] = pd.to_datetime(df['Start'])
df['End'] = pd.to_datetime(df['End'])
df['Trip Length (Days)'] = (df['End'] - df['Start']).dt.days + 1
df['Participants'] = df['Attendees'].apply(len)
df['Bubble Size'] = df['Trip Length (Days)'] * df['Participants']
df['Attendee List'] = df['Attendees'].apply(lambda x: ', '.join(x))

st.markdown("<h2 style='font-size: 20px;'>Timeline of Trips being Planned</h2>", unsafe_allow_html=True)

fig = px.scatter(
    df, x="Type", y="Start", size="Bubble Size", color="Trip", hover_name="Trip",
    custom_data=['Start', 'Attendee List'],
    size_max=55  # MODIFIED: Reduced max size to prevent overflow on mobile
)
fig.update_traces(
    hovertemplate='<b>%{hovertext}</b><br><br>Date: %{customdata[0]|%b %d, %Y}<br>Attendees: %{customdata[1]}<extra></extra>'
)
fig.update_yaxes(autorange="reversed")
fig.update_layout(
    xaxis_title="Intensity Tier", yaxis_title="Date", height=600,
    margin=dict(l=10, r=10, t=40, b=20), showlegend=False
)

# MODIFIED: Added 'staticPlot': True to disable all interactivity except hover
st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False, 'staticPlot': True})

st.divider()

st.header("Trip Details")
selected_trip_name = st.selectbox("Select a trip to see its details:", options=df['Trip'])

if selected_trip_name:
    trip = df[df['Trip'] == selected_trip_name].to_dict('records')[0]

    st.subheader("Attendees")
    if trip['Attendees']:
        for name in trip['Attendees']: st.markdown(f"- {name}")
    else:
        st.write("No one has signed up yet.")

    st.divider()

    st.subheader("Itinerary")
    if trip['Itinerary']:
        for item in trip['Itinerary']:
            with st.container(border=True):
                st.markdown(f"**Day {item['Day']} at {item['Time']}**")
                st.write(item['Activity'])
    else:
        st.write("No itinerary planned yet.")

    st.divider()

    st.subheader("Want to go?")
    if st.button("Request to Join This Trip"):
        st.success(f"Your request to join the '{selected_trip_name}' trip has been sent!")
        st.balloons()
