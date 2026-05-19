# 🏏 IPL Win Predictor & Projected Score Estimator

A Machine Learning-based web application that predicts:

- 🏆 Winning probability of IPL teams during live matches  
- 📊 Projected final score for batting-first innings  

Built using **Python, Streamlit, Scikit-Learn, Pandas, and NumPy**.

---

# 📌 Problem Statement

Cricket fans and analysts often want real-time answers like:

- Which team has a higher chance of winning during a live IPL match?
- What could be the final score while batting first?

This project solves that using Machine Learning models trained on historical IPL match data.

---

# 🎯 Objectives

- Predict match winning probability in real time  
- Estimate projected final score (1st innings)  
- Provide an interactive and user-friendly UI using Streamlit  
- Demonstrate practical use of Machine Learning in sports analytics  

---

# 🧠 Machine Learning Algorithm Used

- Logistic Regression Classification Model  
- Scikit-Learn Pipeline for preprocessing  
- Feature engineering for match state analysis  

---

# 📊 Features Used in Model

The model considers the following match conditions:

- Batting team  
- Bowling team  
- Current score  
- Runs left  
- Balls left  
- Wickets left  
- Current run rate  
- Required run rate  
- Batsman strike rate  
- Bowler economy  

---

# 🛠️ Technologies Used

- Python 🐍  
- Streamlit ⚡  
- Pandas 📊  
- NumPy 🔢  
- Scikit-Learn 🤖  
- Pickle 🧠  

---

# 📂 Project Structure

```text
├── app.py
├── ipl_pred.ipynb
├── ipl_win_model.pkl
├── ipl_preprocessor.pkl
├── requirements.txt
├── screenshots/
├── dataset/

---

# 🚀 How to Run the Project

### 1️⃣ Install dependencies
```bash
pip install -r requirements.txt
streamlit run app.py