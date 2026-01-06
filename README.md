# ✈️ Flight Delay Domino Effect Dashboard

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-239120?style=for-the-badge&logo=plotly&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)

> **An interactive analytics dashboard exploring global flight delay patterns and their cascading economic impact.**

---

## 🎯 Project Overview

Flight delays cost the global aviation industry **billions of dollars annually** and affect millions of passengers. This dashboard analyzes **150,000+ flights** across **48 major airports** worldwide to uncover delay patterns, identify root causes, and simulate improvement scenarios.

### Key Questions Answered:
- 🌍 Which regions experience the most delays?
- ✈️ How do airlines compare in on-time performance?
- 🌧️ How do seasonal factors (monsoon, winter) impact delays?
- 🔄 How does one delay trigger a cascade of subsequent delays?
- 💰 What is the true economic cost of flight delays?
- 🔮 Can we predict which flights will be delayed?

---

## 🚀 Live Demo

🔗 **[View Dashboard](https://flight-delay-domino.streamlit.app)**

---

## 📊 Dashboard Features

### 🏠 Home
- Global KPI overview (flights, delay rate, costs)
- Interactive world map with airport delay rates
- Regional performance comparison

### 📊 Delay Patterns (with Drill Down)
- Airline performance ranking
- Airport delay comparison
- Time-based heatmaps (Hour × Day)
- **Drill down** into specific airlines/airports

### 🔥 Seasonality Analysis
- Month × Region delay heatmap
- Monsoon, winter, and holiday impact visualization
- Time period trends across seasons

### 📈 Pareto Analysis
- **80/20 Rule**: Which airlines/airports cause most delays?
- Cumulative impact visualization
- Actionable insights for targeted improvements

### 🌊 Ripple Effect (Domino Analysis)
- Delay cause breakdown (Carrier, Weather, NAS, Late Aircraft)
- Sankey diagram showing delay flow
- Late aircraft cascade analysis

### 💰 Impact Analysis
- Economic cost breakdown (Airline vs Passenger)
- Regional cost comparison
- Monthly cost trends

### 🔮 What-If Analysis
- **Scenario simulation** with interactive sliders
- Estimate impact of reducing specific delay types
- Cost savings calculator

### 🤖 Delay Predictor
- Machine Learning model (Random Forest)
- Confusion matrix and ROC curve
- Feature importance analysis
- **Predict delay risk** for any flight

### 📍 Case Studies
- 🇮🇳 **India**: Monsoon impact analysis
- 🇦🇪 **Gulf Region**: Hub performance and fog effects
- 🇺🇸 **North America**: Winter storms and holiday rush

---

## 📁 Dataset

| Attribute | Value |
|-----------|-------|
| **Total Flights** | 149,855 |
| **Airports** | 48 (Global hubs) |
| **Airlines** | 30 (Major carriers) |
| **Routes** | 2,112 |
| **Time Period** | January - December 2024 |
| **Regions** | North America, Europe, Middle East, Asia, India, Oceania |

### Key Metrics:
- **Delay Rate**: 29.4%
- **Average Delay**: 38 minutes
- **Total Economic Impact**: $256M+

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **Python** | Core programming language |
| **Streamlit** | Web dashboard framework |
| **Plotly** | Interactive visualizations |
| **Pandas** | Data manipulation |
| **NumPy** | Numerical operations |
| **Scikit-learn** | Machine learning model |

---

## 📂 Project Structure
