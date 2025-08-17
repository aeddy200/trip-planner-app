# trip-planner.py
import streamlit as st
import pandas as pd
import plotly.express as px
import datetime

# --- App Configuration & Data ---
st.set_page_config(page_title="Our Trip Planner", page_icon="🗺️", layout="wide")
TRIP_DATA = [
    {
        "Trip": "Mount Falcon Loop", "Type": "Casual Hiking",
        "Start": "2025-09-05", "End": "2025-09-07",
        "Attendees": ["Dré", "Chanty", "Tracy", "Teresa"],
        "Miles": 10,
        "Itinerary": [{'Day': 1, 'Time': '9:00 AM', 'Activity': 'Meet at the west trailhead parking lot.'}]
    },
    {
        "Trip": "Lost Creek Wilderness Intro", "Type": "Beginner Backpacking",
        "Start": "2026-01-15", "End": "2026-01-18",
        "Attendees": ["Dré", "Chanty", "Tracy", "Teresa"],
        "Miles": 15,
        "Itinerary": [{'Day': 1, 'Time': '10:00 AM', 'Activity': 'Meet at the trailhead, check gear.'}]
    },
    {
        "Trip": "Four Pass Loop", "Type": "Intensive Backpacking",
        "Start": "2026-07-18", "End": "2026-07-22",
        "Attendees": ["Dré", "Chanty", "Tracy", "Teresa"],
        "Miles": 27,
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
df['Bubble Text'] = df.apply(lambda row: f"<b>{row['Participants']} People<br>{row['Trip Length (Days)']} Days<br>{row['Miles']} Miles</b>", axis=1)

st.markdown("<h2 style='font-size: 20px;'>Timeline of Trips being Planned</h2>", unsafe_allow_html=True)

fig = px.scatter(
    df, x="Type", y="Start", color="Trip", text="Bubble Text",
    hover_name="Trip"
)

# --- Chart Formatting ---
fig.update_traces(
    marker=dict(size=85),
    textposition='middle center',
    textfont=dict(color='black', size=12)
)

# MODIFIED: Corrected the function name from update_y_axes to update_yaxes
fig.update_yaxes(autorange="reversed")
fig.update_layout(
    xaxis_title="Intensity Tier", yaxis_title="Date", height=600,
    margin=dict(l=10, r=10, t=40, b=20), showlegend=False,
    plot_bgcolor='rgba(0,0,0,0)'
)

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
