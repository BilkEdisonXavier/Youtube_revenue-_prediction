import streamlit as st
import pickle
import pandas as pd

# Load trained pipeline
with open("youtube_revenue_pipeline.pkl", "rb") as f:
    pipeline = pickle.load(f)

# Page config
st.set_page_config(
    page_title="YouTube Revenue Predictor",
    page_icon="📺",
    layout="wide"
)

# Sidebar
st.sidebar.image("https://www.gstatic.com/youtube/img/branding/youtubelogo/svg/youtubelogo.svg", use_container_width=True)
st.sidebar.header("🔧 Input Video Data")

# Sidebar inputs
views = st.sidebar.number_input("Views", min_value=0)
likes = st.sidebar.number_input("Likes", min_value=0)
comments = st.sidebar.number_input("Comments", min_value=0)
watch_time = st.sidebar.number_input("Watch Time (minutes)", min_value=0)
video_length = st.sidebar.number_input("Video Length (minutes)", min_value=0)
subscribers = st.sidebar.number_input("Subscribers", min_value=0)

category = st.sidebar.selectbox("Category", ['Education', 'Entertainment', 'Music', 'Gaming', 'Other'])
device = st.sidebar.selectbox("Device", ['Mobile', 'Desktop', 'Tablet', 'TV', 'Other'])
country = st.sidebar.selectbox("Country", ['India', 'USA', 'UK', 'Canada', 'Other'])

# Main content
st.title("📺 YouTube Revenue Predictor")
st.markdown("### Predict your video’s estimated revenue based on its engagement and metadata.")

col1, col2 = st.columns([2, 1])

with col1:
    st.video("https://youtu.be/YQ6ShcAU_dQ?si=E4I_bKQjqer39wsX")  # Example placeholder video
    st.markdown("#### Video Insights")
    st.write("Provide video details in the sidebar to estimate potential revenue.")

with col2:
    st.markdown("### 📊 Prediction Result")
    if st.sidebar.button("🎯 Predict Revenue"):
        # Prepare input
        input_data = pd.DataFrame({
            "views": [views],
            "likes": [likes],
            "comments": [comments],
            "watch_time_minutes": [watch_time],
            "video_length_minutes": [video_length],
            "subscribers": [subscribers],
            "category": [category],
            "device": [device],
            "country": [country]
        })

        # Pipeline handles preprocessing + prediction
        prediction = pipeline.predict(input_data)

        st.success(f"💰 Estimated Revenue: **${prediction[0]:.2f}**")
        st.metric("Views", f"{views:,}")
        st.metric("Likes", f"{likes:,}")
        st.metric("Watch Time", f"{watch_time:,} min")
