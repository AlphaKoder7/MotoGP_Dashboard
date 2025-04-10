MotoGP Riders 2024 - Big Data Dashboard 🚴‍♂️🏍️
📄 Project Overview
This project is a Big Data Dashboard that visualizes MotoGP riders' performance data for the 2024 season.
It uses MongoDB to store the riders' data, Streamlit for building the interactive dashboard, and Python for data ingestion.

The dashboard provides an easy and beautiful way to explore, filter, and analyze MotoGP riders' statistics in real-time.

🛠️ Tech Stack
Python 🐍

Streamlit (Dashboard Web App)

Pandas (Data Handling)

MongoDB (Database)

pymongo (MongoDB Connector)

CSV (Initial Data Source)

📂 Project Structure
graphql
Copy
Edit
├── data_import.py           # Script to import RidersSummary.csv into MongoDB
├── dashboard_app.py         # Streamlit app file (your dashboard code)
├── RidersSummary.csv        # CSV file containing riders' performance data
├── requirements.txt         # (Optional) List of dependencies
└── README.md                # Project documentation

📥 Setup Instructions
1. Clone the repository
git clone https://github.com/your-username/motogp-riders-dashboard.git
cd motogp-riders-dashboard

2. Install required libraries
You can install all dependencies in one go:

pip install pandas pymongo streamlit

(Also make sure you have MongoDB installed and running locally.)

3. Import the data into MongoDB
Before running the dashboard, insert the data into MongoDB:
python data_import.py

✅ This will import the data from RidersSummary.csv into the motogp_db database and riders_data collection.

4. Run the Streamlit Dashboard
Start the Streamlit server:

streamlit run motogp_dashboard.py
This will open the dashboard in your default browser at http://localhost:8501.

🛒 Data Source
The data in RidersSummary.csv includes:

Rider ID

Rider Name

Team

Nationality

Points

Bike Number

Number of Wins, Podiums, Poles, Fastest Laps

Other performance metrics

📈 Dashboard Features
Display and filter riders based on teams, nationality, points, etc.

Visualizations of riders’ performance.

Search and dynamic data updates based on MongoDB backend.

Clean and responsive UI with Streamlit.

🤝 Contributing
Pull requests, issues, and feature improvements are welcome!
Feel free to check the issues page.

🏁 Let's race into the world of MotoGP Data! 🏁