# trip_planner.py
import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
import requests
from io import BytesIO

# --- App Configuration ---
st.set_page_config(
    page_title="Our Trip Planner",
    page_icon="🗺️",
    layout="wide"
)

# --- Custom CSS for circular images ---
st.markdown("""
<style>
/* Style for the attendee images */
div[data-testid="stImage"] > img {
    border-radius: 50%;
}
</style>
""", unsafe_allow_html=True)


# --- Helper function to get image data ---
@st.cache_data
def get_image_data(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return BytesIO(response.content)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching image from {url}: {e}")
    return None


# --- Trip Data with Detailed Itineraries and Upgraded Avatars ---
TRIP_DATA = [
    {
        "Trip": "Colorado Backpacking", "Type": "Backpacking", "Start": "2025-07-25", "End": "2025-08-02",
        "Attendees": {
            "Dré": "https://api.dicebear.com/8.x/avataaars/png?seed=dre&top=noHair&facialHair=beardLight&facialHairColor=d64f2a&eyes=happy&mouth=smile&skinColor=ecad80",
            "Chanty": "https://api.dicebear.com/8.x/avataaars/png?seed=chanty&top=longHair&hairColor=2c1b18&eyes=happy&mouth=smile&skinColor=f2d3b1"
        },
        "Itinerary": [
            {'Day': 1, 'Time': '2:00 PM', 'Activity': 'Arrive at Denver International Airport (DEN).'},
            {'Day': 1, 'Time': '4:00 PM', 'Activity': 'Pick up rental vehicle and supplies.'},
            {'Day': 2, 'Time': '9:00 AM', 'Activity': 'Drive to Mount Blue Sky Trailhead.'},
            {'Day': 2, 'Time': '11:00 AM', 'Activity': 'Begin 5-mile hike to Summit Lake.'},
            {'Day': 3, 'Time': '6:00 AM', 'Activity': 'Summit attempt on Mount Blue Sky.'}
        ]
    },
    {
        "Trip": "Fishing at the Lake", "Type": "Relaxing", "Start": "2025-08-15", "End": "2025-08-17",
        "Attendees": {
             "Dré": "https://api.dicebear.com/8.x/avataaars/png?seed=dre&top=noHair&facialHair=beardLight&facialHairColor=d64f2a&eyes=happy&mouth=smile&skinColor=ecad80",
             "Tracy": "https://api.dicebear.com/8.x/avataaars/png?seed=tracy&top=longHair&hairColor=fde3a7&eyes=wink&mouth=grin&skinColor=ecad80"
        },
        "Itinerary": [
            {'Day': 'Friday', 'Time': '3:00 PM', 'Activity': 'Arrive at the lake and set up campsite.'},
            {'Day': 'Friday', 'Time': '5:00 PM', 'Activity': 'Evening fishing session from the shore.'},
            {'Day': 'Saturday', 'Time': '7:00 AM', 'Activity': 'Morning fishing in the boat.'},
            {'Day': 'Saturday', 'Time': '6:00 PM', 'Activity': 'Campfire and cookout.'}
        ]
    },
    {
        "Trip": "Skiing in Utah", "Type": "Active", "Start": "2026-01-20", "End": "2026-01-25",
        "Attendees": {
             "Chanty": "https://api.dicebear.com/8.x/avataaars/png?seed=chanty&top=longHair&hairColor=2c1b18&eyes=happy&mouth=smile&skinColor=f2d3b1",
             "Teresa": "https://api.dicebear.com/8.x/avataaars/png?seed=teresa&top=longHair&hairColor=d64f2a&eyes=squint&mouth=laughing&skinColor=ecad80"
        },
        "Itinerary": [
            {'Day': 1, 'Time': '12:00 PM', 'Activity': 'Land at Salt Lake City (SLC), grab gear.'},
            {'Day': 2, 'Time': '9:00 AM', 'Activity': 'Full day skiing at Alta Ski Area.'},
            {'Day': 3, 'Time': '9:00 AM', 'Activity': 'Full day skiing at Snowbird.'}
        ]
    }
]

# --- Main App ---
st.title("🗺️ Our Adventure Planner")
st.write("An overview of all the trips we have planned for the next year!")

df = pd.DataFrame(TRIP_DATA)
df['Start'] = pd.to_datetime(df['Start'])
df['End'] = pd.to_datetime(df['End'])
df['Trip Length (Days)'] = (df['End'] - df['Start']).dt.days
df['Participants'] = df['Attendees'].apply(len)
df['Bubble Size'] = df['Trip Length (Days)'] * df['Participants']

# --- Bubble Chart ---
fig = px.scatter(
    df, x="Start", y="Type", size="Bubble Size", color="Trip", hover_name="Trip",
    size_max=60, title="Trip Timeline"
)
fig.update_traces(marker={'opacity': 0.7})
fig.update_layout(xaxis_title="Date", yaxis_title="Trip Type")
st.plotly_chart(fig, use_container_width=True)

st.divider()

# --- Combined Trip Details Section ---
st.header("Trip Details")
selected_trip_name = st.selectbox("Select a trip to see its details:", options=df['Trip'])

if selected_trip_name:
    # Find the data for the selected trip
    trip = df[df['Trip'] == selected_trip_name].to_dict('records')[0]

    # --- Display Attendees ---
    st.subheader("Attendees")
    attendees = trip['Attendees']
    if attendees:
        cols = st.columns(len(attendees))
        for i, (name, image_url) in enumerate(attendees.items()):
            with cols[i]:
                image_data = get_image_data(image_url)
                if image_data:
                    st.image(image_data, caption=name, use_container_width=True)
                else:
                    st.error(f"Image not found for {name}")

    st.divider()

    # --- Display Detailed Itinerary ---
    st.subheader("Itinerary")
    itinerary_items = trip['Itinerary']
    if itinerary_items:
        # Group itinerary by day to display in expanders
        itinerary_df = pd.DataFrame(itinerary_items)
        for day, activities in itinerary_df.groupby('Day'):
            with st.expander(f"**Day {day}**"):
                for index, row in activities.iterrows():
                    st.markdown(f"**{row['Time']}**: {row['Activity']}")
    else:
        st.write("No itinerary planned yet.")
