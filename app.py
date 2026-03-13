import streamlit as st
import pandas as pd
import pickle
import numpy as np

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="IPL Win Predictor",
    layout="wide",
    page_icon="🏏"
)

# ---------------- PROFESSIONAL DARK THEME ----------------
dark_css = """
<style>
/* Main background */
.stApp {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: #e2e8f0;
}
/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #0f172a;
}
/* Titles */
h1 {
    color: #38bdf8 !important;
    text-align: center;
    font-weight: 700;
}
h2, h3 {
    color: #f1f5f9 !important;
}
/* Buttons */
button {
    background: linear-gradient(90deg, #3b82f6, #06b6d4) !important;
    color: white !important;
    border-radius: 12px !important;
    height: 45px !important;
    font-size: 16px !important;
    border: none !important;
}
/* Input boxes / select dropdown */
input, div[data-baseweb="select"] > div {
    background-color: #1e293b !important;
    color: white !important;
    border-radius: 8px !important;
}
div[data-baseweb="select"] span {
    color: white !important;
}
div[data-baseweb="select"] div[role="option"] {
    color: black !important;
}
p.subtitle {
    text-align: center;        /* center the text */
    color: #94a3b8;            /* light gray/blue for contrast */
    margin-top: -5px;           /* small top margin */
    margin-bottom: 20px;        /* space below subtitle */
    font-size: 20px;            /* slightly bigger for readability */
    font-weight: 500;           /* medium weight */
}

/* Metric Card */
div[data-testid="stMetric"] {
    background-color: #1e293b;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.4);
}
/* Projected Score Cards */
div.proj-card {
    border-radius: 20px;
    padding: 20px;
    margin: 10px 5px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.6);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    text-align: center;
}
div.proj-card:hover {
    transform: translateY(-5px) scale(1.05);
    box-shadow: 0 12px 30px rgba(0,0,0,0.7);
}

/* Divider */
hr {
    border: 1px solid #334155;
}
</style>
"""
st.markdown(dark_css, unsafe_allow_html=True)
# ---------------- LOAD MODEL ----------------
model = pickle.load(open("ipl_win_model.pkl", "rb"))
preprocessor = pickle.load(open("ipl_preprocessor.pkl", "rb"))

# ---------------- TITLE ----------------
st.markdown("<h1>🏏 IPL Win Predictor</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Predict Match Outcome & Projected Score</p>", unsafe_allow_html=True)
st.divider()

# ---------------- MATCH TYPE ----------------
match_type = st.radio(
    "📌 Select Match Situation",
    ["Batting First", "Batting Second"],
    horizontal=True
)
st.divider()

# ---------------- INPUTS ----------------
col1, col2 = st.columns([1,1])

teams = [
    "Chennai Super Kings",
    "Mumbai Indians",
    "Royal Challengers Bangalore",
    "Kolkata Knight Riders",
    "Rajasthan Royals",
    "Sunrisers Hyderabad",
    "Delhi Capitals",
    "Punjab Kings"
]

with col1:
    st.markdown("### 🏏 Batting Team & Score")
    batting_team = st.selectbox("Select Batting Team", teams, label_visibility="visible")
    current_score = st.number_input("Current Score", min_value=0, step=1, label_visibility="visible")
    overs_completed = st.slider("Overs Completed", 0.1, 20.0, step=0.1, label_visibility="visible")

with col2:
    st.markdown("### 🎯 Bowling Team & Wickets")
    # Ensure dropdown updates dynamically
    bowling_team = st.selectbox("Select Bowling Team", [t for t in teams if t != batting_team], label_visibility="visible")
    wickets_lost = st.slider("Wickets Lost", 0, 10, label_visibility="visible")

if match_type == "Batting Second":
    target = st.number_input("Target Score", min_value=1, step=1, label_visibility="visible")

balls_completed = int(overs_completed * 6)
balls_left = max(120 - balls_completed, 0)
wickets_left = 10 - wickets_lost
st.divider()

# ==========================================================
# 🟢 BATTING FIRST → PROJECTED SCORE (Professional Card Style)
# ==========================================================
# ==========================================================
if match_type == "Batting First":
    if st.button("📊 Calculate Projected Score", use_container_width=True):

        current_rr = current_score / overs_completed if overs_completed > 0 else 0
        balls_remaining = balls_left / 6  # convert balls to overs remaining

        # Dynamic projections: current RPO + 0, +2, +4, +6
        rpo_list = [current_rr, current_rr + 2, current_rr + 4, current_rr + 6]
        projections = [int(current_score + rpo * balls_remaining) for rpo in rpo_list]

        st.subheader("🏏 Projected Final Score (20 Overs)")

        proj_cols = st.columns(4)
        labels = ["Current RPO", "+2 RPO", "+4 RPO", "+6 RPO"]
        colors = [
            "linear-gradient(135deg,#3b82f6,#06b6d4)",
            "linear-gradient(135deg,#06b6d4,#14b8a6)",
            "linear-gradient(135deg,#14b8a6,#22c55e)",
            "linear-gradient(135deg,#22c55e,#84cc16)"
        ]  # gradient colors for cards

        for i, col in enumerate(proj_cols):
            col.markdown(f"""
            <div class='proj-card' style='background:{colors[i]}'>
                <h3 style='color:white;margin-bottom:5px;text-align:center;font-size:20px'>{labels[i]}</h3>
                <p style='font-size:40px;font-weight:800;color:white;text-align:center;margin:5px 0'>{projections[i]} runs</p>
                <p style='color:white;font-size:18px;text-align:center;margin:0'>{rpo_list[i]:.2f} rpo</p>
            </div>
            """, unsafe_allow_html=True)

# ==========================================================
# 🔵 BATTING SECOND → WIN PROBABILITY
# ==========================================================
elif match_type == "Batting Second":

    batsman_sr = 130.0
    bowler_eco = 8.0

    if overs_completed >= 19.0:
        st.subheader("Last Over Inputs")
        batsman_sr = st.number_input("Batsman Strike Rate", min_value=50.0, max_value=600.0, value=130.0)
        bowler_eco = st.number_input("Bowler Economy", min_value=3.0, max_value=36.0, value=8.0)

    if st.button("🔮 Predict Win Probability", use_container_width=True):

        runs_left = target - current_score

        if (overs_completed >= 20 or wickets_lost == 10) and current_score == target:
            st.warning("🤝 Match Ended in a DRAW")
        elif current_score > target:
            st.success(f"🏆 {batting_team} has WON the match!")
            st.balloons()
        elif (overs_completed >= 20 or wickets_lost == 10) and current_score < target:
            st.error(f"🎯 {bowling_team} has WON the match!")
        else:
            run_rate = current_score / overs_completed
            required_run_rate = (runs_left * 6 / max(balls_left, 1))

            input_df = pd.DataFrame([{
                "batting_team": batting_team,
                "bowling_team": bowling_team,
                "current_score": current_score,
                "runs_left": runs_left,
                "balls_left": balls_left,
                "wickets_left": wickets_left,
                "run_rate": run_rate,
                "required_run_rate": required_run_rate,
                "batsman_strike_rate": batsman_sr,
                "bowler_economy": bowler_eco
            }])

            X_input = preprocessor.transform(input_df)
            win_prob = model.predict_proba(X_input)[0][1] * 100

            st.metric("🏆 Batting Team Win Probability", f"{win_prob:.2f}%")

# ---------------- FOOTER ----------------
st.markdown(
    "<hr><p style='text-align:center;color:#64748b;font-size:12px;'>IPL Win Predictor • Machine Learning Project</p>",
    unsafe_allow_html=True
)
