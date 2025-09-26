# Youtube_revenue-_prediction

📺 YouTube Revenue Predictor:
A machine learning web app built with Streamlit that predicts estimated YouTube video revenue based on engagement metrics and metadata such as views, likes, comments, watch time, subscribers, category, device, and country.

🚀 Features:

1)Upload or input YouTube video details.

2)Predict estimated revenue using a trained ML pipeline (youtube_revenue_pipeline.pkl).

3)Interactive Streamlit dashboard for user-friendly inputs.

4)Real-time predictions with clear metrics visualization.

📂 Project Structure:
.
├── youtube_revenue.ipynb      # Jupyter Notebook for model training & evaluation
├── youtube_dash.py            # Streamlit app for revenue prediction
├── youtube_revenue_pipeline.pkl # Saved ML pipeline (preprocessing + model)
└── README.md                  # Project documentation

▶️ Usage

1)Train the model or use the pre-trained pipeline provided.

2)Run the Streamlit app:

3)Open the app in your browser (default: http://localhost:8501).

4)Enter video details in the sidebar and click Predict Revenue.

📊 Example

Input:

  -Views: 50,000
  
  -Likes: 2,000
  
  -Comments: 300
  
  -Watch Time: 120,000 minutes
  
  -Subscribers: 10,000
  
  -Category: Education
  
  -Device: Mobile
  
  -Country: India

Output:
    💰 Estimated Revenue: $125.50 (example)

🛠️ Tech Stack:

1)Python

2)Scikit-learn (ML model training + pipeline)

3)Streamlit (Web app interface)

4)Pandas (Data handling)

📌 Future Improvements

1)Integrate YouTube API to fetch real video data.

2)Add visualizations for revenue vs. engagement.

3)Deploy the app to Streamlit Cloud or Heroku.


