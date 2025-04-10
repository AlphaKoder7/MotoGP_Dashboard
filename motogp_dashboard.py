import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

data = pd.read_csv("RidersSummary.csv")  

st.set_page_config(layout="wide", page_title="MotoGP Rider Analysis")
st.title("🏍️ MotoGP Rider Career Analysis Dashboard")

st.sidebar.header("🏁 Select Rider and Analysis Type")

riders = sorted(data["rider_name"].unique())
selected_rider = st.sidebar.selectbox("Choose a Rider", riders)

rider_data = data[data["rider_name"] == selected_rider].sort_values(by="season")

analysis_type = st.sidebar.radio(
    "📊 Choose Analysis Type",
    ["Career Progression", "Season Comparison", "Class Performance", "Championship Analysis"]
)

col1, col2 = st.columns([2, 1])

with col1:
    if analysis_type == "Career Progression":
        st.header(f"{selected_rider}'s Career Progression")

        fig = px.line(rider_data, x="season", y="points", 
                     color="class", markers=True, 
                     title=f"Points Earned by Season",
                     labels={"points": "Championship Points", "season": "Season"})
        fig.update_layout(height=400, legend_title="Championship Class")
        st.plotly_chart(fig, use_container_width=True)

        cumulative_wins = rider_data["wins"].cumsum()
        cumulative_podiums = rider_data["podium"].cumsum()
        
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=rider_data["season"], y=cumulative_wins, 
                                 mode='lines+markers', name='Cumulative Wins'))
        fig2.add_trace(go.Scatter(x=rider_data["season"], y=cumulative_podiums, 
                                 mode='lines+markers', name='Cumulative Podiums'))
        fig2.update_layout(title="Career Achievements Over Time",
                          xaxis_title="Season", yaxis_title="Count",
                          height=400)
        st.plotly_chart(fig2, use_container_width=True)
        
    elif analysis_type == "Season Comparison":
        st.header(f"{selected_rider}'s Season Performance Comparison")

        metrics = ["wins", "podium", "pole", "fastest_lap", "points"]
        selected_metrics = st.multiselect("Select Metrics to Compare", metrics, default=["wins", "podium", "points"])
        
        if selected_metrics:
            fig = go.Figure()
            for metric in selected_metrics:
                fig.add_trace(go.Bar(
                    x=rider_data["season"],
                    y=rider_data[metric],
                    name=metric.replace("_", " ").title()
                ))
            fig.update_layout(title=f"Season Performance Metrics",
                             barmode='group', height=500,
                             xaxis_title="Season", yaxis_title="Count")
            st.plotly_chart(fig, use_container_width=True)
        
    elif analysis_type == "Class Performance":
        st.header(f"{selected_rider}'s Performance by Class")
 
        class_data = rider_data.groupby("class").agg({
            "races_participated": "sum",
            "wins": "sum",
            "podium": "sum",
            "pole": "sum",
            "fastest_lap": "sum",
            "points": "sum",
            "world_championships": "sum"
        }).reset_index()
        
        class_data["win_percentage"] = (class_data["wins"] / class_data["races_participated"] * 100).round(1)
        class_data["podium_percentage"] = (class_data["podium"] / class_data["races_participated"] * 100).round(1)
        
        fig = px.bar(class_data, x="class", y=["win_percentage", "podium_percentage"],
                    title="Success Rates by Championship Class",
                    labels={"value": "Percentage (%)", "variable": "Metric"})
        st.plotly_chart(fig, use_container_width=True)
        
        class_data["points_per_race"] = (class_data["points"] / class_data["races_participated"]).round(1)
        fig2 = px.bar(class_data, x="class", y="points_per_race",
                     title="Average Points per Race by Class",
                     color="class")
        st.plotly_chart(fig2, use_container_width=True)
        
    elif analysis_type == "Championship Analysis":
        st.header(f"{selected_rider}'s Championship Performance")
        
        championships = rider_data[rider_data["world_championships"] > 0]
        
        if len(championships) > 0:
            st.subheader("🏆 Championship Winning Seasons")
            for _, row in championships.iterrows():
                st.write(f"**{row['season']}** - {row['class']} with {row['team']} ({row['motorcycle']})")
                st.write(f"Performance: {row['wins']} wins, {row['podium']} podiums, {row['points']} points")
                st.write("---")
        else:
            st.info(f"{selected_rider} has not won a world championship in the data provided.")
        
        fig = px.line(rider_data, x="season", y="placed", 
                     color="class", markers=True,
                     title=f"Championship Finishing Position by Season",
                     labels={"placed": "Position", "season": "Season"})
        fig.update_yaxes(autorange="reversed")  
        st.plotly_chart(fig, use_container_width=True)

with col2:
    st.header(f"Rider Profile: {selected_rider}")
    
    latest_data = rider_data.iloc[-1]
    
    st.markdown(f"""
    ### 📋 Current Status
    - **Class:** {latest_data['class']}
    - **Team:** {latest_data['team']}
    - **Motorcycle:** {latest_data['motorcycle']}
    - **Country:** {latest_data['home_country']}
    - **Bike Number:** {latest_data['bike_number']}
    """)
    
    st.markdown("### 📊 Career Statistics")
    
    career_stats = {
        "Seasons": len(rider_data["season"].unique()),
        "Races": rider_data["races_participated"].sum(),
        "Wins": rider_data["wins"].sum(),
        "Podiums": rider_data["podium"].sum(),
        "Poles": rider_data["pole"].sum(),
        "Fastest Laps": rider_data["fastest_lap"].sum(),
        "World Championships": rider_data["world_championships"].sum()
    }
    
    if career_stats["Races"] > 0:
        win_rate = (career_stats["Wins"] / career_stats["Races"] * 100).round(1)
        podium_rate = (career_stats["Podiums"] / career_stats["Races"] * 100).round(1)
    else:
        win_rate = 0
        podium_rate = 0
    
    categories = ["Wins", "Podiums", "Poles", "Fastest Laps"]
    values = [career_stats["Wins"], career_stats["Podiums"], 
              career_stats["Poles"], career_stats["Fastest Laps"]]
    
    normalized_values = [(v / career_stats["Races"] * 100) for v in values]
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=normalized_values,
        theta=categories,
        fill='toself',
        name='Performance Metrics'
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max(normalized_values) * 1.2]
            )
        ),
        title="Performance Profile (% of Races)",
        height=350
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown(f"""
    ### 🏆 Success Metrics
    - **Win Rate:** {win_rate}%
    - **Podium Rate:** {podium_rate}%
    - **Championships:** {career_stats["World Championships"]}
    """)
    
    classes = rider_data["class"].unique()
    st.markdown(f"### 🏁 Classes: {', '.join(classes)}")
    
    teams = rider_data["team"].unique()
    manufacturers = rider_data["motorcycle"].unique()
    
    st.markdown(f"### 🏢 Teams: {len(teams)}")
    for team in teams:
        years = rider_data[rider_data["team"] == team]["season"].values
        st.write(f"- {team} ({min(years)}-{max(years)})")
    
    st.markdown(f"### 🏍️ Motorcycles: {len(manufacturers)}")
    for manufacturer in manufacturers:
        st.write(f"- {manufacturer}")