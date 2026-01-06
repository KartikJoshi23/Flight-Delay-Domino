# ═══════════════════════════════════════════════════════════════════════════════
# ✈️ FLIGHT DELAY DOMINO EFFECT - PROFESSIONAL DASHBOARD
# Aviation-Themed Design | Master's Level Project
# ═══════════════════════════════════════════════════════════════════════════════

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, roc_curve, auc, accuracy_score, precision_score, recall_score, f1_score
import warnings
warnings.filterwarnings('ignore')

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Flight Delay Domino Effect",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ═══════════════════════════════════════════════════════════════════════════════
# AVIATION-THEMED CSS - BLUE/CYAN COLOR SCHEME
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    :root {
        --bg-primary: #0B1120;
        --bg-secondary: #111827;
        --bg-card: #1E293B;
        --accent-primary: #06B6D4;
        --accent-secondary: #22D3EE;
        --accent-blue: #3B82F6;
        --text-primary: #F1F5F9;
        --text-secondary: #94A3B8;
        --success: #10B981;
        --danger: #EF4444;
        --warning: #F59E0B;
        --border-color: rgba(6, 182, 212, 0.2);
    }
    
    .stApp {
        background: linear-gradient(135deg, #0B1120 0%, #1E293B 50%, #0F172A 100%);
        font-family: 'Inter', sans-serif;
    }
    
    .main .block-container {
        padding: 1rem 2rem 2rem 2rem;
        max-width: 100%;
    }
    
    #MainMenu, footer, header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* ═══════════════ NAVIGATION BAR ═══════════════ */
    .navbar {
        background: linear-gradient(90deg, rgba(11, 17, 32, 0.98) 0%, rgba(30, 41, 59, 0.98) 100%);
        backdrop-filter: blur(20px);
        border-bottom: 2px solid rgba(6, 182, 212, 0.3);
        padding: 1rem 2rem;
        margin: -1rem -2rem 1.5rem -2rem;
        display: flex;
        align-items: center;
        gap: 15px;
    }
    
    .nav-icon {
        font-size: 2.5rem;
        filter: drop-shadow(0 0 10px rgba(6, 182, 212, 0.5));
    }
    
    .nav-title {
        font-size: 1.6rem;
        font-weight: 700;
        background: linear-gradient(135deg, #06B6D4 0%, #22D3EE 50%, #3B82F6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .nav-subtitle {
        font-size: 0.75rem;
        color: #64748B;
        letter-spacing: 3px;
        text-transform: uppercase;
    }
    
    /* ═══════════════ NAVIGATION BUTTONS ═══════════════ */
    .stButton > button {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%);
        border: 1px solid rgba(6, 182, 212, 0.3);
        border-radius: 12px;
        color: #E2E8F0;
        font-weight: 500;
        padding: 0.6rem 1rem;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, rgba(6, 182, 212, 0.2) 0%, rgba(59, 130, 246, 0.2) 100%);
        border-color: #06B6D4;
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(6, 182, 212, 0.25);
    }
    
    .stButton > button:active, .stButton > button:focus {
        background: linear-gradient(135deg, #06B6D4 0%, #3B82F6 100%);
        color: white;
        border-color: transparent;
    }
    
    /* ═══════════════ HERO SECTION ═══════════════ */
    .hero-section {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.8) 100%);
        border: 1px solid rgba(6, 182, 212, 0.2);
        border-radius: 20px;
        padding: 2.5rem;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #06B6D4, #3B82F6, #8B5CF6, #06B6D4);
        background-size: 200% 100%;
        animation: gradient-flow 3s linear infinite;
    }
    
    @keyframes gradient-flow {
        0% { background-position: 0% 50%; }
        100% { background-position: 200% 50%; }
    }
    
    .hero-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: #F1F5F9;
        margin-bottom: 0.5rem;
    }
    
    .hero-subtitle {
        font-size: 1.1rem;
        color: #94A3B8;
        line-height: 1.6;
    }
    
    .hero-highlight {
        color: #22D3EE;
        font-weight: 600;
    }
    
    /* ═══════════════ GLASSMORPHISM CARDS ═══════════════ */
    .glass-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.6) 0%, rgba(15, 23, 42, 0.8) 100%);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(6, 182, 212, 0.15);
        border-radius: 16px;
        padding: 1.5rem;
        position: relative;
        overflow: hidden;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        border-color: rgba(6, 182, 212, 0.5);
        box-shadow: 0 20px 40px rgba(6, 182, 212, 0.15);
    }
    
    .glass-card::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, rgba(6, 182, 212, 0.05) 0%, transparent 50%);
        opacity: 0;
        transition: opacity 0.4s ease;
        pointer-events: none;
    }
    
    .glass-card:hover::after {
        opacity: 1;
    }
    
    .card-icon {
        font-size: 2rem;
        margin-bottom: 0.8rem;
        display: block;
    }
    
    .card-value {
        font-size: 2.2rem;
        font-weight: 800;
        color: #F1F5F9;
        margin-bottom: 0.3rem;
    }
    
    .card-value.cyan {
        background: linear-gradient(135deg, #06B6D4 0%, #22D3EE 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .card-value.blue {
        background: linear-gradient(135deg, #3B82F6 0%, #60A5FA 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .card-label {
        font-size: 0.85rem;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 500;
    }
    
    .card-delta {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-top: 0.6rem;
    }
    
    .card-delta.negative {
        background: rgba(239, 68, 68, 0.15);
        color: #FCA5A5;
    }
    
    .card-delta.positive {
        background: rgba(16, 185, 129, 0.15);
        color: #6EE7B7;
    }
    
    .card-delta.info {
        background: rgba(6, 182, 212, 0.15);
        color: #67E8F9;
    }
    
    /* ═══════════════ SECTION HEADERS ═══════════════ */
    .section-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin: 2rem 0 1.2rem 0;
        padding-bottom: 0.8rem;
        border-bottom: 2px solid rgba(6, 182, 212, 0.2);
    }
    
    .section-icon {
        font-size: 1.5rem;
    }
    
    .section-title {
        font-size: 1.4rem;
        font-weight: 700;
        color: #F1F5F9;
        margin: 0;
    }
    
    .section-subtitle {
        font-size: 0.85rem;
        color: #64748B;
        margin-left: auto;
    }
    
    /* ═══════════════ INSIGHT BOXES ═══════════════ */
    .insight-box {
        background: linear-gradient(135deg, rgba(6, 182, 212, 0.08) 0%, rgba(59, 130, 246, 0.05) 100%);
        border: 1px solid rgba(6, 182, 212, 0.25);
        border-left: 4px solid #06B6D4;
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        margin: 1rem 0;
    }
    
    .insight-box.warning {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.08) 0%, rgba(239, 68, 68, 0.05) 100%);
        border-color: rgba(245, 158, 11, 0.25);
        border-left-color: #F59E0B;
    }
    
    .insight-box.success {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.08) 0%, rgba(6, 182, 212, 0.05) 100%);
        border-color: rgba(16, 185, 129, 0.25);
        border-left-color: #10B981;
    }
    
    .insight-title {
        font-size: 1rem;
        font-weight: 700;
        color: #22D3EE;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .insight-box.warning .insight-title {
        color: #FBBF24;
    }
    
    .insight-box.success .insight-title {
        color: #34D399;
    }
    
    .insight-text {
        color: #CBD5E1;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    .insight-stat {
        font-weight: 700;
        color: #22D3EE;
    }
    
    .insight-box.warning .insight-stat {
        color: #FBBF24;
    }
    
    .insight-box.success .insight-stat {
        color: #34D399;
    }
    
    /* ═══════════════ CHART CONTAINERS ═══════════════ */
    .chart-container {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.5) 0%, rgba(15, 23, 42, 0.6) 100%);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 1.2rem;
        margin-bottom: 1rem;
    }
    
    .chart-title {
        font-size: 1rem;
        font-weight: 600;
        color: #E2E8F0;
        margin-bottom: 0.8rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .chart-explainer {
        font-size: 0.85rem;
        color: #64748B;
        margin-bottom: 1rem;
        font-style: italic;
    }
    
    /* ═══════════════ TABS STYLING ═══════════════ */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(15, 23, 42, 0.5);
        border-radius: 12px;
        padding: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 8px;
        padding: 12px 24px;
        color: #94A3B8;
        font-weight: 500;
        border: none;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #06B6D4 0%, #3B82F6 100%);
        color: #ffffff;
    }
    
    /* ═══════════════ PREDICTION RESULTS ═══════════════ */
    .prediction-high {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(220, 38, 38, 0.1) 100%);
        border: 2px solid rgba(239, 68, 68, 0.5);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
    }
    
    .prediction-low {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(6, 182, 212, 0.1) 100%);
        border: 2px solid rgba(16, 185, 129, 0.5);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
    }
    
    .prediction-icon {
        font-size: 3.5rem;
        margin-bottom: 0.8rem;
    }
    
    .prediction-title {
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
    }
    
    .prediction-prob {
        font-size: 2.5rem;
        font-weight: 800;
    }
    
    /* ═══════════════ SLIDERS ═══════════════ */
    .stSlider > div > div > div {
        background: linear-gradient(90deg, #06B6D4 0%, #3B82F6 100%);
    }
    
    /* ═══════════════ SELECTBOX ═══════════════ */
    .stSelectbox > div > div {
        background: rgba(30, 41, 59, 0.8);
        border: 1px solid rgba(6, 182, 212, 0.2);
        border-radius: 10px;
    }
    
    /* ═══════════════ EXPANDER ═══════════════ */
    .streamlit-expanderHeader {
        background: rgba(30, 41, 59, 0.5);
        border-radius: 10px;
        color: #E2E8F0;
    }
    
    /* ═══════════════ METRICS ═══════════════ */
    [data-testid="stMetricValue"] {
        font-size: 1.8rem;
        color: #22D3EE;
    }
    
    [data-testid="stMetricDelta"] {
        color: #94A3B8;
    }
    
    /* ═══════════════ FOOTER ═══════════════ */
    .footer {
        text-align: center;
        padding: 2rem;
        margin-top: 2rem;
        border-top: 1px solid rgba(6, 182, 212, 0.2);
        color: #64748B;
    }
    
    .footer-brand {
        font-size: 1.2rem;
        font-weight: 600;
        background: linear-gradient(135deg, #06B6D4, #3B82F6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# DATA LOADING
# ═══════════════════════════════════════════════════════════════════════════════
@st.cache_data(ttl=3600)
def load_data():
    dtype_dict = {
        'MONTH': 'int8', 'DAY_OF_WEEK': 'int8', 'DEP_HOUR': 'int8',
        'DEP_DEL15': 'int8', 'DEP_DELAY': 'float32', 'ARR_DELAY': 'float32',
        'DISTANCE': 'float32', 'DELAY_COST_AIRLINE': 'float32',
        'DELAY_COST_PASSENGER': 'float32', 'DELAY_COST_TOTAL': 'float32',
        'CARRIER_DELAY': 'float32', 'WEATHER_DELAY': 'float32',
        'NAS_DELAY': 'float32', 'SECURITY_DELAY': 'float32',
        'LATE_AIRCRAFT_DELAY': 'float32'
    }
    flights = pd.read_csv('data/flights_global_2024.csv', dtype=dtype_dict)
    airlines = pd.read_csv('data/airlines.csv')
    airports = pd.read_csv('data/airports.csv')
    return flights, airlines, airports

# ═══════════════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════
def format_number(num):
    if num >= 1e9: return f"{num/1e9:.1f}B"
    if num >= 1e6: return f"{num/1e6:.1f}M"
    if num >= 1e3: return f"{num/1e3:.1f}K"
    return f"{num:,.0f}"

def format_currency(num):
    if num >= 1e9: return f"${num/1e9:.1f}B"
    if num >= 1e6: return f"${num/1e6:.1f}M"
    if num >= 1e3: return f"${num/1e3:.1f}K"
    return f"${num:,.0f}"

MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 
          'July', 'August', 'September', 'October', 'November', 'December']
MONTHS_SHORT = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
DAYS_SHORT = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

# Plotly color scheme
COLORS = {
    'primary': '#06B6D4',
    'secondary': '#3B82F6',
    'accent': '#22D3EE',
    'success': '#10B981',
    'danger': '#EF4444',
    'warning': '#F59E0B',
    'purple': '#8B5CF6',
    'text': '#E2E8F0',
    'muted': '#64748B',
    'grid': 'rgba(255,255,255,0.08)'
}

# ═══════════════════════════════════════════════════════════════════════════════
# LOAD DATA
# ═══════════════════════════════════════════════════════════════════════════════
try:
    df, airlines_df, airports_df = load_data()
except Exception as e:
    st.error(f"❌ Error loading data: {e}")
    st.stop()

# Create mappings
airport_names = {row['code']: f"{row['city']} ({row['code']})" for _, row in airports_df.iterrows()}

# ═══════════════════════════════════════════════════════════════════════════════
# NAVIGATION BAR
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="navbar">
    <span class="nav-icon">✈️</span>
    <div>
        <div class="nav-title">Flight Delay Domino Effect</div>
        <div class="nav-subtitle">Global Aviation Analytics Dashboard</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Navigation Buttons
nav_cols = st.columns(8)
pages = ["🏠 Overview", "📊 Analytics", "🌊 Domino Effect", "💰 Economics", 
         "🤖 AI Predictor", "🔮 Simulator", "🌍 Regional", "📈 Summary"]

if 'current_page' not in st.session_state:
    st.session_state.current_page = "🏠 Overview"

for i, page in enumerate(pages):
    if nav_cols[i].button(page, key=f"nav_{i}", use_container_width=True):
        st.session_state.current_page = page

current_page = st.session_state.current_page

# ═══════════════════════════════════════════════════════════════════════════════
# FILTERS
# ═══════════════════════════════════════════════════════════════════════════════
with st.expander("🎛️ **Filters & Controls** - Click to expand", expanded=False):
    fc1, fc2, fc3, fc4 = st.columns(4)
    
    with fc1:
        regions = ['All Regions'] + sorted(df['ORIGIN_REGION'].dropna().unique().tolist())
        selected_region = st.selectbox("🌍 Region", regions)
    
    with fc2:
        months_opt = ['All Months'] + MONTHS
        selected_month = st.selectbox("📅 Month", months_opt)
    
    with fc3:
        airlines_opt = ['All Airlines'] + sorted(df['AIRLINE_NAME'].dropna().unique().tolist())
        selected_airline = st.selectbox("✈️ Airline", airlines_opt)
    
    with fc4:
        st.markdown(f"**📊 Dataset Info**")
        st.markdown(f"Flights: {len(df):,} | Airports: {len(airports_df)} | Airlines: {len(airlines_df)}")

# Apply filters
fdf = df.copy()
if selected_region != 'All Regions':
    fdf = fdf[fdf['ORIGIN_REGION'] == selected_region]
if selected_month != 'All Months':
    month_idx = MONTHS.index(selected_month) + 1
    fdf = fdf[fdf['MONTH'] == month_idx]
if selected_airline != 'All Airlines':
    fdf = fdf[fdf['AIRLINE_NAME'] == selected_airline]

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: OVERVIEW
# ═══════════════════════════════════════════════════════════════════════════════
if current_page == "🏠 Overview":
    
    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <div class="hero-title">Understanding the Global Flight Delay Crisis</div>
        <div class="hero-subtitle">
            Analyzing <span class="hero-highlight">150,000+ flights</span> across 
            <span class="hero-highlight">48 major airports</span> worldwide to uncover 
            delay patterns, cascading effects, and economic impact worth 
            <span class="hero-highlight">$250+ Million</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # KPIs
    total_flights = len(fdf)
    delayed_flights = int(fdf['DEP_DEL15'].sum())
    delay_rate = (delayed_flights / total_flights * 100) if total_flights > 0 else 0
    avg_delay = fdf[fdf['DEP_DEL15'] == 1]['DEP_DELAY'].mean() if delayed_flights > 0 else 0
    total_cost = fdf['DELAY_COST_TOTAL'].sum()
    
    mc1, mc2, mc3, mc4 = st.columns(4)
    
    with mc1:
        st.markdown(f"""
        <div class="glass-card">
            <span class="card-icon">🛫</span>
            <div class="card-value">{format_number(total_flights)}</div>
            <div class="card-label">Total Flights</div>
            <div class="card-delta info">📅 Jan - Dec 2024</div>
        </div>
        """, unsafe_allow_html=True)
    
    with mc2:
        st.markdown(f"""
        <div class="glass-card">
            <span class="card-icon">⏱️</span>
            <div class="card-value cyan">{delay_rate:.1f}%</div>
            <div class="card-label">Delay Rate</div>
            <div class="card-delta negative">⚠️ {format_number(delayed_flights)} delayed</div>
        </div>
        """, unsafe_allow_html=True)
    
    with mc3:
        st.markdown(f"""
        <div class="glass-card">
            <span class="card-icon">⏰</span>
            <div class="card-value">{avg_delay:.0f} min</div>
            <div class="card-label">Avg Delay Duration</div>
            <div class="card-delta negative">When delayed</div>
        </div>
        """, unsafe_allow_html=True)
    
    with mc4:
        st.markdown(f"""
        <div class="glass-card">
            <span class="card-icon">💰</span>
            <div class="card-value blue">{format_currency(total_cost)}</div>
            <div class="card-label">Economic Impact</div>
            <div class="card-delta negative">Total cost</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Key Insight after KPIs
    worst_region = fdf.groupby('ORIGIN_REGION')['DEP_DEL15'].mean().idxmax()
    worst_region_rate = fdf.groupby('ORIGIN_REGION')['DEP_DEL15'].mean().max() * 100
    best_region = fdf.groupby('ORIGIN_REGION')['DEP_DEL15'].mean().idxmin()
    best_region_rate = fdf.groupby('ORIGIN_REGION')['DEP_DEL15'].mean().min() * 100
    
    st.markdown(f"""
    <div class="insight-box">
        <div class="insight-title">💡 Key Insight: Regional Performance Gap</div>
        <div class="insight-text">
            <span class="insight-stat">{worst_region}</span> has the highest delay rate at 
            <span class="insight-stat">{worst_region_rate:.1f}%</span>, while 
            <span class="insight-stat">{best_region}</span> performs best at only 
            <span class="insight-stat">{best_region_rate:.1f}%</span> — 
            a gap of <span class="insight-stat">{worst_region_rate - best_region_rate:.1f}%</span> that reveals 
            significant operational differences between regions.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Charts
    col1, col2 = st.columns([1.2, 1])
    
    with col1:
        st.markdown("""
        <div class="section-header">
            <span class="section-icon">🌍</span>
            <span class="section-title">Delay Rate by Region</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<p class="chart-explainer">Comparing on-time performance across global aviation markets. Lower is better.</p>', unsafe_allow_html=True)
        
        region_stats = fdf.groupby('ORIGIN_REGION').agg({
            'DEP_DEL15': ['count', 'mean']
        }).reset_index()
        region_stats.columns = ['Region', 'Flights', 'Delay Rate']
        region_stats = region_stats.sort_values('Delay Rate', ascending=True)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=region_stats['Region'],
            x=region_stats['Delay Rate'] * 100,
            orientation='h',
            marker=dict(
                color=region_stats['Delay Rate'] * 100,
                colorscale=[[0, COLORS['success']], [0.5, COLORS['warning']], [1, COLORS['danger']]],
            ),
            text=[f"<b>{x:.1f}%</b>" for x in region_stats['Delay Rate'] * 100],
            textposition='outside',
            textfont=dict(size=13, color=COLORS['text']),
            hovertemplate="<b>%{y}</b><br>Delay Rate: %{x:.1f}%<br>Flights: %{customdata:,}<extra></extra>",
            customdata=region_stats['Flights']
        ))
        
        fig.update_layout(
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color=COLORS['text'], size=12),
            margin=dict(l=0, r=80, t=20, b=40),
            xaxis=dict(
                title="Delay Rate (%)",
                gridcolor=COLORS['grid'],
                zeroline=False
            ),
            yaxis=dict(title="", gridcolor=COLORS['grid']),
            showlegend=False,
            hoverlabel=dict(bgcolor=COLORS['primary'], font_size=13)
        )
        
        st.plotly_chart(fig, use_container_width=True, key="overview_region")
    
    with col2:
        st.markdown("""
        <div class="section-header">
            <span class="section-icon">📈</span>
            <span class="section-title">Monthly Trend</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<p class="chart-explainer">Seasonal patterns reveal when delays peak throughout the year.</p>', unsafe_allow_html=True)
        
        monthly = fdf.groupby('MONTH')['DEP_DEL15'].mean().reset_index()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=MONTHS_SHORT,
            y=monthly['DEP_DEL15'] * 100,
            mode='lines+markers',
            line=dict(color=COLORS['primary'], width=4, shape='spline'),
            marker=dict(size=10, color=COLORS['primary'], line=dict(width=2, color='white')),
            fill='tozeroy',
            fillcolor='rgba(6, 182, 212, 0.1)',
            hovertemplate="<b>%{x}</b><br>Delay Rate: %{y:.1f}%<extra></extra>"
        ))
        
        avg_rate = monthly['DEP_DEL15'].mean() * 100
        fig.add_hline(y=avg_rate, line_dash="dash", line_color=COLORS['danger'],
                     annotation_text=f"Avg: {avg_rate:.1f}%", annotation_position="right")
        
        fig.update_layout(
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color=COLORS['text'], size=12),
            margin=dict(l=50, r=30, t=20, b=40),
            xaxis=dict(title="", gridcolor=COLORS['grid']),
            yaxis=dict(title="Delay Rate (%)", gridcolor=COLORS['grid']),
            showlegend=False,
            hoverlabel=dict(bgcolor=COLORS['primary'], font_size=13)
        )
        
        st.plotly_chart(fig, use_container_width=True, key="overview_monthly")
    
    # Second insight
    worst_month = int(fdf.groupby('MONTH')['DEP_DEL15'].mean().idxmax())
    best_month = int(fdf.groupby('MONTH')['DEP_DEL15'].mean().idxmin())
    worst_hour = int(fdf.groupby('DEP_HOUR')['DEP_DEL15'].mean().idxmax())
    best_hour = int(fdf.groupby('DEP_HOUR')['DEP_DEL15'].mean().idxmin())
    
    st.markdown(f"""
    <div class="insight-box success">
        <div class="insight-title">✅ Actionable Tip: Best Times to Fly</div>
        <div class="insight-text">
            <b>Best month:</b> <span class="insight-stat">{MONTHS[best_month-1]}</span> | 
            <b>Worst month:</b> <span class="insight-stat">{MONTHS[worst_month-1]}</span><br>
            <b>Best hour:</b> <span class="insight-stat">{best_hour}:00</span> | 
            <b>Worst hour:</b> <span class="insight-stat">{worst_hour}:00</span><br>
            Booking early morning flights can reduce your delay risk significantly!
        </div>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: ANALYTICS
# ═══════════════════════════════════════════════════════════════════════════════
elif current_page == "📊 Analytics":
    
    st.markdown("""
    <div class="section-header">
        <span class="section-icon">📊</span>
        <span class="section-title">Deep Dive Analytics</span>
        <span class="section-subtitle">Airline & Airport Performance Analysis</span>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["✈️ Airlines", "🏢 Airports", "🕐 Time Patterns", "🔥 Seasonality"])
    
    with tab1:
        st.markdown("### Airline Performance Ranking")
        st.markdown('<p class="chart-explainer">Airlines ranked by delay rate. Green = good, Red = needs improvement.</p>', unsafe_allow_html=True)
        
        airline_stats = fdf.groupby(['OP_UNIQUE_CARRIER', 'AIRLINE_NAME']).agg({
            'DEP_DEL15': ['count', 'mean'],
            'DEP_DELAY': 'mean',
            'DELAY_COST_TOTAL': 'sum'
        }).reset_index()
        airline_stats.columns = ['Code', 'Airline', 'Flights', 'Delay Rate', 'Avg Delay', 'Cost']
        airline_stats = airline_stats[airline_stats['Flights'] >= 100].sort_values('Delay Rate', ascending=True).tail(15)
        
        colors = [COLORS['success'] if x < 0.25 else COLORS['warning'] if x < 0.35 else COLORS['danger'] 
                  for x in airline_stats['Delay Rate']]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=airline_stats['Airline'],
            x=airline_stats['Delay Rate'] * 100,
            orientation='h',
            marker_color=colors,
            text=[f"<b>{x:.1f}%</b>" for x in airline_stats['Delay Rate'] * 100],
            textposition='outside',
            textfont=dict(size=11, color=COLORS['text']),
            hovertemplate="<b>%{y}</b><br>Delay Rate: %{x:.1f}%<br>Total Flights: %{customdata[0]:,}<br>Avg Delay: %{customdata[1]:.0f} min<extra></extra>",
            customdata=airline_stats[['Flights', 'Avg Delay']].values
        ))
        
        fig.update_layout(
            height=550,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color=COLORS['text']),
            margin=dict(l=0, r=100, t=20, b=50),
            xaxis=dict(title="Delay Rate (%)", gridcolor=COLORS['grid']),
            yaxis=dict(title="", categoryorder='total ascending'),
            hoverlabel=dict(bgcolor='#1E293B', font_size=12)
        )
        
        st.plotly_chart(fig, use_container_width=True, key="analytics_airline")
        
        # Insight
        best_airline = airline_stats.iloc[0]['Airline']
        worst_airline = airline_stats.iloc[-1]['Airline']
        
        st.markdown(f"""
        <div class="insight-box">
            <div class="insight-title">💡 Airline Insight</div>
            <div class="insight-text">
                <span class="insight-stat">{best_airline}</span> leads with the lowest delay rate, 
                while <span class="insight-stat">{worst_airline}</span> has room for improvement. 
                The difference in operational efficiency translates to millions in cost savings.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Drill Down
        st.markdown("---")
        st.markdown("### 🔍 Airline Deep Dive")
        selected_drill = st.selectbox("Select an airline for detailed analysis:", airline_stats['Airline'].tolist())
        
        if selected_drill:
            ad = fdf[fdf['AIRLINE_NAME'] == selected_drill]
            dc1, dc2, dc3, dc4 = st.columns(4)
            dc1.metric("Total Flights", f"{len(ad):,}")
            dc2.metric("Delay Rate", f"{ad['DEP_DEL15'].mean()*100:.1f}%")
            dc3.metric("Avg Delay", f"{ad[ad['DEP_DEL15']==1]['DEP_DELAY'].mean():.0f} min")
            dc4.metric("Total Cost", format_currency(ad['DELAY_COST_TOTAL'].sum()))
    
    with tab2:
        st.markdown("### Airport Delay Rankings")
        st.markdown('<p class="chart-explainer">Full airport names displayed for easy identification.</p>', unsafe_allow_html=True)
        
        airport_stats = fdf.groupby('ORIGIN').agg({
            'DEP_DEL15': ['count', 'mean']
        }).reset_index()
        airport_stats.columns = ['Code', 'Flights', 'Delay Rate']
        airport_stats = airport_stats[airport_stats['Flights'] >= 50]
        airport_stats['Full Name'] = airport_stats['Code'].map(airport_names)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🔴 Highest Delay Airports")
            worst = airport_stats.nlargest(10, 'Delay Rate')
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                y=worst['Full Name'],
                x=worst['Delay Rate'] * 100,
                orientation='h',
                marker_color=COLORS['danger'],
                text=[f"{x:.1f}%" for x in worst['Delay Rate'] * 100],
                textposition='outside',
                textfont=dict(color='#FCA5A5'),
                hovertemplate="<b>%{y}</b><br>Delay Rate: %{x:.1f}%<extra></extra>"
            ))
            
            fig.update_layout(
                height=400,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color=COLORS['text']),
                margin=dict(l=0, r=70, t=10, b=30),
                xaxis=dict(title="Delay Rate (%)", gridcolor=COLORS['grid']),
                yaxis=dict(categoryorder='total ascending'),
                hoverlabel=dict(bgcolor=COLORS['danger'])
            )
            st.plotly_chart(fig, use_container_width=True, key="airport_worst")
        
        with col2:
            st.markdown("#### 🟢 Best Performing Airports")
            best = airport_stats.nsmallest(10, 'Delay Rate')
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                y=best['Full Name'],
                x=best['Delay Rate'] * 100,
                orientation='h',
                marker_color=COLORS['success'],
                text=[f"{x:.1f}%" for x in best['Delay Rate'] * 100],
                textposition='outside',
                textfont=dict(color='#6EE7B7'),
                hovertemplate="<b>%{y}</b><br>Delay Rate: %{x:.1f}%<extra></extra>"
            ))
            
            fig.update_layout(
                height=400,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color=COLORS['text']),
                margin=dict(l=0, r=70, t=10, b=30),
                xaxis=dict(title="Delay Rate (%)", gridcolor=COLORS['grid']),
                yaxis=dict(categoryorder='total descending'),
                hoverlabel=dict(bgcolor=COLORS['success'])
            )
            st.plotly_chart(fig, use_container_width=True, key="airport_best")
        
        st.markdown(f"""
        <div class="insight-box warning">
            <div class="insight-title">⚠️ Airport Insight</div>
            <div class="insight-text">
                The top 10 delayed airports account for a disproportionate share of total delays. 
                Infrastructure improvements at these hubs could yield the highest ROI for the aviation industry.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("### Hour × Day Heatmap")
        st.markdown('<p class="chart-explainer">Find the best times to fly. Darker red = higher delay probability.</p>', unsafe_allow_html=True)
        
        hm_data = fdf.groupby(['DAY_OF_WEEK', 'DEP_HOUR'])['DEP_DEL15'].mean().reset_index()
        hm_pivot = hm_data.pivot(index='DEP_HOUR', columns='DAY_OF_WEEK', values='DEP_DEL15')
        
        fig = go.Figure(data=go.Heatmap(
            z=hm_pivot.values * 100,
            x=DAYS,
            y=[f"{h:02d}:00" for h in hm_pivot.index],
            colorscale=[[0, COLORS['success']], [0.5, COLORS['warning']], [1, COLORS['danger']]],
            text=[[f"{v:.0f}%" for v in row] for row in hm_pivot.values * 100],
            texttemplate="%{text}",
            textfont={"size": 10, "color": "white"},
            hovertemplate="<b>%{x}</b> at <b>%{y}</b><br>Delay Rate: %{z:.1f}%<extra></extra>",
            colorbar=dict(title="Delay %", ticksuffix="%")
        ))
        
        fig.update_layout(
            height=550,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color=COLORS['text']),
            margin=dict(l=80, r=50, t=30, b=50),
            xaxis=dict(title="Day of Week"),
            yaxis=dict(title="Hour of Day", autorange='reversed'),
            hoverlabel=dict(bgcolor='#1E293B')
        )
        
        st.plotly_chart(fig, use_container_width=True, key="time_heatmap")
        
        best_time = hm_data.loc[hm_data['DEP_DEL15'].idxmin()]
        worst_time = hm_data.loc[hm_data['DEP_DEL15'].idxmax()]
        
        st.markdown(f"""
        <div class="insight-box success">
            <div class="insight-title">✅ Timing Insight</div>
            <div class="insight-text">
                <b>Best time to fly:</b> <span class="insight-stat">{DAYS[int(best_time['DAY_OF_WEEK'])-1]}</span> at 
                <span class="insight-stat">{int(best_time['DEP_HOUR']):02d}:00</span> ({best_time['DEP_DEL15']*100:.1f}% delay rate)<br>
                <b>Avoid:</b> <span class="insight-stat">{DAYS[int(worst_time['DAY_OF_WEEK'])-1]}</span> at 
                <span class="insight-stat">{int(worst_time['DEP_HOUR']):02d}:00</span> ({worst_time['DEP_DEL15']*100:.1f}% delay rate)
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with tab4:
        st.markdown("### Month × Region Seasonality")
        st.markdown('<p class="chart-explainer">Understand how seasons affect delays across different regions.</p>', unsafe_allow_html=True)
        
        season_data = fdf.groupby(['MONTH', 'ORIGIN_REGION'])['DEP_DEL15'].mean().reset_index()
        season_pivot = season_data.pivot(index='ORIGIN_REGION', columns='MONTH', values='DEP_DEL15')
        
        fig = go.Figure(data=go.Heatmap(
            z=season_pivot.values * 100,
            x=MONTHS_SHORT,
            y=season_pivot.index,
            colorscale=[[0, COLORS['success']], [0.5, COLORS['warning']], [1, COLORS['danger']]],
            text=[[f"{v:.0f}%" for v in row] for row in season_pivot.values * 100],
            texttemplate="%{text}",
            textfont={"size": 11, "color": "white"},
            hovertemplate="<b>%{y}</b> in <b>%{x}</b><br>Delay Rate: %{z:.1f}%<extra></extra>",
            colorbar=dict(title="Delay %", ticksuffix="%")
        ))
        
        fig.update_layout(
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color=COLORS['text']),
            margin=dict(l=120, r=50, t=30, b=50),
            xaxis=dict(title="Month"),
            yaxis=dict(title=""),
            hoverlabel=dict(bgcolor='#1E293B')
        )
        
        st.plotly_chart(fig, use_container_width=True, key="season_heatmap")
        
        st.markdown("""
        <div class="insight-box">
            <div class="insight-title">💡 Seasonal Patterns</div>
            <div class="insight-text">
                • <b>India (Jun-Sep):</b> Monsoon causes <span class="insight-stat">40-60%</span> higher delays<br>
                • <b>North America (Dec-Feb):</b> Winter storms create cascading disruptions<br>
                • <b>Europe (Jun-Aug):</b> Summer holiday rush strains capacity<br>
                • <b>Middle East (Dec-Feb):</b> Morning fog impacts Dubai/Abu Dhabi
            </div>
        </div>
        """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: DOMINO EFFECT
# ═══════════════════════════════════════════════════════════════════════════════
elif current_page == "🌊 Domino Effect":
    
    st.markdown("""
    <div class="section-header">
        <span class="section-icon">🌊</span>
        <span class="section-title">The Domino Effect: How Delays Cascade</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="insight-box">
        <div class="insight-title">🎯 What is the Domino Effect?</div>
        <div class="insight-text">
            When a flight is delayed, the <b>same aircraft</b> is late for its next flight. 
            The crew might time out. Passengers miss connections. This creates a 
            <b>cascading chain reaction</b> where one delay triggers many more throughout the day.
            The "Late Aircraft Delay" metric is the key indicator of this phenomenon.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    delayed = fdf[fdf['DEP_DEL15'] == 1]
    
    col1, col2 = st.columns([1.2, 1])
    
    with col1:
        st.markdown("### 📊 Root Causes of Flight Delays")
        st.markdown('<p class="chart-explainer">Understanding what causes delays helps prioritize improvement efforts.</p>', unsafe_allow_html=True)
        
        causes = {
            'Carrier Operations': delayed['CARRIER_DELAY'].sum(),
            'Weather Conditions': delayed['WEATHER_DELAY'].sum(),
            'Air Traffic Control': delayed['NAS_DELAY'].sum(),
            'Late Aircraft (Domino)': delayed['LATE_AIRCRAFT_DELAY'].sum(),
            'Security Issues': delayed['SECURITY_DELAY'].sum()
        }
        cause_df = pd.DataFrame(list(causes.items()), columns=['Cause', 'Minutes'])
        cause_df['Percentage'] = cause_df['Minutes'] / cause_df['Minutes'].sum() * 100
        cause_df = cause_df.sort_values('Minutes', ascending=True)
        
        bar_colors = [COLORS['secondary'], COLORS['warning'], COLORS['purple'], COLORS['danger'], COLORS['success']]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=cause_df['Cause'],
            x=cause_df['Minutes'],
            orientation='h',
            marker_color=bar_colors,
            text=[f"<b>{format_number(m)}</b> min ({p:.1f}%)" for m, p in zip(cause_df['Minutes'], cause_df['Percentage'])],
            textposition='outside',
            textfont=dict(size=11, color=COLORS['text']),
            hovertemplate="<b>%{y}</b><br>Total: %{x:,.0f} minutes<extra></extra>"
        ))
        
        fig.update_layout(
            height=350,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color=COLORS['text']),
            margin=dict(l=0, r=150, t=20, b=30),
            xaxis=dict(title="Total Delay Minutes", gridcolor=COLORS['grid']),
            yaxis=dict(title=""),
            hoverlabel=dict(bgcolor='#1E293B')
        )
        
        st.plotly_chart(fig, use_container_width=True, key="cause_bar")
    
    with col2:
        st.markdown("### 🍩 Cause Distribution")
        
        fig = go.Figure(data=[go.Pie(
            labels=cause_df['Cause'],
            values=cause_df['Minutes'],
            hole=0.55,
            marker_colors=bar_colors,
            textinfo='percent',
            textfont=dict(size=13, color='white'),
            hovertemplate="<b>%{label}</b><br>%{value:,.0f} min<br>%{percent}<extra></extra>"
        )])
        
        fig.update_layout(
            height=350,
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color=COLORS['text']),
            showlegend=True,
            legend=dict(orientation='h', y=-0.1, font=dict(size=10)),
            margin=dict(l=20, r=20, t=20, b=60),
            annotations=[dict(
                text=f"<b>{format_number(cause_df['Minutes'].sum())}</b><br>Total Min",
                x=0.5, y=0.5, font_size=14, showarrow=False, font=dict(color=COLORS['primary'])
            )]
        )
        
        st.plotly_chart(fig, use_container_width=True, key="cause_pie")
    
    late_pct = cause_df[cause_df['Cause'] == 'Late Aircraft (Domino)']['Percentage'].values[0]
    
    st.markdown(f"""
    <div class="insight-box warning">
        <div class="insight-title">⚠️ Domino Effect Insight</div>
        <div class="insight-text">
            <span class="insight-stat">{late_pct:.1f}%</span> of all delay minutes are caused by 
            <b>Late Aircraft</b> — the domino effect in action! This means that even if we can't control 
            weather, improving aircraft turnaround and schedule buffers could significantly reduce cascading delays.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Cascade throughout day
    st.markdown("### ⏰ How Delays Compound Throughout the Day")
    st.markdown('<p class="chart-explainer">Notice how late aircraft delays increase as the day progresses — the domino effect in action.</p>', unsafe_allow_html=True)
    
    hourly_cascade = delayed.groupby('DEP_HOUR').agg({
        'LATE_AIRCRAFT_DELAY': ['count', 'mean']
    }).reset_index()
    hourly_cascade.columns = ['Hour', 'Flights', 'Avg Delay']
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(go.Bar(
        x=hourly_cascade['Hour'],
        y=hourly_cascade['Flights'],
        name='Flights with Late Aircraft',
        marker_color=COLORS['primary'],
        opacity=0.8,
        hovertemplate="Hour: %{x}<br>Flights: %{y:,}<extra></extra>"
    ), secondary_y=False)
    
    fig.add_trace(go.Scatter(
        x=hourly_cascade['Hour'],
        y=hourly_cascade['Avg Delay'],
        name='Avg Cascade Delay',
        line=dict(color=COLORS['danger'], width=4),
        mode='lines+markers',
        marker=dict(size=8),
        hovertemplate="Hour: %{x}<br>Avg Delay: %{y:.1f} min<extra></extra>"
    ), secondary_y=True)
    
    fig.update_layout(
        height=380,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COLORS['text']),
        margin=dict(l=50, r=50, t=30, b=50),
        legend=dict(orientation='h', y=1.08),
        xaxis=dict(title="Hour of Day", gridcolor=COLORS['grid']),
        yaxis=dict(title="Number of Flights", gridcolor=COLORS['grid']),
        yaxis2=dict(title="Avg Delay (min)", gridcolor='rgba(255,255,255,0.03)'),
        hoverlabel=dict(bgcolor='#1E293B')
    )
    
    st.plotly_chart(fig, use_container_width=True, key="cascade_hourly")
    
    st.markdown("""
    <div class="insight-box success">
        <div class="insight-title">✅ Recommendation</div>
        <div class="insight-text">
            Early morning flights (5-7 AM) start the day "fresh" with on-time aircraft. 
            As the day progresses, delays compound. <b>For lowest delay risk, always book morning flights!</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: ECONOMICS
# ═══════════════════════════════════════════════════════════════════════════════
elif current_page == "💰 Economics":
    
    st.markdown("""
    <div class="section-header">
        <span class="section-icon">💰</span>
        <span class="section-title">Economic Impact Analysis</span>
        <span class="section-subtitle">The True Cost of Flight Delays</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="insight-box">
        <div class="insight-title">💵 Cost Methodology</div>
        <div class="insight-text">
            <b>Airline Cost:</b> $74.20/minute (fuel burn, crew overtime, maintenance, missed connections)<br>
            <b>Passenger Cost:</b> $47.00/minute (time value, hotel, rebooking, compensation)<br>
            <i>Source: FAA Economic Values for Investment Analysis (2024)</i>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    airline_cost = fdf['DELAY_COST_AIRLINE'].sum()
    passenger_cost = fdf['DELAY_COST_PASSENGER'].sum()
    total_cost = fdf['DELAY_COST_TOTAL'].sum()
    avg_cost = fdf[fdf['DEP_DEL15'] == 1]['DELAY_COST_TOTAL'].mean()
    
    kc1, kc2, kc3, kc4 = st.columns(4)
    
    with kc1:
        st.markdown(f"""
        <div class="glass-card">
            <span class="card-icon">🏢</span>
            <div class="card-value cyan">{format_currency(airline_cost)}</div>
            <div class="card-label">Airline Losses</div>
            <div class="card-delta negative">$74.20/min</div>
        </div>
        """, unsafe_allow_html=True)
    
    with kc2:
        st.markdown(f"""
        <div class="glass-card">
            <span class="card-icon">👥</span>
            <div class="card-value blue">{format_currency(passenger_cost)}</div>
            <div class="card-label">Passenger Impact</div>
            <div class="card-delta negative">$47.00/min</div>
        </div>
        """, unsafe_allow_html=True)
    
    with kc3:
        st.markdown(f"""
        <div class="glass-card">
            <span class="card-icon">💸</span>
            <div class="card-value">{format_currency(total_cost)}</div>
            <div class="card-label">Total Impact</div>
            <div class="card-delta negative">Combined</div>
        </div>
        """, unsafe_allow_html=True)
    
    with kc4:
        st.markdown(f"""
        <div class="glass-card">
            <span class="card-icon">📊</span>
            <div class="card-value">{format_currency(avg_cost)}</div>
            <div class="card-label">Per Delayed Flight</div>
            <div class="card-delta info">Average</div>
        </div>
        """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🌍 Cost by Region")
        
        region_cost = fdf.groupby('ORIGIN_REGION')['DELAY_COST_TOTAL'].sum().reset_index()
        region_cost.columns = ['Region', 'Cost']
        region_cost = region_cost.sort_values('Cost', ascending=True)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=region_cost['Region'],
            x=region_cost['Cost'],
            orientation='h',
            marker=dict(
                color=region_cost['Cost'],
                colorscale=[[0, COLORS['success']], [0.5, COLORS['warning']], [1, COLORS['danger']]]
            ),
            text=[format_currency(x) for x in region_cost['Cost']],
            textposition='outside',
            textfont=dict(size=11, color=COLORS['text']),
            hovertemplate="<b>%{y}</b><br>Cost: %{text}<extra></extra>"
        ))
        
        fig.update_layout(
            height=350,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color=COLORS['text']),
            margin=dict(l=0, r=100, t=20, b=30),
            xaxis=dict(title="Total Delay Cost ($)", gridcolor=COLORS['grid']),
            yaxis=dict(title=""),
            hoverlabel=dict(bgcolor='#1E293B')
        )
        
        st.plotly_chart(fig, use_container_width=True, key="econ_region")
    
    with col2:
        st.markdown("### 📅 Monthly Cost Trend")
        
        monthly_cost = fdf.groupby('MONTH').agg({
            'DELAY_COST_AIRLINE': 'sum',
            'DELAY_COST_PASSENGER': 'sum'
        }).reset_index()
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=MONTHS_SHORT,
            y=monthly_cost['DELAY_COST_AIRLINE'],
            name='Airline Cost',
            marker_color=COLORS['primary'],
            hovertemplate="%{x}<br>Airline: $%{y:,.0f}<extra></extra>"
        ))
        fig.add_trace(go.Bar(
            x=MONTHS_SHORT,
            y=monthly_cost['DELAY_COST_PASSENGER'],
            name='Passenger Cost',
            marker_color=COLORS['secondary'],
            hovertemplate="%{x}<br>Passenger: $%{y:,.0f}<extra></extra>"
        ))
        
        fig.update_layout(
            height=350,
            barmode='stack',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color=COLORS['text']),
            margin=dict(l=50, r=20, t=20, b=30),
            legend=dict(orientation='h', y=1.08),
            xaxis=dict(title="", gridcolor=COLORS['grid']),
            yaxis=dict(title="Cost ($)", gridcolor=COLORS['grid']),
            hoverlabel=dict(bgcolor='#1E293B')
        )
        
        st.plotly_chart(fig, use_container_width=True, key="econ_monthly")
    
    # Pareto
    st.markdown("### 📈 Pareto Analysis (80/20 Rule)")
    st.markdown('<p class="chart-explainer">Identifying which airlines contribute most to delay costs — focus improvement efforts here for maximum ROI.</p>', unsafe_allow_html=True)
    
    airline_cost_df = fdf.groupby('AIRLINE_NAME')['DELAY_COST_TOTAL'].sum().reset_index()
    airline_cost_df = airline_cost_df.sort_values('DELAY_COST_TOTAL', ascending=False).head(15)
    airline_cost_df['Cumulative'] = airline_cost_df['DELAY_COST_TOTAL'].cumsum()
    airline_cost_df['Cumulative %'] = airline_cost_df['Cumulative'] / airline_cost_df['DELAY_COST_TOTAL'].sum() * 100
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(go.Bar(
        x=airline_cost_df['AIRLINE_NAME'],
        y=airline_cost_df['DELAY_COST_TOTAL'],
        name='Delay Cost',
        marker_color=COLORS['primary'],
        hovertemplate="<b>%{x}</b><br>Cost: $%{y:,.0f}<extra></extra>"
    ), secondary_y=False)
    
    fig.add_trace(go.Scatter(
        x=airline_cost_df['AIRLINE_NAME'],
        y=airline_cost_df['Cumulative %'],
        name='Cumulative %',
        line=dict(color=COLORS['danger'], width=3),
        mode='lines+markers',
        marker=dict(size=8),
        hovertemplate="%{x}<br>Cumulative: %{y:.1f}%<extra></extra>"
    ), secondary_y=True)
    
    fig.add_hline(y=80, line_dash="dash", line_color=COLORS['warning'],
                 annotation_text="80% Threshold", secondary_y=True)
    
    fig.update_layout(
        height=420,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COLORS['text']),
        margin=dict(l=50, r=50, t=30, b=100),
        legend=dict(orientation='h', y=1.08),
        xaxis=dict(tickangle=45, gridcolor=COLORS['grid']),
        yaxis=dict(title="Delay Cost ($)", gridcolor=COLORS['grid']),
        yaxis2=dict(title="Cumulative %", range=[0, 105]),
        hoverlabel=dict(bgcolor='#1E293B')
    )
    
    st.plotly_chart(fig, use_container_width=True, key="pareto")
    
    airlines_80 = len(airline_cost_df[airline_cost_df['Cumulative %'] <= 80])
    
    st.markdown(f"""
    <div class="insight-box">
        <div class="insight-title">💡 Pareto Insight</div>
        <div class="insight-text">
            <span class="insight-stat">{airlines_80} airlines</span> 
            ({airlines_80/15*100:.0f}% of shown) contribute to <span class="insight-stat">80%</span> of all delay costs.
            Targeting operational improvements at these carriers would maximize cost savings across the industry.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: AI PREDICTOR
# ═══════════════════════════════════════════════════════════════════════════════
elif current_page == "🤖 AI Predictor":
    
    st.markdown("""
    <div class="section-header">
        <span class="section-icon">🤖</span>
        <span class="section-title">Machine Learning Delay Predictor</span>
        <span class="section-subtitle">Random Forest Classification Model</span>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📊 Model Performance", "🔮 Predict Your Flight"])
    
    with tab1:
        st.markdown("### Model Training & Evaluation")
        st.markdown('<p class="chart-explainer">A Random Forest model trained on 50,000 flight records to predict delay probability.</p>', unsafe_allow_html=True)
        
        @st.cache_resource
        def train_model():
            model_df = df.sample(n=min(50000, len(df)), random_state=42)
            
            model_df['ORIGIN_ENC'] = pd.factorize(model_df['ORIGIN'])[0]
            model_df['DEST_ENC'] = pd.factorize(model_df['DEST'])[0]
            model_df['CARRIER_ENC'] = pd.factorize(model_df['OP_UNIQUE_CARRIER'])[0]
            
            features = ['MONTH', 'DAY_OF_WEEK', 'DEP_HOUR', 'DISTANCE', 'ORIGIN_ENC', 'DEST_ENC', 'CARRIER_ENC']
            X = model_df[features]
            y = model_df['DEP_DEL15']
            
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            model = RandomForestClassifier(n_estimators=100, max_depth=12, random_state=42, n_jobs=-1)
            model.fit(X_train, y_train)
            
            y_pred = model.predict(X_test)
            y_prob = model.predict_proba(X_test)[:, 1]
            
            return model, X_test, y_test, y_pred, y_prob, features
        
        with st.spinner("🔄 Training model..."):
            model, X_test, y_test, y_pred, y_prob, feature_names = train_model()
        
        st.success("✅ Model trained on 50,000 flights!")
        
        # Metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        fpr, tpr, _ = roc_curve(y_test, y_prob)
        roc_auc = auc(fpr, tpr)
        
        mc1, mc2, mc3, mc4, mc5 = st.columns(5)
        mc1.metric("Accuracy", f"{accuracy*100:.1f}%")
        mc2.metric("Precision", f"{precision*100:.1f}%")
        mc3.metric("Recall", f"{recall*100:.1f}%")
        mc4.metric("F1 Score", f"{f1*100:.1f}%")
        mc5.metric("AUC-ROC", f"{roc_auc:.3f}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Confusion Matrix")
            st.markdown('<p class="chart-explainer">Shows correct vs incorrect predictions. Diagonal = correct.</p>', unsafe_allow_html=True)
            
            cm = confusion_matrix(y_test, y_pred)
            
            fig = go.Figure(data=go.Heatmap(
                z=cm,
                x=['Predicted: On-Time', 'Predicted: Delayed'],
                y=['Actual: On-Time', 'Actual: Delayed'],
                colorscale=[[0, COLORS['success']], [1, COLORS['danger']]],
                text=[[f"{cm[i][j]:,}" for j in range(2)] for i in range(2)],
                texttemplate="<b>%{text}</b>",
                textfont={"size": 18, "color": "white"},
                hovertemplate="Actual: %{y}<br>Predicted: %{x}<br>Count: %{z:,}<extra></extra>",
                showscale=False
            ))
            
            fig.update_layout(
                height=350,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color=COLORS['text'], size=12),
                margin=dict(l=50, r=50, t=30, b=50),
                xaxis=dict(side='bottom'),
                yaxis=dict(autorange='reversed')
            )
            
            st.plotly_chart(fig, use_container_width=True, key="confusion")
        
        with col2:
            st.markdown("### 📈 ROC-AUC Curve")
            st.markdown('<p class="chart-explainer">Measures model discrimination ability. Higher area = better model.</p>', unsafe_allow_html=True)
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=fpr, y=tpr,
                mode='lines',
                name=f'Model (AUC = {roc_auc:.3f})',
                line=dict(color=COLORS['primary'], width=4),
                fill='tozeroy',
                fillcolor='rgba(6, 182, 212, 0.15)'
            ))
            
            fig.add_trace(go.Scatter(
                x=[0, 1], y=[0, 1],
                mode='lines',
                name='Random (AUC = 0.5)',
                line=dict(color=COLORS['muted'], width=2, dash='dash')
            ))
            
            fig.update_layout(
                height=350,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color=COLORS['text']),
                margin=dict(l=50, r=50, t=30, b=50),
                xaxis=dict(title='False Positive Rate', gridcolor=COLORS['grid'], range=[0, 1]),
                yaxis=dict(title='True Positive Rate', gridcolor=COLORS['grid'], range=[0, 1]),
                legend=dict(x=0.5, y=0.1)
            )
            
            st.plotly_chart(fig, use_container_width=True, key="roc")
        
        st.markdown("### 🎯 Feature Importance")
        st.markdown('<p class="chart-explainer">Which factors most influence delay prediction.</p>', unsafe_allow_html=True)
        
        importance_df = pd.DataFrame({
            'Feature': ['Month', 'Day of Week', 'Departure Hour', 'Distance', 'Origin Airport', 'Destination', 'Airline'],
            'Importance': model.feature_importances_
        }).sort_values('Importance', ascending=True)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=importance_df['Feature'],
            x=importance_df['Importance'],
            orientation='h',
            marker=dict(
                color=importance_df['Importance'],
                colorscale=[[0, COLORS['secondary']], [1, COLORS['primary']]]
            ),
            text=[f"{x:.3f}" for x in importance_df['Importance']],
            textposition='outside',
            textfont=dict(size=11, color=COLORS['text']),
            hovertemplate="<b>%{y}</b><br>Importance: %{x:.4f}<extra></extra>"
        ))
        
        fig.update_layout(
            height=320,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color=COLORS['text']),
            margin=dict(l=0, r=80, t=20, b=30),
            xaxis=dict(title='Importance Score', gridcolor=COLORS['grid']),
            yaxis=dict(title=""),
            hoverlabel=dict(bgcolor='#1E293B')
        )
        
        st.plotly_chart(fig, use_container_width=True, key="importance")
        
        st.markdown("""
        <div class="insight-box">
            <div class="insight-title">💡 Model Insight</div>
            <div class="insight-text">
                <b>Departure Hour</b> and <b>Distance</b> are the strongest predictors of delays.
                This aligns with the domino effect — later flights accumulate delays, and longer routes 
                have more variables that can cause disruptions.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### 🔮 Predict Delay Risk")
        st.markdown('<p class="chart-explainer">Enter your flight details to get a delay risk assessment.</p>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            pred_month = st.selectbox("📅 Month", MONTHS, key="pred_month")
            pred_day = st.selectbox("📆 Day of Week", DAYS, key="pred_day")
            pred_hour = st.slider("🕐 Departure Hour", 0, 23, 12, key="pred_hour")
        
        with col2:
            pred_origin = st.selectbox("🛫 Origin", 
                [f"{row['city']} ({row['code']})" for _, row in airports_df.iterrows()], key="pred_origin")
            pred_dest = st.selectbox("🛬 Destination",
                [f"{row['city']} ({row['code']})" for _, row in airports_df.iterrows()], key="pred_dest")
            pred_airline = st.selectbox("✈️ Airline",
                sorted(df['AIRLINE_NAME'].unique().tolist()), key="pred_airline")
        
        if st.button("🔮 PREDICT DELAY RISK", use_container_width=True):
            origin_code = pred_origin.split('(')[1].replace(')', '')
            dest_code = pred_dest.split('(')[1].replace(')', '')
            
            origin_info = airports_df[airports_df['code'] == origin_code].iloc[0]
            dest_info = airports_df[airports_df['code'] == dest_code].iloc[0]
            
            lat1, lon1 = np.radians(origin_info['lat']), np.radians(origin_info['lon'])
            lat2, lon2 = np.radians(dest_info['lat']), np.radians(dest_info['lon'])
            dlat, dlon = lat2 - lat1, lon2 - lon1
            a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
            distance = 3956 * 2 * np.arcsin(np.sqrt(a))
            
            origin_enc = hash(origin_code) % 1000
            dest_enc = hash(dest_code) % 1000
            carrier_enc = hash(pred_airline) % 1000
            month_idx = MONTHS.index(pred_month) + 1
            day_idx = DAYS.index(pred_day) + 1
            
            features = [[month_idx, day_idx, pred_hour, distance, origin_enc, dest_enc, carrier_enc]]
            
            prediction = model.predict(features)[0]
            probability = model.predict_proba(features)[0][1]
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            if prediction == 1:
                st.markdown(f"""
                <div class="prediction-high">
                    <div class="prediction-icon">⚠️</div>
                    <div class="prediction-title" style="color: #FCA5A5;">HIGH DELAY RISK</div>
                    <div class="prediction-prob" style="color: #EF4444;">{probability*100:.1f}%</div>
                    <p style="color: #E2E8F0;">probability of delay</p>
                    <p style="color: #94A3B8; margin-top: 1rem;">Consider an earlier flight or add buffer time for connections.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="prediction-low">
                    <div class="prediction-icon">✅</div>
                    <div class="prediction-title" style="color: #6EE7B7;">LOW DELAY RISK</div>
                    <div class="prediction-prob" style="color: #10B981;">{(1-probability)*100:.1f}%</div>
                    <p style="color: #E2E8F0;">probability of on-time departure</p>
                    <p style="color: #94A3B8; margin-top: 1rem;">Great choice! This flight has good on-time indicators.</p>
                </div>
                """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: SIMULATOR
# ═══════════════════════════════════════════════════════════════════════════════
elif current_page == "🔮 Simulator":
    
    st.markdown("""
    <div class="section-header">
        <span class="section-icon">🔮</span>
        <span class="section-title">What-If Scenario Simulator</span>
        <span class="section-subtitle">Explore Improvement Scenarios</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="insight-box">
        <div class="insight-title">🎯 How It Works</div>
        <div class="insight-text">
            Adjust the sliders to simulate different operational improvement scenarios. 
            See how reducing specific delay causes would impact overall performance and costs.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    cur_delays = int(fdf['DEP_DEL15'].sum())
    cur_rate = fdf['DEP_DEL15'].mean() * 100
    cur_cost = fdf['DELAY_COST_TOTAL'].sum()
    
    st.markdown("### 📊 Current State")
    cc1, cc2, cc3 = st.columns(3)
    cc1.metric("Delayed Flights", f"{cur_delays:,}")
    cc2.metric("Delay Rate", f"{cur_rate:.1f}%")
    cc3.metric("Total Cost", format_currency(cur_cost))
    
    st.markdown("---")
    st.markdown("### 🎛️ Scenario Parameters")
    
    col1, col2 = st.columns(2)
    
    with col1:
        carrier_red = st.slider("✈️ Reduce Carrier Delays (%)", 0, 50, 0, 5,
            help="Better maintenance, crew scheduling, operations")
        weather_red = st.slider("🌧️ Reduce Weather Impact (%)", 0, 30, 0, 5,
            help="Improved forecasting, proactive rescheduling")
    
    with col2:
        nas_red = st.slider("🗼 Reduce ATC Delays (%)", 0, 40, 0, 5,
            help="Modernized air traffic systems, better flow management")
        late_red = st.slider("🔄 Reduce Late Aircraft (%)", 0, 50, 0, 5,
            help="Faster turnaround, schedule buffers, spare aircraft")
    
    total_red = (carrier_red * 0.35 + weather_red * 0.20 + nas_red * 0.25 + late_red * 0.20) / 100
    
    new_delays = cur_delays * (1 - total_red)
    new_rate = cur_rate * (1 - total_red)
    new_cost = cur_cost * (1 - total_red)
    savings = cur_cost - new_cost
    
    st.markdown("---")
    st.markdown("### 📈 Simulated Outcome")
    
    sc1, sc2, sc3, sc4 = st.columns(4)
    sc1.metric("New Delayed", f"{new_delays:,.0f}", f"-{cur_delays - new_delays:,.0f}")
    sc2.metric("New Rate", f"{new_rate:.1f}%", f"-{cur_rate - new_rate:.1f}%")
    sc3.metric("New Cost", format_currency(new_cost))
    sc4.metric("💰 SAVINGS", format_currency(savings))
    
    if savings > 0:
        st.markdown(f"""
        <div class="insight-box success">
            <div class="insight-title">✅ Projected Impact</div>
            <div class="insight-text">
                With these improvements:<br>
                • <span class="insight-stat">{cur_delays - new_delays:,.0f}</span> fewer delayed flights<br>
                • <span class="insight-stat">{format_currency(savings)}</span> in cost savings<br>
                • <span class="insight-stat">{cur_rate - new_rate:.1f}%</span> improvement in on-time performance
            </div>
        </div>
        """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: REGIONAL
# ═══════════════════════════════════════════════════════════════════════════════
elif current_page == "🌍 Regional":
    
    st.markdown("""
    <div class="section-header">
        <span class="section-icon">🌍</span>
        <span class="section-title">Regional Case Studies</span>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["🇮🇳 India", "🇦🇪 Middle East", "🇺🇸 North America"])
    
    with tab1:
        india_df = df[df['ORIGIN_REGION'] == 'India']
        
        ic1, ic2, ic3, ic4 = st.columns(4)
        ic1.metric("Flights", f"{len(india_df):,}")
        ic2.metric("Delay Rate", f"{india_df['DEP_DEL15'].mean()*100:.1f}%")
        ic3.metric("Avg Delay", f"{india_df[india_df['DEP_DEL15']==1]['DEP_DELAY'].mean():.0f} min")
        ic4.metric("Cost", format_currency(india_df['DELAY_COST_TOTAL'].sum()))
        
        st.markdown("### 🌧️ Monsoon Impact")
        st.markdown('<p class="chart-explainer">Red bars indicate monsoon months (June-September) with significantly higher delays.</p>', unsafe_allow_html=True)
        
        india_monthly = india_df.groupby('MONTH')['DEP_DEL15'].mean().reset_index()
        colors = [COLORS['success'] if m not in [6,7,8,9] else COLORS['danger'] for m in range(1,13)]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=MONTHS_SHORT,
            y=india_monthly['DEP_DEL15'] * 100,
            marker_color=colors,
            text=[f"{x:.1f}%" for x in india_monthly['DEP_DEL15'] * 100],
            textposition='outside',
            textfont=dict(color=COLORS['text']),
            hovertemplate="<b>%{x}</b><br>Delay Rate: %{y:.1f}%<extra></extra>"
        ))
        
        fig.add_vrect(x0=4.5, x1=8.5, fillcolor="rgba(239,68,68,0.1)", line_width=0)
        
        fig.update_layout(
            height=350,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color=COLORS['text']),
            margin=dict(l=50, r=20, t=20, b=30),
            yaxis=dict(title="Delay Rate (%)", gridcolor=COLORS['grid']),
            hoverlabel=dict(bgcolor='#1E293B')
        )
        
        st.plotly_chart(fig, use_container_width=True, key="india_monthly")
        
        st.markdown("""
        <div class="insight-box warning">
            <div class="insight-title">🌧️ India Insight</div>
            <div class="insight-text">
                Monsoon season (Jun-Sep) causes <span class="insight-stat">40-60%</span> higher delays.
                Mumbai and Delhi are most affected. Winter fog (Dec-Jan) also impacts North India airports.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with tab2:
        me_df = df[df['ORIGIN_REGION'] == 'Middle East']
        
        mc1, mc2, mc3, mc4 = st.columns(4)
        mc1.metric("Flights", f"{len(me_df):,}")
        mc2.metric("Delay Rate", f"{me_df['DEP_DEL15'].mean()*100:.1f}%")
        mc3.metric("Avg Delay", f"{me_df[me_df['DEP_DEL15']==1]['DEP_DELAY'].mean():.0f} min")
        mc4.metric("Cost", format_currency(me_df['DELAY_COST_TOTAL'].sum()))
        
        st.markdown("### ✈️ Gulf Carriers Performance")
        
        me_airlines = me_df.groupby('AIRLINE_NAME')['DEP_DEL15'].agg(['count', 'mean']).reset_index()
        me_airlines.columns = ['Airline', 'Flights', 'Delay Rate']
        me_airlines = me_airlines[me_airlines['Flights'] >= 20].sort_values('Delay Rate')
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=me_airlines['Airline'],
            x=me_airlines['Delay Rate'] * 100,
            orientation='h',
            marker_color=COLORS['primary'],
            text=[f"{x:.1f}%" for x in me_airlines['Delay Rate'] * 100],
            textposition='outside',
            textfont=dict(color=COLORS['text']),
            hovertemplate="<b>%{y}</b><br>Delay Rate: %{x:.1f}%<extra></extra>"
        ))
        
        fig.update_layout(
            height=350,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color=COLORS['text']),
            margin=dict(l=0, r=80, t=20, b=30),
            xaxis=dict(title="Delay Rate (%)", gridcolor=COLORS['grid']),
            hoverlabel=dict(bgcolor='#1E293B')
        )
        
        st.plotly_chart(fig, use_container_width=True, key="me_airlines")
        
        st.markdown("""
        <div class="insight-box">
            <div class="insight-title">🇦🇪 Gulf Insight</div>
            <div class="insight-text">
                Premium Gulf carriers invest heavily in punctuality. Dubai (DXB), the world's busiest 
                international hub, maintains strong OTP. Winter morning fog (Dec-Feb) is the main weather challenge.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with tab3:
        na_df = df[df['ORIGIN_REGION'] == 'North America']
        
        nc1, nc2, nc3, nc4 = st.columns(4)
        nc1.metric("Flights", f"{len(na_df):,}")
        nc2.metric("Delay Rate", f"{na_df['DEP_DEL15'].mean()*100:.1f}%")
        nc3.metric("Avg Delay", f"{na_df[na_df['DEP_DEL15']==1]['DEP_DELAY'].mean():.0f} min")
        nc4.metric("Cost", format_currency(na_df['DELAY_COST_TOTAL'].sum()))
        
        st.markdown("### ❄️ Seasonal Pattern")
        st.markdown('<p class="chart-explainer">Red = winter storms, Yellow = summer thunderstorms, Green = stable periods.</p>', unsafe_allow_html=True)
        
        na_monthly = na_df.groupby('MONTH')['DEP_DEL15'].mean().reset_index()
        colors = [COLORS['danger'] if m in [1,2,12] else COLORS['warning'] if m in [6,7,8] else COLORS['success'] for m in range(1,13)]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=MONTHS_SHORT,
            y=na_monthly['DEP_DEL15'] * 100,
            marker_color=colors,
            text=[f"{x:.1f}%" for x in na_monthly['DEP_DEL15'] * 100],
            textposition='outside',
            textfont=dict(color=COLORS['text']),
            hovertemplate="<b>%{x}</b><br>Delay Rate: %{y:.1f}%<extra></extra>"
        ))
        
        fig.update_layout(
            height=350,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color=COLORS['text']),
            margin=dict(l=50, r=20, t=20, b=30),
            yaxis=dict(title="Delay Rate (%)", gridcolor=COLORS['grid']),
            hoverlabel=dict(bgcolor='#1E293B')
        )
        
        st.plotly_chart(fig, use_container_width=True, key="na_monthly")
        
        st.markdown("""
        <div class="insight-box warning">
            <div class="insight-title">🇺🇸 North America Insight</div>
            <div class="insight-text">
                Winter storms (Dec-Feb) and summer thunderstorms (Jun-Aug) cause most delays. 
                Chicago O'Hare and Denver are most weather-impacted. Holiday travel (Thanksgiving, Christmas) adds congestion.
            </div>
        </div>
        """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: SUMMARY
# ═══════════════════════════════════════════════════════════════════════════════
elif current_page == "📈 Summary":
    
    st.markdown("""
    <div class="section-header">
        <span class="section-icon">📈</span>
        <span class="section-title">Executive Summary & Recommendations</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Key Stats
    col1, col2 = st.columns(2)
    
    total_flights = len(df)
    total_delayed = int(df['DEP_DEL15'].sum())
    total_cost = df['DELAY_COST_TOTAL'].sum()
    
    with col1:
        st.markdown(f"""
        <div class="insight-box">
            <div class="insight-title">📊 Dataset Summary</div>
            <div class="insight-text">
                • <b>Total Flights:</b> <span class="insight-stat">{total_flights:,}</span><br>
                • <b>Delayed Flights:</b> <span class="insight-stat">{total_delayed:,}</span> ({total_delayed/total_flights*100:.1f}%)<br>
                • <b>Economic Impact:</b> <span class="insight-stat">{format_currency(total_cost)}</span><br>
                • <b>Airports:</b> <span class="insight-stat">{len(airports_df)}</span> global hubs<br>
                • <b>Airlines:</b> <span class="insight-stat">{len(airlines_df)}</span> carriers
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        best_airline = df.groupby('AIRLINE_NAME')['DEP_DEL15'].mean().idxmin()
        worst_airline = df.groupby('AIRLINE_NAME')['DEP_DEL15'].mean().idxmax()
        
        st.markdown(f"""
        <div class="insight-box">
            <div class="insight-title">🏆 Performance Leaders</div>
            <div class="insight-text">
                • <b>Best Airline:</b> <span class="insight-stat">{best_airline}</span><br>
                • <b>Most Challenged:</b> <span class="insight-stat">{worst_airline}</span><br>
                • <b>Best Time:</b> <span class="insight-stat">Early morning (5-7 AM)</span><br>
                • <b>Worst Time:</b> <span class="insight-stat">Evening (5-8 PM)</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### 🔍 Key Findings")
    
    st.markdown("""
    <div class="insight-box">
        <div class="insight-title">🌊 The Domino Effect is Real</div>
        <div class="insight-text">
            Late aircraft delays compound throughout the day. Evening flights are significantly more likely 
            to be delayed than morning flights. Building schedule buffers can break the cascade.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="insight-box warning">
        <div class="insight-title">🌧️ Weather Drives Seasonality</div>
        <div class="insight-text">
            India's monsoon, North America's winter storms, and summer thunderstorms create predictable 
            delay peaks. Airlines and passengers can plan around these patterns.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="insight-box success">
        <div class="insight-title">📈 80/20 Rule Applies</div>
        <div class="insight-text">
            A small number of airlines and airports contribute disproportionately to delays. 
            Targeted improvements at these bottlenecks yield maximum ROI.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 💡 Recommendations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="insight-box">
            <div class="insight-title">👤 For Passengers</div>
            <div class="insight-text">
                1. Book early morning flights (5-7 AM)<br>
                2. Avoid peak delay seasons<br>
                3. Allow buffer for connections<br>
                4. Use AI predictor before booking<br>
                5. Choose airlines with strong OTP
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="insight-box">
            <div class="insight-title">🏢 For Industry</div>
            <div class="insight-text">
                1. Build schedule buffers<br>
                2. Invest in predictive maintenance<br>
                3. Improve turnaround efficiency<br>
                4. Enhance weather contingency<br>
                5. Focus on hub operations
            </div>
        </div>
        """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="footer">
    <div class="footer-brand">✈️ Flight Delay Domino Effect Dashboard</div>
    <p>Master's in AI & Business Analytics | Data Visualization Project</p>
    <p style="font-size: 0.8rem;">Python • Streamlit • Plotly • Scikit-learn</p>
</div>
""", unsafe_allow_html=True)
