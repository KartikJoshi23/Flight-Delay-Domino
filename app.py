# === FLIGHT DELAY DOMINO EFFECT DASHBOARD ===
# Optimized for Streamlit Cloud - Fixed Version

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# === PAGE CONFIG ===
st.set_page_config(
    page_title="Flight Delay Domino Effect",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# === CSS ===
st.markdown("""
<style>
    .main .block-container {padding-top: 1rem;}
    .metric-card {
        background: linear-gradient(135deg, #1E2130 0%, #262D3D 100%);
        padding: 1.2rem; border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.1); margin-bottom: 0.8rem;
    }
    .metric-value {font-size: 2rem; font-weight: 700; color: #FFFFFF; margin: 0;}
    .metric-label {font-size: 0.85rem; color: #B0B8C4; margin-top: 0.3rem; text-transform: uppercase;}
    .info-card {
        background: linear-gradient(135deg, #1a1f2e 0%, #252b3b 100%);
        padding: 1rem; border-radius: 10px;
        border-left: 4px solid #FF6B6B; margin: 0.8rem 0;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# === DATA LOADING ===
@st.cache_data(ttl=3600)
def load_data():
    dtype_dict = {
        'MONTH': 'int8', 'DAY_OF_WEEK': 'int8', 'DEP_HOUR': 'int8',
        'DEP_DEL15': 'int8', 'DEP_DELAY': 'float32', 'DISTANCE': 'float32',
        'DELAY_COST_AIRLINE': 'float32', 'DELAY_COST_PASSENGER': 'float32',
        'DELAY_COST_TOTAL': 'float32', 'CARRIER_DELAY': 'float32',
        'WEATHER_DELAY': 'float32', 'NAS_DELAY': 'float32', 'LATE_AIRCRAFT_DELAY': 'float32'
    }
    flights = pd.read_csv('data/flights_global_2024.csv', dtype=dtype_dict)
    airlines = pd.read_csv('data/airlines.csv')
    airports = pd.read_csv('data/airports.csv')
    return flights, airlines, airports

# Helpers
def format_number(num):
    if num >= 1e6: return f"{num/1e6:.1f}M"
    if num >= 1e3: return f"{num/1e3:.1f}K"
    return f"{num:.0f}"

def format_currency(num):
    if num >= 1e6: return f"${num/1e6:.1f}M"
    if num >= 1e3: return f"${num/1e3:.1f}K"
    return f"${num:.0f}"

def metric_card(value, label, subtitle=None):
    sub = f'<p style="color:#B0B8C4;font-size:0.75rem;margin:0">{subtitle}</p>' if subtitle else ""
    return f'<div class="metric-card"><p class="metric-value">{value}</p><p class="metric-label">{label}</p>{sub}</div>'

# Load data
with st.spinner("Loading flight data..."):
    try:
        df, airlines_df, airports_df = load_data()
    except Exception as e:
        st.error(f"Error: {e}")
        st.stop()

# === SIDEBAR ===
with st.sidebar:
    st.markdown("## ✈️ Flight Delay")
    st.markdown("## Domino Effect")
    st.markdown("---")
    
    page = st.radio("Navigation", [
        "🏠 Home", "📊 Delay Patterns", "🔥 Seasonality", 
        "📈 Pareto", "🌊 Ripple Effect", "💰 Impact",
        "🔮 What-If", "📍 Case Studies"
    ], label_visibility="collapsed")
    
    st.markdown("---")
    st.markdown("### 🎛️ Filters")
    
    regions = ['All'] + sorted(df['ORIGIN_REGION'].dropna().unique().tolist())
    selected_region = st.selectbox("Region", regions)
    
    months_list = ['All'] + list(range(1, 13))
    selected_month = st.selectbox("Month", months_list, 
        format_func=lambda x: 'All' if x == 'All' else pd.Timestamp(2024, x, 1).strftime('%B'))
    
    fdf = df.copy()
    if selected_region != 'All':
        fdf = fdf[fdf['ORIGIN_REGION'] == selected_region]
    if selected_month != 'All':
        fdf = fdf[fdf['MONTH'] == selected_month]
    
    st.markdown("---")
    st.caption(f"Showing {len(fdf):,} of {len(df):,} flights")

MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

# === HOME ===
if page == "🏠 Home":
    st.markdown("# ✈️ Flight Delay Domino Effect")
    st.markdown("*Analyzing Global Flight Delays & Their Cascading Impact*")
    
    c1, c2, c3, c4 = st.columns(4)
    total = len(fdf)
    delayed = int(fdf['DEP_DEL15'].sum())
    rate = delayed/total*100 if total else 0
    avg_del = fdf[fdf['DEP_DEL15']==1]['DEP_DELAY'].mean() if delayed else 0
    cost = fdf['DELAY_COST_TOTAL'].sum()
    
    c1.markdown(metric_card(format_number(total), "Total Flights", "2024"), unsafe_allow_html=True)
    c2.markdown(metric_card(f"{rate:.1f}%", "Delay Rate", f"{format_number(delayed)} delayed"), unsafe_allow_html=True)
    c3.markdown(metric_card(f"{avg_del:.0f} min", "Avg Delay", "When delayed"), unsafe_allow_html=True)
    c4.markdown(metric_card(format_currency(cost), "Total Cost", "Economic impact"), unsafe_allow_html=True)
    
    st.markdown("---")
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("### 🌍 Delay by Region")
        reg = fdf.groupby('ORIGIN_REGION')['DEP_DEL15'].agg(['count','mean']).reset_index()
        reg.columns = ['Region','Flights','Rate']
        reg = reg.sort_values('Rate')
        
        fig = go.Figure(go.Bar(
            y=reg['Region'], x=reg['Rate']*100, orientation='h',
            marker=dict(color=reg['Rate'], colorscale='RdYlGn_r'),
            text=[f"{x:.1f}%" for x in reg['Rate']*100], textposition='outside'
        ))
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font_color='#FFF', height=350, margin=dict(l=0,r=60,t=10,b=30),
            xaxis=dict(title="Delay Rate (%)", gridcolor='#333'), yaxis=dict(title="")
        )
        st.plotly_chart(fig, key="home_region", use_container_width=True)
    
    with col2:
        st.markdown("### 📈 Monthly Trend")
        mon = fdf.groupby('MONTH')['DEP_DEL15'].mean().reset_index()
        
        fig = go.Figure(go.Scatter(
            x=MONTHS, y=mon['DEP_DEL15']*100,
            mode='lines+markers', line=dict(color='#FF6B6B', width=3), marker=dict(size=8)
        ))
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font_color='#FFF', height=350, margin=dict(l=50,r=20,t=10,b=30),
            xaxis=dict(gridcolor='#333'), yaxis=dict(title="Delay Rate (%)", gridcolor='#333')
        )
        st.plotly_chart(fig, key="home_monthly", use_container_width=True)
    
    st.markdown("### 💡 Quick Insights")
    c1, c2, c3 = st.columns(3)
    worst_region = fdf.groupby('ORIGIN_REGION')['DEP_DEL15'].mean().idxmax()
    worst_month = int(fdf.groupby('MONTH')['DEP_DEL15'].mean().idxmax())
    worst_hour = int(fdf.groupby('DEP_HOUR')['DEP_DEL15'].mean().idxmax())
    
    c1.markdown(f'<div class="info-card"><b>🌍 Highest Delays</b><br>{worst_region}</div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="info-card"><b>📅 Worst Month</b><br>{MONTHS[worst_month-1]}</div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="info-card"><b>🕐 Peak Hour</b><br>{worst_hour}:00</div>', unsafe_allow_html=True)

# === DELAY PATTERNS ===
elif page == "📊 Delay Patterns":
    st.markdown("# 📊 Delay Patterns")
    
    tab1, tab2, tab3 = st.tabs(["✈️ Airlines", "🏢 Airports", "🕐 Time"])
    
    with tab1:
        agg = fdf.groupby('AIRLINE_NAME')['DEP_DEL15'].agg(['count','mean']).reset_index()
        agg.columns = ['Airline','Flights','Rate']
        agg = agg[agg['Flights']>=100].sort_values('Rate').tail(15)
        
        fig = go.Figure(go.Bar(
            y=agg['Airline'], x=agg['Rate']*100, orientation='h',
            marker=dict(color=agg['Rate'], colorscale='RdYlGn_r'),
            text=[f"{x:.1f}%" for x in agg['Rate']*100], textposition='outside'
        ))
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font_color='#FFF', height=500, margin=dict(l=0,r=80,t=10,b=30),
            xaxis=dict(title="Delay Rate (%)", gridcolor='#333'), yaxis=dict(title="")
        )
        st.plotly_chart(fig, key="pat_airline", use_container_width=True)
        
        st.markdown("### 🔍 Drill Down")
        sel = st.selectbox("Select Airline", agg['Airline'].tolist())
        if sel:
            ad = fdf[fdf['AIRLINE_NAME']==sel]
            c1,c2,c3 = st.columns(3)
            c1.metric("Flights", f"{len(ad):,}")
            c2.metric("Delay Rate", f"{ad['DEP_DEL15'].mean()*100:.1f}%")
            c3.metric("Avg Delay", f"{ad[ad['DEP_DEL15']==1]['DEP_DELAY'].mean():.0f} min")
    
    with tab2:
        ap = fdf.groupby('ORIGIN')['DEP_DEL15'].agg(['count','mean']).reset_index()
        ap.columns = ['Airport','Flights','Rate']
        ap = ap[ap['Flights']>=50]
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### 🔴 Most Delayed")
            worst = ap.nlargest(10,'Rate')
            fig = go.Figure(go.Bar(
                y=worst['Airport'], x=worst['Rate']*100, orientation='h',
                marker_color='#FF5252', text=[f"{x:.1f}%" for x in worst['Rate']*100], textposition='outside'
            ))
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                font_color='#FFF', height=350, margin=dict(l=0,r=60,t=10,b=30),
                xaxis=dict(gridcolor='#333'), yaxis=dict(categoryorder='total ascending')
            )
            st.plotly_chart(fig, key="pat_worst", use_container_width=True)
        
        with c2:
            st.markdown("#### 🟢 Best Performing")
            best = ap.nsmallest(10,'Rate')
            fig = go.Figure(go.Bar(
                y=best['Airport'], x=best['Rate']*100, orientation='h',
                marker_color='#69F0AE', text=[f"{x:.1f}%" for x in best['Rate']*100], textposition='outside'
            ))
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                font_color='#FFF', height=350, margin=dict(l=0,r=60,t=10,b=30),
                xaxis=dict(gridcolor='#333'), yaxis=dict(categoryorder='total descending')
            )
            st.plotly_chart(fig, key="pat_best", use_container_width=True)
    
    with tab3:
        st.markdown("### Hour × Day Heatmap")
        hm = fdf.groupby(['DAY_OF_WEEK','DEP_HOUR'])['DEP_DEL15'].mean().reset_index()
        piv = hm.pivot(index='DEP_HOUR', columns='DAY_OF_WEEK', values='DEP_DEL15')
        days = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
        
        fig = go.Figure(go.Heatmap(
            z=piv.values*100, x=days, y=[f"{h:02d}:00" for h in piv.index],
            colorscale='RdYlGn_r', text=[[f"{v:.0f}%" for v in row] for row in piv.values*100],
            texttemplate="%{text}", textfont={"size":9}
        ))
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font_color='#FFF', height=500, margin=dict(l=60,r=20,t=10,b=30),
            yaxis=dict(autorange='reversed')
        )
        st.plotly_chart(fig, key="pat_heatmap", use_container_width=True)

# === SEASONALITY ===
elif page == "🔥 Seasonality":
    st.markdown("# 🔥 Seasonality Analysis")
    st.markdown("### Month × Region Heatmap")
    
    sea = fdf.groupby(['MONTH','ORIGIN_REGION'])['DEP_DEL15'].mean().reset_index()
    piv = sea.pivot(index='ORIGIN_REGION', columns='MONTH', values='DEP_DEL15')
    
    fig = go.Figure(go.Heatmap(
        z=piv.values*100, x=MONTHS, y=piv.index, colorscale='RdYlGn_r',
        text=[[f"{v:.0f}%" for v in row] for row in piv.values*100],
        texttemplate="%{text}", textfont={"size":11}
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font_color='#FFF', height=400, margin=dict(l=120,r=20,t=10,b=30)
    )
    st.plotly_chart(fig, key="sea_hm", use_container_width=True)
    
    st.markdown("### 💡 Seasonal Insights")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="info-card"><b>🌧️ India Monsoon</b><br>Jun-Sep: 40-60% higher delays</div>', unsafe_allow_html=True)
        st.markdown('<div class="info-card"><b>❄️ NA Winter</b><br>Dec-Feb: Snow/ice impacts</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="info-card"><b>🌫️ Gulf Fog</b><br>Dec-Feb: Morning fog in Dubai</div>', unsafe_allow_html=True)
        st.markdown('<div class="info-card"><b>☀️ Europe Summer</b><br>Jun-Aug: High volume delays</div>', unsafe_allow_html=True)

# === PARETO ===
elif page == "📈 Pareto":
    st.markdown("# 📈 Pareto Analysis (80/20 Rule)")
    st.markdown('<div class="info-card">The Pareto Principle: <b>80% of delays may come from 20% of sources</b></div>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["✈️ Airlines", "🏢 Airports"])
    
    with tab1:
        dba = fdf[fdf['DEP_DEL15']==1].groupby('AIRLINE_NAME').size().reset_index(name='count')
        dba = dba.sort_values('count', ascending=False).head(15)
        dba['cum'] = dba['count'].cumsum()
        dba['cum_pct'] = dba['cum']/dba['count'].sum()*100
        
        fig = make_subplots(specs=[[{"secondary_y":True}]])
        fig.add_trace(go.Bar(x=dba['AIRLINE_NAME'], y=dba['count'], name='Delays', marker_color='#FF6B6B'), secondary_y=False)
        fig.add_trace(go.Scatter(x=dba['AIRLINE_NAME'], y=dba['cum_pct'], name='Cumulative %', line=dict(color='#42A5F5',width=3), mode='lines+markers'), secondary_y=True)
        fig.add_hline(y=80, line_dash="dash", line_color="#FFB74D", annotation_text="80%", secondary_y=True)
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font_color='#FFF', height=450, margin=dict(t=60,b=100),
            xaxis=dict(tickangle=45), yaxis=dict(title="Delayed Flights", gridcolor='#333'),
            yaxis2=dict(title="Cumulative %", range=[0,105]), legend=dict(orientation='h',y=1.1)
        )
        st.plotly_chart(fig, key="par_air", use_container_width=True)
        n80 = len(dba[dba['cum_pct']<=80])
        st.info(f"🎯 **{n80} airlines** account for ~80% of delays")
    
    with tab2:
        dba = fdf[fdf['DEP_DEL15']==1].groupby('ORIGIN').size().reset_index(name='count')
        dba = dba.sort_values('count', ascending=False).head(15)
        dba['cum'] = dba['count'].cumsum()
        dba['cum_pct'] = dba['cum']/dba['count'].sum()*100
        
        fig = make_subplots(specs=[[{"secondary_y":True}]])
        fig.add_trace(go.Bar(x=dba['ORIGIN'], y=dba['count'], name='Delays', marker_color='#FF6B6B'), secondary_y=False)
        fig.add_trace(go.Scatter(x=dba['ORIGIN'], y=dba['cum_pct'], name='Cumulative %', line=dict(color='#42A5F5',width=3), mode='lines+markers'), secondary_y=True)
        fig.add_hline(y=80, line_dash="dash", line_color="#FFB74D", annotation_text="80%", secondary_y=True)
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font_color='#FFF', height=450, margin=dict(t=60,b=50),
            yaxis=dict(title="Delayed Flights", gridcolor='#333'),
            yaxis2=dict(title="Cumulative %", range=[0,105]), legend=dict(orientation='h',y=1.1)
        )
        st.plotly_chart(fig, key="par_apt", use_container_width=True)

# === RIPPLE EFFECT ===
elif page == "🌊 Ripple Effect":
    st.markdown("# 🌊 Domino Effect Analysis")
    st.markdown('<div class="info-card"><b>🔄 The Cascade:</b> One delayed flight causes late aircraft for next flights</div>', unsafe_allow_html=True)
    
    delayed = fdf[fdf['DEP_DEL15']==1]
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### Delay Causes")
        causes = {
            'Carrier': delayed['CARRIER_DELAY'].sum(),
            'Weather': delayed['WEATHER_DELAY'].sum(),
            'NAS/ATC': delayed['NAS_DELAY'].sum(),
            'Late Aircraft': delayed['LATE_AIRCRAFT_DELAY'].sum()
        }
        cdf = pd.DataFrame(list(causes.items()), columns=['Cause','Minutes']).sort_values('Minutes')
        
        fig = go.Figure(go.Bar(
            y=cdf['Cause'], x=cdf['Minutes'], orientation='h',
            marker_color=['#42A5F5','#FFB74D','#9575CD','#FF5252'],
            text=[format_number(x) for x in cdf['Minutes']], textposition='outside'
        ))
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font_color='#FFF', height=300, margin=dict(l=0,r=80,t=10,b=30),
            xaxis=dict(title="Total Minutes", gridcolor='#333')
        )
        st.plotly_chart(fig, key="rip_cause", use_container_width=True)
    
    with c2:
        st.markdown("### Distribution")
        fig = px.pie(cdf, values='Minutes', names='Cause', hole=0.5,
                     color_discrete_sequence=['#42A5F5','#FFB74D','#9575CD','#FF5252'])
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', font_color='#FFF', height=300,
            margin=dict(l=20,r=20,t=10,b=30)
        )
        st.plotly_chart(fig, key="rip_pie", use_container_width=True)
    
    st.markdown("### Late Aircraft by Hour")
    lh = delayed.groupby('DEP_HOUR')['LATE_AIRCRAFT_DELAY'].mean().reset_index()
    fig = go.Figure(go.Bar(x=lh['DEP_HOUR'], y=lh['LATE_AIRCRAFT_DELAY'], marker_color='#FF6B6B'))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font_color='#FFF', height=300, margin=dict(l=50,r=20,t=10,b=50),
        xaxis=dict(title="Hour", gridcolor='#333'), yaxis=dict(title="Avg Delay (min)", gridcolor='#333')
    )
    st.plotly_chart(fig, key="rip_hour", use_container_width=True)
    st.info("💡 Late aircraft delays compound throughout the day. Book morning flights!")

# === IMPACT ===
elif page == "💰 Impact":
    st.markdown("# 💰 Economic Impact")
    
    c1,c2,c3,c4 = st.columns(4)
    ac = fdf['DELAY_COST_AIRLINE'].sum()
    pc = fdf['DELAY_COST_PASSENGER'].sum()
    tc = fdf['DELAY_COST_TOTAL'].sum()
    avg = fdf[fdf['DEP_DEL15']==1]['DELAY_COST_TOTAL'].mean()
    
    c1.markdown(metric_card(format_currency(ac), "Airline Cost", "$74.20/min"), unsafe_allow_html=True)
    c2.markdown(metric_card(format_currency(pc), "Passenger Cost", "$47.00/min"), unsafe_allow_html=True)
    c3.markdown(metric_card(format_currency(tc), "Total Cost", "Combined"), unsafe_allow_html=True)
    c4.markdown(metric_card(format_currency(avg), "Avg per Delay", "Per flight"), unsafe_allow_html=True)
    
    st.markdown("---")
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown("### Cost by Region")
        rc = fdf.groupby('ORIGIN_REGION')['DELAY_COST_TOTAL'].sum().reset_index()
        rc.columns = ['Region','Cost']
        rc = rc.sort_values('Cost')
        
        fig = go.Figure(go.Bar(
            y=rc['Region'], x=rc['Cost'], orientation='h', marker_color='#FF6B6B',
            text=[format_currency(x) for x in rc['Cost']], textposition='outside'
        ))
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font_color='#FFF', height=300, margin=dict(l=0,r=80,t=10,b=30),
            xaxis=dict(gridcolor='#333')
        )
        st.plotly_chart(fig, key="imp_reg", use_container_width=True)
    
    with c2:
        st.markdown("### Monthly Trend")
        mc = fdf.groupby('MONTH')['DELAY_COST_TOTAL'].sum().reset_index()
        fig = go.Figure(go.Bar(x=MONTHS, y=mc['DELAY_COST_TOTAL'], marker_color='#FF6B6B'))
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font_color='#FFF', height=300, margin=dict(l=50,r=20,t=10,b=30),
            yaxis=dict(title="Cost ($)", gridcolor='#333')
        )
        st.plotly_chart(fig, key="imp_mon", use_container_width=True)

# === WHAT-IF ===
elif page == "🔮 What-If":
    st.markdown("# 🔮 What-If Analysis")
    st.markdown('<div class="info-card">Simulate delay reduction scenarios</div>', unsafe_allow_html=True)
    
    cur_del = int(fdf['DEP_DEL15'].sum())
    cur_rate = fdf['DEP_DEL15'].mean()*100
    cur_cost = fdf['DELAY_COST_TOTAL'].sum()
    
    st.markdown("### Current State")
    c1,c2,c3 = st.columns(3)
    c1.metric("Delayed Flights", f"{cur_del:,}")
    c2.metric("Delay Rate", f"{cur_rate:.1f}%")
    c3.metric("Total Cost", format_currency(cur_cost))
    
    st.markdown("---")
    st.markdown("### Scenario Parameters")
    c1, c2 = st.columns(2)
    with c1:
        cr = st.slider("Reduce Carrier Delays (%)", 0, 50, 0, 5)
        wr = st.slider("Reduce Weather Delays (%)", 0, 30, 0, 5)
    with c2:
        nr = st.slider("Reduce NAS Delays (%)", 0, 40, 0, 5)
        lr = st.slider("Reduce Late Aircraft (%)", 0, 50, 0, 5)
    
    red = (cr*0.35 + wr*0.25 + nr*0.25 + lr*0.15)/100
    new_del = cur_del*(1-red)
    new_rate = cur_rate*(1-red)
    new_cost = cur_cost*(1-red)
    savings = cur_cost - new_cost
    
    st.markdown("---")
    st.markdown("### Simulated Outcome")
    c1,c2,c3 = st.columns(3)
    c1.metric("New Delayed", f"{new_del:,.0f}", f"-{cur_del-new_del:,.0f}")
    c2.metric("New Rate", f"{new_rate:.1f}%", f"-{cur_rate-new_rate:.1f}%")
    c3.metric("Savings", format_currency(savings))
    
    if savings > 0:
        st.success(f"✅ Potential savings: **{format_currency(savings)}**")

# === CASE STUDIES ===
elif page == "📍 Case Studies":
    st.markdown("# 📍 Regional Case Studies")
    
    tab1, tab2, tab3 = st.tabs(["🇮🇳 India", "🇦🇪 Gulf", "🇺🇸 North America"])
    
    with tab1:
        idf = df[df['ORIGIN_REGION']=='India']
        c1,c2,c3 = st.columns(3)
        c1.metric("Flights", f"{len(idf):,}")
        c2.metric("Delay Rate", f"{idf['DEP_DEL15'].mean()*100:.1f}%")
        c3.metric("Cost", format_currency(idf['DELAY_COST_TOTAL'].sum()))
        
        st.markdown("### Monsoon Effect")
        im = idf.groupby('MONTH')['DEP_DEL15'].mean().reset_index()
        colors = ['#69F0AE' if m not in [6,7,8,9] else '#FF5252' for m in range(1,13)]
        fig = go.Figure(go.Bar(x=MONTHS, y=im['DEP_DEL15']*100, marker_color=colors))
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font_color='#FFF', height=300, yaxis=dict(title="Delay Rate (%)", gridcolor='#333')
        )
        st.plotly_chart(fig, key="cs_india", use_container_width=True)
        st.info("🌧️ Jun-Sep (Monsoon) shows significantly higher delays")
    
    with tab2:
        gdf = df[df['ORIGIN_REGION']=='Middle East']
        c1,c2,c3 = st.columns(3)
        c1.metric("Flights", f"{len(gdf):,}")
        c2.metric("Delay Rate", f"{gdf['DEP_DEL15'].mean()*100:.1f}%")
        c3.metric("Cost", format_currency(gdf['DELAY_COST_TOTAL'].sum()))
        
        st.markdown("### Gulf Carriers")
        ga = gdf.groupby('AIRLINE_NAME')['DEP_DEL15'].mean().reset_index()
        ga.columns = ['Airline','Rate']
        ga = ga.sort_values('Rate')
        fig = go.Figure(go.Bar(y=ga['Airline'], x=ga['Rate']*100, orientation='h', marker_color='#42A5F5'))
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font_color='#FFF', height=300, xaxis=dict(title="Delay Rate (%)", gridcolor='#333')
        )
        st.plotly_chart(fig, key="cs_gulf", use_container_width=True)
        st.info("🌫️ Dec-Feb fog impacts Dubai operations")
    
    with tab3:
        ndf = df[df['ORIGIN_REGION']=='North America']
        c1,c2,c3 = st.columns(3)
        c1.metric("Flights", f"{len(ndf):,}")
        c2.metric("Delay Rate", f"{ndf['DEP_DEL15'].mean()*100:.1f}%")
        c3.metric("Cost", format_currency(ndf['DELAY_COST_TOTAL'].sum()))
        
        st.markdown("### Seasonal Pattern")
        nm = ndf.groupby('MONTH')['DEP_DEL15'].mean().reset_index()
        colors = ['#FF5252' if m in [1,2,12] else '#FFB74D' if m in [6,7,8] else '#69F0AE' for m in range(1,13)]
        fig = go.Figure(go.Bar(x=MONTHS, y=nm['DEP_DEL15']*100, marker_color=colors))
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font_color='#FFF', height=300, yaxis=dict(title="Delay Rate (%)", gridcolor='#333')
        )
        st.plotly_chart(fig, key="cs_na", use_container_width=True)
        st.info("❄️ Winter storms (Dec-Feb) cause most delays")

# Footer
st.markdown("---")
st.markdown("<center>✈️ Flight Delay Domino Effect Dashboard | Built with Streamlit</center>", unsafe_allow_html=True)
