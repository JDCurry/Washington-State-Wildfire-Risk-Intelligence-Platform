"""
WA FireWatch - Washington State Wildfire Risk Intelligence Platform
Professional wildfire risk analysis and mitigation planning tool

Author: Josh Curry
Organization: Washington State Emergency Management
Last Updated: November 2025
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Washington State Wildfire Risk Intelligence Platform - Home",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #d32f2f;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .stMetric label {
        font-size: 0.9rem !important;
        font-weight: 600 !important;
        color: #424242 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .stMetric [data-testid="stMetricValue"] {
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        color: #d32f2f !important;
    }
    .metric-delta {
        font-size: 0.85rem !important;
    }
    h1 {
        color: #1a237e;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    h2, h3 {
        color: #283593;
        font-weight: 600;
    }
    .info-box {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #1976d2;
        margin: 20px 0;
    }
    .warning-box {
        background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #f57c00;
        margin: 20px 0;
    }
    .critical-box {
        background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #c62828;
        margin: 20px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    """Load the integrated dashboard dataset"""
    df = pd.read_csv('data/WA_Climate_Fire_Dashboard_Data.csv')
    return df

@st.cache_data
def load_fema_data():
    """Load FEMA disaster data"""
    try:
        fema = pd.read_csv('data/FEMA_Disasters_Geocoded.csv')
        fema['declarationDate'] = pd.to_datetime(fema['declarationDate'])
        return fema
    except FileNotFoundError:
        return None

try:
    df = load_data()
    fema_data = load_fema_data()
except FileNotFoundError:
    st.error("⚠️ Data files not found. Please ensure data/ folder contains required files.")
    st.stop()

# Header with branding
col1, col2 = st.columns([3, 1])
with col1:
    st.title("🔥 Washington State Wildfire Risk Intelligence Platform")
    st.subheader("WA FireWatch")
    st.caption(f"Real-time risk analysis and mitigation planning • Updated {datetime.now().strftime('%B %d, %Y')}")

with col2:
    st.markdown("""
    <div style='text-align: right; padding-top: 20px;'>
        <div style='font-size: 0.8rem; color: #666;'>Powered by</div>
        <div style='font-size: 1.1rem; font-weight: 600; color: #1976d2;'>Washington State</div>
        <div style='font-size: 0.9rem; color: #666;'>Emergency Management</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Executive Summary Metrics
st.markdown("### 📊 Executive Summary")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    critical_count = len(df[df['risk_category'] == 'Critical'])
    high_count = len(df[df['risk_category'] == 'High'])
    st.metric(
        "Critical Risk",
        f"{critical_count}",
        delta=f"{high_count} High Risk",
        help="Counties requiring immediate mitigation action"
    )

with col2:
    total_pop_risk = df['population_at_risk'].sum() / 1000000
    st.metric(
        "Population at Risk",
        f"{total_pop_risk:.2f}M",
        delta=f"{(total_pop_risk / (df['population'].sum() / 1000000) * 100):.0f}% of WUI pop.",
        help="Residents in high-risk Wildland-Urban Interface areas"
    )

with col3:
    fema_count = len(fema_data) if fema_data is not None else 126
    recent_disasters = len(fema_data[fema_data['declarationDate'] >= '2020-01-01']) if fema_data is not None else 0
    st.metric(
        "Federal Disasters",
        f"{fema_count}",
        delta=f"{recent_disasters} since 2020",
        help="Total FEMA fire disaster declarations (1991-2024)"
    )

with col4:
    warming_counties = len(df[df['climate_trend'].str.contains('Warming', na=False)])
    st.metric(
        "Climate Concern",
        f"{warming_counties}",
        delta=f"{(warming_counties/len(df)*100):.0f}% of counties",
        help="Counties showing warming or warming & drying trends"
    )

with col5:
    avg_risk = df['climate_fire_risk_score'].mean()
    high_risk_avg = df[df['risk_category'].isin(['High', 'Critical'])]['climate_fire_risk_score'].mean()
    st.metric(
        "Avg Risk Score",
        f"{avg_risk:.1f}",
        delta=f"{high_risk_avg:.1f} (High/Critical)",
        help="Statewide average climate-fire risk score"
    )

st.markdown("---")

# Key Insights Section
st.markdown("### 🎯 Key Insights & Priorities")

col1, col2 = st.columns([2, 1])

with col1:
    # Top risk counties
    st.markdown("#### Highest Risk Counties")
    top_counties = df.nlargest(10, 'climate_fire_risk_score')[['County', 'climate_fire_risk_score', 'risk_category', 'climate_trend', 'population_at_risk']]
    top_counties['population_at_risk'] = top_counties['population_at_risk'].apply(lambda x: f"{x:,.0f}")
    top_counties.columns = ['County', 'Risk Score', 'Category', 'Climate Trend', 'Pop. at Risk']
    
    # Add color coding
    def color_risk(val):
        if val == 'Critical':
            return 'background-color: #ffcdd2'
        elif val == 'High':
            return 'background-color: #fff3e0'
        return ''
    
    styled_df = top_counties.style.map(color_risk, subset=['Category'])
    st.dataframe(styled_df, width='stretch', hide_index=True, height=400)

with col2:
    # Risk distribution
    st.markdown("#### Risk Distribution")
    risk_counts = df['risk_category'].value_counts()
    
    fig_risk = go.Figure(data=[go.Pie(
        labels=risk_counts.index,
        values=risk_counts.values,
        marker=dict(colors=['#8B0000', '#FF4500', '#FFA500', '#90EE90']),
        hole=0.4
    )])
    
    fig_risk.update_layout(
        showlegend=True,
        height=250,
        margin=dict(l=20, r=20, t=30, b=20),
        annotations=[dict(text='Counties', x=0.5, y=0.5, font_size=14, showarrow=False)]
    )
    st.plotly_chart(fig_risk, width='stretch')
    
    # Climate trends
    st.markdown("#### Climate Trends")
    trend_counts = df['climate_trend'].value_counts()
    
    fig_trend = go.Figure(data=[go.Bar(
        x=trend_counts.values,
        y=trend_counts.index,
        orientation='h',
        marker=dict(color=['#d32f2f' if t == 'Warming & Drying' else '#f57c00' if t == 'Warming' else '#1976d2' if t == 'Cooling' else '#7cb342' for t in trend_counts.index])
    )])
    
    fig_trend.update_layout(
        showlegend=False,
        height=200,
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis_title="Counties",
        yaxis_title=""
    )
    st.plotly_chart(fig_trend, width='stretch')

st.markdown("---")

# Historical Trends
st.markdown("### 📈 Historical Disaster Trends")

if fema_data is not None:
    # Disasters by year
    fema_data['year'] = fema_data['declarationDate'].dt.year
    yearly_disasters = fema_data.groupby('year').size().reset_index(name='count')
    
    fig_timeline = go.Figure()
    
    fig_timeline.add_trace(go.Scatter(
        x=yearly_disasters['year'],
        y=yearly_disasters['count'],
        mode='lines+markers',
        name='Annual Disasters',
        line=dict(color='#d32f2f', width=3),
        marker=dict(size=8),
        fill='tozeroy',
        fillcolor='rgba(211, 47, 47, 0.1)'
    ))
    
    # Add trend line
    z = np.polyfit(yearly_disasters['year'], yearly_disasters['count'], 1)
    p = np.poly1d(z)
    fig_timeline.add_trace(go.Scatter(
        x=yearly_disasters['year'],
        y=p(yearly_disasters['year']),
        mode='lines',
        name='Trend',
        line=dict(color='#1976d2', width=2, dash='dash')
    ))
    
    fig_timeline.update_layout(
        title="Federal Fire Disaster Declarations Over Time",
        xaxis_title="Year",
        yaxis_title="Number of Declarations",
        hovermode='x unified',
        height=400
    )
    
    st.plotly_chart(fig_timeline, width='stretch')
    
    # Recent disaster highlights
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class='info-box'>
            <h4>📅 Most Recent Disasters</h4>
        """, unsafe_allow_html=True)
        recent = fema_data.nlargest(5, 'declarationDate')[['declarationTitle', 'County', 'declarationDate']]
        for _, row in recent.iterrows():
            st.markdown(f"**{row['declarationTitle']}**  \n{row['County']} County - {row['declarationDate'].strftime('%b %Y')}")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='warning-box'>
            <h4>🔥 Most Impacted Counties</h4>
        """, unsafe_allow_html=True)
        county_disasters = fema_data['County'].value_counts().head(5)
        for county, count in county_disasters.items():
            st.markdown(f"**{county} County**: {count} disasters")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='critical-box'>
            <h4>⚠️ Escalating Threat</h4>
        """, unsafe_allow_html=True)
        last_5_years = len(fema_data[fema_data['year'] >= 2020])
        prev_5_years = len(fema_data[(fema_data['year'] >= 2015) & (fema_data['year'] < 2020)])
        pct_increase = ((last_5_years - prev_5_years) / prev_5_years * 100) if prev_5_years > 0 else 0
        st.markdown(f"**{last_5_years}** disasters (2020-2024)")
        st.markdown(f"**{prev_5_years}** disasters (2015-2019)")
        st.markdown(f"**{pct_increase:+.0f}%** change")
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# Action Items
st.markdown("### 🎯 Recommended Actions")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    #### Immediate Priorities (0-6 months)
    
    1. **Critical Risk Counties** - Initiate emergency mitigation planning for counties with risk scores >60
    2. **WUI Defensible Space** - Launch public education campaigns in high-risk interface areas
    3. **Pre-positioning Resources** - Stage firefighting equipment in warming & drying trend counties
    4. **Evacuation Planning** - Update and test evacuation routes for top 10 highest-risk counties
    5. **Interagency Coordination** - Establish mutual aid agreements with neighboring jurisdictions
    """)

with col2:
    st.markdown("""
    #### Strategic Planning (6-24 months)
    
    1. **Fuel Management** - Implement prescribed burns and mechanical thinning in high-risk areas
    2. **Infrastructure Hardening** - Upgrade critical infrastructure in vulnerable counties
    3. **Climate Adaptation** - Develop long-term strategies for warming trend counties
    4. **Community Firewise** - Expand Firewise USA certification program statewide
    5. **Risk Modeling** - Integrate real-time weather data for dynamic risk assessment
    """)

st.markdown("---")

# Navigation
st.markdown("### 🗺️ Platform Navigation")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.page_link("pages/1_🗺️_Interactive_Map.py", label="🗺️ Interactive Risk Map", help="Explore county-level risk with detailed overlays")

with col2:
    st.page_link("pages/2_📊_Analytics.py", label="📊 Deep Analytics", help="Advanced statistical analysis and trends")

with col3:
    st.page_link("pages/3_📄_Reports.py", label="📄 Generate Reports", help="Create custom reports and exports")

with col4:
    st.page_link("pages/4_ℹ️_About.py", label="ℹ️ About & Methodology", help="Data sources and risk calculation details")

st.markdown("---")

# Sidebar
with st.sidebar:
    st.markdown("### 🔥 WA FireWatch")
    st.markdown("**Wildfire Risk Intelligence**")
    st.markdown("---")
    
    st.markdown("#### Platform Features")
    st.markdown("""
    - ✅ Real-time risk scoring
    - ✅ Multi-layer mapping
    - ✅ Historical analysis
    - ✅ Predictive modeling
    - ✅ Custom reports
    - ✅ Export capabilities
    """)
    
    st.markdown("---")
    
    st.markdown("#### Quick Stats")
    st.metric("Counties Analyzed", len(df))
    st.metric("Data Sources", "5+")
    st.metric("Historical Range", "1991-2024")
    
    st.markdown("---")
    
    st.markdown("#### Contact & Support")
    st.markdown("""
    **Josh Curry**  
    Emergency Management Specialist  
    
    📧 [josh.curry@wa.gov](mailto:josh.curry@wa.gov)  
    🌐 [wa.gov/firewatch](#)
    
    ---
    
    *For technical support or data inquiries, please contact the Emergency Management Division.*
    """)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; font-size: 0.85rem;'>
        <b>Washington State Wildfire Risk Intelligence Platform</b> (WA FireWatch)<br>
        Data Sources: NOAA Climate Normals | FEMA Declarations | USDA Forest Service WUI | U.S. Census Bureau<br>
        Last Updated: November 2025 | Version 2.0
    </div>
""", unsafe_allow_html=True)
