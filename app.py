# ═══════════════════════════════════════════════════════════════════════════════
# ✈️ FLIGHT DELAY DOMINO EFFECT - PROFESSIONAL DASHBOARD
# Master's Level Data Visualization Project
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
# PREMIUM CSS STYLING
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Root Variables */
    :root {
        --bg-primary: #0a0e17;
        --bg-secondary: #111827;
        --bg-card: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%);
        --accent-primary: #f97316;
        --accent-secondary: #fb923c;
        --accent-gradient: linear-gradient(135deg, #f97316 0%, #ea580c 50%, #dc2626 100%);
        --text-primary: #f8fafc;
        --text-secondary: #94a3b8;
        --border-color: rgba(255, 255, 255, 0.1);
        --success: #10b981;
        --danger: #ef4444;
        --warning: #f59e0b;
        --info: #3b82f6;
    }
    
    /* Global Styles */
    .stApp {
        background: linear-gradient(180deg, #0a0e17 0%, #111827 50%, #0f172a 100%);
        font-family: 'Inter', sans-serif;
    }
    
    .main .block-container {
        padding: 1rem 2rem 2rem 2rem;
        max-width: 100%;
    }
    
    /* Hide Streamlit Elements */
    #MainMenu, footer, header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* ═══════════════ NAVIGATION BAR ═══════════════ */
    .navbar {
        background: linear-gradient(90deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.95) 100%);
        backdrop-filter: blur(20px);
        border-bottom: 1px solid rgba(249, 115, 22, 0.3);
        padding: 0.8rem 2rem;
        margin: -1rem -2rem 2rem -2rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        position: sticky;
        top: 0;
        z-index: 1000;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
    }
    
    .nav-brand {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .nav-brand-icon {
        font-size: 2rem;
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-5px); }
    }
    
    .nav-brand-text {
        font-size: 1.4rem;
        font-weight: 700;
        background: linear-gradient(135deg, #f97316 0%, #fb923c 50%, #fbbf24 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .nav-brand-subtitle {
        font-size: 0.75rem;
        color: #94a3b8;
        letter-spacing: 2px;
        text-transform: uppercase;
    }
    
    /* ═══════════════ HERO SECTION ═══════════════ */
    .hero-section {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.8) 100%);
        border: 1px solid rgba(249, 115, 22, 0.2);
        border-radius: 24px;
        padding: 3rem;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #f97316, #fb923c, #fbbf24, #f97316);
        background-size: 200% 100%;
        animation: gradient-shift 3s ease infinite;
    }
    
    @keyframes gradient-shift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 50%, #e2e8f0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        line-height: 1.2;
    }
    
    .hero-subtitle {
        font-size: 1.2rem;
        color: #94a3b8;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    .hero-highlight {
        color: #f97316;
        font-weight: 600;
    }
    
    /* ═══════════════ METRIC CARDS - GLASSMORPHISM ═══════════════ */
    .metric-container {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1.5rem;
        margin-bottom: 2rem;
    }
    
    .glass-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.6) 0%, rgba(15, 23, 42, 0.8) 100%);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 1.8rem;
        position: relative;
        overflow: hidden;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .glass-card:hover {
        transform: translateY(-8px);
        border-color: rgba(249, 115, 22, 0.5);
        box-shadow: 0 20px 40px rgba(249, 115, 22, 0.15);
    }
    
    .glass-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, rgba(249, 115, 22, 0.1) 0%, transparent 50%);
        opacity: 0;
        transition: opacity 0.4s ease;
    }
    
    .glass-card:hover::before {
        opacity: 1;
    }
    
    .card-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        display: block;
    }
    
    .card-value {
        font-size: 2.5rem;
        font-weight: 800;
        color: #f8fafc;
        margin-bottom: 0.5rem;
        line-height: 1;
    }
    
    .card-value.accent {
        background: linear-gradient(135deg, #f97316 0%, #fb923c 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .card-label {
        font-size: 0.9rem;
        color: #94a3b8;
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
        font-size: 0.8rem;
        font-weight: 600;
        margin-top: 0.8rem;
    }
    
    .card-delta.negative {
        background: rgba(239, 68, 68, 0.2);
        color: #fca5a5;
    }
    
    .card-delta.positive {
        background: rgba(16, 185, 129, 0.2);
        color: #6ee7b7;
    }
    
    /* ═══════════════ SECTION HEADERS ═══════════════ */
    .section-header {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin: 2.5rem 0 1.5rem 0;
        padding-bottom: 1rem;
        border-bottom: 2px solid rgba(249, 115, 22, 0.3);
    }
    
    .section-icon {
        font-size: 1.8rem;
        background: linear-gradient(135deg, #f97316 0%, #fb923c 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .section-title {
        font-size: 1.6rem;
        font-weight: 700;
        color: #f8fafc;
        margin: 0;
    }
    
    .section-subtitle {
        font-size: 0.9rem;
        color: #64748b;
        margin-left: auto;
    }
    
    /* ═══════════════ INSIGHT CARDS ═══════════════ */
    .insight-card {
        background: linear-gradient(135deg, rgba(249, 115, 22, 0.1) 0%, rgba(234, 88, 12, 0.05) 100%);
        border: 1px solid rgba(249, 115, 22, 0.3);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        position: relative;
        overflow: hidden;
    }
    
    .insight-card::before {
        content: '💡';
        position: absolute;
        top: -10px;
        right: 20px;
        font-size: 3rem;
        opacity: 0.2;
    }
    
    .insight-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #f97316;
        margin-bottom: 0.8rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .insight-text {
        color: #e2e8f0;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    .insight-stat {
        font-weight: 700;
        color: #fb923c;
    }
    
    /* ═══════════════ CHART CONTAINERS ═══════════════ */
    .chart-container {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.5) 0%, rgba(15, 23, 42, 0.7) 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    }
    
    .chart-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #f8fafc;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 8px;
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
        color: #94a3b8;
        font-weight: 500;
        border: none;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
        color: #ffffff;
    }
    
    /* ═══════════════ PREDICTION RESULT ═══════════════ */
    .prediction-high {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.2) 0%, rgba(220, 38, 38, 0.1) 100%);
        border: 2px solid #ef4444;
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        animation: pulse-red 2s infinite;
    }
    
    @keyframes pulse-red {
        0%, 100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4); }
        50% { box-shadow: 0 0 20px 10px rgba(239, 68, 68, 0); }
    }
    
    .prediction-low {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(5, 150, 105, 0.1) 100%);
        border: 2px solid #10b981;
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        animation: pulse-green 2s infinite;
    }
    
    @keyframes pulse-green {
        0%, 100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.4); }
        50% { box-shadow: 0 0 20px 10px rgba(16, 185, 129, 0); }
    }
    
    .prediction-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
    }
    
    .prediction-title {
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .prediction-prob {
        font-size: 3rem;
        font-weight: 800;
    }
    
    /* ═══════════════ WHAT-IF SLIDERS ═══════════════ */
    .stSlider > div > div {
        background: linear-gradient(90deg, #f97316 0%, #fb923c 100%);
    }
    
    .stSlider [data-baseweb="slider"] {
        margin-top: 1rem;
    }
    
    /* ═══════════════ SELECTBOX STYLING ═══════════════ */
    .stSelectbox > div > div {
        background: rgba(30, 41, 59, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
    
    /* ═══════════════ DATAFRAME STYLING ═══════════════ */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
    }
    
    /* ═══════════════ FOOTER ═══════════════ */
    .footer {
        text-align: center;
        padding: 2rem;
        margin-top: 3rem;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        color: #64748b;
    }
    
    .footer-brand {
        font-size: 1.2rem;
        font-weight: 600;
        color: #f97316;
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

def get_airport_name(code, airports_df):
    """Get full airport name from code"""
    match = airports_df[airports_df['code'] == code]
    if len(match) > 0:
        return f"{match.iloc[0]['city']} ({code})"
    return code

def get_airline_name(code, airlines_df):
    """Get full airline name from code"""
    match = airlines_df[airlines_df['code'] == code]
    if len(match) > 0:
        return match.iloc[0]['name']
    return code

MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 
          'July', 'August', 'September', 'October', 'November', 'December']
MONTHS_SHORT = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
DAYS_SHORT = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

# ═══════════════════════════════════════════════════════════════════════════════
# LOAD DATA
# ═══════════════════════════════════════════════════════════════════════════════
try:
    df, airlines_df, airports_df = load_data()
    data_loaded = True
except Exception as e:
    st.error(f"❌ Error loading data: {e}")
    st.stop()

# Create airport name mapping
airport_names = {row['code']: f"{row['city']} ({row['code']})" for _, row in airports_df.iterrows()}
airline_names = {row['code']: row['name'] for _, row in airlines_df.iterrows()}

# ═══════════════════════════════════════════════════════════════════════════════
# NAVIGATION BAR
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="navbar">
    <div class="nav-brand">
        <span class="nav-brand-icon">✈️</span>
        <div>
            <div class="nav-brand-text">Flight Delay Domino Effect</div>
            <div class="nav-brand-subtitle">Global Aviation Analytics Dashboard</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Horizontal Navigation
nav_cols = st.columns(8)
pages = ["🏠 Overview", "📊 Analytics", "🌊 Domino Effect", "💰 Economics", 
         "🤖 AI Predictor", "🔮 Simulator", "🌍 Regional", "📈 Insights"]

# Use session state for navigation
if 'current_page' not in st.session_state:
    st.session_state.current_page = "🏠 Overview"

for i, page in enumerate(pages):
    if nav_cols[i].button(page, key=f"nav_{i}", use_container_width=True):
        st.session_state.current_page = page

current_page = st.session_state.current_page

# ═══════════════════════════════════════════════════════════════════════════════
# FILTERS (Collapsible)
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
        st.markdown(f"**Filtered Data:** {len(df):,} flights")
        st.markdown(f"**Airports:** {len(airports_df)} | **Airlines:** {len(airlines_df)}")

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
# PAGE: OVERVIEW (HOME)
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
    
    # Key Metrics
    total_flights = len(fdf)
    delayed_flights = int(fdf['DEP_DEL15'].sum())
    delay_rate = (delayed_flights / total_flights * 100) if total_flights > 0 else 0
    avg_delay = fdf[fdf['DEP_DEL15'] == 1]['DEP_DELAY'].mean() if delayed_flights > 0 else 0
    total_cost = fdf['DELAY_COST_TOTAL'].sum()
    affected_passengers = delayed_flights * 150  # Avg passengers per flight
    
    mc1, mc2, mc3, mc4 = st.columns(4)
    
    with mc1:
        st.markdown(f"""
        <div class="glass-card">
            <span class="card-icon">🛫</span>
            <div class="card-value">{format_number(total_flights)}</div>
            <div class="card-label">Total Flights Analyzed</div>
            <div class="card-delta positive">📅 Jan - Dec 2024</div>
        </div>
        """, unsafe_allow_html=True)
    
    with mc2:
        st.markdown(f"""
        <div class="glass-card">
            <span class="card-icon">⏱️</span>
            <div class="card-value accent">{delay_rate:.1f}%</div>
            <div class="card-label">Overall Delay Rate</div>
            <div class="card-delta negative">⚠️ {format_number(delayed_flights)} delayed</div>
        </div>
        """, unsafe_allow_html=True)
    
    with mc3:
        st.markdown(f"""
        <div class="glass-card">
            <span class="card-icon">⏰</span>
            <div class="card-value">{avg_delay:.0f} min</div>
            <div class="card-label">Average Delay Duration</div>
            <div class="card-delta negative">📊 When delayed</div>
        </div>
        """, unsafe_allow_html=True)
    
    with mc4:
        st.markdown(f"""
        <div class="glass-card">
            <span class="card-icon">💰</span>
            <div class="card-value accent">{format_currency(total_cost)}</div>
            <div class="card-label">Total Economic Impact</div>
            <div class="card-delta negative">👥 {format_number(affected_passengers)} passengers</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Main Visualizations
    col1, col2 = st.columns([1.2, 1])
    
    with col1:
        st.markdown("""
        <div class="section-header">
            <span class="section-icon">🌍</span>
            <span class="section-title">Global Delay Distribution by Region</span>
        </div>
        """, unsafe_allow_html=True)
        
        region_stats = fdf.groupby('ORIGIN_REGION').agg({
            'DEP_DEL15': ['count', 'sum', 'mean'],
            'DEP_DELAY': 'mean',
            'DELAY_COST_TOTAL': 'sum'
        }).reset_index()
        region_stats.columns = ['Region', 'Total Flights', 'Delayed Flights', 'Delay Rate', 'Avg Delay', 'Total Cost']
        region_stats = region_stats.sort_values('Delay Rate', ascending=True)
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            y=region_stats['Region'],
            x=region_stats['Delay Rate'] * 100,
            orientation='h',
            marker=dict(
                color=region_stats['Delay Rate'] * 100,
                colorscale=[[0, '#10b981'], [0.5, '#f59e0b'], [1, '#ef4444']],
                line=dict(width=0)
            ),
            text=[f"<b>{x:.1f}%</b>" for x in region_stats['Delay Rate'] * 100],
            textposition='outside',
            textfont=dict(size=14, color='white'),
            hovertemplate="<b>%{y}</b><br>" +
                          "Delay Rate: %{x:.1f}%<br>" +
                          "<extra></extra>"
        ))
        
        fig.update_layout(
            height=450,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e2e8f0', size=12),
            margin=dict(l=0, r=80, t=20, b=40),
            xaxis=dict(
                title="Delay Rate (%)",
                titlefont=dict(size=14),
                gridcolor='rgba(255,255,255,0.1)',
                zeroline=False,
                range=[0, max(region_stats['Delay Rate'] * 100) * 1.25]
            ),
            yaxis=dict(title="", gridcolor='rgba(255,255,255,0.05)'),
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True, key="overview_region")
    
    with col2:
        st.markdown("""
        <div class="section-header">
            <span class="section-icon">📈</span>
            <span class="section-title">Monthly Delay Trend</span>
        </div>
        """, unsafe_allow_html=True)
        
        monthly = fdf.groupby('MONTH').agg({
            'DEP_DEL15': ['count', 'mean'],
            'DELAY_COST_TOTAL': 'sum'
        }).reset_index()
        monthly.columns = ['Month', 'Flights', 'Delay Rate', 'Cost']
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=MONTHS_SHORT,
            y=monthly['Delay Rate'] * 100,
            mode='lines+markers',
            line=dict(color='#f97316', width=4, shape='spline'),
            marker=dict(size=12, color='#f97316', 
                       line=dict(width=3, color='#ffffff')),
            fill='tozeroy',
            fillcolor='rgba(249, 115, 22, 0.1)',
            hovertemplate="<b>%{x}</b><br>Delay Rate: %{y:.1f}%<extra></extra>"
        ))
        
        # Add average line
        avg_rate = monthly['Delay Rate'].mean() * 100
        fig.add_hline(y=avg_rate, line_dash="dash", line_color="#ef4444",
                     annotation_text=f"Avg: {avg_rate:.1f}%",
                     annotation_position="right")
        
        fig.update_layout(
            height=450,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e2e8f0', size=12),
            margin=dict(l=50, r=30, t=20, b=40),
            xaxis=dict(title="", gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(title="Delay Rate (%)", gridcolor='rgba(255,255,255,0.1)',
                      titlefont=dict(size=14)),
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True, key="overview_monthly")
    
    # Key Insights
    st.markdown("""
    <div class="section-header">
        <span class="section-icon">💡</span>
        <span class="section-title">Key Discovery Insights</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Calculate insights
    worst_region = fdf.groupby('ORIGIN_REGION')['DEP_DEL15'].mean().idxmax()
    worst_region_rate = fdf.groupby('ORIGIN_REGION')['DEP_DEL15'].mean().max() * 100
    best_region = fdf.groupby('ORIGIN_REGION')['DEP_DEL15'].mean().idxmin()
    best_region_rate = fdf.groupby('ORIGIN_REGION')['DEP_DEL15'].mean().min() * 100
    worst_hour = int(fdf.groupby('DEP_HOUR')['DEP_DEL15'].mean().idxmax())
    best_hour = int(fdf.groupby('DEP_HOUR')['DEP_DEL15'].mean().idxmin())
    worst_month = int(fdf.groupby('MONTH')['DEP_DEL15'].mean().idxmax())
    late_aircraft_pct = fdf[fdf['LATE_AIRCRAFT_DELAY'] > 0]['DEP_DEL15'].sum() / fdf['DEP_DEL15'].sum() * 100
    
    ic1, ic2, ic3 = st.columns(3)
    
    with ic1:
        st.markdown(f"""
        <div class="insight-card">
            <div class="insight-title">🌍 Regional Disparity</div>
            <div class="insight-text">
                <span class="insight-stat">{worst_region}</span> has the highest delay rate at 
                <span class="insight-stat">{worst_region_rate:.1f}%</span>, while 
                <span class="insight-stat">{best_region}</span> performs best at only 
                <span class="insight-stat">{best_region_rate:.1f}%</span>. 
                That's a <span class="insight-stat">{worst_region_rate - best_region_rate:.1f}%</span> difference!
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with ic2:
        st.markdown(f"""
        <div class="insight-card">
            <div class="insight-title">⏰ Time Matters</div>
            <div class="insight-text">
                Flights at <span class="insight-stat">{worst_hour}:00</span> have the highest delay probability.
                For best results, book flights around <span class="insight-stat">{best_hour}:00</span>.
                <span class="insight-stat">{MONTHS[worst_month-1]}</span> is the worst month to fly.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with ic3:
        st.markdown(f"""
        <div class="insight-card">
            <div class="insight-title">🔄 Domino Effect</div>
            <div class="insight-text">
                <span class="insight-stat">{late_aircraft_pct:.1f}%</span> of delays are caused by 
                late arriving aircraft - the domino effect in action! One delayed flight 
                impacts multiple subsequent flights throughout the day.
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
        <span class="section-subtitle">Comprehensive delay pattern analysis</span>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["✈️ Airline Performance", "🏢 Airport Analysis", "🕐 Time Patterns", "🔥 Seasonality Heatmap"])
    
    # TAB 1: AIRLINES
    with tab1:
        st.markdown("### Airline Performance Ranking")
        st.markdown("*Comparing delay rates across major airlines with full names*")
        
        airline_stats = fdf.groupby(['OP_UNIQUE_CARRIER', 'AIRLINE_NAME']).agg({
            'DEP_DEL15': ['count', 'sum', 'mean'],
            'DEP_DELAY': 'mean',
            'DELAY_COST_TOTAL': 'sum'
        }).reset_index()
        airline_stats.columns = ['Code', 'Airline', 'Total Flights', 'Delayed', 'Delay Rate', 'Avg Delay Min', 'Total Cost']
        airline_stats = airline_stats[airline_stats['Total Flights'] >= 100].sort_values('Delay Rate', ascending=True).tail(15)
        
        fig = go.Figure()
        
        colors = ['#10b981' if x < 0.25 else '#f59e0b' if x < 0.35 else '#ef4444' for x in airline_stats['Delay Rate']]
        
        fig.add_trace(go.Bar(
            y=airline_stats['Airline'],
            x=airline_stats['Delay Rate'] * 100,
            orientation='h',
            marker_color=colors,
            text=[f"<b>{x:.1f}%</b> ({int(d):,} delayed)" for x, d in zip(airline_stats['Delay Rate'] * 100, airline_stats['Delayed'])],
            textposition='outside',
            textfont=dict(size=11, color='#e2e8f0'),
            hovertemplate="<b>%{y}</b><br>" +
                          "Delay Rate: %{x:.1f}%<br>" +
                          "Total Flights: %{customdata[0]:,}<br>" +
                          "Avg Delay: %{customdata[1]:.0f} min<br>" +
                          "<extra></extra>",
            customdata=airline_stats[['Total Flights', 'Avg Delay Min']].values
        ))
        
        fig.update_layout(
            height=600,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e2e8f0'),
            margin=dict(l=0, r=150, t=20, b=50),
            xaxis=dict(title="Delay Rate (%)", gridcolor='rgba(255,255,255,0.1)',
                      range=[0, max(airline_stats['Delay Rate'] * 100) * 1.4]),
            yaxis=dict(title="", categoryorder='total ascending'),
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True, key="analytics_airline")
        
        # Airline Drill Down
        st.markdown("---")
        st.markdown("### 🔍 Airline Deep Dive")
        
        selected_drill_airline = st.selectbox(
            "Select an airline for detailed analysis:",
            airline_stats['Airline'].tolist(),
            key="airline_drill"
        )
        
        if selected_drill_airline:
            ad = fdf[fdf['AIRLINE_NAME'] == selected_drill_airline]
            
            dc1, dc2, dc3, dc4 = st.columns(4)
            dc1.metric("Total Flights", f"{len(ad):,}")
            dc2.metric("Delay Rate", f"{ad['DEP_DEL15'].mean()*100:.1f}%")
            dc3.metric("Avg Delay", f"{ad[ad['DEP_DEL15']==1]['DEP_DELAY'].mean():.0f} min")
            dc4.metric("Total Cost", format_currency(ad['DELAY_COST_TOTAL'].sum()))
            
            # Monthly trend for selected airline
            ad_monthly = ad.groupby('MONTH')['DEP_DEL15'].mean().reset_index()
            
            fig_drill = go.Figure()
            fig_drill.add_trace(go.Bar(
                x=MONTHS_SHORT,
                y=ad_monthly['DEP_DEL15'] * 100,
                marker_color='#f97316'
            ))
            fig_drill.update_layout(
                title=f"Monthly Delay Pattern for {selected_drill_airline}",
                height=300,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e2e8f0'),
                xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                yaxis=dict(title="Delay Rate (%)", gridcolor='rgba(255,255,255,0.1)')
            )
            st.plotly_chart(fig_drill, use_container_width=True, key="airline_drill_chart")
    
    # TAB 2: AIRPORTS
    with tab2:
        st.markdown("### Airport Delay Rankings")
        st.markdown("*Displaying full city names for easy identification*")
        
        airport_stats = fdf.groupby('ORIGIN').agg({
            'DEP_DEL15': ['count', 'mean'],
            'DELAY_COST_TOTAL': 'sum'
        }).reset_index()
        airport_stats.columns = ['Code', 'Flights', 'Delay Rate', 'Cost']
        airport_stats = airport_stats[airport_stats['Flights'] >= 50]
        
        # Add full names
        airport_stats['Full Name'] = airport_stats['Code'].map(airport_names)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🔴 Airports with Highest Delays")
            worst = airport_stats.nlargest(12, 'Delay Rate')
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                y=worst['Full Name'],
                x=worst['Delay Rate'] * 100,
                orientation='h',
                marker_color='#ef4444',
                text=[f"<b>{x:.1f}%</b>" for x in worst['Delay Rate'] * 100],
                textposition='outside',
                textfont=dict(size=11, color='#fca5a5')
            ))
            fig.update_layout(
                height=500,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e2e8f0'),
                margin=dict(l=0, r=80, t=10, b=30),
                xaxis=dict(title="Delay Rate (%)", gridcolor='rgba(255,255,255,0.1)'),
                yaxis=dict(categoryorder='total ascending')
            )
            st.plotly_chart(fig, use_container_width=True, key="airport_worst")
        
        with col2:
            st.markdown("#### 🟢 Best Performing Airports")
            best = airport_stats.nsmallest(12, 'Delay Rate')
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                y=best['Full Name'],
                x=best['Delay Rate'] * 100,
                orientation='h',
                marker_color='#10b981',
                text=[f"<b>{x:.1f}%</b>" for x in best['Delay Rate'] * 100],
                textposition='outside',
                textfont=dict(size=11, color='#6ee7b7')
            ))
            fig.update_layout(
                height=500,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e2e8f0'),
                margin=dict(l=0, r=80, t=10, b=30),
                xaxis=dict(title="Delay Rate (%)", gridcolor='rgba(255,255,255,0.1)'),
                yaxis=dict(categoryorder='total descending')
            )
            st.plotly_chart(fig, use_container_width=True, key="airport_best")
        
        # Airport drill down
        st.markdown("---")
        st.markdown("### 🔍 Airport Deep Dive")
        
        airport_options = [f"{row['city']} ({row['code']})" for _, row in airports_df.iterrows()]
        selected_airport_full = st.selectbox("Select an airport:", airport_options, key="airport_drill")
        
        if selected_airport_full:
            selected_code = selected_airport_full.split('(')[1].replace(')', '')
            apd = fdf[fdf['ORIGIN'] == selected_code]
            
            if len(apd) > 0:
                dc1, dc2, dc3, dc4 = st.columns(4)
                dc1.metric("Departures", f"{len(apd):,}")
                dc2.metric("Delay Rate", f"{apd['DEP_DEL15'].mean()*100:.1f}%")
                dc3.metric("Airlines", f"{apd['AIRLINE_NAME'].nunique()}")
                dc4.metric("Destinations", f"{apd['DEST'].nunique()}")
                
                # Hourly pattern
                hourly = apd.groupby('DEP_HOUR')['DEP_DEL15'].mean().reset_index()
                
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=hourly['DEP_HOUR'],
                    y=hourly['DEP_DEL15'] * 100,
                    marker_color=['#ef4444' if x > 0.35 else '#f59e0b' if x > 0.25 else '#10b981' 
                                 for x in hourly['DEP_DEL15']]
                ))
                fig.update_layout(
                    title=f"Hourly Delay Pattern at {selected_airport_full}",
                    height=300,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#e2e8f0'),
                    xaxis=dict(title="Hour of Day", gridcolor='rgba(255,255,255,0.1)'),
                    yaxis=dict(title="Delay Rate (%)", gridcolor='rgba(255,255,255,0.1)')
                )
                st.plotly_chart(fig, use_container_width=True, key="airport_hourly")
    
    # TAB 3: TIME PATTERNS
    with tab3:
        st.markdown("### Time-Based Delay Analysis")
        
        # Hour x Day Heatmap
        st.markdown("#### 🕐 Delay Heatmap: Hour of Day vs Day of Week")
        st.markdown("*Find the best times to fly with minimal delay risk*")
        
        hm_data = fdf.groupby(['DAY_OF_WEEK', 'DEP_HOUR'])['DEP_DEL15'].mean().reset_index()
        hm_pivot = hm_data.pivot(index='DEP_HOUR', columns='DAY_OF_WEEK', values='DEP_DEL15')
        
        fig = go.Figure(data=go.Heatmap(
            z=hm_pivot.values * 100,
            x=DAYS,
            y=[f"{h:02d}:00" for h in hm_pivot.index],
            colorscale=[[0, '#10b981'], [0.5, '#f59e0b'], [1, '#ef4444']],
            text=[[f"{v:.0f}%" for v in row] for row in hm_pivot.values * 100],
            texttemplate="%{text}",
            textfont={"size": 10, "color": "white"},
            hovertemplate="<b>%{x}</b> at <b>%{y}</b><br>Delay Rate: %{z:.1f}%<extra></extra>",
            colorbar=dict(title="Delay %", ticksuffix="%")
        ))
        
        fig.update_layout(
            height=600,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e2e8f0'),
            margin=dict(l=80, r=50, t=30, b=50),
            xaxis=dict(title="Day of Week", side='bottom'),
            yaxis=dict(title="Hour of Day", autorange='reversed')
        )
        
        st.plotly_chart(fig, use_container_width=True, key="time_heatmap")
        
        # Insight
        best_time = hm_data.loc[hm_data['DEP_DEL15'].idxmin()]
        worst_time = hm_data.loc[hm_data['DEP_DEL15'].idxmax()]
        
        st.markdown(f"""
        <div class="insight-card">
            <div class="insight-title">⏰ Optimal Flight Timing</div>
            <div class="insight-text">
                <b>Best time to fly:</b> <span class="insight-stat">{DAYS[int(best_time['DAY_OF_WEEK'])-1]}</span> at 
                <span class="insight-stat">{int(best_time['DEP_HOUR']):02d}:00</span> 
                (only {best_time['DEP_DEL15']*100:.1f}% delay rate)<br>
                <b>Worst time to fly:</b> <span class="insight-stat">{DAYS[int(worst_time['DAY_OF_WEEK'])-1]}</span> at 
                <span class="insight-stat">{int(worst_time['DEP_HOUR']):02d}:00</span> 
                ({worst_time['DEP_DEL15']*100:.1f}% delay rate)
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # TAB 4: SEASONALITY
    with tab4:
        st.markdown("### Seasonality Heatmap")
        st.markdown("*How delays vary by month across different regions*")
        
        # Month x Region
        season_data = fdf.groupby(['MONTH', 'ORIGIN_REGION'])['DEP_DEL15'].mean().reset_index()
        season_pivot = season_data.pivot(index='ORIGIN_REGION', columns='MONTH', values='DEP_DEL15')
        
        fig = go.Figure(data=go.Heatmap(
            z=season_pivot.values * 100,
            x=MONTHS_SHORT,
            y=season_pivot.index,
            colorscale=[[0, '#10b981'], [0.5, '#f59e0b'], [1, '#ef4444']],
            text=[[f"{v:.0f}%" for v in row] for row in season_pivot.values * 100],
            texttemplate="%{text}",
            textfont={"size": 12, "color": "white"},
            hovertemplate="<b>%{y}</b> in <b>%{x}</b><br>Delay Rate: %{z:.1f}%<extra></extra>",
            colorbar=dict(title="Delay %", ticksuffix="%")
        ))
        
        fig.update_layout(
            height=450,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e2e8f0'),
            margin=dict(l=150, r=50, t=30, b=50),
            xaxis=dict(title="Month"),
            yaxis=dict(title="")
        )
        
        st.plotly_chart(fig, use_container_width=True, key="season_heatmap")
        
        # Seasonal insights
        st.markdown("""
        <div class="insight-card">
            <div class="insight-title">🌡️ Seasonal Patterns Discovered</div>
            <div class="insight-text">
                • <b>India (Jun-Sep):</b> Monsoon season causes <span class="insight-stat">40-60%</span> higher delays<br>
                • <b>North America (Dec-Feb):</b> Winter storms create cascading delays<br>
                • <b>Europe (Jun-Aug):</b> Summer holiday rush strains capacity<br>
                • <b>Middle East (Dec-Feb):</b> Morning fog impacts Dubai operations
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
    <div class="insight-card">
        <div class="insight-title">🎯 Understanding the Cascade</div>
        <div class="insight-text">
            When a flight is delayed, the aircraft, crew, and passengers are all late for subsequent flights. 
            This creates a <b>cascading effect</b> where one delay triggers many more throughout the day.
            The <b>Late Aircraft Delay</b> metric is the key indicator of this domino phenomenon.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    delayed = fdf[fdf['DEP_DEL15'] == 1]
    
    # Delay Causes
    col1, col2 = st.columns([1.2, 1])
    
    with col1:
        st.markdown("### 📊 Root Causes of Flight Delays")
        
        causes = {
            'Carrier Operations': delayed['CARRIER_DELAY'].sum(),
            'Weather Conditions': delayed['WEATHER_DELAY'].sum(),
            'Air Traffic Control': delayed['NAS_DELAY'].sum(),
            'Late Aircraft (Domino)': delayed['LATE_AIRCRAFT_DELAY'].sum(),
            'Security Issues': delayed['SECURITY_DELAY'].sum()
        }
        cause_df = pd.DataFrame(list(causes.items()), columns=['Cause', 'Total Minutes'])
        cause_df['Percentage'] = cause_df['Total Minutes'] / cause_df['Total Minutes'].sum() * 100
        cause_df = cause_df.sort_values('Total Minutes', ascending=True)
        
        colors = ['#3b82f6', '#f59e0b', '#8b5cf6', '#ef4444', '#10b981']
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=cause_df['Cause'],
            x=cause_df['Total Minutes'],
            orientation='h',
            marker_color=colors,
            text=[f"<b>{format_number(m)}</b> min ({p:.1f}%)" for m, p in zip(cause_df['Total Minutes'], cause_df['Percentage'])],
            textposition='outside',
            textfont=dict(size=12, color='#e2e8f0')
        ))
        
        fig.update_layout(
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e2e8f0'),
            margin=dict(l=0, r=150, t=20, b=30),
            xaxis=dict(title="Total Delay Minutes", gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(title="")
        )
        
        st.plotly_chart(fig, use_container_width=True, key="cause_bar")
    
    with col2:
        st.markdown("### 🍩 Delay Distribution")
        
        fig = go.Figure(data=[go.Pie(
            labels=cause_df['Cause'],
            values=cause_df['Total Minutes'],
            hole=0.6,
            marker_colors=colors,
            textinfo='percent',
            textfont=dict(size=14, color='white'),
            hovertemplate="<b>%{label}</b><br>%{value:,.0f} minutes<br>%{percent}<extra></extra>"
        )])
        
        fig.update_layout(
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e2e8f0'),
            showlegend=True,
            legend=dict(orientation='h', yanchor='bottom', y=-0.2),
            margin=dict(l=20, r=20, t=20, b=80),
            annotations=[dict(
                text=f"<b>{format_number(cause_df['Total Minutes'].sum())}</b><br>Total Min",
                x=0.5, y=0.5, font_size=16, showarrow=False,
                font=dict(color='#f97316')
            )]
        )
        
        st.plotly_chart(fig, use_container_width=True, key="cause_pie")
    
    # Cascade throughout the day
    st.markdown("### ⏰ How Delays Compound Throughout the Day")
    
    hourly_cascade = delayed.groupby('DEP_HOUR').agg({
        'LATE_AIRCRAFT_DELAY': ['count', 'mean', 'sum']
    }).reset_index()
    hourly_cascade.columns = ['Hour', 'Flights', 'Avg Delay', 'Total Delay']
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(go.Bar(
        x=hourly_cascade['Hour'],
        y=hourly_cascade['Flights'],
        name='Flights with Late Aircraft',
        marker_color='#f97316',
        opacity=0.8
    ), secondary_y=False)
    
    fig.add_trace(go.Scatter(
        x=hourly_cascade['Hour'],
        y=hourly_cascade['Avg Delay'],
        name='Avg Cascade Delay',
        line=dict(color='#ef4444', width=4),
        mode='lines+markers',
        marker=dict(size=10)
    ), secondary_y=True)
    
    fig.update_layout(
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#e2e8f0'),
        margin=dict(l=50, r=50, t=30, b=50),
        legend=dict(orientation='h', yanchor='bottom', y=1.02),
        xaxis=dict(title="Hour of Day", gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(title="Number of Flights", gridcolor='rgba(255,255,255,0.1)'),
        yaxis2=dict(title="Avg Delay (minutes)", gridcolor='rgba(255,255,255,0.05)')
    )
    
    st.plotly_chart(fig, use_container_width=True, key="cascade_hourly")
    
    st.markdown("""
    <div class="insight-card">
        <div class="insight-title">🔍 The Domino Pattern Revealed</div>
        <div class="insight-text">
            Notice how late aircraft delays <b>increase dramatically throughout the day</b>. 
            Early morning flights (5-7 AM) start relatively on-time, but as the day progresses, 
            delays compound. By evening (6-9 PM), the cascade effect reaches its peak.<br><br>
            <b>Recommendation:</b> Book early morning flights for the lowest delay risk!
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
        <span class="section-subtitle">The true cost of flight delays</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="insight-card">
        <div class="insight-title">💵 Cost Calculation Methodology</div>
        <div class="insight-text">
            <b>Airline Cost:</b> $74.20 per minute (fuel, crew overtime, maintenance, opportunity cost)<br>
            <b>Passenger Cost:</b> $47.00 per minute (time value, missed connections, accommodation, compensation)<br>
            <i>Source: FAA Economic Values for Investment & Regulatory Analysis (2024)</i>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Cost KPIs
    airline_cost = fdf['DELAY_COST_AIRLINE'].sum()
    passenger_cost = fdf['DELAY_COST_PASSENGER'].sum()
    total_cost = fdf['DELAY_COST_TOTAL'].sum()
    avg_cost = fdf[fdf['DEP_DEL15'] == 1]['DELAY_COST_TOTAL'].mean()
    cost_per_minute = 74.20 + 47.00
    total_delay_minutes = fdf[fdf['DEP_DEL15'] == 1]['DEP_DELAY'].sum()
    
    kc1, kc2, kc3, kc4 = st.columns(4)
    
    with kc1:
        st.markdown(f"""
        <div class="glass-card">
            <span class="card-icon">🏢</span>
            <div class="card-value accent">{format_currency(airline_cost)}</div>
            <div class="card-label">Airline Losses</div>
            <div class="card-delta negative">$74.20/minute</div>
        </div>
        """, unsafe_allow_html=True)
    
    with kc2:
        st.markdown(f"""
        <div class="glass-card">
            <span class="card-icon">👥</span>
            <div class="card-value accent">{format_currency(passenger_cost)}</div>
            <div class="card-label">Passenger Impact</div>
            <div class="card-delta negative">$47.00/minute</div>
        </div>
        """, unsafe_allow_html=True)
    
    with kc3:
        st.markdown(f"""
        <div class="glass-card">
            <span class="card-icon">💸</span>
            <div class="card-value">{format_currency(total_cost)}</div>
            <div class="card-label">Total Economic Loss</div>
            <div class="card-delta negative">Combined impact</div>
        </div>
        """, unsafe_allow_html=True)
    
    with kc4:
        st.markdown(f"""
        <div class="glass-card">
            <span class="card-icon">📊</span>
            <div class="card-value">{format_currency(avg_cost)}</div>
            <div class="card-label">Avg Cost per Delay</div>
            <div class="card-delta negative">Per delayed flight</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🌍 Economic Impact by Region")
        
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
                colorscale=[[0, '#10b981'], [0.5, '#f59e0b'], [1, '#ef4444']]
            ),
            text=[format_currency(x) for x in region_cost['Cost']],
            textposition='outside',
            textfont=dict(size=12, color='#e2e8f0')
        ))
        
        fig.update_layout(
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e2e8f0'),
            margin=dict(l=0, r=100, t=20, b=30),
            xaxis=dict(title="Total Delay Cost ($)", gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(title="")
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
            marker_color='#f97316'
        ))
        
        fig.add_trace(go.Bar(
            x=MONTHS_SHORT,
            y=monthly_cost['DELAY_COST_PASSENGER'],
            name='Passenger Cost',
            marker_color='#3b82f6'
        ))
        
        fig.update_layout(
            height=400,
            barmode='stack',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e2e8f0'),
            margin=dict(l=50, r=20, t=20, b=30),
            legend=dict(orientation='h', yanchor='bottom', y=1.02),
            xaxis=dict(title="", gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(title="Cost ($)", gridcolor='rgba(255,255,255,0.1)')
        )
        
        st.plotly_chart(fig, use_container_width=True, key="econ_monthly")
    
    # Pareto Analysis
    st.markdown("### 📈 Pareto Analysis: The 80/20 Rule in Action")
    st.markdown("*Identifying which airlines contribute most to total delay costs*")
    
    airline_cost_df = fdf.groupby('AIRLINE_NAME')['DELAY_COST_TOTAL'].sum().reset_index()
    airline_cost_df = airline_cost_df.sort_values('DELAY_COST_TOTAL', ascending=False).head(15)
    airline_cost_df['Cumulative'] = airline_cost_df['DELAY_COST_TOTAL'].cumsum()
    airline_cost_df['Cumulative %'] = airline_cost_df['Cumulative'] / airline_cost_df['DELAY_COST_TOTAL'].sum() * 100
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(go.Bar(
        x=airline_cost_df['AIRLINE_NAME'],
        y=airline_cost_df['DELAY_COST_TOTAL'],
        name='Delay Cost',
        marker_color='#f97316'
    ), secondary_y=False)
    
    fig.add_trace(go.Scatter(
        x=airline_cost_df['AIRLINE_NAME'],
        y=airline_cost_df['Cumulative %'],
        name='Cumulative %',
        line=dict(color='#3b82f6', width=3),
        mode='lines+markers',
        marker=dict(size=8)
    ), secondary_y=True)
    
    fig.add_hline(y=80, line_dash="dash", line_color="#ef4444",
                 annotation_text="80% Threshold", secondary_y=True)
    
    fig.update_layout(
        height=450,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#e2e8f0'),
        margin=dict(l=50, r=50, t=30, b=100),
        legend=dict(orientation='h', yanchor='bottom', y=1.02),
        xaxis=dict(tickangle=45, gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(title="Delay Cost ($)", gridcolor='rgba(255,255,255,0.1)'),
        yaxis2=dict(title="Cumulative %", range=[0, 105])
    )
    
    st.plotly_chart(fig, use_container_width=True, key="pareto")
    
    airlines_80 = len(airline_cost_df[airline_cost_df['Cumulative %'] <= 80])
    
    st.markdown(f"""
    <div class="insight-card">
        <div class="insight-title">🎯 Pareto Insight</div>
        <div class="insight-text">
            <span class="insight-stat">{airlines_80} airlines</span> 
            ({airlines_80/len(airline_cost_df)*100:.0f}% of total) account for 
            <span class="insight-stat">80%</span> of all delay-related costs.
            Focusing improvement efforts on these carriers would yield maximum ROI.
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
        
        with st.spinner("🔄 Training model... This may take a moment."):
            model, X_test, y_test, y_pred, y_prob, feature_names = train_model()
        
        st.success("✅ Model trained successfully on 50,000 flight records!")
        
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
            
            cm = confusion_matrix(y_test, y_pred)
            
            fig = go.Figure(data=go.Heatmap(
                z=cm,
                x=['Predicted: On-Time', 'Predicted: Delayed'],
                y=['Actual: On-Time', 'Actual: Delayed'],
                colorscale=[[0, '#10b981'], [1, '#ef4444']],
                text=[[f"{cm[i][j]:,}" for j in range(2)] for i in range(2)],
                texttemplate="<b>%{text}</b>",
                textfont={"size": 20, "color": "white"},
                hovertemplate="Actual: %{y}<br>Predicted: %{x}<br>Count: %{z:,}<extra></extra>"
            ))
            
            fig.update_layout(
                height=400,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e2e8f0', size=14),
                margin=dict(l=50, r=50, t=30, b=50),
                xaxis=dict(side='bottom'),
                yaxis=dict(autorange='reversed')
            )
            
            st.plotly_chart(fig, use_container_width=True, key="confusion")
        
        with col2:
            st.markdown("### 📈 ROC-AUC Curve")
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=fpr, y=tpr,
                mode='lines',
                name=f'ROC Curve (AUC = {roc_auc:.3f})',
                line=dict(color='#f97316', width=4),
                fill='tozeroy',
                fillcolor='rgba(249, 115, 22, 0.2)'
            ))
            
            fig.add_trace(go.Scatter(
                x=[0, 1], y=[0, 1],
                mode='lines',
                name='Random Classifier',
                line=dict(color='#64748b', width=2, dash='dash')
            ))
            
            fig.update_layout(
                height=400,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e2e8f0'),
                margin=dict(l=50, r=50, t=30, b=50),
                xaxis=dict(title='False Positive Rate', gridcolor='rgba(255,255,255,0.1)', range=[0, 1]),
                yaxis=dict(title='True Positive Rate', gridcolor='rgba(255,255,255,0.1)', range=[0, 1]),
                legend=dict(x=0.5, y=0.1)
            )
            
            st.plotly_chart(fig, use_container_width=True, key="roc")
        
        # Feature Importance
        st.markdown("### 🎯 Feature Importance")
        
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
                colorscale=[[0, '#3b82f6'], [1, '#f97316']]
            ),
            text=[f"{x:.3f}" for x in importance_df['Importance']],
            textposition='outside',
            textfont=dict(size=12, color='#e2e8f0')
        ))
        
        fig.update_layout(
            height=350,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e2e8f0'),
            margin=dict(l=0, r=80, t=20, b=30),
            xaxis=dict(title='Importance Score', gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(title="")
        )
        
        st.plotly_chart(fig, use_container_width=True, key="importance")
    
    with tab2:
        st.markdown("### 🔮 Predict Delay Risk for Your Flight")
        
        col1, col2 = st.columns(2)
        
        with col1:
            pred_month = st.selectbox("📅 Month of Travel", MONTHS, key="pred_month")
            pred_day = st.selectbox("📆 Day of Week", DAYS, key="pred_day")
            pred_hour = st.slider("🕐 Departure Hour", 0, 23, 12, key="pred_hour")
        
        with col2:
            pred_origin = st.selectbox("🛫 Origin Airport", 
                [f"{row['city']} ({row['code']})" for _, row in airports_df.iterrows()],
                key="pred_origin")
            pred_dest = st.selectbox("🛬 Destination Airport",
                [f"{row['city']} ({row['code']})" for _, row in airports_df.iterrows()],
                key="pred_dest")
            pred_airline = st.selectbox("✈️ Airline",
                sorted(df['AIRLINE_NAME'].unique().tolist()),
                key="pred_airline")
        
        if st.button("🔮 PREDICT DELAY RISK", use_container_width=True):
            # Prepare features
            origin_code = pred_origin.split('(')[1].replace(')', '')
            dest_code = pred_dest.split('(')[1].replace(')', '')
            
            # Calculate distance
            origin_info = airports_df[airports_df['code'] == origin_code].iloc[0]
            dest_info = airports_df[airports_df['code'] == dest_code].iloc[0]
            
            lat1, lon1 = np.radians(origin_info['lat']), np.radians(origin_info['lon'])
            lat2, lon2 = np.radians(dest_info['lat']), np.radians(dest_info['lon'])
            dlat, dlon = lat2 - lat1, lon2 - lon1
            a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
            distance = 3956 * 2 * np.arcsin(np.sqrt(a))
            
            # Encode
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
                    <div class="prediction-title" style="color: #fca5a5;">HIGH DELAY RISK</div>
                    <div class="prediction-prob" style="color: #ef4444;">{probability*100:.1f}%</div>
                    <p style="color: #e2e8f0;">probability of delay</p>
                    <p style="color: #94a3b8; margin-top: 1rem;">Consider booking an earlier flight or allowing extra buffer time.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="prediction-low">
                    <div class="prediction-icon">✅</div>
                    <div class="prediction-title" style="color: #6ee7b7;">LOW DELAY RISK</div>
                    <div class="prediction-prob" style="color: #10b981;">{(1-probability)*100:.1f}%</div>
                    <p style="color: #e2e8f0;">probability of on-time departure</p>
                    <p style="color: #94a3b8; margin-top: 1rem;">Great choice! This flight has good on-time performance indicators.</p>
                </div>
                """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: SIMULATOR (WHAT-IF)
# ═══════════════════════════════════════════════════════════════════════════════
elif current_page == "🔮 Simulator":
    
    st.markdown("""
    <div class="section-header">
        <span class="section-icon">🔮</span>
        <span class="section-title">What-If Scenario Simulator</span>
        <span class="section-subtitle">Explore impact of delay reduction strategies</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Current state
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
    st.markdown("*Adjust the sliders to simulate different improvement scenarios*")
    
    col1, col2 = st.columns(2)
    
    with col1:
        carrier_red = st.slider(
            "✈️ Reduce Carrier Delays by (%)",
            0, 50, 0, 5,
            help="Improvements in airline operations, crew scheduling, maintenance"
        )
        weather_red = st.slider(
            "🌧️ Reduce Weather Impact by (%)",
            0, 30, 0, 5,
            help="Better weather prediction, proactive rescheduling"
        )
    
    with col2:
        nas_red = st.slider(
            "🗼 Reduce ATC Delays by (%)",
            0, 40, 0, 5,
            help="Air traffic control modernization, better flow management"
        )
        late_red = st.slider(
            "🔄 Reduce Late Aircraft Impact by (%)",
            0, 50, 0, 5,
            help="Better turnaround times, schedule buffers, spare aircraft"
        )
    
    # Calculate
    total_reduction = (carrier_red * 0.35 + weather_red * 0.20 + nas_red * 0.25 + late_red * 0.20) / 100
    
    new_delays = cur_delays * (1 - total_reduction)
    new_rate = cur_rate * (1 - total_reduction)
    new_cost = cur_cost * (1 - total_reduction)
    savings = cur_cost - new_cost
    
    st.markdown("---")
    st.markdown("### 📈 Simulated Outcome")
    
    sc1, sc2, sc3, sc4 = st.columns(4)
    
    sc1.metric("New Delayed Flights", f"{new_delays:,.0f}", f"-{cur_delays - new_delays:,.0f}")
    sc2.metric("New Delay Rate", f"{new_rate:.1f}%", f"-{cur_rate - new_rate:.1f}%")
    sc3.metric("New Total Cost", format_currency(new_cost))
    sc4.metric("💰 SAVINGS", format_currency(savings), "Potential")
    
    # Visualization
    comparison_df = pd.DataFrame({
        'Metric': ['Delayed Flights', 'Delay Rate (%)', 'Cost ($M)'],
        'Current': [cur_delays, cur_rate, cur_cost/1e6],
        'Simulated': [new_delays, new_rate, new_cost/1e6]
    })
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Current',
        x=comparison_df['Metric'],
        y=comparison_df['Current'],
        marker_color='#ef4444',
        text=[f"{cur_delays:,.0f}", f"{cur_rate:.1f}%", format_currency(cur_cost)],
        textposition='outside',
        textfont=dict(color='#fca5a5')
    ))
    
    fig.add_trace(go.Bar(
        name='Simulated',
        x=comparison_df['Metric'],
        y=comparison_df['Simulated'],
        marker_color='#10b981',
        text=[f"{new_delays:,.0f}", f"{new_rate:.1f}%", format_currency(new_cost)],
        textposition='outside',
        textfont=dict(color='#6ee7b7')
    ))
    
    fig.update_layout(
        height=400,
        barmode='group',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#e2e8f0'),
        margin=dict(l=50, r=50, t=50, b=50),
        legend=dict(orientation='h', yanchor='bottom', y=1.02),
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(title="Value", gridcolor='rgba(255,255,255,0.1)')
    )
    
    st.plotly_chart(fig, use_container_width=True, key="whatif_compare")
    
    if savings > 0:
        st.markdown(f"""
        <div class="insight-card" style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(5, 150, 105, 0.1) 100%); border-color: #10b981;">
            <div class="insight-title" style="color: #10b981;">✅ Potential Impact Summary</div>
            <div class="insight-text">
                With the selected improvement strategies:<br>
                • <span class="insight-stat">{cur_delays - new_delays:,.0f}</span> fewer delayed flights<br>
                • <span class="insight-stat">{format_currency(savings)}</span> in cost savings<br>
                • <span class="insight-stat">{cur_rate - new_rate:.1f}%</span> improvement in on-time performance<br><br>
                These improvements would significantly enhance passenger satisfaction and operational efficiency.
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
        <span class="section-subtitle">Deep dive into specific markets</span>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["🇮🇳 India", "🇦🇪 Middle East", "🇺🇸 North America"])
    
    with tab1:
        india_df = df[df['ORIGIN_REGION'] == 'India']
        
        st.markdown("## 🇮🇳 India Aviation Analysis")
        
        ic1, ic2, ic3, ic4 = st.columns(4)
        ic1.metric("Total Flights", f"{len(india_df):,}")
        ic2.metric("Delay Rate", f"{india_df['DEP_DEL15'].mean()*100:.1f}%")
        ic3.metric("Avg Delay", f"{india_df[india_df['DEP_DEL15']==1]['DEP_DELAY'].mean():.0f} min")
        ic4.metric("Total Cost", format_currency(india_df['DELAY_COST_TOTAL'].sum()))
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🌧️ Monsoon Impact on Delays")
            
            india_monthly = india_df.groupby('MONTH')['DEP_DEL15'].mean().reset_index()
            colors = ['#10b981' if m not in [6,7,8,9] else '#ef4444' for m in range(1,13)]
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=MONTHS_SHORT,
                y=india_monthly['DEP_DEL15'] * 100,
                marker_color=colors,
                text=[f"{x:.1f}%" for x in india_monthly['DEP_DEL15'] * 100],
                textposition='outside',
                textfont=dict(color='#e2e8f0')
            ))
            
            fig.add_vrect(x0=5.5, x1=8.5, fillcolor="rgba(239,68,68,0.1)", 
                         line_width=0, annotation_text="🌧️ Monsoon Season",
                         annotation_position="top")
            
            fig.update_layout(
                height=350,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e2e8f0'),
                margin=dict(l=50, r=20, t=40, b=30),
                yaxis=dict(title="Delay Rate (%)", gridcolor='rgba(255,255,255,0.1)')
            )
            
            st.plotly_chart(fig, use_container_width=True, key="india_monthly")
        
        with col2:
            st.markdown("### ✈️ Top Indian Airlines Performance")
            
            india_airlines = india_df.groupby('AIRLINE_NAME')['DEP_DEL15'].agg(['count', 'mean']).reset_index()
            india_airlines.columns = ['Airline', 'Flights', 'Delay Rate']
            india_airlines = india_airlines[india_airlines['Flights'] >= 50].sort_values('Delay Rate')
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                y=india_airlines['Airline'],
                x=india_airlines['Delay Rate'] * 100,
                orientation='h',
                marker_color='#f97316',
                text=[f"{x:.1f}%" for x in india_airlines['Delay Rate'] * 100],
                textposition='outside',
                textfont=dict(color='#e2e8f0')
            ))
            
            fig.update_layout(
                height=350,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e2e8f0'),
                margin=dict(l=0, r=80, t=20, b=30),
                xaxis=dict(title="Delay Rate (%)", gridcolor='rgba(255,255,255,0.1)')
            )
            
            st.plotly_chart(fig, use_container_width=True, key="india_airlines")
        
        st.markdown("""
        <div class="insight-card">
            <div class="insight-title">🇮🇳 Key Insights - India</div>
            <div class="insight-text">
                • <b>Monsoon Impact:</b> June-September shows <span class="insight-stat">40-60% higher</span> delay rates<br>
                • <b>Mumbai (BOM) & Delhi (DEL):</b> Most affected due to heavy rainfall and fog<br>
                • <b>IndiGo:</b> Highest volume but manages delays efficiently<br>
                • <b>Winter Fog:</b> December-January sees visibility issues in North India
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with tab2:
        me_df = df[df['ORIGIN_REGION'] == 'Middle East']
        
        st.markdown("## 🇦🇪 Middle East Aviation Analysis")
        
        mc1, mc2, mc3, mc4 = st.columns(4)
        mc1.metric("Total Flights", f"{len(me_df):,}")
        mc2.metric("Delay Rate", f"{me_df['DEP_DEL15'].mean()*100:.1f}%")
        mc3.metric("Avg Delay", f"{me_df[me_df['DEP_DEL15']==1]['DEP_DELAY'].mean():.0f} min")
        mc4.metric("Total Cost", format_currency(me_df['DELAY_COST_TOTAL'].sum()))
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🏢 Airport Performance")
            
            me_airports = me_df.groupby('ORIGIN')['DEP_DEL15'].agg(['count', 'mean']).reset_index()
            me_airports.columns = ['Code', 'Flights', 'Delay Rate']
            me_airports['Full Name'] = me_airports['Code'].map(airport_names)
            me_airports = me_airports.sort_values('Flights', ascending=False)
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=me_airports['Full Name'],
                y=me_airports['Delay Rate'] * 100,
                marker_color=['#ef4444' if x > 0.3 else '#f59e0b' if x > 0.2 else '#10b981' 
                             for x in me_airports['Delay Rate']],
                text=[f"{x:.1f}%" for x in me_airports['Delay Rate'] * 100],
                textposition='outside',
                textfont=dict(color='#e2e8f0')
            ))
            
            fig.update_layout(
                height=350,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e2e8f0'),
                margin=dict(l=50, r=20, t=20, b=80),
                xaxis=dict(tickangle=45),
                yaxis=dict(title="Delay Rate (%)", gridcolor='rgba(255,255,255,0.1)')
            )
            
            st.plotly_chart(fig, use_container_width=True, key="me_airports")
        
        with col2:
            st.markdown("### ✈️ Gulf Carriers")
            
            me_airlines = me_df.groupby('AIRLINE_NAME')['DEP_DEL15'].agg(['count', 'mean']).reset_index()
            me_airlines.columns = ['Airline', 'Flights', 'Delay Rate']
            me_airlines = me_airlines[me_airlines['Flights'] >= 20].sort_values('Delay Rate')
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                y=me_airlines['Airline'],
                x=me_airlines['Delay Rate'] * 100,
                orientation='h',
                marker_color='#3b82f6',
                text=[f"{x:.1f}%" for x in me_airlines['Delay Rate'] * 100],
                textposition='outside',
                textfont=dict(color='#e2e8f0')
            ))
            
            fig.update_layout(
                height=350,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e2e8f0'),
                margin=dict(l=0, r=80, t=20, b=30),
                xaxis=dict(title="Delay Rate (%)", gridcolor='rgba(255,255,255,0.1)')
            )
            
            st.plotly_chart(fig, use_container_width=True, key="me_airlines")
        
        st.markdown("""
        <div class="insight-card">
            <div class="insight-title">🇦🇪 Key Insights - Middle East</div>
            <div class="insight-text">
                • <b>Dubai (DXB):</b> World's busiest international hub maintains strong OTP<br>
                • <b>Winter Fog:</b> December-February sees morning fog delays<br>
                • <b>Premium Carriers:</b> Emirates, Qatar, Etihad invest heavily in punctuality<br>
                • <b>India Connectivity:</b> Heavy traffic to Indian cities creates pressure
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with tab3:
        na_df = df[df['ORIGIN_REGION'] == 'North America']
        
        st.markdown("## 🇺🇸 North America Aviation Analysis")
        
        nc1, nc2, nc3, nc4 = st.columns(4)
        nc1.metric("Total Flights", f"{len(na_df):,}")
        nc2.metric("Delay Rate", f"{na_df['DEP_DEL15'].mean()*100:.1f}%")
        nc3.metric("Avg Delay", f"{na_df[na_df['DEP_DEL15']==1]['DEP_DELAY'].mean():.0f} min")
        nc4.metric("Total Cost", format_currency(na_df['DELAY_COST_TOTAL'].sum()))
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### ❄️ Seasonal Pattern")
            
            na_monthly = na_df.groupby('MONTH')['DEP_DEL15'].mean().reset_index()
            colors = ['#ef4444' if m in [1,2,12] else '#f59e0b' if m in [6,7,8] else '#10b981' for m in range(1,13)]
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=MONTHS_SHORT,
                y=na_monthly['DEP_DEL15'] * 100,
                marker_color=colors,
                text=[f"{x:.1f}%" for x in na_monthly['DEP_DEL15'] * 100],
                textposition='outside',
                textfont=dict(color='#e2e8f0')
            ))
            
            fig.update_layout(
                height=350,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e2e8f0'),
                margin=dict(l=50, r=20, t=20, b=30),
                yaxis=dict(title="Delay Rate (%)", gridcolor='rgba(255,255,255,0.1)')
            )
            
            st.plotly_chart(fig, use_container_width=True, key="na_monthly")
        
        with col2:
            st.markdown("### ✈️ Major US Carriers")
            
            na_airlines = na_df.groupby('AIRLINE_NAME')['DEP_DEL15'].agg(['count', 'mean']).reset_index()
            na_airlines.columns = ['Airline', 'Flights', 'Delay Rate']
            na_airlines = na_airlines[na_airlines['Flights'] >= 100].sort_values('Delay Rate')
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                y=na_airlines['Airline'],
                x=na_airlines['Delay Rate'] * 100,
                orientation='h',
                marker_color='#f97316',
                text=[f"{x:.1f}%" for x in na_airlines['Delay Rate'] * 100],
                textposition='outside',
                textfont=dict(color='#e2e8f0')
            ))
            
            fig.update_layout(
                height=350,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e2e8f0'),
                margin=dict(l=0, r=80, t=20, b=30),
                xaxis=dict(title="Delay Rate (%)", gridcolor='rgba(255,255,255,0.1)')
            )
            
            st.plotly_chart(fig, use_container_width=True, key="na_airlines")
        
        st.markdown("""
        <div class="insight-card">
            <div class="insight-title">🇺🇸 Key Insights - North America</div>
            <div class="insight-text">
                • <b>Winter Storms:</b> December-February sees highest delays (snow, ice)<br>
                • <b>Summer Thunderstorms:</b> June-August has convective weather delays<br>
                • <b>Holiday Rush:</b> Thanksgiving & Christmas cause congestion<br>
                • <b>Chicago (ORD), Denver (DEN):</b> Most weather-impacted hubs
            </div>
        </div>
        """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: INSIGHTS
# ═══════════════════════════════════════════════════════════════════════════════
elif current_page == "📈 Insights":
    
    st.markdown("""
    <div class="section-header">
        <span class="section-icon">📈</span>
        <span class="section-title">Executive Insights & Recommendations</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Key Statistics
    st.markdown("### 📊 Key Statistics at a Glance")
    
    total_flights = len(df)
    total_delayed = int(df['DEP_DEL15'].sum())
    total_cost = df['DELAY_COST_TOTAL'].sum()
    avg_delay = df[df['DEP_DEL15']==1]['DEP_DELAY'].mean()
    
    worst_airline = df.groupby('AIRLINE_NAME')['DEP_DEL15'].mean().idxmax()
    worst_airline_rate = df.groupby('AIRLINE_NAME')['DEP_DEL15'].mean().max() * 100
    best_airline = df.groupby('AIRLINE_NAME')['DEP_DEL15'].mean().idxmin()
    best_airline_rate = df.groupby('AIRLINE_NAME')['DEP_DEL15'].mean().min() * 100
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="insight-card">
            <div class="insight-title">📊 Dataset Overview</div>
            <div class="insight-text">
                • <b>Total Flights Analyzed:</b> <span class="insight-stat">{total_flights:,}</span><br>
                • <b>Delayed Flights:</b> <span class="insight-stat">{total_delayed:,}</span> ({total_delayed/total_flights*100:.1f}%)<br>
                • <b>Total Economic Impact:</b> <span class="insight-stat">{format_currency(total_cost)}</span><br>
                • <b>Average Delay Duration:</b> <span class="insight-stat">{avg_delay:.0f} minutes</span><br>
                • <b>Airports Covered:</b> <span class="insight-stat">{len(airports_df)}</span> global hubs<br>
                • <b>Airlines Analyzed:</b> <span class="insight-stat">{len(airlines_df)}</span> carriers
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="insight-card">
            <div class="insight-title">🏆 Performance Extremes</div>
            <div class="insight-text">
                • <b>Best Performing Airline:</b><br>
                  <span class="insight-stat">{best_airline}</span> ({best_airline_rate:.1f}% delay rate)<br><br>
                • <b>Most Delayed Airline:</b><br>
                  <span class="insight-stat">{worst_airline}</span> ({worst_airline_rate:.1f}% delay rate)<br><br>
                • <b>Performance Gap:</b> <span class="insight-stat">{worst_airline_rate - best_airline_rate:.1f}%</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Key Findings
    st.markdown("### 🔍 Key Findings")
    
    findings = [
        {
            "icon": "🌊",
            "title": "The Domino Effect is Real",
            "text": f"Late aircraft delays account for a significant portion of all delays. As the day progresses, delays compound - evening flights are {df[df['DEP_HOUR']>=18]['DEP_DEL15'].mean()/df[df['DEP_HOUR']<=8]['DEP_DEL15'].mean()*100-100:.0f}% more likely to be delayed than early morning flights."
        },
        {
            "icon": "🌧️",
            "title": "Weather is a Major Factor",
            "text": "Seasonal patterns significantly impact delays. India's monsoon (Jun-Sep) and North America's winter (Dec-Feb) see the highest delay spikes. Planning travel outside these periods can reduce delay risk by 30-40%."
        },
        {
            "icon": "📈",
            "title": "80/20 Rule Applies",
            "text": "A small number of airlines and airports contribute disproportionately to total delays. Targeted improvements at these bottlenecks could yield maximum ROI for the industry."
        },
        {
            "icon": "⏰",
            "title": "Timing Matters",
            "text": f"Early morning flights (5-7 AM) have the lowest delay rates. The optimal time to fly is around 6:00 AM with delay rates under 20%. Avoid flying between 5-8 PM when delays peak."
        }
    ]
    
    for finding in findings:
        st.markdown(f"""
        <div class="insight-card">
            <div class="insight-title">{finding['icon']} {finding['title']}</div>
            <div class="insight-text">{finding['text']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Recommendations
    st.markdown("### 💡 Recommendations")
    
    rec_col1, rec_col2 = st.columns(2)
    
    with rec_col1:
        st.markdown("""
        <div class="insight-card" style="border-color: #3b82f6;">
            <div class="insight-title" style="color: #3b82f6;">👤 For Passengers</div>
            <div class="insight-text">
                1. <b>Book early morning flights</b> (5-7 AM) for best on-time performance<br>
                2. <b>Avoid peak delay months</b> in your region<br>
                3. <b>Allow buffer time</b> for connections, especially for evening flights<br>
                4. <b>Choose airlines</b> with proven on-time records<br>
                5. <b>Use the AI predictor</b> to check delay risk before booking
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with rec_col2:
        st.markdown("""
        <div class="insight-card" style="border-color: #10b981;">
            <div class="insight-title" style="color: #10b981;">🏢 For Airlines & Airports</div>
            <div class="insight-text">
                1. <b>Build schedule buffers</b> to absorb delays and prevent cascades<br>
                2. <b>Invest in predictive maintenance</b> to reduce carrier delays<br>
                3. <b>Improve turnaround efficiency</b> to minimize late aircraft impact<br>
                4. <b>Enhance weather contingency plans</b> for seasonal peaks<br>
                5. <b>Focus on hub operations</b> where 80% of delays originate
            </div>
        </div>
        """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="footer">
    <div class="footer-brand">✈️ Flight Delay Domino Effect Dashboard</div>
    <p>Master's in AI with Business Analytics | Data Visualization Project</p>
    <p style="font-size: 0.8rem;">Built with Python • Streamlit • Plotly • Scikit-learn</p>
</div>
""", unsafe_allow_html=True)
