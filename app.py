# ═══════════════════════════════════════════════════════════════════════════════
# ✈️ FLIGHT DELAY DOMINO EFFECT - PROFESSIONAL DASHBOARD
# Executive Boardroom Presentation Ready
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
from datetime import datetime, timedelta
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
# PREMIUM EXECUTIVE DARK THEME CSS
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    :root {
        --bg-primary: #0F0F1A;
        --bg-secondary: #1A1A2E;
        --bg-tertiary: #16213E;
        --bg-card: linear-gradient(145deg, #1A1A2E 0%, #0F0F1A 100%);
        
        --accent-purple: #8B5CF6;
        --accent-violet: #A78BFA;
        --accent-pink: #EC4899;
        --accent-rose: #F43F5E;
        --accent-emerald: #10B981;
        --accent-teal: #14B8A6;
        --accent-sky: #0EA5E9;
        --accent-amber: #F59E0B;
        --accent-orange: #F97316;
        
        --text-primary: #FFFFFF;
        --text-secondary: #E2E8F0;
        --text-muted: #94A3B8;
        --text-dim: #64748B;
        
        --border-subtle: rgba(139, 92, 246, 0.2);
        --border-accent: rgba(139, 92, 246, 0.4);
        
        --gradient-purple: linear-gradient(135deg, #8B5CF6 0%, #6366F1 100%);
        --gradient-pink: linear-gradient(135deg, #EC4899 0%, #F43F5E 100%);
        --gradient-emerald: linear-gradient(135deg, #10B981 0%, #14B8A6 100%);
        --gradient-sky: linear-gradient(135deg, #0EA5E9 0%, #6366F1 100%);
        --gradient-amber: linear-gradient(135deg, #F59E0B 0%, #F97316 100%);
    }
    
    /* ═══════════════ GLOBAL STYLES ═══════════════ */
    .stApp {
        background: linear-gradient(180deg, #0F0F1A 0%, #1A1A2E 40%, #16213E 70%, #0F0F1A 100%);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .main .block-container {
        padding: 0.8rem 2rem 2rem 2rem;
        max-width: 100%;
    }
    
    #MainMenu, footer, header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* ═══════════════ NAVIGATION BAR ═══════════════ */
    .navbar-container {
        background: linear-gradient(90deg, rgba(15, 15, 26, 0.98) 0%, rgba(26, 26, 46, 0.98) 100%);
        backdrop-filter: blur(20px);
        border-bottom: 1px solid rgba(139, 92, 246, 0.3);
        padding: 1rem 2rem;
        margin: -0.8rem -2rem 1.5rem -2rem;
        display: flex;
        align-items: center;
        gap: 20px;
    }
    
    .nav-logo {
        font-size: 2.2rem;
        filter: drop-shadow(0 0 15px rgba(139, 92, 246, 0.5));
    }
    
    .nav-title {
        font-size: 1.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #FFFFFF 0%, #E2E8F0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .nav-subtitle {
        font-size: 0.7rem;
        color: #8B5CF6;
        letter-spacing: 3px;
        text-transform: uppercase;
        font-weight: 600;
    }
    
    /* ═══════════════ NAVIGATION BUTTONS - ALL IDENTICAL ═══════════════ */
    .stButton > button {
        background: linear-gradient(145deg, rgba(26, 26, 46, 0.9) 0%, rgba(15, 15, 26, 0.95) 100%) !important;
        border: 1px solid rgba(139, 92, 246, 0.3) !important;
        border-radius: 10px !important;
        color: #E2E8F0 !important;
        font-weight: 500 !important;
        font-size: 0.85rem !important;
        padding: 0.5rem 0.8rem !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        white-space: nowrap !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(145deg, rgba(139, 92, 246, 0.2) 0%, rgba(99, 102, 241, 0.15) 100%) !important;
        border-color: rgba(139, 92, 246, 0.6) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(139, 92, 246, 0.2) !important;
        color: #FFFFFF !important;
    }
    
    .stButton > button:focus, .stButton > button:active {
        background: linear-gradient(135deg, #8B5CF6 0%, #6366F1 100%) !important;
        border-color: transparent !important;
        color: #FFFFFF !important;
        box-shadow: 0 0 20px rgba(139, 92, 246, 0.4) !important;
    }
    
    /* ═══════════════ HERO SECTION ═══════════════ */
    .hero-section {
        background: linear-gradient(145deg, rgba(26, 26, 46, 0.8) 0%, rgba(22, 33, 62, 0.6) 100%);
        border: 1px solid rgba(139, 92, 246, 0.25);
        border-radius: 20px;
        padding: 2.5rem 3rem;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, #8B5CF6, #EC4899, #F59E0B, #10B981, #8B5CF6);
        background-size: 200% 100%;
        animation: gradient-flow 4s linear infinite;
    }
    
    @keyframes gradient-flow {
        0% { background-position: 0% 50%; }
        100% { background-position: 200% 50%; }
    }
    
    .hero-title {
        font-size: 2.4rem;
        font-weight: 800;
        color: #FFFFFF;
        margin-bottom: 0.8rem;
        text-shadow: 0 2px 20px rgba(139, 92, 246, 0.3);
    }
    
    .hero-subtitle {
        font-size: 1.1rem;
        color: #CBD5E1;
        line-height: 1.7;
    }
    
    .hero-highlight {
        color: #A78BFA;
        font-weight: 700;
    }
    
    /* ═══════════════ GLASS CARDS ═══════════════ */
    .glass-card {
        background: linear-gradient(145deg, rgba(26, 26, 46, 0.7) 0%, rgba(15, 15, 26, 0.8) 100%);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(139, 92, 246, 0.15);
        border-radius: 16px;
        padding: 1.5rem;
        position: relative;
        overflow: hidden;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        border-color: rgba(139, 92, 246, 0.4);
        box-shadow: 0 20px 40px rgba(139, 92, 246, 0.15);
    }
    
    .glass-card.purple { border-left: 4px solid #8B5CF6; }
    .glass-card.pink { border-left: 4px solid #EC4899; }
    .glass-card.emerald { border-left: 4px solid #10B981; }
    .glass-card.amber { border-left: 4px solid #F59E0B; }
    .glass-card.sky { border-left: 4px solid #0EA5E9; }
    
    .card-icon {
        font-size: 1.8rem;
        margin-bottom: 0.6rem;
        display: block;
    }
    
    .card-value {
        font-size: 2rem;
        font-weight: 800;
        color: #FFFFFF;
        margin-bottom: 0.3rem;
    }
    
    .card-value.purple { color: #A78BFA; }
    .card-value.pink { color: #F472B6; }
    .card-value.emerald { color: #34D399; }
    .card-value.amber { color: #FBBF24; }
    .card-value.sky { color: #38BDF8; }
    
    .card-label {
        font-size: 0.8rem;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }
    
    .card-delta {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.72rem;
        font-weight: 600;
        margin-top: 0.5rem;
    }
    
    .card-delta.negative { background: rgba(244, 63, 94, 0.15); color: #FDA4AF; }
    .card-delta.positive { background: rgba(16, 185, 129, 0.15); color: #6EE7B7; }
    .card-delta.info { background: rgba(139, 92, 246, 0.15); color: #C4B5FD; }
    
    /* ═══════════════ SECTION HEADERS ═══════════════ */
    .section-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin: 2rem 0 1.2rem 0;
        padding-bottom: 0.8rem;
        border-bottom: 2px solid rgba(139, 92, 246, 0.3);
    }
    
    .section-icon { font-size: 1.4rem; }
    
    .section-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #FFFFFF;
        margin: 0;
    }
    
    /* ═══════════════ CHART EXPLAINER - VISIBLE ═══════════════ */
    .chart-explainer {
        font-size: 0.95rem;
        color: #CBD5E1;
        margin-bottom: 1rem;
        padding: 0.8rem 1rem;
        background: rgba(139, 92, 246, 0.1);
        border-left: 3px solid #8B5CF6;
        border-radius: 0 8px 8px 0;
    }
    
    /* ═══════════════ INSIGHT BOXES ═══════════════ */
    .insight-box {
        background: linear-gradient(145deg, rgba(139, 92, 246, 0.1) 0%, rgba(99, 102, 241, 0.05) 100%);
        border: 1px solid rgba(139, 92, 246, 0.3);
        border-left: 4px solid #8B5CF6;
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        margin: 1rem 0;
    }
    
    .insight-box.warning {
        background: linear-gradient(145deg, rgba(245, 158, 11, 0.1) 0%, rgba(249, 115, 22, 0.05) 100%);
        border-color: rgba(245, 158, 11, 0.3);
        border-left-color: #F59E0B;
    }
    
    .insight-box.success {
        background: linear-gradient(145deg, rgba(16, 185, 129, 0.1) 0%, rgba(20, 184, 166, 0.05) 100%);
        border-color: rgba(16, 185, 129, 0.3);
        border-left-color: #10B981;
    }
    
    .insight-box.danger {
        background: linear-gradient(145deg, rgba(244, 63, 94, 0.1) 0%, rgba(236, 72, 153, 0.05) 100%);
        border-color: rgba(244, 63, 94, 0.3);
        border-left-color: #F43F5E;
    }
    
    .insight-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: #A78BFA;
        margin-bottom: 0.6rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .insight-box.warning .insight-title { color: #FBBF24; }
    .insight-box.success .insight-title { color: #34D399; }
    .insight-box.danger .insight-title { color: #FB7185; }
    
    .insight-text {
        color: #E2E8F0;
        font-size: 0.95rem;
        line-height: 1.7;
    }
    
    .insight-stat {
        font-weight: 700;
        color: #C4B5FD;
    }
    
    .insight-box.warning .insight-stat { color: #FDE68A; }
    .insight-box.success .insight-stat { color: #6EE7B7; }
    .insight-box.danger .insight-stat { color: #FECDD3; }
    
    /* ═══════════════ TABS ═══════════════ */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(15, 15, 26, 0.6);
        border-radius: 12px;
        padding: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 8px;
        padding: 10px 20px;
        color: #94A3B8;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #8B5CF6 0%, #6366F1 100%);
        color: #FFFFFF;
    }
    
    /* ═══════════════ PREDICTION CARDS ═══════════════ */
    .prediction-high {
        background: linear-gradient(145deg, rgba(244, 63, 94, 0.15) 0%, rgba(239, 68, 68, 0.1) 100%);
        border: 2px solid rgba(244, 63, 94, 0.5);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
    }
    
    .prediction-low {
        background: linear-gradient(145deg, rgba(16, 185, 129, 0.15) 0%, rgba(20, 184, 166, 0.1) 100%);
        border: 2px solid rgba(16, 185, 129, 0.5);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
    }
    
    .prediction-icon { font-size: 3.5rem; margin-bottom: 0.8rem; }
    .prediction-title { font-size: 1.5rem; font-weight: 700; margin-bottom: 0.3rem; }
    .prediction-prob { font-size: 2.5rem; font-weight: 800; }
    
    /* ═══════════════ ERROR MESSAGE ═══════════════ */
    .error-box {
        background: linear-gradient(145deg, rgba(244, 63, 94, 0.15) 0%, rgba(239, 68, 68, 0.1) 100%);
        border: 1px solid rgba(244, 63, 94, 0.4);
        border-radius: 12px;
        padding: 1.2rem;
        margin: 1rem 0;
    }
    
    .error-title {
        color: #FB7185;
        font-weight: 700;
        font-size: 1rem;
        margin-bottom: 0.5rem;
    }
    
    .error-text {
        color: #FDA4AF;
        font-size: 0.9rem;
    }
    
    /* ═══════════════ METRICS ═══════════════ */
    [data-testid="stMetricValue"] {
        font-size: 1.6rem;
        color: #A78BFA;
    }
    
    /* ═══════════════ SLIDERS ═══════════════ */
    .stSlider > div > div > div {
        background: linear-gradient(90deg, #8B5CF6 0%, #EC4899 100%);
    }
    
    /* ═══════════════ SELECT BOX ═══════════════ */
    .stSelectbox > div > div {
        background: rgba(26, 26, 46, 0.8);
        border: 1px solid rgba(139, 92, 246, 0.2);
        border-radius: 10px;
    }
    
    /* ═══════════════ DATE INPUT ═══════════════ */
    .stDateInput > div > div {
        background: rgba(26, 26, 46, 0.8);
        border: 1px solid rgba(139, 92, 246, 0.2);
        border-radius: 10px;
    }
    
    /* ═══════════════ FOOTER ═══════════════ */
    .footer {
        text-align: center;
        padding: 2rem;
        margin-top: 2rem;
        border-top: 1px solid rgba(139, 92, 246, 0.2);
    }
    
    .footer-brand {
        font-size: 1.2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #8B5CF6, #EC4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .footer-text {
        color: #64748B;
        font-size: 0.85rem;
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

# Color palette for charts
COLORS = {
    'purple': '#8B5CF6',
    'violet': '#A78BFA',
    'pink': '#EC4899',
    'rose': '#F43F5E',
    'emerald': '#10B981',
    'teal': '#14B8A6',
    'sky': '#0EA5E9',
    'amber': '#F59E0B',
    'orange': '#F97316',
    'red': '#EF4444',
    'text': '#E2E8F0',
    'muted': '#94A3B8',
    'grid': 'rgba(139, 92, 246, 0.1)',
    'success': '#10B981',
    'warning': '#F59E0B',
    'danger': '#EF4444'
}

# Gulf carriers list (for proper filtering)
GULF_CARRIERS = ['Emirates', 'Qatar Airways', 'Etihad Airways', 'Gulf Air', 'Oman Air', 
                 'Kuwait Airways', 'Saudia', 'flydubai', 'Air Arabia']

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
<div class="navbar-container">
    <span class="nav-logo">✈️</span>
    <div>
        <div class="nav-title">Flight Delay Domino Effect</div>
        <div class="nav-subtitle">Global Aviation Analytics Dashboard</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Navigation - ALL BUTTONS IDENTICAL
nav_cols = st.columns(8)
pages = ["Overview", "Analytics", "Domino Effect", "Economics", 
         "AI Predictor", "Simulator", "Regional", "Summary"]

if 'current_page' not in st.session_state:
    st.session_state.current_page = "Overview"

for i, page in enumerate(pages):
    if nav_cols[i].button(page, key=f"nav_{i}", use_container_width=True):
        st.session_state.current_page = page

current_page = st.session_state.current_page

# ═══════════════════════════════════════════════════════════════════════════════
# FILTERS
# ═══════════════════════════════════════════════════════════════════════════════
with st.expander("🎛️ **Global Filters** - Click to expand", expanded=False):
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
        st.markdown(f"**📊 Dataset:**")
        st.markdown(f"{len(df):,} flights • {len(airports_df)} airports • {len(airlines_df)} airlines")

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
if current_page == "Overview":
    
    st.markdown("""
    <div class="hero-section">
        <div class="hero-title">Understanding the Global Flight Delay Crisis</div>
        <div class="hero-subtitle">
            Comprehensive analysis of <span class="hero-highlight">150,000+ flights</span> across 
            <span class="hero-highlight">48 major airports</span> worldwide, revealing delay patterns, 
            cascading effects, and an economic impact exceeding <span class="hero-highlight">$250 Million</span>.
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
        <div class="glass-card purple">
            <span class="card-icon">🛫</span>
            <div class="card-value">{format_number(total_flights)}</div>
            <div class="card-label">Total Flights</div>
            <div class="card-delta info">Jan - Dec 2024</div>
        </div>
        """, unsafe_allow_html=True)
    
    with mc2:
        st.markdown(f"""
        <div class="glass-card pink">
            <span class="card-icon">⏱️</span>
            <div class="card-value pink">{delay_rate:.1f}%</div>
            <div class="card-label">Delay Rate</div>
            <div class="card-delta negative">{format_number(delayed_flights)} delayed</div>
        </div>
        """, unsafe_allow_html=True)
    
    with mc3:
        st.markdown(f"""
        <div class="glass-card amber">
            <span class="card-icon">⏰</span>
            <div class="card-value amber">{avg_delay:.0f} min</div>
            <div class="card-label">Avg Delay Duration</div>
            <div class="card-delta negative">When delayed</div>
        </div>
        """, unsafe_allow_html=True)
    
    with mc4:
        st.markdown(f"""
        <div class="glass-card emerald">
            <span class="card-icon">💰</span>
            <div class="card-value emerald">{format_currency(total_cost)}</div>
            <div class="card-label">Economic Impact</div>
            <div class="card-delta negative">Total cost</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Key Insight
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
            <span class="insight-stat">{best_region}</span> leads with only 
            <span class="insight-stat">{best_region_rate:.1f}%</span> — 
            a performance gap of <span class="insight-stat">{worst_region_rate - best_region_rate:.1f}%</span>.
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
        
        st.markdown('<div class="chart-explainer">Comparing on-time performance across global aviation markets. Green indicates better performance, red indicates higher delays.</div>', unsafe_allow_html=True)
        
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
                colorscale=[[0, COLORS['emerald']], [0.5, COLORS['amber']], [1, COLORS['rose']]],
            ),
            text=[f"<b>{x:.1f}%</b>" for x in region_stats['Delay Rate'] * 100],
            textposition='outside',
            textfont=dict(size=13, color=COLORS['text']),
            hovertemplate="<b>%{y}</b><br>Delay Rate: %{x:.1f}%<br>Flights: %{customdata:,}<extra></extra>",
            customdata=region_stats['Flights']
        ))
        
        fig.update_layout(
            height=380,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color=COLORS['text'], size=12),
            margin=dict(l=0, r=80, t=10, b=40),
            xaxis=dict(title="Delay Rate (%)", gridcolor=COLORS['grid'], zeroline=False),
            yaxis=dict(title="", gridcolor=COLORS['grid']),
            hoverlabel=dict(bgcolor='#1A1A2E', font_size=13, bordercolor=COLORS['purple'])
        )
        
        st.plotly_chart(fig, use_container_width=True, key="overview_region")
    
    with col2:
        st.markdown("""
        <div class="section-header">
            <span class="section-icon">📈</span>
            <span class="section-title">Monthly Trend</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="chart-explainer">Seasonal patterns in flight delays throughout the year. Red dashed line shows the annual average.</div>', unsafe_allow_html=True)
        
        monthly = fdf.groupby('MONTH')['DEP_DEL15'].mean().reset_index()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=MONTHS_SHORT,
            y=monthly['DEP_DEL15'] * 100,
            mode='lines+markers',
            line=dict(color=COLORS['purple'], width=4, shape='spline'),
            marker=dict(size=10, color=COLORS['purple'], line=dict(width=2, color='white')),
            fill='tozeroy',
            fillcolor='rgba(139, 92, 246, 0.1)',
            hovertemplate="<b>%{x}</b><br>Delay Rate: %{y:.1f}%<extra></extra>"
        ))
        
        avg_rate = monthly['DEP_DEL15'].mean() * 100
        fig.add_hline(y=avg_rate, line_dash="dash", line_color=COLORS['rose'],
                     annotation_text=f"Avg: {avg_rate:.1f}%", annotation_position="right")
        
        fig.update_layout(
            height=380,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color=COLORS['text'], size=12),
            margin=dict(l=50, r=30, t=10, b=40),
            xaxis=dict(title="", gridcolor=COLORS['grid']),
            yaxis=dict(title="Delay Rate (%)", gridcolor=COLORS['grid']),
            hoverlabel=dict(bgcolor='#1A1A2E', font_size=13, bordercolor=COLORS['purple'])
        )
        
        st.plotly_chart(fig, use_container_width=True, key="overview_monthly")
    
    # Second insight
    worst_month = int(fdf.groupby('MONTH')['DEP_DEL15'].mean().idxmax())
    best_month = int(fdf.groupby('MONTH')['DEP_DEL15'].mean().idxmin())
    worst_hour = int(fdf.groupby('DEP_HOUR')['DEP_DEL15'].mean().idxmax())
    best_hour = int(fdf.groupby('DEP_HOUR')['DEP_DEL15'].mean().idxmin())
    
    st.markdown(f"""
    <div class="insight-box success">
        <div class="insight-title">✅ Actionable Recommendation</div>
        <div class="insight-text">
            <b>Best month to fly:</b> <span class="insight-stat">{MONTHS[best_month-1]}</span> • 
            <b>Worst month:</b> <span class="insight-stat">{MONTHS[worst_month-1]}</span><br>
            <b>Optimal departure time:</b> <span class="insight-stat">{best_hour}:00</span> • 
            <b>Avoid:</b> <span class="insight-stat">{worst_hour}:00</span><br>
            Early morning flights consistently show lower delay rates across all regions.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: ANALYTICS
# ═══════════════════════════════════════════════════════════════════════════════
elif current_page == "Analytics":
    
    st.markdown("""
    <div class="section-header">
        <span class="section-icon">📊</span>
        <span class="section-title">Deep Dive Analytics</span>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["✈️ Airlines", "🏢 Airports", "🕐 Time Patterns", "🔥 Seasonality"])
    
    with tab1:
        st.markdown("### Airline Performance Ranking")
        st.markdown('<div class="chart-explainer">Airlines ranked by on-time performance. Green indicates excellent performance (below 25%), yellow indicates moderate (25-35%), and red indicates needs improvement (above 35%).</div>', unsafe_allow_html=True)
        
        airline_stats = fdf.groupby(['OP_UNIQUE_CARRIER', 'AIRLINE_NAME']).agg({
            'DEP_DEL15': ['count', 'mean'],
            'DEP_DELAY': 'mean',
            'DELAY_COST_TOTAL': 'sum'
        }).reset_index()
        airline_stats.columns = ['Code', 'Airline', 'Flights', 'Delay Rate', 'Avg Delay', 'Cost']
        airline_stats = airline_stats[airline_stats['Flights'] >= 100].sort_values('Delay Rate', ascending=True).tail(15)
        
        colors = [COLORS['emerald'] if x < 0.25 else COLORS['amber'] if x < 0.35 else COLORS['rose'] 
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
            hovertemplate="<b>%{y}</b><br>Delay Rate: %{x:.1f}%<br>Flights: %{customdata[0]:,}<br>Avg Delay: %{customdata[1]:.0f} min<extra></extra>",
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
            hoverlabel=dict(bgcolor='#1A1A2E', bordercolor=COLORS['purple'])
        )
        
        st.plotly_chart(fig, use_container_width=True, key="analytics_airline")
        
        best_airline = airline_stats.iloc[0]['Airline']
        worst_airline = airline_stats.iloc[-1]['Airline']
        
        st.markdown(f"""
        <div class="insight-box">
            <div class="insight-title">💡 Airline Performance Insight</div>
            <div class="insight-text">
                <span class="insight-stat">{best_airline}</span> leads with the best on-time record, 
                while <span class="insight-stat">{worst_airline}</span> shows the most room for improvement. 
                The operational efficiency difference translates to significant cost variations.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### Airport Delay Rankings")
        st.markdown('<div class="chart-explainer">Full airport names displayed for easy identification. Compare the best and worst performing airports based on departure delay rates.</div>', unsafe_allow_html=True)
        
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
                marker_color=COLORS['rose'],
                text=[f"{x:.1f}%" for x in worst['Delay Rate'] * 100],
                textposition='outside',
                textfont=dict(color='#FDA4AF', size=11),
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
                hoverlabel=dict(bgcolor='#1A1A2E', bordercolor=COLORS['rose'])
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
                marker_color=COLORS['emerald'],
                text=[f"{x:.1f}%" for x in best['Delay Rate'] * 100],
                textposition='outside',
                textfont=dict(color='#6EE7B7', size=11),
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
                hoverlabel=dict(bgcolor='#1A1A2E', bordercolor=COLORS['emerald'])
            )
            st.plotly_chart(fig, use_container_width=True, key="airport_best")
        
        st.markdown("""
        <div class="insight-box warning">
            <div class="insight-title">⚠️ Infrastructure Insight</div>
            <div class="insight-text">
                The top delayed airports contribute disproportionately to overall system delays. 
                Targeted infrastructure investments at these hubs could yield the highest ROI for the entire aviation network.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("### Hour × Day Heatmap")
        st.markdown('<div class="chart-explainer">This heatmap reveals the optimal and worst times to fly. Each cell shows the delay probability for that specific hour and day combination. Darker red indicates higher delay risk.</div>', unsafe_allow_html=True)
        
        hm_data = fdf.groupby(['DAY_OF_WEEK', 'DEP_HOUR'])['DEP_DEL15'].mean().reset_index()
        hm_pivot = hm_data.pivot(index='DEP_HOUR', columns='DAY_OF_WEEK', values='DEP_DEL15')
        
        fig = go.Figure(data=go.Heatmap(
            z=hm_pivot.values * 100,
            x=DAYS,
            y=[f"{h:02d}:00" for h in hm_pivot.index],
            colorscale=[[0, COLORS['emerald']], [0.5, COLORS['amber']], [1, COLORS['rose']]],
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
            margin=dict(l=80, r=50, t=20, b=50),
            xaxis=dict(title="Day of Week"),
            yaxis=dict(title="Hour of Day", autorange='reversed'),
            hoverlabel=dict(bgcolor='#1A1A2E', bordercolor=COLORS['purple'])
        )
        
        st.plotly_chart(fig, use_container_width=True, key="time_heatmap")
        
        best_time = hm_data.loc[hm_data['DEP_DEL15'].idxmin()]
        worst_time = hm_data.loc[hm_data['DEP_DEL15'].idxmax()]
        
        st.markdown(f"""
        <div class="insight-box success">
            <div class="insight-title">✅ Optimal Flight Timing</div>
            <div class="insight-text">
                <b>Best time to fly:</b> <span class="insight-stat">{DAYS[int(best_time['DAY_OF_WEEK'])-1]}</span> at 
                <span class="insight-stat">{int(best_time['DEP_HOUR']):02d}:00</span> (only {best_time['DEP_DEL15']*100:.1f}% delay rate)<br>
                <b>Worst time to fly:</b> <span class="insight-stat">{DAYS[int(worst_time['DAY_OF_WEEK'])-1]}</span> at 
                <span class="insight-stat">{int(worst_time['DEP_HOUR']):02d}:00</span> ({worst_time['DEP_DEL15']*100:.1f}% delay rate)
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with tab4:
        st.markdown("### Month × Region Seasonality Heatmap")
        st.markdown('<div class="chart-explainer">This heatmap shows how delay rates vary by month across different regions. Identify seasonal patterns like monsoon in India, winter storms in North America, and summer congestion in Europe.</div>', unsafe_allow_html=True)
        
        season_data = fdf.groupby(['MONTH', 'ORIGIN_REGION'])['DEP_DEL15'].mean().reset_index()
        season_pivot = season_data.pivot(index='ORIGIN_REGION', columns='MONTH', values='DEP_DEL15')
        
        fig = go.Figure(data=go.Heatmap(
            z=season_pivot.values * 100,
            x=MONTHS_SHORT,
            y=season_pivot.index,
            colorscale=[[0, COLORS['emerald']], [0.5, COLORS['amber']], [1, COLORS['rose']]],
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
            margin=dict(l=120, r=50, t=20, b=50),
            xaxis=dict(title="Month"),
            yaxis=dict(title=""),
            hoverlabel=dict(bgcolor='#1A1A2E', bordercolor=COLORS['purple'])
        )
        
        st.plotly_chart(fig, use_container_width=True, key="season_heatmap")
        
        st.markdown("""
        <div class="insight-box">
            <div class="insight-title">💡 Seasonal Patterns Identified</div>
            <div class="insight-text">
                • <b>India (Jun-Sep):</b> Monsoon causes <span class="insight-stat">40-60%</span> higher delays<br>
                • <b>North America (Dec-Feb):</b> Winter storms create cascading disruptions<br>
                • <b>Europe (Jun-Aug):</b> Summer holiday rush strains airport capacity<br>
                • <b>Middle East (Dec-Feb):</b> Morning fog impacts Dubai and Abu Dhabi operations
            </div>
        </div>
        """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: DOMINO EFFECT
# ═══════════════════════════════════════════════════════════════════════════════
elif current_page == "Domino Effect":
    
    st.markdown("""
    <div class="section-header">
        <span class="section-icon">🌊</span>
        <span class="section-title">The Domino Effect: Understanding Delay Cascades</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="insight-box">
        <div class="insight-title">🎯 What is the Domino Effect?</div>
        <div class="insight-text">
            When a flight is delayed, the <b>same aircraft</b> arrives late for its next scheduled flight. 
            Crew members may time out due to duty regulations. Passengers miss connections. 
            This creates a <b>cascading chain reaction</b> where one delay triggers many more throughout the day.
            The "Late Aircraft Delay" metric is the primary indicator of this phenomenon.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    delayed = fdf[fdf['DEP_DEL15'] == 1]
    
    col1, col2 = st.columns([1.2, 1])
    
    with col1:
        st.markdown("### Root Causes of Flight Delays")
        st.markdown('<div class="chart-explainer">Breakdown of delay causes by total minutes. Understanding root causes helps prioritize improvement investments for maximum impact.</div>', unsafe_allow_html=True)
        
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
        
        bar_colors = [COLORS['sky'], COLORS['amber'], COLORS['purple'], COLORS['rose'], COLORS['emerald']]
        
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
            margin=dict(l=0, r=180, t=20, b=30),
            xaxis=dict(title="Total Delay Minutes", gridcolor=COLORS['grid']),
            yaxis=dict(title=""),
            hoverlabel=dict(bgcolor='#1A1A2E', bordercolor=COLORS['purple'])
        )
        
        st.plotly_chart(fig, use_container_width=True, key="cause_bar")
    
    with col2:
        st.markdown("### Cause Distribution")
        
        fig = go.Figure(data=[go.Pie(
            labels=cause_df['Cause'],
            values=cause_df['Minutes'],
            hole=0.55,
            marker_colors=bar_colors,
            textinfo='percent',
            textfont=dict(size=12, color='white'),
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
                x=0.5, y=0.5, font_size=14, showarrow=False, font=dict(color=COLORS['violet'])
            )]
        )
        
        st.plotly_chart(fig, use_container_width=True, key="cause_pie")
    
    late_pct = cause_df[cause_df['Cause'] == 'Late Aircraft (Domino)']['Percentage'].values[0]
    
    st.markdown(f"""
    <div class="insight-box warning">
        <div class="insight-title">⚠️ Critical Domino Effect Finding</div>
        <div class="insight-text">
            <span class="insight-stat">{late_pct:.1f}%</span> of all delay minutes are caused by 
            <b>Late Aircraft</b> — the domino effect in action. This cascading impact can be mitigated through 
            better schedule buffers, improved turnaround times, and strategic positioning of spare aircraft.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Cascade throughout day
    st.markdown("### How Delays Compound Throughout the Day")
    st.markdown('<div class="chart-explainer">This dual-axis chart shows both the number of flights affected by late aircraft (bars) and the average cascade delay in minutes (line). Notice how both metrics increase as the day progresses.</div>', unsafe_allow_html=True)
    
    hourly_cascade = delayed.groupby('DEP_HOUR').agg({
        'LATE_AIRCRAFT_DELAY': ['count', 'mean']
    }).reset_index()
    hourly_cascade.columns = ['Hour', 'Flights', 'Avg Delay']
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(go.Bar(
        x=hourly_cascade['Hour'],
        y=hourly_cascade['Flights'],
        name='Flights Affected',
        marker_color=COLORS['purple'],
        opacity=0.8,
        hovertemplate="Hour: %{x}:00<br>Flights: %{y:,}<extra></extra>"
    ), secondary_y=False)
    
    fig.add_trace(go.Scatter(
        x=hourly_cascade['Hour'],
        y=hourly_cascade['Avg Delay'],
        name='Avg Cascade Delay (min)',
        line=dict(color=COLORS['pink'], width=4),
        mode='lines+markers',
        marker=dict(size=8),
        hovertemplate="Hour: %{x}:00<br>Avg Delay: %{y:.1f} min<extra></extra>"
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
        hoverlabel=dict(bgcolor='#1A1A2E', bordercolor=COLORS['purple'])
    )
    
    st.plotly_chart(fig, use_container_width=True, key="cascade_hourly")
    
    st.markdown("""
    <div class="insight-box success">
        <div class="insight-title">✅ Strategic Recommendation</div>
        <div class="insight-text">
            Early morning flights (5-7 AM) start with "fresh" aircraft that haven't accumulated delays. 
            As the day progresses, delays compound exponentially. <b>For business-critical travel, always prioritize morning departures.</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: ECONOMICS
# ═══════════════════════════════════════════════════════════════════════════════
elif current_page == "Economics":
    
    st.markdown("""
    <div class="section-header">
        <span class="section-icon">💰</span>
        <span class="section-title">Economic Impact Analysis</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="insight-box">
        <div class="insight-title">💵 Cost Calculation Methodology</div>
        <div class="insight-text">
            <b>Airline Cost:</b> $74.20 per minute of delay (fuel burn, crew overtime, aircraft repositioning, maintenance windows)<br>
            <b>Passenger Cost:</b> $47.00 per minute (value of time, missed connections, hotel accommodations, compensation)<br>
            <i>Source: FAA Economic Values for Investment and Regulatory Analysis, 2024</i>
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
        <div class="glass-card purple">
            <span class="card-icon">🏢</span>
            <div class="card-value purple">{format_currency(airline_cost)}</div>
            <div class="card-label">Airline Losses</div>
            <div class="card-delta negative">$74.20/min</div>
        </div>
        """, unsafe_allow_html=True)
    
    with kc2:
        st.markdown(f"""
        <div class="glass-card pink">
            <span class="card-icon">👥</span>
            <div class="card-value pink">{format_currency(passenger_cost)}</div>
            <div class="card-label">Passenger Impact</div>
            <div class="card-delta negative">$47.00/min</div>
        </div>
        """, unsafe_allow_html=True)
    
    with kc3:
        st.markdown(f"""
        <div class="glass-card amber">
            <span class="card-icon">💸</span>
            <div class="card-value amber">{format_currency(total_cost)}</div>
            <div class="card-label">Total Impact</div>
            <div class="card-delta negative">Combined</div>
        </div>
        """, unsafe_allow_html=True)
    
    with kc4:
        st.markdown(f"""
        <div class="glass-card emerald">
            <span class="card-icon">📊</span>
            <div class="card-value emerald">{format_currency(avg_cost)}</div>
            <div class="card-label">Per Delayed Flight</div>
            <div class="card-delta info">Average</div>
        </div>
        """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Economic Impact by Region")
        st.markdown('<div class="chart-explainer">Total delay costs by region. Higher costs indicate both higher delay frequency and longer average delay durations.</div>', unsafe_allow_html=True)
        
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
                colorscale=[[0, COLORS['emerald']], [0.5, COLORS['amber']], [1, COLORS['rose']]]
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
            margin=dict(l=0, r=100, t=10, b=30),
            xaxis=dict(title="Total Delay Cost ($)", gridcolor=COLORS['grid']),
            yaxis=dict(title=""),
            hoverlabel=dict(bgcolor='#1A1A2E', bordercolor=COLORS['purple'])
        )
        
        st.plotly_chart(fig, use_container_width=True, key="econ_region")
    
    with col2:
        st.markdown("### Monthly Cost Distribution")
        st.markdown('<div class="chart-explainer">Stacked bar chart showing airline vs passenger cost contribution each month. Seasonal patterns affect both cost components.</div>', unsafe_allow_html=True)
        
        monthly_cost = fdf.groupby('MONTH').agg({
            'DELAY_COST_AIRLINE': 'sum',
            'DELAY_COST_PASSENGER': 'sum'
        }).reset_index()
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=MONTHS_SHORT,
            y=monthly_cost['DELAY_COST_AIRLINE'],
            name='Airline Cost',
            marker_color=COLORS['purple'],
            hovertemplate="%{x}<br>Airline: $%{y:,.0f}<extra></extra>"
        ))
        fig.add_trace(go.Bar(
            x=MONTHS_SHORT,
            y=monthly_cost['DELAY_COST_PASSENGER'],
            name='Passenger Cost',
            marker_color=COLORS['pink'],
            hovertemplate="%{x}<br>Passenger: $%{y:,.0f}<extra></extra>"
        ))
        
        fig.update_layout(
            height=350,
            barmode='stack',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color=COLORS['text']),
            margin=dict(l=50, r=20, t=10, b=30),
            legend=dict(orientation='h', y=1.08),
            xaxis=dict(title="", gridcolor=COLORS['grid']),
            yaxis=dict(title="Cost ($)", gridcolor=COLORS['grid']),
            hoverlabel=dict(bgcolor='#1A1A2E', bordercolor=COLORS['purple'])
        )
        
        st.plotly_chart(fig, use_container_width=True, key="econ_monthly")
    
    # Pareto
    st.markdown("### Pareto Analysis: The 80/20 Rule in Action")
    st.markdown('<div class="chart-explainer">Pareto analysis identifies which airlines contribute most to total delay costs. The red line shows cumulative percentage — focus improvement efforts on airlines below the 80% threshold for maximum ROI.</div>', unsafe_allow_html=True)
    
    airline_cost_df = fdf.groupby('AIRLINE_NAME')['DELAY_COST_TOTAL'].sum().reset_index()
    airline_cost_df = airline_cost_df.sort_values('DELAY_COST_TOTAL', ascending=False).head(15)
    airline_cost_df['Cumulative'] = airline_cost_df['DELAY_COST_TOTAL'].cumsum()
    airline_cost_df['Cumulative %'] = airline_cost_df['Cumulative'] / airline_cost_df['DELAY_COST_TOTAL'].sum() * 100
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(go.Bar(
        x=airline_cost_df['AIRLINE_NAME'],
        y=airline_cost_df['DELAY_COST_TOTAL'],
        name='Delay Cost',
        marker_color=COLORS['purple'],
        hovertemplate="<b>%{x}</b><br>Cost: $%{y:,.0f}<extra></extra>"
    ), secondary_y=False)
    
    fig.add_trace(go.Scatter(
        x=airline_cost_df['AIRLINE_NAME'],
        y=airline_cost_df['Cumulative %'],
        name='Cumulative %',
        line=dict(color=COLORS['rose'], width=3),
        mode='lines+markers',
        marker=dict(size=8),
        hovertemplate="%{x}<br>Cumulative: %{y:.1f}%<extra></extra>"
    ), secondary_y=True)
    
    fig.add_hline(y=80, line_dash="dash", line_color=COLORS['amber'],
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
        hoverlabel=dict(bgcolor='#1A1A2E', bordercolor=COLORS['purple'])
    )
    
    st.plotly_chart(fig, use_container_width=True, key="pareto")
    
    airlines_80 = len(airline_cost_df[airline_cost_df['Cumulative %'] <= 80])
    
    st.markdown(f"""
    <div class="insight-box">
        <div class="insight-title">💡 Pareto Insight for Strategic Planning</div>
        <div class="insight-text">
            <span class="insight-stat">{airlines_80} airlines</span> 
            contribute to approximately <span class="insight-stat">80%</span> of all delay-related costs.
            Focusing operational improvement initiatives on these carriers would maximize return on investment for industry-wide efficiency gains.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: AI PREDICTOR
# ═══════════════════════════════════════════════════════════════════════════════
elif current_page == "AI Predictor":
    
    st.markdown("""
    <div class="section-header">
        <span class="section-icon">🤖</span>
        <span class="section-title">Machine Learning Delay Predictor</span>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📊 Model Performance", "🔮 Predict Your Flight"])
    
    with tab1:
        st.markdown("### Model Architecture & Evaluation")
        st.markdown('<div class="chart-explainer">A Random Forest classifier trained on 50,000 flight records to predict the probability of flight delays based on multiple features including time, route, and carrier information.</div>', unsafe_allow_html=True)
        
        @st.cache_resource
        def train_model():
            model_df = df.sample(n=min(50000, len(df)), random_state=42)
            
            model_df['ORIGIN_ENC'] = pd.factorize(model_df['ORIGIN'])[0]
            model_df['DEST_ENC'] = pd.factorize(model_df['DEST'])[0]
            model_df['CARRIER_ENC'] = pd.factorize(model_df['OP_UNIQUE_CARRIER'])[0]
            
            features = ['MONTH', 'DAY_OF_WEEK', 'DEP_HOUR', 'DISTANCE', 'ORIGIN_ENC', 'DEST_ENC', 'CARRIER_ENC']
            X = model_df[features]
            y = model_df['DEP_DEL15']
            
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
            
            model = RandomForestClassifier(n_estimators=100, max_depth=12, random_state=42, n_jobs=-1)
            model.fit(X_train, y_train)
            
            y_pred = model.predict(X_test)
            y_prob = model.predict_proba(X_test)[:, 1]
            
            return model, X_test, y_test, y_pred, y_prob, features
        
        with st.spinner("🔄 Training model on 50,000 flight records..."):
            model, X_test, y_test, y_pred, y_prob, feature_names = train_model()
        
        st.success("✅ Model trained successfully!")
        
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
            st.markdown("### Confusion Matrix")
            st.markdown('<div class="chart-explainer">Shows prediction accuracy breakdown: True Negatives (on-time predicted correctly), False Positives (on-time predicted as delayed), False Negatives (delayed predicted as on-time), True Positives (delayed predicted correctly).</div>', unsafe_allow_html=True)
            
            cm = confusion_matrix(y_test, y_pred)
            
            # FIXED: Proper 2x2 confusion matrix
            labels = [['True Negative<br>(Correct On-Time)', 'False Positive<br>(Wrong Delay Pred)'],
                     ['False Negative<br>(Missed Delay)', 'True Positive<br>(Correct Delay)']]
            
            fig = go.Figure(data=go.Heatmap(
                z=cm,
                x=['Predicted: On-Time', 'Predicted: Delayed'],
                y=['Actual: On-Time', 'Actual: Delayed'],
                colorscale=[[0, COLORS['emerald']], [0.25, '#5EEAD4'], [0.5, COLORS['amber']], [0.75, '#FB923C'], [1, COLORS['rose']]],
                text=[[f"<b>{cm[i][j]:,}</b><br><span style='font-size:10px'>{labels[i][j]}</span>" for j in range(2)] for i in range(2)],
                texttemplate="%{text}",
                textfont={"size": 14, "color": "white"},
                hovertemplate="<b>%{y}</b> → <b>%{x}</b><br>Count: %{z:,}<extra></extra>",
                showscale=True,
                colorbar=dict(title="Count")
            ))
            
            fig.update_layout(
                height=400,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color=COLORS['text'], size=12),
                margin=dict(l=50, r=50, t=30, b=50),
                xaxis=dict(side='bottom', tickfont=dict(size=11)),
                yaxis=dict(autorange='reversed', tickfont=dict(size=11))
            )
            
            st.plotly_chart(fig, use_container_width=True, key="confusion")
        
        with col2:
            st.markdown("### ROC-AUC Curve")
            st.markdown('<div class="chart-explainer">Receiver Operating Characteristic curve measuring model discrimination ability. The area under the curve (AUC) closer to 1.0 indicates better performance. Our model significantly outperforms random classification (diagonal line).</div>', unsafe_allow_html=True)
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=fpr, y=tpr,
                mode='lines',
                name=f'Model (AUC = {roc_auc:.3f})',
                line=dict(color=COLORS['purple'], width=4),
                fill='tozeroy',
                fillcolor='rgba(139, 92, 246, 0.15)',
                hovertemplate="FPR: %{x:.3f}<br>TPR: %{y:.3f}<extra></extra>"
            ))
            
            fig.add_trace(go.Scatter(
                x=[0, 1], y=[0, 1],
                mode='lines',
                name='Random (AUC = 0.5)',
                line=dict(color=COLORS['muted'], width=2, dash='dash')
            ))
            
            fig.update_layout(
                height=400,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color=COLORS['text']),
                margin=dict(l=50, r=50, t=30, b=50),
                xaxis=dict(title='False Positive Rate', gridcolor=COLORS['grid'], range=[0, 1]),
                yaxis=dict(title='True Positive Rate', gridcolor=COLORS['grid'], range=[0, 1]),
                legend=dict(x=0.5, y=0.15),
                hoverlabel=dict(bgcolor='#1A1A2E', bordercolor=COLORS['purple'])
            )
            
            st.plotly_chart(fig, use_container_width=True, key="roc")
        
        st.markdown("### Feature Importance Analysis")
        st.markdown('<div class="chart-explainer">Ranking of features by their contribution to prediction accuracy. Higher importance means the feature has more influence on whether a flight will be delayed.</div>', unsafe_allow_html=True)
        
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
                colorscale=[[0, COLORS['sky']], [0.5, COLORS['purple']], [1, COLORS['pink']]]
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
            hoverlabel=dict(bgcolor='#1A1A2E', bordercolor=COLORS['purple'])
        )
        
        st.plotly_chart(fig, use_container_width=True, key="importance")
        
        st.markdown("""
        <div class="insight-box">
            <div class="insight-title">💡 Model Interpretation</div>
            <div class="insight-text">
                <b>Departure Hour</b> and <b>Distance</b> are the strongest predictors of delays.
                This aligns with the domino effect theory — later flights accumulate delays, and longer routes 
                have more variables that can cause disruptions. Airline and airport factors also play significant roles.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### Predict Delay Risk for Your Flight")
        st.markdown('<div class="chart-explainer">Enter your flight details below. The model will validate that the airline operates on your selected route and provide a delay probability assessment.</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # DATE INPUT - REQUIRED
            pred_date = st.date_input(
                "📅 Travel Date",
                value=datetime.now() + timedelta(days=7),
                min_value=datetime.now(),
                max_value=datetime(2025, 12, 31),
                key="pred_date"
            )
            
            pred_hour = st.slider("🕐 Departure Hour", 0, 23, 12, key="pred_hour",
                                 help="Select the scheduled departure time")
        
        with col2:
            pred_origin = st.selectbox("🛫 Origin Airport", 
                [f"{row['city']} ({row['code']})" for _, row in airports_df.iterrows()], 
                key="pred_origin")
            
            pred_dest = st.selectbox("🛬 Destination Airport",
                [f"{row['city']} ({row['code']})" for _, row in airports_df.iterrows()], 
                key="pred_dest")
        
        # Get codes
        origin_code = pred_origin.split('(')[1].replace(')', '')
        dest_code = pred_dest.split('(')[1].replace(')', '')
        
        # VALIDATE: Get airlines that actually operate this route
        route_airlines = df[(df['ORIGIN'] == origin_code) & (df['DEST'] == dest_code)]['AIRLINE_NAME'].unique().tolist()
        
        if len(route_airlines) == 0:
            st.markdown("""
            <div class="error-box">
                <div class="error-title">⚠️ No Direct Route Available</div>
                <div class="error-text">No airlines in our database operate direct flights between these airports. Please select a different origin-destination pair.</div>
            </div>
            """, unsafe_allow_html=True)
            pred_airline = None
        else:
            pred_airline = st.selectbox("✈️ Airline (Operating this Route)",
                sorted(route_airlines), key="pred_airline")
        
        if pred_airline and st.button("🔮 PREDICT DELAY RISK", use_container_width=True):
            # Same origin/destination check
            if origin_code == dest_code:
                st.markdown("""
                <div class="error-box">
                    <div class="error-title">⚠️ Invalid Route</div>
                    <div class="error-text">Origin and destination cannot be the same airport.</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                # Calculate features
                origin_info = airports_df[airports_df['code'] == origin_code].iloc[0]
                dest_info = airports_df[airports_df['code'] == dest_code].iloc[0]
                
                lat1, lon1 = np.radians(origin_info['lat']), np.radians(origin_info['lon'])
                lat2, lon2 = np.radians(dest_info['lat']), np.radians(dest_info['lon'])
                dlat, dlon = lat2 - lat1, lon2 - lon1
                a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
                distance = 3956 * 2 * np.arcsin(np.sqrt(a))
                
                # Use date for month and day
                month_idx = pred_date.month
                day_idx = pred_date.weekday() + 1  # Monday = 1
                
                origin_enc = hash(origin_code) % 1000
                dest_enc = hash(dest_code) % 1000
                carrier_enc = hash(pred_airline) % 1000
                
                features = [[month_idx, day_idx, pred_hour, distance, origin_enc, dest_enc, carrier_enc]]
                
                prediction = model.predict(features)[0]
                probability = model.predict_proba(features)[0][1]
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Show flight details
                st.markdown(f"""
                **Flight Details:**
                - **Date:** {pred_date.strftime('%A, %B %d, %Y')}
                - **Route:** {pred_origin} → {pred_dest}
                - **Airline:** {pred_airline}
                - **Time:** {pred_hour:02d}:00
                - **Distance:** {distance:,.0f} miles
                """)
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                if prediction == 1 or probability > 0.4:
                    st.markdown(f"""
                    <div class="prediction-high">
                        <div class="prediction-icon">⚠️</div>
                        <div class="prediction-title" style="color: #FDA4AF;">HIGH DELAY RISK</div>
                        <div class="prediction-prob" style="color: #F43F5E;">{probability*100:.1f}%</div>
                        <p style="color: #E2E8F0;">probability of delay (>15 minutes)</p>
                        <p style="color: #94A3B8; margin-top: 1rem;">Consider booking an earlier flight or allow extra buffer time for connections.</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="prediction-low">
                        <div class="prediction-icon">✅</div>
                        <div class="prediction-title" style="color: #6EE7B7;">LOW DELAY RISK</div>
                        <div class="prediction-prob" style="color: #10B981;">{(1-probability)*100:.1f}%</div>
                        <p style="color: #E2E8F0;">probability of on-time departure</p>
                        <p style="color: #94A3B8; margin-top: 1rem;">This flight has favorable on-time performance indicators.</p>
                    </div>
                    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: SIMULATOR
# ═══════════════════════════════════════════════════════════════════════════════
elif current_page == "Simulator":
    
    st.markdown("""
    <div class="section-header">
        <span class="section-icon">🔮</span>
        <span class="section-title">What-If Scenario Simulator</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="insight-box">
        <div class="insight-title">🎯 Strategic Planning Tool</div>
        <div class="insight-text">
            Use this simulator to model the impact of operational improvements. Adjust the sliders to see how 
            reducing specific delay causes would affect overall performance metrics and cost savings.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    cur_delays = int(fdf['DEP_DEL15'].sum())
    cur_rate = fdf['DEP_DEL15'].mean() * 100
    cur_cost = fdf['DELAY_COST_TOTAL'].sum()
    
    st.markdown("### Current Baseline")
    st.markdown('<div class="chart-explainer">These are the current performance metrics based on your filter selections.</div>', unsafe_allow_html=True)
    
    cc1, cc2, cc3 = st.columns(3)
    cc1.metric("Delayed Flights", f"{cur_delays:,}")
    cc2.metric("Delay Rate", f"{cur_rate:.1f}%")
    cc3.metric("Total Cost", format_currency(cur_cost))
    
    st.markdown("---")
    st.markdown("### Improvement Scenarios")
    st.markdown('<div class="chart-explainer">Move the sliders to simulate different operational improvement scenarios. Each category has different implementation costs and feasibility.</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        carrier_red = st.slider("✈️ Carrier Operations Improvement (%)", 0, 50, 0, 5,
            help="Better maintenance scheduling, crew optimization, ground operations")
        weather_red = st.slider("🌧️ Weather Impact Mitigation (%)", 0, 30, 0, 5,
            help="Advanced forecasting, proactive rescheduling, de-icing efficiency")
    
    with col2:
        nas_red = st.slider("🗼 Air Traffic Control Efficiency (%)", 0, 40, 0, 5,
            help="NextGen implementation, better flow management, reduced ground stops")
        late_red = st.slider("🔄 Late Aircraft Recovery (%)", 0, 50, 0, 5,
            help="Schedule buffers, faster turnaround, spare aircraft positioning")
    
    total_red = (carrier_red * 0.35 + weather_red * 0.20 + nas_red * 0.25 + late_red * 0.20) / 100
    
    new_delays = cur_delays * (1 - total_red)
    new_rate = cur_rate * (1 - total_red)
    new_cost = cur_cost * (1 - total_red)
    savings = cur_cost - new_cost
    
    st.markdown("---")
    st.markdown("### Projected Outcomes")
    
    sc1, sc2, sc3, sc4 = st.columns(4)
    sc1.metric("New Delayed Flights", f"{new_delays:,.0f}", f"-{cur_delays - new_delays:,.0f}")
    sc2.metric("New Delay Rate", f"{new_rate:.1f}%", f"-{cur_rate - new_rate:.1f}%")
    sc3.metric("New Total Cost", format_currency(new_cost))
    sc4.metric("💰 PROJECTED SAVINGS", format_currency(savings))
    
    if savings > 0:
        st.markdown(f"""
        <div class="insight-box success">
            <div class="insight-title">✅ Scenario Impact Summary</div>
            <div class="insight-text">
                Implementing these improvements would result in:<br>
                • <span class="insight-stat">{cur_delays - new_delays:,.0f}</span> fewer delayed flights annually<br>
                • <span class="insight-stat">{format_currency(savings)}</span> in total cost savings<br>
                • <span class="insight-stat">{cur_rate - new_rate:.1f}%</span> improvement in on-time performance<br>
                • Improved passenger satisfaction and brand reputation
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Adjust the sliders above to simulate improvement scenarios.")

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: REGIONAL
# ═══════════════════════════════════════════════════════════════════════════════
elif current_page == "Regional":
    
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
        ic1.metric("Total Flights", f"{len(india_df):,}")
        ic2.metric("Delay Rate", f"{india_df['DEP_DEL15'].mean()*100:.1f}%")
        ic3.metric("Avg Delay", f"{india_df[india_df['DEP_DEL15']==1]['DEP_DELAY'].mean():.0f} min")
        ic4.metric("Economic Impact", format_currency(india_df['DELAY_COST_TOTAL'].sum()))
        
        st.markdown("### Monsoon Impact on Flight Operations")
        st.markdown('<div class="chart-explainer">June through September marks India\'s monsoon season. Red bars highlight these months with significantly elevated delay rates due to heavy rainfall, thunderstorms, and reduced visibility.</div>', unsafe_allow_html=True)
        
        india_monthly = india_df.groupby('MONTH')['DEP_DEL15'].mean().reset_index()
        colors = [COLORS['emerald'] if m not in [6,7,8,9] else COLORS['rose'] for m in range(1,13)]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=MONTHS_SHORT,
            y=india_monthly['DEP_DEL15'] * 100,
            marker_color=colors,
            text=[f"{x:.1f}%" for x in india_monthly['DEP_DEL15'] * 100],
            textposition='outside',
            textfont=dict(color=COLORS['text'], size=11),
            hovertemplate="<b>%{x}</b><br>Delay Rate: %{y:.1f}%<extra></extra>"
        ))
        
        fig.add_vrect(x0=4.5, x1=8.5, fillcolor="rgba(244,63,94,0.1)", line_width=0,
                     annotation_text="Monsoon Season", annotation_position="top")
        
        fig.update_layout(
            height=350,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color=COLORS['text']),
            margin=dict(l=50, r=20, t=40, b=30),
            yaxis=dict(title="Delay Rate (%)", gridcolor=COLORS['grid']),
            hoverlabel=dict(bgcolor='#1A1A2E', bordercolor=COLORS['purple'])
        )
        
        st.plotly_chart(fig, use_container_width=True, key="india_monthly")
        
        # Indian airlines only
        st.markdown("### Top Indian Carriers Performance")
        indian_carriers = ['IndiGo', 'Air India', 'SpiceJet', 'Vistara', 'Go First', 'AirAsia India', 'Air India Express']
        india_airlines = india_df[india_df['AIRLINE_NAME'].isin(indian_carriers)].groupby('AIRLINE_NAME')['DEP_DEL15'].agg(['count', 'mean']).reset_index()
        india_airlines.columns = ['Airline', 'Flights', 'Delay Rate']
        india_airlines = india_airlines[india_airlines['Flights'] >= 20].sort_values('Delay Rate')
        
        if len(india_airlines) > 0:
            fig = go.Figure()
            fig.add_trace(go.Bar(
                y=india_airlines['Airline'],
                x=india_airlines['Delay Rate'] * 100,
                orientation='h',
                marker_color=COLORS['amber'],
                text=[f"{x:.1f}%" for x in india_airlines['Delay Rate'] * 100],
                textposition='outside',
                textfont=dict(color=COLORS['text'])
            ))
            fig.update_layout(
                height=300,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color=COLORS['text']),
                margin=dict(l=0, r=80, t=10, b=30),
                xaxis=dict(title="Delay Rate (%)", gridcolor=COLORS['grid'])
            )
            st.plotly_chart(fig, use_container_width=True, key="india_airlines")
        
        st.markdown("""
        <div class="insight-box warning">
            <div class="insight-title">🌧️ India Aviation Insight</div>
            <div class="insight-text">
                Monsoon season (Jun-Sep) causes <span class="insight-stat">40-60%</span> higher delays.
                Mumbai (BOM) and Delhi (DEL) are most affected. Winter fog (Dec-Jan) also severely impacts 
                North Indian airports, particularly in early morning hours.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with tab2:
        me_df = df[df['ORIGIN_REGION'] == 'Middle East']
        
        mc1, mc2, mc3, mc4 = st.columns(4)
        mc1.metric("Total Flights", f"{len(me_df):,}")
        mc2.metric("Delay Rate", f"{me_df['DEP_DEL15'].mean()*100:.1f}%")
        mc3.metric("Avg Delay", f"{me_df[me_df['DEP_DEL15']==1]['DEP_DELAY'].mean():.0f} min")
        mc4.metric("Economic Impact", format_currency(me_df['DELAY_COST_TOTAL'].sum()))
        
        st.markdown("### Gulf Carriers Performance")
        st.markdown('<div class="chart-explainer">Performance comparison of Gulf-based carriers only (Emirates, Qatar Airways, Etihad, etc.). These premium carriers typically maintain industry-leading on-time performance.</div>', unsafe_allow_html=True)
        
        # FIXED: Filter to only ACTUAL Gulf carriers
        gulf_airlines_df = me_df[me_df['AIRLINE_NAME'].isin(GULF_CARRIERS)].groupby('AIRLINE_NAME')['DEP_DEL15'].agg(['count', 'mean']).reset_index()
        gulf_airlines_df.columns = ['Airline', 'Flights', 'Delay Rate']
        gulf_airlines_df = gulf_airlines_df[gulf_airlines_df['Flights'] >= 10].sort_values('Delay Rate')
        
        if len(gulf_airlines_df) > 0:
            fig = go.Figure()
            fig.add_trace(go.Bar(
                y=gulf_airlines_df['Airline'],
                x=gulf_airlines_df['Delay Rate'] * 100,
                orientation='h',
                marker_color=COLORS['purple'],
                text=[f"{x:.1f}%" for x in gulf_airlines_df['Delay Rate'] * 100],
                textposition='outside',
                textfont=dict(color=COLORS['text'], size=11),
                hovertemplate="<b>%{y}</b><br>Delay Rate: %{x:.1f}%<extra></extra>"
            ))
            
            fig.update_layout(
                height=350,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color=COLORS['text']),
                margin=dict(l=0, r=80, t=10, b=30),
                xaxis=dict(title="Delay Rate (%)", gridcolor=COLORS['grid']),
                hoverlabel=dict(bgcolor='#1A1A2E', bordercolor=COLORS['purple'])
            )
            
            st.plotly_chart(fig, use_container_width=True, key="gulf_airlines")
        else:
            st.info("No Gulf carrier data available with the current filters.")
        
        st.markdown("""
        <div class="insight-box">
            <div class="insight-title">🇦🇪 Gulf Region Insight</div>
            <div class="insight-text">
                Premium Gulf carriers invest heavily in operational excellence and punctuality.
                Dubai International (DXB), the world's busiest international hub, maintains 
                strong on-time performance despite massive traffic volumes. Winter morning fog (Dec-Feb) 
                remains the primary weather challenge in the region.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with tab3:
        na_df = df[df['ORIGIN_REGION'] == 'North America']
        
        nc1, nc2, nc3, nc4 = st.columns(4)
        nc1.metric("Total Flights", f"{len(na_df):,}")
        nc2.metric("Delay Rate", f"{na_df['DEP_DEL15'].mean()*100:.1f}%")
        nc3.metric("Avg Delay", f"{na_df[na_df['DEP_DEL15']==1]['DEP_DELAY'].mean():.0f} min")
        nc4.metric("Economic Impact", format_currency(na_df['DELAY_COST_TOTAL'].sum()))
        
        st.markdown("### Seasonal Delay Pattern")
        st.markdown('<div class="chart-explainer">Color coding: Red = Winter storms (Dec-Feb), Yellow = Summer thunderstorms (Jun-Aug), Green = Stable weather periods. North America experiences the most pronounced seasonal variations.</div>', unsafe_allow_html=True)
        
        na_monthly = na_df.groupby('MONTH')['DEP_DEL15'].mean().reset_index()
        colors = [COLORS['rose'] if m in [1,2,12] else COLORS['amber'] if m in [6,7,8] else COLORS['emerald'] for m in range(1,13)]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=MONTHS_SHORT,
            y=na_monthly['DEP_DEL15'] * 100,
            marker_color=colors,
            text=[f"{x:.1f}%" for x in na_monthly['DEP_DEL15'] * 100],
            textposition='outside',
            textfont=dict(color=COLORS['text'], size=11),
            hovertemplate="<b>%{x}</b><br>Delay Rate: %{y:.1f}%<extra></extra>"
        ))
        
        fig.update_layout(
            height=350,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color=COLORS['text']),
            margin=dict(l=50, r=20, t=20, b=30),
            yaxis=dict(title="Delay Rate (%)", gridcolor=COLORS['grid']),
            hoverlabel=dict(bgcolor='#1A1A2E', bordercolor=COLORS['purple'])
        )
        
        st.plotly_chart(fig, use_container_width=True, key="na_monthly")
        
        st.markdown("""
        <div class="insight-box warning">
            <div class="insight-title">🇺🇸 North America Insight</div>
            <div class="insight-text">
                Winter storms (Dec-Feb) cause the highest delays due to snow, ice, and de-icing requirements.
                Summer thunderstorms (Jun-Aug) create ground stops at major hubs. Chicago O'Hare (ORD), 
                Denver (DEN), and New York airports are most frequently impacted by weather.
                Holiday travel (Thanksgiving, Christmas) adds significant congestion.
            </div>
        </div>
        """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: SUMMARY
# ═══════════════════════════════════════════════════════════════════════════════
elif current_page == "Summary":
    
    st.markdown("""
    <div class="section-header">
        <span class="section-icon">📈</span>
        <span class="section-title">Executive Summary & Strategic Recommendations</span>
    </div>
    """, unsafe_allow_html=True)
    
    total_flights = len(df)
    total_delayed = int(df['DEP_DEL15'].sum())
    total_cost = df['DELAY_COST_TOTAL'].sum()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="insight-box">
            <div class="insight-title">📊 Analysis Summary</div>
            <div class="insight-text">
                • <b>Total Flights Analyzed:</b> <span class="insight-stat">{total_flights:,}</span><br>
                • <b>Delayed Flights:</b> <span class="insight-stat">{total_delayed:,}</span> ({total_delayed/total_flights*100:.1f}%)<br>
                • <b>Total Economic Impact:</b> <span class="insight-stat">{format_currency(total_cost)}</span><br>
                • <b>Global Coverage:</b> <span class="insight-stat">{len(airports_df)}</span> airports, <span class="insight-stat">{len(airlines_df)}</span> airlines<br>
                • <b>Time Period:</b> January - December 2024
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        best_airline = df.groupby('AIRLINE_NAME')['DEP_DEL15'].mean().idxmin()
        worst_airline = df.groupby('AIRLINE_NAME')['DEP_DEL15'].mean().idxmax()
        
        st.markdown(f"""
        <div class="insight-box">
            <div class="insight-title">🏆 Performance Benchmarks</div>
            <div class="insight-text">
                • <b>Best Performing Airline:</b> <span class="insight-stat">{best_airline}</span><br>
                • <b>Most Challenged Airline:</b> <span class="insight-stat">{worst_airline}</span><br>
                • <b>Best Departure Time:</b> <span class="insight-stat">5:00 - 7:00 AM</span><br>
                • <b>Highest Risk Time:</b> <span class="insight-stat">5:00 - 8:00 PM</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### Key Strategic Findings")
    
    st.markdown("""
    <div class="insight-box">
        <div class="insight-title">🌊 Finding 1: The Domino Effect is Quantifiable</div>
        <div class="insight-text">
            Late aircraft delays compound throughout the day. Our analysis shows evening flights are 
            significantly more likely to be delayed than morning flights. Airlines can break this cascade 
            through strategic schedule buffering and spare aircraft positioning at hub airports.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="insight-box warning">
        <div class="insight-title">🌧️ Finding 2: Weather Creates Predictable Seasonal Patterns</div>
        <div class="insight-text">
            India's monsoon, North America's winter storms, and summer thunderstorms create 
            predictable delay peaks. Airlines and passengers can leverage this predictability 
            for better planning. Pre-emptive schedule adjustments during high-risk periods could 
            reduce cascading impacts by 15-25%.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="insight-box success">
        <div class="insight-title">📈 Finding 3: Pareto Principle Applies to Aviation Delays</div>
        <div class="insight-text">
            A small number of airlines and airports contribute disproportionately to overall delay minutes. 
            Targeted infrastructure investments and operational improvements at these bottlenecks would 
            yield maximum ROI for the entire aviation ecosystem.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Strategic Recommendations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="insight-box">
            <div class="insight-title">👤 For Travelers & Corporate Travel Managers</div>
            <div class="insight-text">
                1. Prioritize early morning departures (5-7 AM) for critical trips<br>
                2. Avoid peak delay seasons in your destination region<br>
                3. Build minimum 90-minute buffers for connections<br>
                4. Use the AI predictor to assess delay risk before booking<br>
                5. Consider airlines with proven on-time performance track records
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="insight-box">
            <div class="insight-title">🏢 For Airlines & Airport Operators</div>
            <div class="insight-text">
                1. Implement strategic schedule buffers at hub rotations<br>
                2. Invest in predictive maintenance to reduce carrier delays<br>
                3. Optimize turnaround processes to minimize late aircraft impact<br>
                4. Develop advanced weather contingency protocols<br>
                5. Focus improvement resources on highest-impact routes
            </div>
        </div>
        """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="footer">
    <div class="footer-brand">✈️ Flight Delay Domino Effect Dashboard</div>
    <p class="footer-text">Master's in AI & Business Analytics | Data Visualization & Analysis Project</p>
    <p class="footer-text" style="font-size: 0.75rem;">Built with Python • Streamlit • Plotly • Scikit-learn</p>
</div>
""", unsafe_allow_html=True)
