# trip_planner.py
import streamlit as st
import pandas as pd
import plotly.express as px
import datetime

# --- App Configuration & Data ---
st.set_page_config(page_title="Our Trip Planner", page_icon="🗺️", layout="wide")
TRIP_DATA = [
    {
        "Trip": "Garden of the Gods & Pikes Peak",
        "Type": "Casual Hiking",
        "Start": "2025-09-05", "End": "2025-09-07",
        "Attendees": ["Dré", "Chanty", "Tracy", "Teresa"],
        "Miles": 15,
        "Itinerary": [
            {'Day': 1, 'Time': '12:00 PM', 'Activity': 'Arrive in Colorado Springs, check into lodging.'},
            {'Day': 1, 'Time': '3:00 PM', 'Activity': 'Explore Garden of the Gods Park (Perkins Central Garden Trail).'},
            {'Day': 2, 'Time': '9:00 AM', 'Activity': 'Drive up the Pikes Peak Highway, stopping at viewpoints.'},
            {'Day': 2, 'Time': '12:00 PM', 'Activity': 'Lunch at the Summit Visitor Center.'},
            {'Day': 3, 'Time': '10:00 AM', 'Activity': 'Visit the Manitou Cliff Dwellings before departing.'}
        ]
    },
    {
        "Trip": "Yellowstone NP - Grand Prismatic",
        "Type": "Beginner Backpacking",
        "Start": "2026-06-12", "End": "2026-06-15",
        "Attendees": ["Dré", "Chanty", "Tracy", "Teresa"],
        "Miles": 20,
        "Itinerary": [
            {'Day': 1, 'Time': '10:00 AM', 'Activity': 'Arrive at West Yellowstone, pick up backcountry permits.'},
            {'Day': 1, 'Time': '2:00 PM', 'Activity': 'Hike 3 miles to the first campsite near Fairy Falls.'},
            {'Day': 2, 'Time': '9:00 AM', 'Activity': 'Day hike to the Grand Prismatic Spring Overlook.'},
            {'Day': 2, 'Time': '1:00 PM', 'Activity': 'Explore Midway and Upper Geyser Basins (Old Faithful).'},
            {'Day': 3, 'Time': '10:00 AM', 'Activity': 'Hike 5 miles along the Firehole River to the next site.'},
            {'Day': 4, 'Time': '9:00 AM', 'Activity': 'Hike out and return to West Yellowstone.'}
        ]
    },
    {
        "Trip": "Teton Crest Trail - Paintbrush Canyon",
        "Type": "Experienced Backpacking", # Renamed Category
        "Start": "2026-08-20", "End": "2026-08-24",
        "Attendees": ["Dré", "Chanty", "Tracy", "Teresa"],
        "Miles": 35,
        "Itinerary": [
            {'Day': 1, 'Time': '8:00 AM', 'Activity': 'Start at String Lake Trailhead, hike to Holly Lake.'},
            {'Day': 2, 'Time': '7:00 AM', 'Activity': 'Climb over Paintbrush Divide and camp at Lake Solitude.'},
            {'Day': 3, 'Time': '8:00 AM', 'Activity': 'Hike through the North Fork Cascade Canyon.'},
            {'Day': 4, 'Time': '9:00 AM', 'Activity': 'Continue through Cascade Canyon, past Inspiration Point.'},
            {'Day': 5, 'Time': '8:00 AM', 'Activity': 'Hike out via Jenny Lake and finish the trail.'}
        ]
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

fig.update_yaxes(autorange="reversed")
# MODIFIED: Adjustments for x-axis label formatting
fig.update_xaxes(
    # Move the category labels down slightly
    tickfont=dict(size=10),
    # Shift the entire axis to the left
    range=[-0.5, 2.5]
)
fig.update_layout(
    xaxis_title="Intensity Tier", yaxis_title="Date", height=600,
    margin=dict(l=10, r=10, t=40, b=20), showlegend=False,
    plot_bgcolor='rgba(0,0,0,0)',
    # Set x-axis tick labels to be horizontal and wrap if needed
    xaxis_tickangle=0
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
