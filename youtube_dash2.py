import streamlit as st
import pickle
import pandas as pd
from googleapiclient.discovery import build
import re
import isodate

# ===============================
# Load trained pipeline
# ===============================
with open("youtube_revenue_pipeline.pkl", "rb") as f:
    pipeline = pickle.load(f)

# ===============================
# YouTube API setup
# ===============================
API_KEY = "AIzaSyC_k8aZDrjDacU-LysyJ1JILiI6QkOZ8sc"  # replace with your API key
youtube = build("youtube", "v3", developerKey=API_KEY)

# ===============================
# Helper functions
# ===============================
def extract_video_id(url: str):
    """Extract video ID from YouTube URL."""
    pattern = r"(?:v=|youtu\.be/)([0-9A-Za-z_-]{11})"
    match = re.search(pattern, url)
    return match.group(1) if match else None


def get_video_stats(video_id: str):
    """Fetch video details using YouTube Data API."""
    request = youtube.videos().list(
        part="snippet,statistics,contentDetails",
        id=video_id
    )
    response = request.execute()

    if "items" not in response or len(response["items"]) == 0:
        return None

    video = response["items"][0]
    stats = video["statistics"]
    snippet = video["snippet"]
    content = video["contentDetails"]

    # Duration (ISO 8601 → minutes)
    duration = isodate.parse_duration(content["duration"]).total_seconds() / 60

    data = {
        "title": snippet["title"],
        "category": snippet.get("categoryId", "Other"),
        "views": int(stats.get("viewCount", 0)),
        "likes": int(stats.get("likeCount", 0)),
        "comments": int(stats.get("commentCount", 0)),
        "video_length_minutes": round(duration, 2),
        "channel_id": snippet["channelId"]
    }
    return data


def get_channel_subscribers(channel_id: str):
    """Fetch subscriber count for a given channel."""
    request = youtube.channels().list(
        part="statistics",
        id=channel_id
    )
    response = request.execute()
    if "items" in response and len(response["items"]) > 0:
        return int(response["items"][0]["statistics"].get("subscriberCount", 0))
    return 0

# ===============================
# Streamlit App
# ===============================
st.set_page_config(page_title="YouTube Revenue Predictor", page_icon="📺", layout="wide")
st.title("📺 YouTube Revenue Predictor")
st.markdown("Paste a YouTube link and get estimated revenue instantly.")

# User input
youtube_url = st.text_input("🔗 Enter YouTube Video URL")
device = st.selectbox("Device", ['Mobile', 'Desktop', 'Tablet', 'TV', 'Other'])
country = st.selectbox("Country", ['India', 'USA', 'UK', 'Canada', 'Other'])

# Predict button
if st.button("🎯 Predict Revenue"):
    video_id = extract_video_id(youtube_url)
    if not video_id:
        st.error("❌ Invalid YouTube URL.")
    else:
        video_data = get_video_stats(video_id)
        if not video_data:
            st.error("❌ Could not fetch video data. Check API key or video availability.")
        else:
            # Fetch subscribers automatically
            subscribers = get_channel_subscribers(video_data["channel_id"])

            # Estimate watch time (approx: 30% of video length watched per view)
            avg_view_duration = video_data["video_length_minutes"] * 0.3
            watch_time = video_data["views"] * avg_view_duration

            # Prepare input DataFrame
            input_data = pd.DataFrame({
                "views": [video_data["views"]],
                "likes": [video_data["likes"]],
                "comments": [video_data["comments"]],
                "watch_time_minutes": [watch_time],
                "video_length_minutes": [video_data["video_length_minutes"]],
                "subscribers": [subscribers],
                "category": [video_data["category"]],
                "device": [device],
                "country": [country]
            })

            # Predict revenue
            prediction = pipeline.predict(input_data)

            # Show results
            st.video(youtube_url)
            st.subheader(video_data["title"])
            st.success(f"💰 Estimated Revenue: **${prediction[0]:.2f}**")

            # Metrics
            st.metric("Subscribers", f"{subscribers:,}")
            st.metric("Views", f"{video_data['views']:,}")
            st.metric("Likes", f"{video_data['likes']:,}")
            st.metric("Comments", f"{video_data['comments']:,}")
            st.metric("Duration", f"{video_data['video_length_minutes']} min")
            st.metric("Watch Time", f"{watch_time:,.0f} min")
