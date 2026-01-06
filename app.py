# === FLIGHT DELAY DOMINO EFFECT DASHBOARD ===
# Main Application File - Enhanced Version

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, roc_curve, auc
import warnings
warnings.filterwarnings('ignore')

# === PAGE CONFIG ===
st.set_page_config(
    page_title="Flight Delay Domino Effect",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# === THEME DETECTION & CSS ===
def get_theme_colors():
    """Return colors based on theme"""
    return {
        'bg_primary': '#0E1117',
        'bg_secondary': '#1E2130',
        'bg_card': '#262D3D',
        'bg_card_hover': '#323B4F',
        'text_primary': '#FFFFFF',
        'text_secondary': '#B0B8C4',
        'accent': '#FF6B6B',
        'success': '#4CAF50',
        'warning': '#FFB74D',
        'danger': '#FF5252',
        'info': '#42A5F5',
        'delay_bad': '#FF5252',
        'delay_good': '#69F0AE',
        'plotly_template': 'plotly_dark'
    }

colors = get_theme_colors()

# === CUSTOM CSS ===
st.markdown("""
<style>
    /* Main container */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #1E2130 0%, #262D3D 100%);
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid rgba(255,255,255,0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        margin-bottom: 1rem;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0,0,0,0.4);
        border: 1px solid rgba(255,107,107,0.3);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #FFFFFF;
        margin: 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #B0B8C4;
        margin-top: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .metric-delta-positive {
        color: #69F0AE;
        font-size: 0.85rem;
    }
    
    .metric-delta-negative {
        color: #FF5252;
        font-size: 0.85rem;
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #FFFFFF;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #FF6B6B;
    }
    
    /* Info cards */
    .info-card {
        background: linear-gradient(135deg, #1a1f2e 0%, #252b3b 100%);
        padding: 1.2rem;
        border-radius: 12px;
        border-left: 4px solid #FF6B6B;
        margin: 1rem 0;
    }
    
    /* Stat highlight */
    .stat-highlight {
        background: linear-gradient(135deg, #FF6B6B 0%, #FF8E53 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700;
    }
    
    /* Custom tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #1E2130;
        border-radius: 8px;
        padding: 10px 20px;
        color: #B0B8C4;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #FF6B6B;
        color: #FFFFFF;
    }
    
    /* Drill down card */
    .drill-down-card {
        background: linear-gradient(135deg, #1E2130 0%, #2D3748 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #3D4663;
        margin: 1rem 0;
    }
    
    /* What-if result card */
    .whatif-result {
        background: linear-gradient(135deg, #1a472a 0%, #2d5a3d 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #4CAF50;
        margin: 1rem 0;
    }
    
    /* Pareto line */
    .pareto-insight {
        background: linear-gradient(135deg, #1E2130 0%, #2D3748 100%);
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #FFB74D;
        margin: 0.5rem 0;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
</style>
""", unsafe_allow_html=True)

# === DATA LOADING ===
@st.cache_data
def load_data():
    """Load all datasets"""
    flights = pd.read_csv('data/flights_global_2024.csv')
    airlines = pd.read_csv('data/airlines.csv')
    airports = pd.read_csv('data/airports.csv')
    
    flights['FL_DATE'] = pd.to_datetime(flights['FL_DATE'])
    
    return flights, airlines, airports

# Load data
try:
    df, airlines_df, airports_df = load_data()
    data_loaded = True
except Exception as e:
    st.error(f"Error loading data: {e}")
    data_loaded = False

# === HELPER FUNCTIONS ===
def format_number(num):
    """Format large numbers"""
    if num >= 1_000_000:
        return f"{num/1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num/1_000:.1f}K"
    else:
        return f"{num:.0f}"

def format_currency(num):
    """Format currency"""
    if num >= 1_000_000:
        return f"${num/1_000_000:.1f}M"
    elif num >= 1_000:
        return f"${num/1_000:.1f}K"
    else:
        return f"${num:.0f}"

def create_metric_card(value, label, delta=None, delta_type="neutral"):
    """Create HTML metric card"""
    delta_html = ""
    if delta:
        delta_class = "metric-delta-positive" if delta_type == "positive" else "metric-delta-negative"
        delta_html = f'<p class="{delta_class}">{delta}</p>'
    
    return f"""
    <div class="metric-card">
        <p class="metric-value">{value}</p>
        <p class="metric-label">{label}</p>
        {delta_html}
    </div>
    """

def create_pareto_chart(data, category_col, value_col, title):
    """Create Pareto chart with cumulative line"""
    data_sorted = data.sort_values(value_col, ascending=False).reset_index(drop=True)
    data_sorted['cumulative'] = data_sorted[value_col].cumsum()
    data_sorted['cumulative_pct'] = data_sorted['cumulative'] / data_sorted[value_col].sum() * 100
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Bar chart
    fig.add_trace(
        go.Bar(
            x=data_sorted[category_col],
            y=data_sorted[value_col],
            name='Count',
            marker_color='#FF6B6B'
        ),
        secondary_y=False
    )
    
    # Cumulative line
    fig.add_trace(
        go.Scatter(
            x=data_sorted[category_col],
            y=data_sorted['cumulative_pct'],
            name='Cumulative %',
            line=dict(color='#42A5F5', width=3),
            mode='lines+markers'
        ),
        secondary_y=True
    )
    
    # 80% reference line
    fig.add_hline(y=80, line_dash="dash", line_color="#FFB74D", 
                  annotation_text="80%", secondary_y=True)
    
    fig.update_layout(
        title=title,
        paper_bgcolor='#0E1117',
        plot_bgcolor='#0E1117',
        font_color='#FFFFFF',
        height=400,
        xaxis=dict(title="", tickangle=45, gridcolor='#2D3748'),
        yaxis=dict(title="Delayed Flights", gridcolor='#2D3748'),
        yaxis2=dict(title="Cumulative %", gridcolor='#2D3748', range=[0, 105]),
        legend=dict(orientation='h', yanchor='bottom', y=1.02),
        margin=dict(t=80, b=100)
    )
    
    return fig, data_sorted

# === SIDEBAR NAVIGATION ===
with st.sidebar:
    st.markdown("## ✈️ Flight Delay")
    st.markdown("## Domino Effect")
    st.markdown("---")
    
    page = st.radio(
        "Navigation",
        ["🏠 Home", "📊 Delay Patterns", "🔥 Seasonality", "📈 Pareto Analysis", 
         "🌊 Ripple Effect", "💰 Impact Analysis", "🔮 What-If Analysis",
         "🤖 Delay Predictor", "📍 Case Studies"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Filters
    st.markdown("### 🎛️ Filters")
    
    if data_loaded:
        regions = ['All'] + sorted(df['ORIGIN_REGION'].unique().tolist())
        selected_region = st.selectbox("Region", regions)
        
        months = ['All'] + list(range(1, 13))
        selected_month = st.selectbox("Month", months, format_func=lambda x: 'All' if x == 'All' else pd.Timestamp(2024, x, 1).strftime('%B'))
        
        filtered_df = df.copy()
        if selected_region != 'All':
            filtered_df = filtered_df[filtered_df['ORIGIN_REGION'] == selected_region]
        if selected_month != 'All':
            filtered_df = filtered_df[filtered_df['MONTH'] == selected_month]
    
    st.markdown("---")
    st.markdown("### 📊 Dataset Info")
    if data_loaded:
        st.markdown(f"**Flights:** {len(df):,}")
        st.markdown(f"**Airports:** {len(airports_df)}")
        st.markdown(f"**Airlines:** {len(airlines_df)}")
        st.markdown(f"**Period:** Jan-Dec 2024")

# === PAGE: HOME ===
if page == "🏠 Home":
    
    st.markdown("# ✈️ Flight Delay Domino Effect")
    st.markdown("### *Analyzing Global Flight Delays and Their Cascading Impact*")
    
    if data_loaded:
        # Key Metrics Row
        col1, col2, col3, col4 = st.columns(4)
        
        total_flights = len(filtered_df)
        delayed_flights = filtered_df['DEP_DEL15'].sum()
        delay_rate = (delayed_flights / total_flights * 100) if total_flights > 0 else 0
        avg_delay = filtered_df[filtered_df['DEP_DEL15'] == 1]['DEP_DELAY'].mean()
        total_cost = filtered_df['DELAY_COST_TOTAL'].sum()
        
        with col1:
            st.markdown(create_metric_card(
                format_number(total_flights),
                "Total Flights",
                "Jan - Dec 2024"
            ), unsafe_allow_html=True)
        
        with col2:
            st.markdown(create_metric_card(
                f"{delay_rate:.1f}%",
                "Delay Rate",
                f"{format_number(delayed_flights)} delayed",
                "negative" if delay_rate > 25 else "positive"
            ), unsafe_allow_html=True)
        
        with col3:
            st.markdown(create_metric_card(
                f"{avg_delay:.0f} min",
                "Avg Delay Duration",
                "When delayed",
                "negative"
            ), unsafe_allow_html=True)
        
        with col4:
            st.markdown(create_metric_card(
                format_currency(total_cost),
                "Total Delay Cost",
                "Airline + Passenger",
                "negative"
            ), unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Two column layout
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### 🌍 Global Delay Overview")
            
            airport_delays = filtered_df.groupby('ORIGIN').agg({
                'DEP_DEL15': ['count', 'sum', 'mean']
            }).reset_index()
            airport_delays.columns = ['ORIGIN', 'total_flights', 'delayed_flights', 'delay_rate']
            airport_delays = airport_delays.merge(airports_df, left_on='ORIGIN', right_on='code', how='left')
            
            fig_map = px.scatter_geo(
                airport_delays,
                lat='lat',
                lon='lon',
                size='total_flights',
                color='delay_rate',
                hover_name='name',
                hover_data={
                    'total_flights': True,
                    'delayed_flights': True,
                    'delay_rate': ':.1%',
                    'lat': False,
                    'lon': False
                },
                color_continuous_scale='RdYlGn_r',
                size_max=40,
                title=""
            )
            
            fig_map.update_layout(
                geo=dict(
                    showland=True,
                    landcolor='#1E2130',
                    showocean=True,
                    oceancolor='#0E1117',
                    showcoastlines=True,
                    coastlinecolor='#3D4663',
                    projection_type='natural earth',
                    bgcolor='#0E1117'
                ),
                paper_bgcolor='#0E1117',
                plot_bgcolor='#0E1117',
                font_color='#FFFFFF',
                margin=dict(l=0, r=0, t=30, b=0),
                height=450,
                coloraxis_colorbar=dict(
                    title="Delay Rate",
                    tickformat=".0%"
                )
            )
            
            st.plotly_chart(fig_map, use_container_width=True)
        
        with col2:
            st.markdown("### 📊 Regional Performance")
            
            region_stats = filtered_df.groupby('ORIGIN_REGION').agg({
                'DEP_DEL15': ['count', 'mean']
            }).reset_index()
            region_stats.columns = ['Region', 'Flights', 'Delay Rate']
            region_stats = region_stats.sort_values('Delay Rate', ascending=True)
            
            fig_region = go.Figure()
            
            fig_region.add_trace(go.Bar(
                y=region_stats['Region'],
                x=region_stats['Delay Rate'] * 100,
                orientation='h',
                marker=dict(
                    color=region_stats['Delay Rate'],
                    colorscale='RdYlGn_r',
                    line=dict(width=0)
                ),
                text=[f"{x:.1f}%" for x in region_stats['Delay Rate'] * 100],
                textposition='outside',
                textfont=dict(color='white', size=12)
            ))
            
            fig_region.update_layout(
                paper_bgcolor='#0E1117',
                plot_bgcolor='#0E1117',
                font_color='#FFFFFF',
                height=400,
                margin=dict(l=0, r=50, t=30, b=0),
                xaxis=dict(
                    title="Delay Rate (%)",
                    gridcolor='#2D3748',
                    range=[0, max(region_stats['Delay Rate'] * 100) * 1.3]
                ),
                yaxis=dict(title="", gridcolor='#2D3748'),
                showlegend=False
            )
            
            st.plotly_chart(fig_region, use_container_width=True)
        
        st.markdown("---")
        
        # Quick Insights
        st.markdown("### 💡 Quick Insights")
        
        col1, col2, col3 = st.columns(3)
        
        worst_region = filtered_df.groupby('ORIGIN_REGION')['DEP_DEL15'].mean().idxmax()
        worst_region_rate = filtered_df.groupby('ORIGIN_REGION')['DEP_DEL15'].mean().max() * 100
        
        best_airline = filtered_df.groupby('AIRLINE_NAME')['DEP_DEL15'].mean().idxmin()
        best_airline_rate = filtered_df.groupby('AIRLINE_NAME')['DEP_DEL15'].mean().min() * 100
        
        worst_hour = filtered_df.groupby('DEP_HOUR')['DEP_DEL15'].mean().idxmax()
        
        with col1:
            st.markdown(f"""
            <div class="info-card">
                <h4>🌍 Most Affected Region</h4>
                <p><span class="stat-highlight">{worst_region}</span></p>
                <p style="color: #B0B8C4;">{worst_region_rate:.1f}% delay rate</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="info-card">
                <h4>✈️ Best Performing Airline</h4>
                <p><span class="stat-highlight">{best_airline}</span></p>
                <p style="color: #B0B8C4;">{best_airline_rate:.1f}% delay rate</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="info-card">
                <h4>🕐 Worst Time to Fly</h4>
                <p><span class="stat-highlight">{worst_hour}:00</span></p>
                <p style="color: #B0B8C4;">Highest delay probability</p>
            </div>
            """, unsafe_allow_html=True)

# === PAGE: DELAY PATTERNS (with Drill Down) ===
elif page == "📊 Delay Patterns":
    
    st.markdown("# 📊 Delay Patterns Analysis")
    st.markdown("### *Understanding When and Where Delays Occur*")
    st.markdown("##### 🔍 Click on any element to drill down for more details")
    
    if data_loaded:
        
        tab1, tab2, tab3 = st.tabs(["✈️ By Airline", "🏢 By Airport", "🕐 By Time"])
        
        # TAB 1: BY AIRLINE with Drill Down
        with tab1:
            st.markdown("### Airline Performance Comparison")
            
            airline_stats = filtered_df.groupby(['OP_UNIQUE_CARRIER', 'AIRLINE_NAME']).agg({
                'DEP_DEL15': ['count', 'sum', 'mean'],
                'DEP_DELAY': 'mean',
                'DELAY_COST_TOTAL': 'sum'
            }).reset_index()
            airline_stats.columns = ['Code', 'Airline', 'Total Flights', 'Delayed Flights', 'Delay Rate', 'Avg Delay', 'Total Cost']
            airline_stats = airline_stats.sort_values('Total Flights', ascending=False).head(15)
            
            fig_airline = go.Figure()
            
            fig_airline.add_trace(go.Bar(
                y=airline_stats['Airline'],
                x=airline_stats['Delay Rate'] * 100,
                orientation='h',
                marker=dict(
                    color=airline_stats['Delay Rate'] * 100,
                    colorscale='RdYlGn_r',
                    cmin=15,
                    cmax=45
                ),
                text=[f"{x:.1f}%" for x in airline_stats['Delay Rate'] * 100],
                textposition='outside',
                hovertemplate="<b>%{y}</b><br>Delay Rate: %{x:.1f}%<br><extra></extra>",
                customdata=airline_stats[['Code']].values
            ))
            
            fig_airline.update_layout(
                paper_bgcolor='#0E1117',
                plot_bgcolor='#0E1117',
                font_color='#FFFFFF',
                height=500,
                margin=dict(l=0, r=100, t=30, b=50),
                xaxis=dict(title="Delay Rate (%)", gridcolor='#2D3748'),
                yaxis=dict(title="", categoryorder='total ascending'),
                showlegend=False
            )
            
            st.plotly_chart(fig_airline, use_container_width=True)
            
            # Drill Down Section
            st.markdown("### 🔍 Drill Down: Select an Airline")
            
            selected_airline = st.selectbox(
                "Choose airline for detailed analysis",
                options=airline_stats['Airline'].tolist(),
                key='airline_drill'
            )
            
            if selected_airline:
                airline_code = airline_stats[airline_stats['Airline'] == selected_airline]['Code'].values[0]
                airline_data = filtered_df[filtered_df['OP_UNIQUE_CARRIER'] == airline_code]
                
                st.markdown(f"""
                <div class="drill-down-card">
                    <h4>📊 {selected_airline} - Detailed Analysis</h4>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Total Flights", f"{len(airline_data):,}")
                with col2:
                    st.metric("Delay Rate", f"{airline_data['DEP_DEL15'].mean()*100:.1f}%")
                with col3:
                    st.metric("Avg Delay", f"{airline_data[airline_data['DEP_DEL15']==1]['DEP_DELAY'].mean():.0f} min")
                with col4:
                    st.metric("Total Cost", format_currency(airline_data['DELAY_COST_TOTAL'].sum()))
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### Monthly Trend")
                    monthly = airline_data.groupby('MONTH')['DEP_DEL15'].mean().reset_index()
                    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                    
                    fig_monthly = go.Figure()
                    fig_monthly.add_trace(go.Scatter(
                        x=month_names,
                        y=monthly['DEP_DEL15'] * 100,
                        mode='lines+markers',
                        line=dict(color='#FF6B6B', width=3),
                        marker=dict(size=10)
                    ))
                    fig_monthly.update_layout(
                        paper_bgcolor='#0E1117',
                        plot_bgcolor='#0E1117',
                        font_color='#FFFFFF',
                        height=250,
                        xaxis=dict(title="", gridcolor='#2D3748'),
                        yaxis=dict(title="Delay Rate (%)", gridcolor='#2D3748'),
                        margin=dict(l=50, r=20, t=20, b=50)
                    )
                    st.plotly_chart(fig_monthly, use_container_width=True)
                
                with col2:
                    st.markdown("#### Top Routes (by delays)")
                    airline_data['ROUTE'] = airline_data['ORIGIN'] + ' → ' + airline_data['DEST']
                    route_stats = airline_data.groupby('ROUTE')['DEP_DEL15'].agg(['count', 'mean']).reset_index()
                    route_stats.columns = ['Route', 'Flights', 'Delay Rate']
                    route_stats = route_stats[route_stats['Flights'] >= 10].nlargest(5, 'Delay Rate')
                    
                    fig_routes = go.Figure()
                    fig_routes.add_trace(go.Bar(
                        y=route_stats['Route'],
                        x=route_stats['Delay Rate'] * 100,
                        orientation='h',
                        marker_color='#FFB74D'
                    ))
                    fig_routes.update_layout(
                        paper_bgcolor='#0E1117',
                        plot_bgcolor='#0E1117',
                        font_color='#FFFFFF',
                        height=250,
                        xaxis=dict(title="Delay Rate (%)", gridcolor='#2D3748'),
                        yaxis=dict(title=""),
                        margin=dict(l=100, r=20, t=20, b=50)
                    )
                    st.plotly_chart(fig_routes, use_container_width=True)
        
        # TAB 2: BY AIRPORT with Drill Down
        with tab2:
            st.markdown("### Airport Delay Rankings")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 🔴 Most Delayed Airports")
                
                airport_stats = filtered_df.groupby('ORIGIN').agg({
                    'DEP_DEL15': ['count', 'mean']
                }).reset_index()
                airport_stats.columns = ['Airport', 'Flights', 'Delay Rate']
                airport_stats = airport_stats[airport_stats['Flights'] >= 100]
                
                worst_airports = airport_stats.nlargest(10, 'Delay Rate')
                worst_airports = worst_airports.merge(airports_df[['code', 'name', 'city']], left_on='Airport', right_on='code')
                
                fig_worst = go.Figure()
                fig_worst.add_trace(go.Bar(
                    x=worst_airports['Delay Rate'] * 100,
                    y=worst_airports['code'] + ' - ' + worst_airports['city'],
                    orientation='h',
                    marker_color='#FF5252',
                    text=[f"{x:.1f}%" for x in worst_airports['Delay Rate'] * 100],
                    textposition='outside'
                ))
                
                fig_worst.update_layout(
                    paper_bgcolor='#0E1117',
                    plot_bgcolor='#0E1117',
                    font_color='#FFFFFF',
                    height=400,
                    margin=dict(l=0, r=80, t=10, b=50),
                    xaxis=dict(title="Delay Rate (%)", gridcolor='#2D3748'),
                    yaxis=dict(title="", categoryorder='total ascending'),
                    showlegend=False
                )
                
                st.plotly_chart(fig_worst, use_container_width=True)
            
            with col2:
                st.markdown("#### 🟢 Best Performing Airports")
                
                best_airports = airport_stats.nsmallest(10, 'Delay Rate')
                best_airports = best_airports.merge(airports_df[['code', 'name', 'city']], left_on='Airport', right_on='code')
                
                fig_best = go.Figure()
                fig_best.add_trace(go.Bar(
                    x=best_airports['Delay Rate'] * 100,
                    y=best_airports['code'] + ' - ' + best_airports['city'],
                    orientation='h',
                    marker_color='#69F0AE',
                    text=[f"{x:.1f}%" for x in best_airports['Delay Rate'] * 100],
                    textposition='outside'
                ))
                
                fig_best.update_layout(
                    paper_bgcolor='#0E1117',
                    plot_bgcolor='#0E1117',
                    font_color='#FFFFFF',
                    height=400,
                    margin=dict(l=0, r=80, t=10, b=50),
                    xaxis=dict(title="Delay Rate (%)", gridcolor='#2D3748'),
                    yaxis=dict(title="", categoryorder='total descending'),
                    showlegend=False
                )
                
                st.plotly_chart(fig_best, use_container_width=True)
            
            # Airport Drill Down
            st.markdown("### 🔍 Drill Down: Select an Airport")
            
            airport_list = airports_df['code'].tolist()
            selected_airport = st.selectbox("Choose airport for detailed analysis", airport_list, key='airport_drill')
            
            if selected_airport:
                airport_data = filtered_df[filtered_df['ORIGIN'] == selected_airport]
                airport_info = airports_df[airports_df['code'] == selected_airport].iloc[0]
                
                if len(airport_data) > 0:
                    st.markdown(f"""
                    <div class="drill-down-card">
                        <h4>🏢 {airport_info['name']} ({selected_airport}) - {airport_info['city']}</h4>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Departures", f"{len(airport_data):,}")
                    with col2:
                        st.metric("Delay Rate", f"{airport_data['DEP_DEL15'].mean()*100:.1f}%")
                    with col3:
                        st.metric("Airlines Operating", f"{airport_data['OP_UNIQUE_CARRIER'].nunique()}")
                    with col4:
                        st.metric("Destinations", f"{airport_data['DEST'].nunique()}")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("#### Hourly Delay Pattern")
                        hourly = airport_data.groupby('DEP_HOUR')['DEP_DEL15'].mean().reset_index()
                        
                        fig_hourly = go.Figure()
                        fig_hourly.add_trace(go.Bar(
                            x=hourly['DEP_HOUR'],
                            y=hourly['DEP_DEL15'] * 100,
                            marker_color=['#FF5252' if x > 0.35 else '#FFB74D' if x > 0.25 else '#69F0AE' for x in hourly['DEP_DEL15']]
                        ))
                        fig_hourly.update_layout(
                            paper_bgcolor='#0E1117',
                            plot_bgcolor='#0E1117',
                            font_color='#FFFFFF',
                            height=250,
                            xaxis=dict(title="Hour", gridcolor='#2D3748'),
                            yaxis=dict(title="Delay Rate (%)", gridcolor='#2D3748')
                        )
                        st.plotly_chart(fig_hourly, use_container_width=True)
                    
                    with col2:
                        st.markdown("#### Top Airlines at this Airport")
                        airport_airlines = airport_data.groupby('AIRLINE_NAME')['DEP_DEL15'].agg(['count', 'mean']).reset_index()
                        airport_airlines.columns = ['Airline', 'Flights', 'Delay Rate']
                        airport_airlines = airport_airlines.nlargest(5, 'Flights')
                        
                        fig_airport_airlines = go.Figure()
                        fig_airport_airlines.add_trace(go.Bar(
                            y=airport_airlines['Airline'],
                            x=airport_airlines['Delay Rate'] * 100,
                            orientation='h',
                            marker_color='#42A5F5'
                        ))
                        fig_airport_airlines.update_layout(
                            paper_bgcolor='#0E1117',
                            plot_bgcolor='#0E1117',
                            font_color='#FFFFFF',
                            height=250,
                            xaxis=dict(title="Delay Rate (%)", gridcolor='#2D3748'),
                            yaxis=dict(title="")
                        )
                        st.plotly_chart(fig_airport_airlines, use_container_width=True)
                else:
                    st.warning(f"No data available for {selected_airport}")
        
        # TAB 3: BY TIME
        with tab3:
            st.markdown("### Time-Based Delay Patterns")
            
            # Heatmap: Hour vs Day of Week
            st.markdown("#### 🕐 Delay Heatmap: Hour × Day of Week")
            
            heatmap_data = filtered_df.groupby(['DAY_OF_WEEK', 'DEP_HOUR'])['DEP_DEL15'].mean().reset_index()
            heatmap_pivot = heatmap_data.pivot(index='DEP_HOUR', columns='DAY_OF_WEEK', values='DEP_DEL15')
            
            day_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            
            fig_heatmap = go.Figure(data=go.Heatmap(
                z=heatmap_pivot.values * 100,
                x=day_names,
                y=[f"{h:02d}:00" for h in heatmap_pivot.index],
                colorscale='RdYlGn_r',
                text=[[f"{val:.0f}%" for val in row] for row in heatmap_pivot.values * 100],
                texttemplate="%{text}",
                textfont={"size": 10},
                hovertemplate="Day: %{x}<br>Hour: %{y}<br>Delay Rate: %{z:.1f}%<extra></extra>"
            ))
            
            fig_heatmap.update_layout(
                paper_bgcolor='#0E1117',
                plot_bgcolor='#0E1117',
                font_color='#FFFFFF',
                height=600,
                margin=dict(l=80, r=50, t=30, b=50),
                xaxis=dict(title="Day of Week", side='bottom'),
                yaxis=dict(title="Hour of Day", autorange='reversed')
            )
            
            st.plotly_chart(fig_heatmap, use_container_width=True)

# === PAGE: SEASONALITY HEATMAP ===
elif page == "🔥 Seasonality":
    
    st.markdown("# 🔥 Seasonality Analysis")
    st.markdown("### *Understanding Seasonal Delay Patterns Across Regions*")
    
    if data_loaded:
        
        # Month x Region Heatmap
        st.markdown("### 📅 Delay Rate: Month × Region")
        
        seasonality_data = filtered_df.groupby(['MONTH', 'ORIGIN_REGION'])['DEP_DEL15'].mean().reset_index()
        seasonality_pivot = seasonality_data.pivot(index='ORIGIN_REGION', columns='MONTH', values='DEP_DEL15')
        
        month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        
        fig_season = go.Figure(data=go.Heatmap(
            z=seasonality_pivot.values * 100,
            x=month_names,
            y=seasonality_pivot.index,
            colorscale='RdYlGn_r',
            text=[[f"{val:.0f}%" for val in row] for row in seasonality_pivot.values * 100],
            texttemplate="%{text}",
            textfont={"size": 12},
            hovertemplate="Region: %{y}<br>Month: %{x}<br>Delay Rate: %{z:.1f}%<extra></extra>",
            colorbar=dict(title="Delay %")
        ))
        
        fig_season.update_layout(
            paper_bgcolor='#0E1117',
            plot_bgcolor='#0E1117',
            font_color='#FFFFFF',
            height=400,
            margin=dict(l=150, r=50, t=30, b=50),
            xaxis=dict(title="Month"),
            yaxis=dict(title="")
        )
        
        st.plotly_chart(fig_season, use_container_width=True)
        
        # Insights from seasonality
        st.markdown("### 💡 Seasonal Insights")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="info-card">
                <h4>🌧️ India - Monsoon Effect</h4>
                <p><strong>Peak Delays:</strong> June - September</p>
                <p>Heavy rainfall disrupts operations at major airports like Mumbai (BOM) and Delhi (DEL)</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="info-card">
                <h4>❄️ North America - Winter Storms</h4>
                <p><strong>Peak Delays:</strong> December - February</p>
                <p>Snow and ice affect Chicago (ORD), Denver (DEN), and Northeast airports</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="info-card">
                <h4>🌫️ Middle East - Fog Season</h4>
                <p><strong>Peak Delays:</strong> December - February</p>
                <p>Morning fog impacts Dubai (DXB) and other Gulf airports</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="info-card">
                <h4>☀️ Europe - Summer Rush</h4>
                <p><strong>Peak Delays:</strong> June - August</p>
                <p>High passenger volume strains airport capacity</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Month x Day of Week Heatmap
        st.markdown("### 📆 Delay Rate: Month × Day of Week")
        
        month_dow = filtered_df.groupby(['MONTH', 'DAY_OF_WEEK'])['DEP_DEL15'].mean().reset_index()
        month_dow_pivot = month_dow.pivot(index='DAY_OF_WEEK', columns='MONTH', values='DEP_DEL15')
        
        day_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        
        fig_month_dow = go.Figure(data=go.Heatmap(
            z=month_dow_pivot.values * 100,
            x=month_names,
            y=day_names,
            colorscale='RdYlGn_r',
            text=[[f"{val:.0f}%" for val in row] for row in month_dow_pivot.values * 100],
            texttemplate="%{text}",
            textfont={"size": 11},
            hovertemplate="Day: %{y}<br>Month: %{x}<br>Delay Rate: %{z:.1f}%<extra></extra>"
        ))
        
        fig_month_dow.update_layout(
            paper_bgcolor='#0E1117',
            plot_bgcolor='#0E1117',
            font_color='#FFFFFF',
            height=350,
            margin=dict(l=80, r=50, t=30, b=50),
            xaxis=dict(title="Month"),
            yaxis=dict(title="")
        )
        
        st.plotly_chart(fig_month_dow, use_container_width=True)
        
        # Time Period Analysis
        st.markdown("### 🕐 Delay by Time Period Across Months")
        
        period_month = filtered_df.groupby(['MONTH', 'DEP_PERIOD'])['DEP_DEL15'].mean().reset_index()
        
        fig_period_month = px.line(
            period_month,
            x='MONTH',
            y='DEP_DEL15',
            color='DEP_PERIOD',
            markers=True,
            labels={'DEP_DEL15': 'Delay Rate', 'MONTH': 'Month', 'DEP_PERIOD': 'Time Period'},
            color_discrete_map={
                'Morning': '#FFB74D',
                'Afternoon': '#FF6B6B',
                'Evening': '#9575CD',
                'Night': '#42A5F5'
            }
        )
        
        fig_period_month.update_layout(
            paper_bgcolor='#0E1117',
            plot_bgcolor='#0E1117',
            font_color='#FFFFFF',
            height=400,
            xaxis=dict(
                title="Month",
                tickmode='array',
                tickvals=list(range(1, 13)),
                ticktext=month_names,
                gridcolor='#2D3748'
            ),
            yaxis=dict(title="Delay Rate", tickformat=".0%", gridcolor='#2D3748'),
            legend=dict(orientation='h', yanchor='bottom', y=1.02)
        )
        
        fig_period_month.update_traces(line=dict(width=3))
        
        st.plotly_chart(fig_period_month, use_container_width=True)

# === PAGE: PARETO ANALYSIS ===
elif page == "📈 Pareto Analysis":
    
    st.markdown("# 📈 Pareto Analysis")
    st.markdown("### *The 80/20 Rule in Flight Delays*")
    
    st.markdown("""
    <div class="info-card">
        <h4>📊 What is Pareto Analysis?</h4>
        <p>The Pareto Principle (80/20 rule) suggests that roughly 80% of effects come from 20% of causes.</p>
        <p>In flight delays: <strong>A small number of airlines/airports may be responsible for most delays.</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    if data_loaded:
        
        tab1, tab2, tab3 = st.tabs(["✈️ Airlines", "🏢 Airports", "🛤️ Routes"])
        
        with tab1:
            st.markdown("### ✈️ Airline Pareto Analysis")
            
            delayed_by_airline = filtered_df[filtered_df['DEP_DEL15'] == 1].groupby('AIRLINE_NAME').size().reset_index(name='delayed_count')
            
            fig_pareto_airline, pareto_data = create_pareto_chart(
                delayed_by_airline, 
                'AIRLINE_NAME', 
                'delayed_count',
                'Airlines Contributing to Delays'
            )
            
            st.plotly_chart(fig_pareto_airline, use_container_width=True)
            
            # Find 80% threshold
            threshold_80 = pareto_data[pareto_data['cumulative_pct'] <= 80]
            num_airlines_80 = len(threshold_80)
            total_airlines = len(pareto_data)
            
            st.markdown(f"""
            <div class="pareto-insight">
                <h4>🎯 Key Finding</h4>
                <p><strong>{num_airlines_80} airlines</strong> ({num_airlines_80/total_airlines*100:.0f}% of total) account for <strong>80%</strong> of all delayed flights.</p>
                <p>Top contributors: {', '.join(threshold_80['AIRLINE_NAME'].head(5).tolist())}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with tab2:
            st.markdown("### 🏢 Airport Pareto Analysis")
            
            delayed_by_airport = filtered_df[filtered_df['DEP_DEL15'] == 1].groupby('ORIGIN').size().reset_index(name='delayed_count')
            delayed_by_airport = delayed_by_airport.merge(airports_df[['code', 'city']], left_on='ORIGIN', right_on='code')
            delayed_by_airport['Airport'] = delayed_by_airport['ORIGIN'] + ' - ' + delayed_by_airport['city']
            
            fig_pareto_airport, pareto_airport_data = create_pareto_chart(
                delayed_by_airport.head(20),
                'Airport',
                'delayed_count',
                'Airports Contributing to Delays (Top 20)'
            )
            
            st.plotly_chart(fig_pareto_airport, use_container_width=True)
            
            threshold_80_airports = pareto_airport_data[pareto_airport_data['cumulative_pct'] <= 80]
            
            st.markdown(f"""
            <div class="pareto-insight">
                <h4>🎯 Key Finding</h4>
                <p><strong>{len(threshold_80_airports)} airports</strong> account for <strong>80%</strong> of all delayed flights.</p>
                <p>Focus improvement efforts on these hub airports for maximum impact.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with tab3:
            st.markdown("### 🛤️ Route Pareto Analysis")
            
            filtered_df['ROUTE'] = filtered_df['ORIGIN'] + ' → ' + filtered_df['DEST']
            delayed_by_route = filtered_df[filtered_df['DEP_DEL15'] == 1].groupby('ROUTE').size().reset_index(name='delayed_count')
            
            fig_pareto_route, pareto_route_data = create_pareto_chart(
                delayed_by_route.head(20),
                'ROUTE',
                'delayed_count',
                'Routes Contributing to Delays (Top 20)'
            )
            
            st.plotly_chart(fig_pareto_route, use_container_width=True)
            
            threshold_80_routes = pareto_route_data[pareto_route_data['cumulative_pct'] <= 80]
            
            st.markdown(f"""
            <div class="pareto-insight">
                <h4>🎯 Key Finding</h4>
                <p><strong>{len(threshold_80_routes)} routes</strong> account for <strong>80%</strong> of delays in top 20.</p>
                <p>These high-traffic routes need operational optimization.</p>
            </div>
            """, unsafe_allow_html=True)

# === PAGE: RIPPLE EFFECT ===
elif page == "🌊 Ripple Effect":
    
    st.markdown("# 🌊 The Domino Effect")
    st.markdown("### *How One Delay Triggers Many More*")
    
    if data_loaded:
        
        st.markdown("""
        <div class="info-card">
            <h4>🎯 Understanding the Domino Effect</h4>
            <p>When a flight is delayed, the aircraft, crew, and passengers are all late for subsequent flights. 
            This creates a <strong>cascading effect</strong> where one delay can impact dozens of other flights throughout the day.</p>
            <p><strong>Late Aircraft Delay</strong> is the key indicator of this domino effect.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🧩 Delay Cause Breakdown")
            
            delayed_flights = filtered_df[filtered_df['DEP_DEL15'] == 1].copy()
            
            cause_totals = {
                'Carrier Issues': delayed_flights['CARRIER_DELAY'].sum(),
                'Weather': delayed_flights['WEATHER_DELAY'].sum(),
                'Air Traffic (NAS)': delayed_flights['NAS_DELAY'].sum(),
                'Security': delayed_flights['SECURITY_DELAY'].sum(),
                'Late Aircraft': delayed_flights['LATE_AIRCRAFT_DELAY'].sum()
            }
            
            cause_df = pd.DataFrame(list(cause_totals.items()), columns=['Cause', 'Total Minutes'])
            cause_df = cause_df.sort_values('Total Minutes', ascending=True)
            
            colors_causes = ['#42A5F5', '#FFB74D', '#9575CD', '#4CAF50', '#FF5252']
            
            fig_causes = go.Figure()
            fig_causes.add_trace(go.Bar(
                y=cause_df['Cause'],
                x=cause_df['Total Minutes'],
                orientation='h',
                marker_color=colors_causes,
                text=[format_number(x) + ' min' for x in cause_df['Total Minutes']],
                textposition='outside'
            ))
            
            fig_causes.update_layout(
                paper_bgcolor='#0E1117',
                plot_bgcolor='#0E1117',
                font_color='#FFFFFF',
                height=350,
                margin=dict(l=0, r=100, t=30, b=50),
                xaxis=dict(title="Total Delay Minutes", gridcolor='#2D3748'),
                yaxis=dict(title=""),
                showlegend=False
            )
            
            st.plotly_chart(fig_causes, use_container_width=True)
        
        with col2:
            st.markdown("### 🌳 Delay Distribution")
            
            cause_pct = cause_df.copy()
            cause_pct['Percentage'] = cause_pct['Total Minutes'] / cause_pct['Total Minutes'].sum() * 100
            
            fig_tree = px.treemap(
                cause_pct,
                path=['Cause'],
                values='Total Minutes',
                color='Percentage',
                color_continuous_scale='RdYlGn_r',
                custom_data=['Percentage']
            )
            
            fig_tree.update_traces(
                texttemplate="<b>%{label}</b><br>%{customdata[0]:.1f}%",
                textfont=dict(size=14)
            )
            
            fig_tree.update_layout(
                paper_bgcolor='#0E1117',
                plot_bgcolor='#0E1117',
                font_color='#FFFFFF',
                height=350,
                margin=dict(l=10, r=10, t=30, b=10),
                coloraxis_showscale=False
            )
            
            st.plotly_chart(fig_tree, use_container_width=True)
        
        st.markdown("---")
        
        # Late Aircraft Cascade
        st.markdown("### ✈️ Late Aircraft: The Domino Trigger")
        
        col1, col2, col3 = st.columns(3)
        
        late_aircraft_delays = delayed_flights[delayed_flights['LATE_AIRCRAFT_DELAY'] > 0]
        
        with col1:
            pct_late_aircraft = len(late_aircraft_delays) / len(delayed_flights) * 100 if len(delayed_flights) > 0 else 0
            st.markdown(create_metric_card(
                f"{pct_late_aircraft:.1f}%",
                "Delays Involve Late Aircraft",
                "Primary domino indicator"
            ), unsafe_allow_html=True)
        
        with col2:
            avg_late_aircraft = late_aircraft_delays['LATE_AIRCRAFT_DELAY'].mean() if len(late_aircraft_delays) > 0 else 0
            st.markdown(create_metric_card(
                f"{avg_late_aircraft:.0f} min",
                "Avg Late Aircraft Delay",
                "Per affected flight"
            ), unsafe_allow_html=True)
        
        with col3:
            total_late_cost = late_aircraft_delays['DELAY_COST_TOTAL'].sum()
            st.markdown(create_metric_card(
                format_currency(total_late_cost),
                "Cost from Late Aircraft",
                "Cascading impact"
            ), unsafe_allow_html=True)
        
        # Cascade visualization
        st.markdown("### 🔄 Delay Propagation by Time of Day")
        
        hourly_late = delayed_flights.groupby('DEP_HOUR').agg({
            'LATE_AIRCRAFT_DELAY': ['count', 'mean']
        }).reset_index()
        hourly_late.columns = ['Hour', 'Count', 'Avg Delay']
        
        fig_cascade = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig_cascade.add_trace(
            go.Bar(
                x=hourly_late['Hour'],
                y=hourly_late['Count'],
                name='Flights with Late Aircraft',
                marker_color='#FF6B6B'
            ),
            secondary_y=False
        )
        
        fig_cascade.add_trace(
            go.Scatter(
                x=hourly_late['Hour'],
                y=hourly_late['Avg Delay'],
                name='Avg Cascade Delay (min)',
                line=dict(color='#42A5F5', width=3),
                mode='lines+markers'
            ),
            secondary_y=True
        )
        
        fig_cascade.update_layout(
            paper_bgcolor='#0E1117',
            plot_bgcolor='#0E1117',
            font_color='#FFFFFF',
            height=400,
            xaxis=dict(title="Hour of Day", gridcolor='#2D3748'),
            yaxis=dict(title="Number of Flights", gridcolor='#2D3748'),
            yaxis2=dict(title="Avg Delay (min)", gridcolor='#2D3748'),
            legend=dict(orientation='h', yanchor='bottom', y=1.02),
            margin=dict(t=60)
        )
        
        st.plotly_chart(fig_cascade, use_container_width=True)
        
        st.markdown("""
        <div class="info-card">
            <h4>💡 Insight: The Cascade Effect</h4>
            <p>Notice how <strong>late aircraft delays increase throughout the day</strong>. 
            Early morning flights start on time, but as delays accumulate, afternoon and evening flights face compounding issues.</p>
            <p><strong>Recommendation:</strong> Book early morning flights for lowest delay risk.</p>
        </div>
        """, unsafe_allow_html=True)

# === PAGE: IMPACT ANALYSIS ===
elif page == "💰 Impact Analysis":
    
    st.markdown("# 💰 Economic Impact Analysis")
    st.markdown("### *The True Cost of Flight Delays*")
    
    if data_loaded:
        
        st.markdown("""
        <div class="info-card">
            <h4>💵 Cost Calculation Methodology</h4>
            <p><strong>Airline Cost:</strong> $74.20 per minute (fuel, crew, maintenance, opportunity cost)</p>
            <p><strong>Passenger Cost:</strong> $47.00 per minute (time value, missed connections, accommodation)</p>
            <p><em>Source: FAA/Eurocontrol industry estimates</em></p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        total_airline_cost = filtered_df['DELAY_COST_AIRLINE'].sum()
        total_passenger_cost = filtered_df['DELAY_COST_PASSENGER'].sum()
        total_cost = filtered_df['DELAY_COST_TOTAL'].sum()
        avg_cost_per_delay = filtered_df[filtered_df['DEP_DEL15'] == 1]['DELAY_COST_TOTAL'].mean()
        
        with col1:
            st.markdown(create_metric_card(
                format_currency(total_airline_cost),
                "Airline Losses",
                "Direct operational cost"
            ), unsafe_allow_html=True)
        
        with col2:
            st.markdown(create_metric_card(
                format_currency(total_passenger_cost),
                "Passenger Impact",
                "Time & inconvenience"
            ), unsafe_allow_html=True)
        
        with col3:
            st.markdown(create_metric_card(
                format_currency(total_cost),
                "Total Economic Loss",
                "Combined impact"
            ), unsafe_allow_html=True)
        
        with col4:
            st.markdown(create_metric_card(
                format_currency(avg_cost_per_delay),
                "Avg Cost per Delay",
                "Per delayed flight"
            ), unsafe_allow_html=True)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🌍 Cost by Region")
            
            region_cost = filtered_df.groupby('ORIGIN_REGION')['DELAY_COST_TOTAL'].sum().reset_index()
            region_cost.columns = ['Region', 'Total Cost']
            region_cost = region_cost.sort_values('Total Cost', ascending=True)
            
            fig_region_cost = go.Figure()
            fig_region_cost.add_trace(go.Bar(
                y=region_cost['Region'],
                x=region_cost['Total Cost'],
                orientation='h',
                marker_color='#FF6B6B',
                text=[format_currency(x) for x in region_cost['Total Cost']],
                textposition='outside'
            ))
            
            fig_region_cost.update_layout(
                paper_bgcolor='#0E1117',
                plot_bgcolor='#0E1117',
                font_color='#FFFFFF',
                height=350,
                margin=dict(l=0, r=100, t=30, b=50),
                xaxis=dict(title="Total Delay Cost ($)", gridcolor='#2D3748'),
                yaxis=dict(title=""),
                showlegend=False
            )
            
            st.plotly_chart(fig_region_cost, use_container_width=True)
        
        with col2:
            st.markdown("### 📊 Cost Breakdown")
            
            fig_donut = go.Figure(data=[go.Pie(
                labels=['Airline Cost', 'Passenger Cost'],
                values=[total_airline_cost, total_passenger_cost],
                hole=0.6,
                marker_colors=['#FF6B6B', '#42A5F5'],
                textinfo='label+percent',
                textposition='outside'
            )])
            
            fig_donut.update_layout(
                paper_bgcolor='#0E1117',
                plot_bgcolor='#0E1117',
                font_color='#FFFFFF',
                height=350,
                showlegend=False,
                annotations=[dict(
                    text=format_currency(total_cost),
                    x=0.5, y=0.5,
                    font_size=20,
                    font_color='#FFFFFF',
                    showarrow=False
                )]
            )
            
            st.plotly_chart(fig_donut, use_container_width=True)
        
        # Monthly cost trend
        st.markdown("### 📈 Monthly Cost Trend")
        
        monthly_cost = filtered_df.groupby('MONTH').agg({
            'DELAY_COST_AIRLINE': 'sum',
            'DELAY_COST_PASSENGER': 'sum',
            'DELAY_COST_TOTAL': 'sum'
        }).reset_index()
        
        month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        
        fig_monthly_cost = go.Figure()
        
        fig_monthly_cost.add_trace(go.Bar(
            x=month_names,
            y=monthly_cost['DELAY_COST_AIRLINE'],
            name='Airline Cost',
            marker_color='#FF6B6B'
        ))
        
        fig_monthly_cost.add_trace(go.Bar(
            x=month_names,
            y=monthly_cost['DELAY_COST_PASSENGER'],
            name='Passenger Cost',
            marker_color='#42A5F5'
        ))
        
        fig_monthly_cost.update_layout(
            paper_bgcolor='#0E1117',
            plot_bgcolor='#0E1117',
            font_color='#FFFFFF',
            height=400,
            barmode='stack',
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
            xaxis=dict(title=""),
            yaxis=dict(title="Cost ($)", gridcolor='#2D3748'),
            margin=dict(t=50)
        )
        
        st.plotly_chart(fig_monthly_cost, use_container_width=True)

# === PAGE: WHAT-IF ANALYSIS ===
elif page == "🔮 What-If Analysis":
    
    st.markdown("# 🔮 What-If Analysis")
    st.markdown("### *Scenario Simulation for Delay Reduction*")
    
    if data_loaded:
        
        st.markdown("""
        <div class="info-card">
            <h4>🎯 Explore Different Scenarios</h4>
            <p>Use the sliders below to simulate the impact of reducing delays in specific areas.</p>
            <p>See how targeted improvements could save costs and improve on-time performance.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Current state
        current_delays = filtered_df['DEP_DEL15'].sum()
        current_delay_rate = filtered_df['DEP_DEL15'].mean() * 100
        current_cost = filtered_df['DELAY_COST_TOTAL'].sum()
        current_avg_delay = filtered_df[filtered_df['DEP_DEL15'] == 1]['DEP_DELAY'].mean()
        
        st.markdown("### 📊 Current State")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Delayed Flights", f"{current_delays:,}")
        with col2:
            st.metric("Delay Rate", f"{current_delay_rate:.1f}%")
        with col3:
            st.metric("Total Cost", format_currency(current_cost))
        with col4:
            st.metric("Avg Delay Duration", f"{current_avg_delay:.0f} min")
        
        st.markdown("---")
        
        # Scenario sliders
        st.markdown("### 🎛️ Scenario Parameters")
        
        col1, col2 = st.columns(2)
        
        with col1:
            carrier_reduction = st.slider(
                "✈️ Reduce Carrier Delays by (%)",
                min_value=0, max_value=50, value=0, step=5,
                help="Improvement in airline operational efficiency"
            )
            
            weather_reduction = st.slider(
                "🌧️ Reduce Weather Delays by (%)",
                min_value=0, max_value=30, value=0, step=5,
                help="Better weather prediction and proactive scheduling"
            )
            
            nas_reduction = st.slider(
                "🗼 Reduce NAS/ATC Delays by (%)",
                min_value=0, max_value=40, value=0, step=5,
                help="Air traffic control improvements"
            )
        
        with col2:
            late_aircraft_reduction = st.slider(
                "🔄 Reduce Late Aircraft Delays by (%)",
                min_value=0, max_value=50, value=0, step=5,
                help="Better aircraft turnaround and scheduling buffer"
            )
            
            delay_duration_reduction = st.slider(
                "⏱️ Reduce Avg Delay Duration by (%)",
                min_value=0, max_value=30, value=0, step=5,
                help="Faster recovery from delays"
            )
        
        # Calculate new scenario
        st.markdown("---")
        st.markdown("### 📈 Simulated Outcome")
        
        # Simplified simulation
        total_reduction_factor = (
            carrier_reduction * 0.35 +  # Carrier is 35% of delays
            weather_reduction * 0.25 +  # Weather is 25%
            nas_reduction * 0.25 +  # NAS is 25%
            late_aircraft_reduction * 0.15  # Late aircraft is 15%
        ) / 100
        
        new_delays = current_delays * (1 - total_reduction_factor)
        new_delay_rate = current_delay_rate * (1 - total_reduction_factor)
        new_avg_delay = current_avg_delay * (1 - delay_duration_reduction/100)
        new_cost = current_cost * (1 - total_reduction_factor) * (1 - delay_duration_reduction/100)
        
        # Savings
        delay_savings = current_delays - new_delays
        cost_savings = current_cost - new_cost
        rate_improvement = current_delay_rate - new_delay_rate
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("New Delayed Flights", f"{new_delays:,.0f}", f"-{delay_savings:,.0f}")
        with col2:
            st.metric("New Delay Rate", f"{new_delay_rate:.1f}%", f"-{rate_improvement:.1f}%")
        with col3:
            st.metric("New Total Cost", format_currency(new_cost), f"-{format_currency(cost_savings)}")
        with col4:
            st.metric("New Avg Duration", f"{new_avg_delay:.0f} min", f"-{current_avg_delay - new_avg_delay:.0f} min")
        
        # Visual comparison
        st.markdown("### 📊 Before vs After Comparison")
        
        comparison_data = {
            'Metric': ['Delayed Flights', 'Delay Rate (%)', 'Total Cost ($M)', 'Avg Delay (min)'],
            'Current': [current_delays, current_delay_rate, current_cost/1e6, current_avg_delay],
            'Simulated': [new_delays, new_delay_rate, new_cost/1e6, new_avg_delay]
        }
        comparison_df = pd.DataFrame(comparison_data)
        
        fig_comparison = go.Figure()
        
        fig_comparison.add_trace(go.Bar(
            name='Current',
            x=comparison_df['Metric'],
            y=comparison_df['Current'],
            marker_color='#FF6B6B'
        ))
        
        fig_comparison.add_trace(go.Bar(
            name='Simulated',
            x=comparison_df['Metric'],
            y=comparison_df['Simulated'],
            marker_color='#69F0AE'
        ))
        
        fig_comparison.update_layout(
            paper_bgcolor='#0E1117',
            plot_bgcolor='#0E1117',
            font_color='#FFFFFF',
            height=400,
            barmode='group',
            legend=dict(orientation='h', yanchor='bottom', y=1.02),
            xaxis=dict(title=""),
            yaxis=dict(title="Value", gridcolor='#2D3748')
        )
        
        st.plotly_chart(fig_comparison, use_container_width=True)
        
        # Summary insight
        if cost_savings > 0:
            st.markdown(f"""
            <div class="whatif-result">
                <h4>✅ Potential Impact Summary</h4>
                <p>With the selected improvements:</p>
                <ul>
                    <li><strong>{delay_savings:,.0f} fewer delayed flights</strong></li>
                    <li><strong>{format_currency(cost_savings)} in cost savings</strong></li>
                    <li><strong>{rate_improvement:.1f} percentage point improvement</strong> in on-time performance</li>
                </ul>
                <p>These improvements would significantly enhance passenger satisfaction and operational efficiency.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="info-card">
                <h4>ℹ️ Adjust the sliders above to see potential improvements</h4>
                <p>Try increasing the reduction percentages to simulate different improvement scenarios.</p>
            </div>
            """, unsafe_allow_html=True)

# === PAGE: DELAY PREDICTOR ===
elif page == "🤖 Delay Predictor":
    
    st.markdown("# 🤖 Flight Delay Predictor")
    st.markdown("### *Machine Learning Model to Predict Delays*")
    
    if data_loaded:
        
        tab1, tab2 = st.tabs(["📊 Model Performance", "🔮 Predict Delay"])
        
        with tab1:
            st.markdown("### Model Training & Evaluation")
            
            @st.cache_data
            def train_model():
                features = ['MONTH', 'DAY_OF_WEEK', 'DEP_HOUR', 'DISTANCE']
                
                model_df = df.copy()
                model_df['ORIGIN_ENCODED'] = pd.factorize(model_df['ORIGIN'])[0]
                model_df['DEST_ENCODED'] = pd.factorize(model_df['DEST'])[0]
                model_df['CARRIER_ENCODED'] = pd.factorize(model_df['OP_UNIQUE_CARRIER'])[0]
                
                features_extended = features + ['ORIGIN_ENCODED', 'DEST_ENCODED', 'CARRIER_ENCODED']
                
                X = model_df[features_extended]
                y = model_df['DEP_DEL15']
                
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
                
                model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1)
                model.fit(X_train, y_train)
                
                y_pred = model.predict(X_test)
                y_prob = model.predict_proba(X_test)[:, 1]
                
                return model, X_test, y_test, y_pred, y_prob, features_extended
            
            with st.spinner("Training model..."):
                model, X_test, y_test, y_pred, y_prob, feature_names = train_model()
            
            st.success("✅ Model trained successfully!")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 📊 Confusion Matrix")
                
                cm = confusion_matrix(y_test, y_pred)
                
                fig_cm = go.Figure(data=go.Heatmap(
                    z=cm,
                    x=['Predicted On-Time', 'Predicted Delayed'],
                    y=['Actual On-Time', 'Actual Delayed'],
                    colorscale='RdYlGn_r',
                    text=cm,
                    texttemplate="%{text:,}",
                    textfont={"size": 16}
                ))
                
                fig_cm.update_layout(
                    paper_bgcolor='#0E1117',
                    plot_bgcolor='#0E1117',
                    font_color='#FFFFFF',
                    height=350,
                    margin=dict(l=50, r=50, t=30, b=50)
                )
                
                st.plotly_chart(fig_cm, use_container_width=True)
            
            with col2:
                st.markdown("#### 📈 ROC Curve")
                
                fpr, tpr, _ = roc_curve(y_test, y_prob)
                roc_auc = auc(fpr, tpr)
                
                fig_roc = go.Figure()
                fig_roc.add_trace(go.Scatter(
                    x=fpr, y=tpr,
                    mode='lines',
                    name=f'ROC Curve (AUC = {roc_auc:.3f})',
                    line=dict(color='#FF6B6B', width=3)
                ))
                fig_roc.add_trace(go.Scatter(
                    x=[0, 1], y=[0, 1],
                    mode='lines',
                    name='Random Classifier',
                    line=dict(color='#4A5568', width=2, dash='dash')
                ))
                
                fig_roc.update_layout(
                    paper_bgcolor='#0E1117',
                    plot_bgcolor='#0E1117',
                    font_color='#FFFFFF',
                    height=350,
                    xaxis=dict(title='False Positive Rate', gridcolor='#2D3748'),
                    yaxis=dict(title='True Positive Rate', gridcolor='#2D3748'),
                    legend=dict(x=0.5, y=0.1),
                    margin=dict(l=50, r=50, t=30, b=50)
                )
                
                st.plotly_chart(fig_roc, use_container_width=True)
            
            # Feature Importance
            st.markdown("#### 🎯 Feature Importance")
            
            importance_df = pd.DataFrame({
                'Feature': feature_names,
                'Importance': model.feature_importances_
            }).sort_values('Importance', ascending=True)
            
            fig_importance = go.Figure()
            fig_importance.add_trace(go.Bar(
                y=importance_df['Feature'],
                x=importance_df['Importance'],
                orientation='h',
                marker_color='#42A5F5'
            ))
            
            fig_importance.update_layout(
                paper_bgcolor='#0E1117',
                plot_bgcolor='#0E1117',
                font_color='#FFFFFF',
                height=300,
                margin=dict(l=0, r=50, t=30, b=50),
                xaxis=dict(title='Importance Score', gridcolor='#2D3748'),
                yaxis=dict(title='')
            )
            
            st.plotly_chart(fig_importance, use_container_width=True)
            
            # Model metrics
            from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
            
            col1, col2, col3, col4 = st.columns(4)
            
            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred)
            recall = recall_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred)
            
            with col1:
                st.markdown(create_metric_card(f"{accuracy*100:.1f}%", "Accuracy"), unsafe_allow_html=True)
            with col2:
                st.markdown(create_metric_card(f"{precision*100:.1f}%", "Precision"), unsafe_allow_html=True)
            with col3:
                st.markdown(create_metric_card(f"{recall*100:.1f}%", "Recall"), unsafe_allow_html=True)
            with col4:
                st.markdown(create_metric_card(f"{roc_auc:.3f}", "AUC Score"), unsafe_allow_html=True)
        
        with tab2:
            st.markdown("### 🔮 Predict Your Flight's Delay Risk")
            
            col1, col2 = st.columns(2)
            
            with col1:
                selected_month = st.selectbox("Month", list(range(1, 13)), format_func=lambda x: pd.Timestamp(2024, x, 1).strftime('%B'))
                selected_day = st.selectbox("Day of Week", list(range(1, 8)), format_func=lambda x: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][x-1])
                selected_hour = st.slider("Departure Hour", 0, 23, 12)
            
            with col2:
                selected_origin = st.selectbox("Origin Airport", airports_df['code'].tolist())
                selected_dest = st.selectbox("Destination Airport", airports_df['code'].tolist())
                selected_airline = st.selectbox("Airline", airlines_df['code'].tolist(), format_func=lambda x: airlines_df[airlines_df['code']==x]['name'].values[0])
            
            if st.button("🔮 Predict Delay Risk", use_container_width=True):
                origin_data = airports_df[airports_df['code'] == selected_origin].iloc[0]
                dest_data = airports_df[airports_df['code'] == selected_dest].iloc[0]
                
                lat1, lon1 = np.radians(origin_data['lat']), np.radians(origin_data['lon'])
                lat2, lon2 = np.radians(dest_data['lat']), np.radians(dest_data['lon'])
                dlat, dlon = lat2 - lat1, lon2 - lon1
                a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
                distance = 3956 * 2 * np.arcsin(np.sqrt(a))
                
                origin_encoded = pd.factorize(df['ORIGIN'])[1].tolist().index(selected_origin) if selected_origin in df['ORIGIN'].values else 0
                dest_encoded = pd.factorize(df['DEST'])[1].tolist().index(selected_dest) if selected_dest in df['DEST'].values else 0
                carrier_encoded = pd.factorize(df['OP_UNIQUE_CARRIER'])[1].tolist().index(selected_airline) if selected_airline in df['OP_UNIQUE_CARRIER'].values else 0
                
                features = [[selected_month, selected_day, selected_hour, distance, origin_encoded, dest_encoded, carrier_encoded]]
                prediction = model.predict(features)[0]
                probability = model.predict_proba(features)[0][1]
                
                st.markdown("---")
                
                if prediction == 1:
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #FF5252 0%, #FF8A80 100%); padding: 2rem; border-radius: 16px; text-align: center;">
                        <h2 style="color: white; margin: 0;">⚠️ HIGH DELAY RISK</h2>
                        <p style="color: white; font-size: 2rem; margin: 1rem 0;">{probability*100:.1f}% chance of delay</p>
                        <p style="color: rgba(255,255,255,0.8);">Consider booking earlier flights or buffer time for connections</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #4CAF50 0%, #81C784 100%); padding: 2rem; border-radius: 16px; text-align: center;">
                        <h2 style="color: white; margin: 0;">✅ LOW DELAY RISK</h2>
                        <p style="color: white; font-size: 2rem; margin: 1rem 0;">{(1-probability)*100:.1f}% chance of on-time</p>
                        <p style="color: rgba(255,255,255,0.8);">Good flight selection!</p>
                    </div>
                    """, unsafe_allow_html=True)

# === PAGE: CASE STUDIES ===
elif page == "📍 Case Studies":
    
    st.markdown("# 📍 Regional Case Studies")
    st.markdown("### *Deep Dive into Specific Markets*")
    
    if data_loaded:
        
        tab1, tab2, tab3 = st.tabs(["🇮🇳 India", "🇦🇪 Gulf Region", "🇺🇸 North America"])
        
        # INDIA TAB
        with tab1:
            st.markdown("## 🇮🇳 India Aviation Analysis")
            
            india_df = df[df['ORIGIN_REGION'] == 'India']
            
            if len(india_df) > 0:
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.markdown(create_metric_card(
                        format_number(len(india_df)),
                        "Total Flights",
                        "India region"
                    ), unsafe_allow_html=True)
                
                with col2:
                    delay_rate = india_df['DEP_DEL15'].mean() * 100
                    st.markdown(create_metric_card(
                        f"{delay_rate:.1f}%",
                        "Delay Rate",
                        "Higher than global avg"
                    ), unsafe_allow_html=True)
                
                with col3:
                    avg_delay = india_df[india_df['DEP_DEL15']==1]['DEP_DELAY'].mean()
                    st.markdown(create_metric_card(
                        f"{avg_delay:.0f} min",
                        "Avg Delay",
                        "When delayed"
                    ), unsafe_allow_html=True)
                
                with col4:
                    total_cost = india_df['DELAY_COST_TOTAL'].sum()
                    st.markdown(create_metric_card(
                        format_currency(total_cost),
                        "Total Cost",
                        "Economic impact"
                    ), unsafe_allow_html=True)
                
                st.markdown("---")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### 📊 Monthly Delay Pattern (Monsoon Effect)")
                    
                    india_monthly = india_df.groupby('MONTH')['DEP_DEL15'].mean().reset_index()
                    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                    
                    colors_monsoon = ['#69F0AE' if m not in [6,7,8,9] else '#FF5252' for m in range(1, 13)]
                    
                    fig_india_monthly = go.Figure()
                    fig_india_monthly.add_trace(go.Bar(
                        x=month_names,
                        y=india_monthly['DEP_DEL15'] * 100,
                        marker_color=colors_monsoon,
                        text=[f"{x:.1f}%" for x in india_monthly['DEP_DEL15'] * 100],
                        textposition='outside'
                    ))
                    
                    fig_india_monthly.add_vrect(x0=5.5, x1=8.5, fillcolor="rgba(255,82,82,0.1)", 
                                                line_width=0, annotation_text="🌧️ Monsoon",
                                                annotation_position="top")
                    
                    fig_india_monthly.update_layout(
                        paper_bgcolor='#0E1117',
                        plot_bgcolor='#0E1117',
                        font_color='#FFFFFF',
                        height=350,
                        margin=dict(t=50),
                        xaxis=dict(title=""),
                        yaxis=dict(title="Delay Rate (%)", gridcolor='#2D3748'),
                        showlegend=False
                    )
                    
                    st.plotly_chart(fig_india_monthly, use_container_width=True)
                
                with col2:
                    st.markdown("### ✈️ Top Indian Airlines")
                    
                    india_airlines = india_df.groupby('AIRLINE_NAME').agg({
                        'DEP_DEL15': ['count', 'mean']
                    }).reset_index()
                    india_airlines.columns = ['Airline', 'Flights', 'Delay Rate']
                    india_airlines = india_airlines.sort_values('Flights', ascending=True)
                    
                    fig_india_airlines = go.Figure()
                    fig_india_airlines.add_trace(go.Bar(
                        y=india_airlines['Airline'],
                        x=india_airlines['Delay Rate'] * 100,
                        orientation='h',
                        marker_color='#FF6B6B',
                        text=[f"{x:.1f}%" for x in india_airlines['Delay Rate'] * 100],
                        textposition='outside'
                    ))
                    
                    fig_india_airlines.update_layout(
                        paper_bgcolor='#0E1117',
                        plot_bgcolor='#0E1117',
                        font_color='#FFFFFF',
                        height=350,
                        margin=dict(l=0, r=80),
                        xaxis=dict(title="Delay Rate (%)", gridcolor='#2D3748'),
                        yaxis=dict(title="")
                    )
                    
                    st.plotly_chart(fig_india_airlines, use_container_width=True)
                
                st.markdown("""
                <div class="info-card">
                    <h4>💡 Key Insights - India</h4>
                    <ul>
                        <li><strong>Monsoon Impact:</strong> June-September shows 40-60% higher delay rates</li>
                        <li><strong>IndiGo Dominance:</strong> Highest volume but managing delays efficiently</li>
                        <li><strong>Infrastructure:</strong> Delhi and Mumbai face congestion-related delays</li>
                        <li><strong>Winter Fog:</strong> December-January sees visibility issues in North India</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
        
        # GULF TAB
        with tab2:
            st.markdown("## 🇦🇪 Gulf Region Analysis")
            
            gulf_df = df[df['ORIGIN_REGION'] == 'Middle East']
            
            if len(gulf_df) > 0:
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.markdown(create_metric_card(
                        format_number(len(gulf_df)),
                        "Total Flights",
                        "Middle East"
                    ), unsafe_allow_html=True)
                
                with col2:
                    delay_rate = gulf_df['DEP_DEL15'].mean() * 100
                    st.markdown(create_metric_card(
                        f"{delay_rate:.1f}%",
                        "Delay Rate",
                        "Below global avg"
                    ), unsafe_allow_html=True)
                
                with col3:
                    st.markdown(create_metric_card(
                        "DXB",
                        "Busiest Hub",
                        "Dubai International"
                    ), unsafe_allow_html=True)
                
                with col4:
                    total_cost = gulf_df['DELAY_COST_TOTAL'].sum()
                    st.markdown(create_metric_card(
                        format_currency(total_cost),
                        "Total Cost",
                        "Economic impact"
                    ), unsafe_allow_html=True)
                
                st.markdown("---")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### 🏢 Airport Performance")
                    
                    gulf_airports = gulf_df.groupby('ORIGIN').agg({
                        'DEP_DEL15': ['count', 'mean']
                    }).reset_index()
                    gulf_airports.columns = ['Airport', 'Flights', 'Delay Rate']
                    gulf_airports = gulf_airports.sort_values('Flights', ascending=False)
                    
                    fig_gulf_airports = go.Figure()
                    fig_gulf_airports.add_trace(go.Bar(
                        x=gulf_airports['Airport'],
                        y=gulf_airports['Delay Rate'] * 100,
                        marker_color=['#FFB74D' if x > 0.25 else '#69F0AE' for x in gulf_airports['Delay Rate']],
                        text=[f"{x:.1f}%" for x in gulf_airports['Delay Rate'] * 100],
                        textposition='outside'
                    ))
                    
                    fig_gulf_airports.update_layout(
                        paper_bgcolor='#0E1117',
                        plot_bgcolor='#0E1117',
                        font_color='#FFFFFF',
                        height=350,
                        xaxis=dict(title=""),
                        yaxis=dict(title="Delay Rate (%)", gridcolor='#2D3748')
                    )
                    
                    st.plotly_chart(fig_gulf_airports, use_container_width=True)
                
                with col2:
                    st.markdown("### ✈️ Gulf Carriers")
                    
                    gulf_carriers = gulf_df[gulf_df['AIRLINE_NAME'].isin(['Emirates', 'Qatar Airways', 'Etihad Airways', 'FlyDubai', 'Gulf Air', 'Saudia'])]
                    carrier_stats = gulf_carriers.groupby('AIRLINE_NAME')['DEP_DEL15'].agg(['count', 'mean']).reset_index()
                    carrier_stats.columns = ['Airline', 'Flights', 'Delay Rate']
                    carrier_stats = carrier_stats.sort_values('Delay Rate', ascending=True)
                    
                    fig_gulf_carriers = go.Figure()
                    fig_gulf_carriers.add_trace(go.Bar(
                        y=carrier_stats['Airline'],
                        x=carrier_stats['Delay Rate'] * 100,
                        orientation='h',
                        marker_color='#42A5F5',
                        text=[f"{x:.1f}%" for x in carrier_stats['Delay Rate'] * 100],
                        textposition='outside'
                    ))
                    
                    fig_gulf_carriers.update_layout(
                        paper_bgcolor='#0E1117',
                        plot_bgcolor='#0E1117',
                        font_color='#FFFFFF',
                        height=350,
                        margin=dict(l=0, r=80),
                        xaxis=dict(title="Delay Rate (%)", gridcolor='#2D3748'),
                        yaxis=dict(title="")
                    )
                    
                    st.plotly_chart(fig_gulf_carriers, use_container_width=True)
                
                st.markdown("""
                <div class="info-card">
                    <h4>💡 Key Insights - Gulf Region</h4>
                    <ul>
                        <li><strong>Dubai Fog:</strong> December-February sees fog-related delays</li>
                        <li><strong>Hub Excellence:</strong> Emirates, Qatar, Etihad maintain high OTP</li>
                        <li><strong>India Connectivity:</strong> Heavy traffic to Indian cities</li>
                        <li><strong>Premium Service:</strong> Gulf carriers invest heavily in punctuality</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
        
        # NORTH AMERICA TAB
        with tab3:
            st.markdown("## 🇺🇸 North America Analysis")
            
            na_df = df[df['ORIGIN_REGION'] == 'North America']
            
            if len(na_df) > 0:
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.markdown(create_metric_card(
                        format_number(len(na_df)),
                        "Total Flights",
                        "North America"
                    ), unsafe_allow_html=True)
                
                with col2:
                    delay_rate = na_df['DEP_DEL15'].mean() * 100
                    st.markdown(create_metric_card(
                        f"{delay_rate:.1f}%",
                        "Delay Rate",
                        "Winter impact"
                    ), unsafe_allow_html=True)
                
                with col3:
                    st.markdown(create_metric_card(
                        "ATL",
                        "Busiest Hub",
                        "Hartsfield-Jackson"
                    ), unsafe_allow_html=True)
                
                with col4:
                    total_cost = na_df['DELAY_COST_TOTAL'].sum()
                    st.markdown(create_metric_card(
                        format_currency(total_cost),
                        "Highest Cost",
                        "Global leader"
                    ), unsafe_allow_html=True)
                
                st.markdown("---")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### 📊 Seasonal Pattern")
                    
                    na_monthly = na_df.groupby('MONTH')['DEP_DEL15'].mean().reset_index()
                    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                    
                    colors_winter = ['#FF5252' if m in [1,2,12] else '#FFB74D' if m in [6,7,8,11] else '#69F0AE' for m in range(1, 13)]
                    
                    fig_na_monthly = go.Figure()
                    fig_na_monthly.add_trace(go.Bar(
                        x=month_names,
                        y=na_monthly['DEP_DEL15'] * 100,
                        marker_color=colors_winter,
                        text=[f"{x:.1f}%" for x in na_monthly['DEP_DEL15'] * 100],
                        textposition='outside'
                    ))
                    
                    fig_na_monthly.update_layout(
                        paper_bgcolor='#0E1117',
                        plot_bgcolor='#0E1117',
                        font_color='#FFFFFF',
                        height=350,
                        xaxis=dict(title=""),
                        yaxis=dict(title="Delay Rate (%)", gridcolor='#2D3748')
                    )
                    
                    st.plotly_chart(fig_na_monthly, use_container_width=True)
                
                with col2:
                    st.markdown("### ✈️ US Carriers")
                    
                    us_carriers = na_df[na_df['AIRLINE_NAME'].isin(['American Airlines', 'Delta Air Lines', 'United Airlines', 'Southwest Airlines'])]
                    carrier_stats = us_carriers.groupby('AIRLINE_NAME')['DEP_DEL15'].agg(['count', 'mean']).reset_index()
                    carrier_stats.columns = ['Airline', 'Flights', 'Delay Rate']
                    carrier_stats = carrier_stats.sort_values('Delay Rate', ascending=True)
                    
                    fig_us_carriers = go.Figure()
                    fig_us_carriers.add_trace(go.Bar(
                        y=carrier_stats['Airline'],
                        x=carrier_stats['Delay Rate'] * 100,
                        orientation='h',
                        marker_color='#42A5F5',
                        text=[f"{x:.1f}%" for x in carrier_stats['Delay Rate'] * 100],
                        textposition='outside'
                    ))
                    
                    fig_us_carriers.update_layout(
                        paper_bgcolor='#0E1117',
                        plot_bgcolor='#0E1117',
                        font_color='#FFFFFF',
                        height=350,
                        margin=dict(l=0, r=80),
                        xaxis=dict(title="Delay Rate (%)", gridcolor='#2D3748'),
                        yaxis=dict(title="")
                    )
                    
                    st.plotly_chart(fig_us_carriers, use_container_width=True)
                
                st.markdown("""
                <div class="info-card">
                    <h4>💡 Key Insights - North America</h4>
                    <ul>
                        <li><strong>Winter Storms:</strong> December-February sees highest delays</li>
                        <li><strong>Summer Thunderstorms:</strong> June-August has convective weather delays</li>
                        <li><strong>Holiday Rush:</strong> Thanksgiving (Nov) and Christmas cause congestion</li>
                        <li><strong>Delta Performance:</strong> Best among Big 4 US carriers</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

# === FOOTER ===
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #B0B8C4; padding: 1rem;">
    <p>✈️ <strong>Flight Delay Domino Effect Dashboard</strong></p>
    <p>Built with Streamlit | Data: Global Flight Operations 2024</p>
    <p>Features: Drill Down | Seasonality Heatmap | Pareto Analysis | What-If Simulation</p>
</div>
""", unsafe_allow_html=True)
