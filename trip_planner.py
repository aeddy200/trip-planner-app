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
        "TripAbbreviation": "GoG/Pikes",
        "Type": "Casual Hiking",
        "Start": "2025-09-05", "End": "2025-09-07",
        "Attendees": ["Dré", "Chanty", "Tracy", "Teresa"],
        "Miles": 15,
        "Itinerary": [
            {'Day': 1, 'Time': '12:00 PM', 'Activity': 'Arrive at Colorado Springs Airport (COS), pick up rental car.'},
            {'Day': 1, 'Time': '2:00 PM', 'Activity': 'Check into hotel and have a late lunch.'},
            {'Day': 1, 'Time': '4:00 PM', 'Activity': 'Easy walk through Garden of the Gods (Perkins Central Garden Trail).'},
            {'Day': 2, 'Time': '9:00 AM', 'Activity': 'Drive up the Pikes Peak Highway, stopping at viewpoints.'},
            {'Day': 2, 'Time': '12:00 PM', 'Activity': 'Lunch and acclimatization at the Summit Visitor Center.'},
            {'Day': 3, 'Time': '10:00 AM', 'Activity': 'Visit the Manitou Cliff Dwellings.'},
            {'Day': 3, 'Time': '1:00 PM', 'Activity': 'Depart from Colorado Springs Airport (COS).'}
        ]
    },
    {
        "Trip": "Yellowstone NP - Grand Prismatic",
        "TripAbbreviation": "Yellowstone",
        "Type": "Beginner Backpacking",
        "Start": "2026-06-12", "End": "2026-06-15",
        "Attendees": ["Dré", "Chanty", "Tracy", "Teresa"],
        "Miles": 20,
        "Itinerary": [
            {'Day': 1, 'Time': '10:00 AM', 'Activity': 'Arrive at Bozeman Yellowstone Int\'l (BZN), drive to West Yellowstone.'},
            {'Day': 1, 'Time': '2:00 PM', 'Activity': 'Pick up backcountry permits and bear canisters from ranger station.'},
            {'Day': 1, 'Time': '4:00 PM', 'Activity': 'Hike 3 miles to the first campsite near Fairy Falls.'},
            {'Day': 2, 'Time': '9:00 AM', 'Activity': 'Day hike to the Grand Prismatic Spring Overlook.'},
            {'Day': 2, 'Time': '1:00 PM', 'Activity': 'Explore Midway and Upper Geyser Basins (Old Faithful).'},
            {'Day': 3, 'Time': '10:00 AM', 'Activity': 'Hike 5 miles along the Firehole River to the next site.'},
            {'Day': 4, 'Time': '9:00 AM', 'Activity': 'Hike out and drive back to Bozeman for departure.'}
        ]
    },
    {
        "Trip": "Teton Crest Trail - Paintbrush Canyon",
        "TripAbbreviation": "Tetons",
        "Type": "Experienced Backpacking",
        "Start": "2026-08-20", "End": "2026-08-24",
        "Attendees": ["Dré", "Chanty", "Tracy", "Teresa"],
        "Miles": 35,
        "Itinerary": [
            {'Day': 1, 'Time': '9:00 AM', 'Activity': 'Arrive at Jackson Hole Airport (JAC), shuttle to Jenny Lake.'},
            {'Day': 1, 'Time': '11:00 AM', 'Activity': 'Start at String Lake Trailhead, hike to Holly Lake campsite.'},
            {'Day': 2, 'Time': '7:00 AM', 'Activity': 'Climb over Paintbrush Divide and camp at Lake Solitude.'},
            {'Day': 3, 'Time': '8:00 AM', 'Activity': 'Hike through the North Fork Cascade Canyon.'},
            {'Day': 4, 'Time': '9:00 AM', 'Activity': 'Continue through Cascade Canyon, past Inspiration Point.'},
            {'Day': 5, 'Time': '8:00 AM', 'Activity': 'Hike out via Jenny Lake and shuttle back to Jackson.'},
            {'Day': 5, 'Time': '2:00 PM', 'Activity': 'Depart from Jackson Hole Airport (JAC).'}
        ]
    }
]

# --- Main App Logic ---
st.markdown("<h1 style='font-size: 24px;'>🗺️ Our Adventure Planner</h1>", unsafe_allow_html=True)

# --- NEW: Photo Gallery ---
st.write("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.image("https://images.pexels.com/photos/1586252/pexels-photo-1586252.jpeg", caption="Garden of the Gods")
with col2:
    st.image("https://images.pexels.com/photos/414160/pexels-photo-414160.jpeg", caption="Yellowstone")
with col3:
    st.image("https://images.pexels.com/photos/1770809/pexels-photo-1770809.jpeg", caption="Grand Tetons")
st.write("---")


df = pd.DataFrame(TRIP_DATA)
df['Start'] = pd.to_datetime(df['Start'])
df['End'] = pd.to_datetime(df['End'])
df['Trip Length (Days)'] = (df['End'] - df['Start']).dt.days + 1
df['Participants'] = df['Attendees'].apply(len)
# MODIFIED: Updated Bubble Text to include trip abbreviation
df['Bubble Text'] = df.apply(
    lambda row: f"<b>{row['TripAbbreviation']}</b><br>{row['Participants']} People<br>{row['Trip Length (Days)']} Days<br>{row['Miles']} Miles",
    axis=1
)

abbreviation_map = {"Casual Hiking": "Casual", "Beginner Backpacking": "Beginner", "Experienced Backpacking": "Experienced"}
df['Type Abbreviated'] = df['Type'].map(abbreviation_map)

st.markdown("<h2 style='font-size: 20px;'>Timeline of Trips being Planned</h2>", unsafe_allow_html=True)

fig = px.scatter(
    df, x="Type Abbreviated", y="Start", color="Trip", text="Bubble Text",
    hover_name="Trip", custom_data=['Type']
)

# --- Chart Formatting ---
fig.update_traces(
    marker=dict(size=100), # Slightly larger bubble for more text
    textposition='middle center',
    textfont=dict(color='black', size=11), # Slightly smaller font to fit
    hovertemplate='<b>%{hovertext}</b><br>Type: %{customdata[0]}<extra></extra>'
)

fig.update_yaxes(autorange="reversed")
fig.update_xaxes(tickfont=dict(size=12))
fig.update_layout(
    xaxis_title="Trip Type", yaxis_title="Date", height=600,
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
        itinerary_df = pd.DataFrame(trip['Itinerary'])
        for day, activities in itinerary_df.groupby('Day'):
            with st.expander(f"**Day {day}**"):
                for index, row in activities.iterrows():
                    st.markdown(f"**{row['Time']}**: {row['Activity']}")
    else:
        st.write("No itinerary planned yet.")

    st.divider()

    st.subheader("Want to go?")
    if st.button("Request to Join This Trip"):
        st.success(f"Your request to join the '{selected_trip_name}' trip has been sent!")
        st.balloons()
