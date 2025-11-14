"""
Report Generation Page
Custom report builder with PDF export and email capabilities
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import io

st.set_page_config(
    page_title="WA FireWatch - Reports",
    page_icon="📄",
    layout="wide"
)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('data/WA_Climate_Fire_Dashboard_Data.csv')
    return df

@st.cache_data
def load_fema_data():
    try:
        fema = pd.read_csv('data/FEMA_Disasters_Geocoded.csv')
        fema['declarationDate'] = pd.to_datetime(fema['declarationDate'])
        return fema
    except FileNotFoundError:
        return None

df = load_data()
fema_data = load_fema_data()

# Header
st.title("📄 Report Generation Center")
st.markdown("Create custom reports for stakeholders and decision-makers")
st.markdown("---")

# Sidebar - Report Configuration
with st.sidebar:
    st.header("📋 Report Configuration")
    
    report_type = st.selectbox(
        "Report Type",
        [
            "Executive Summary",
            "County Risk Assessment",
            "Regional Analysis",
            "Mitigation Planning",
            "Historical Analysis",
            "Custom Report"
        ]
    )
    
    st.markdown("---")
    
    st.subheader("Scope")
    
    if report_type == "County Risk Assessment":
        selected_counties = st.multiselect(
            "Select Counties",
            sorted(df['County'].unique()),
            default=[df.nlargest(1, 'climate_fire_risk_score')['County'].values[0]]
        )
    elif report_type == "Regional Analysis":
        region = st.selectbox(
            "Select Region",
            ["Eastern Washington", "Western Washington", "Statewide", "Custom"]
        )
        
        if region == "Custom":
            selected_counties = st.multiselect(
                "Select Counties",
                sorted(df['County'].unique())
            )
    else:
        selected_counties = []
    
    st.markdown("---")
    
    st.subheader("Content Sections")
    
    include_summary = st.checkbox("Executive Summary", value=True)
    include_risk_maps = st.checkbox("Risk Maps", value=True)
    include_statistics = st.checkbox("Statistical Analysis", value=True)
    include_trends = st.checkbox("Historical Trends", value=True)
    include_projections = st.checkbox("Future Projections", value=False)
    include_recommendations = st.checkbox("Recommendations", value=True)
    include_appendix = st.checkbox("Data Appendix", value=False)
    
    st.markdown("---")
    
    st.subheader("Format Options")
    
    report_format = st.selectbox(
        "Output Format",
        ["PDF", "HTML", "Word Document", "PowerPoint"]
    )
    
    include_charts = st.checkbox("Include Charts/Graphs", value=True)
    include_tables = st.checkbox("Include Data Tables", value=True)
    color_scheme = st.selectbox(
        "Color Scheme",
        ["Professional", "High Contrast", "Grayscale"]
    )

# Main content area
if report_type == "Executive Summary":
    st.header("📊 Executive Summary Report")
    st.markdown("High-level overview for leadership and stakeholders")
    
    # Preview
    st.subheader("Report Preview")
    
    with st.expander("📄 View Report Content", expanded=True):
        st.markdown(f"""
        # Washington State Wildfire Risk Intelligence Report
        ## Executive Summary
        
        **Date:** {datetime.now().strftime('%B %d, %Y')}  
        **Prepared by:** WA FireWatch Platform  
        **Classification:** For Official Use Only
        
        ---
        
        ### Key Findings
        
        **Overall Risk Assessment:**
        - **{len(df[df['risk_category'] == 'Critical'])}** counties classified as Critical Risk
        - **{len(df[df['risk_category'] == 'High'])}** counties classified as High Risk
        - **{df['population_at_risk'].sum() / 1000000:.2f} million** residents in high-risk WUI areas
        - **{len(df[df['climate_trend'].str.contains('Warming', na=False)])}** counties showing concerning climate trends
        
        **Top Risk Counties:**
        """)
        
        top_5 = df.nlargest(5, 'climate_fire_risk_score')
        for idx, row in top_5.iterrows():
            st.markdown(f"""
            {row['County']} County
            - Risk Score: {row['climate_fire_risk_score']:.1f} ({row['risk_category']})
            - Climate Trend: {row['climate_trend']}
            - Population at Risk: {row['population_at_risk']:,.0f}
            """)
        
        st.markdown("""
        ---
        
        ### Critical Trends
        
        **Climate Change Impact:**
        - Increasing heat stress in {len(df[df['heat_stress'] > 20])} counties
        - Drought conditions affecting {len(df[df['drought_stress'] > 10])} counties
        - Warming & drying pattern observed in {len(df[df['climate_trend'] == 'Warming & Drying'])} counties
        
        **Historical Context:**
        """)
        
        if fema_data is not None:
            recent_disasters = len(fema_data[fema_data['declarationDate'] >= '2020-01-01'])
            st.markdown(f"""
            - **{len(fema_data)}** federal fire disaster declarations since 1991
            - **{recent_disasters}** disasters in the last 5 years
            - Average of **{len(fema_data) / (2024 - 1991):.1f}** disasters per year
            """)
        
        st.markdown("""
        ---
        
        ### Immediate Priorities
        
        1. **Critical Risk Mitigation** - Deploy resources to {len(df[df['risk_category'] == 'Critical'])} critical counties
        2. **WUI Defensible Space** - Expand programs in high-exposure areas
        3. **Climate Adaptation** - Develop strategies for warming trend counties
        4. **Resource Pre-positioning** - Stage equipment in highest-risk areas
        5. **Public Education** - Launch awareness campaigns in vulnerable communities
        
        ---
        
        ### Budget Implications
        
        **Estimated Investment Needs:**
        - Immediate mitigation (0-6 months): $XX million
        - Strategic planning (6-24 months): $XX million
        - Long-term adaptation: $XX million
        
        **Cost of Inaction:**
        - Based on historical disaster costs, inadequate preparation could result in:
          - Property damage: $XXX million per major event
          - Economic disruption: $XXX million annually
          - Emergency response costs: $XX million per incident
        
        ---
        
        ### Recommendations
        
        **Short-term (0-6 months):**
        - Activate emergency mitigation planning for critical counties
        - Conduct vulnerability assessments for top 10 risk areas
        - Update mutual aid agreements with neighboring jurisdictions
        
        **Medium-term (6-24 months):**
        - Implement fuel management programs
        - Upgrade infrastructure in vulnerable areas
        - Expand Firewise USA participation
        
        **Long-term (2+ years):**
        - Integrate climate adaptation into all planning
        - Develop regional coordination frameworks
        - Invest in predictive modeling capabilities
        
        ---
        
        ### Conclusion
        
        Washington State faces escalating wildfire risk driven by climate change, expanding wildland-urban interface, and increasing fire frequency. Immediate action is required to protect lives, property, and ecosystems. This report provides the analytical foundation for evidence-based mitigation planning and resource allocation.
        
        **For additional analysis or specific county assessments, contact:**  
        Josh Curry, Emergency Management Specialist  
        josh.curry@wa.gov
        """)

elif report_type == "County Risk Assessment":
    st.header("🏘️ County Risk Assessment Report")
    
    if selected_counties:
        for county in selected_counties:
            county_data = df[df['County'] == county].iloc[0]
            
            with st.expander(f"📍 {county} County Report", expanded=True):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"""
                    # {county} County Wildfire Risk Assessment
                    
                    **Assessment Date:** {datetime.now().strftime('%B %d, %Y')}
                    
                    ---
                    
                    ## Executive Summary
                    
                    **Overall Risk Classification:** {county_data['risk_category']}  
                    **Climate-Fire Risk Score:** {county_data['climate_fire_risk_score']:.1f} / 100
                    
                    {county} County is classified as **{county_data['risk_category']}** risk with a composite score of {county_data['climate_fire_risk_score']:.1f}. 
                    The county shows a **{county_data['climate_trend']}** climate pattern and has experienced **{county_data['Fire_Count']}** recorded fire events.
                    
                    ---
                    
                    ## Risk Factor Analysis
                    
                    ### Climate Factors
                    - **Heat Stress Index:** {county_data['heat_stress']:.2f}
                    - **Drought Stress Index:** {county_data['drought_stress']:.2f}
                    - **Climate Trend:** {county_data['climate_trend']}
                    - **Temperature Anomaly (Mean):** {county_data['TMAX_Z_mean']:.2f}°C
                    - **Precipitation Anomaly (Mean):** {county_data['PRCP_Z_mean']:.2f} inches
                    
                    ### Fire History
                    - **Historical Fire Events:** {county_data['Fire_Count']}
                    - **Fire History Score:** {county_data['fire_history_score']:.2f}
                    """)
                    
                    if fema_data is not None:
                        county_fema = fema_data[fema_data['County'] == county]
                        if len(county_fema) > 0:
                            st.markdown(f"- **FEMA Disaster Declarations:** {len(county_fema)}")
                            st.markdown("- **Recent Disasters:**")
                            for _, fire in county_fema.nlargest(3, 'declarationDate').iterrows():
                                st.markdown(f"  - {fire['declarationTitle']} ({fire['declarationDate'].strftime('%Y')})")
                    
                    st.markdown(f"""
                    ### Wildland-Urban Interface
                    - **WUI Exposure Score:** {county_data['wui_exposure_score']:.2f}
                    - **Interface Areas:** {county_data['pct_interface'] * 100:.1f}%
                    - **Intermix Areas:** {county_data['pct_intermix'] * 100:.1f}%
                    - **Overall WUI Exposure:** {county_data['wui_exposure_pct']:.1f}%
                    
                    ### Population Impact
                    - **Total Population:** {county_data['population']:,}
                    - **Population at Risk:** {county_data['population_at_risk']:,.0f}
                    - **Mean Population Density:** {county_data['mean_pop_density']:.1f} per sq mi
                    - **Average Housing Density:** {county_data['avg_housing_density']:.1f} per sq mi
                    
                    ---
                    
                    ## Recommendations
                    
                    ### Immediate Actions (0-6 months)
                    """)
                    
                    if county_data['risk_category'] in ['Critical', 'High']:
                        st.markdown("""
                        1. **Emergency Mitigation Planning** - Initiate county-wide risk reduction strategies
                        2. **Community Outreach** - Launch public education on fire preparedness
                        3. **Evacuation Planning** - Update and test evacuation routes
                        4. **Resource Staging** - Pre-position firefighting equipment
                        5. **Defensible Space** - Enforce regulations in WUI areas
                        """)
                    else:
                        st.markdown("""
                        1. **Preventive Planning** - Maintain current mitigation efforts
                        2. **Community Education** - Continue Firewise programs
                        3. **Monitoring** - Track climate and fire indicators
                        """)
                    
                    st.markdown("""
                    ### Strategic Planning (6-24 months)
                    
                    1. **Fuel Management** - Implement prescribed burns and mechanical thinning
                    2. **Infrastructure Hardening** - Upgrade critical facilities
                    3. **Zoning Updates** - Revise codes to reduce fire risk
                    4. **Regional Coordination** - Establish mutual aid partnerships
                    
                    ---
                    
                    ## Conclusion
                    """)
                    
                    risk_level_text = {
                        'Critical': 'immediate and comprehensive action',
                        'High': 'urgent mitigation measures',
                        'Moderate': 'proactive risk reduction strategies',
                        'Low': 'continued vigilance and preventive measures'
                    }
                    
                    st.markdown(f"""
                    {county} County's {county_data['risk_category'].lower()} risk classification indicates the need for 
                    {risk_level_text[county_data['risk_category']]}. With {county_data['population_at_risk']:,.0f} residents 
                    in wildland-urban interface areas and a {county_data['climate_trend'].lower()} climate trend, the county 
                    faces significant wildfire challenges that require coordinated response from emergency management, 
                    fire services, and community stakeholders.
                    """)
                
                with col2:
                    st.markdown("### Risk Profile")
                    
                    # Risk gauge
                    fig_gauge = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=county_data['climate_fire_risk_score'],
                        domain={'x': [0, 1], 'y': [0, 1]},
                        gauge={
                            'axis': {'range': [None, 100]},
                            'bar': {'color': "darkred" if county_data['risk_category'] == 'Critical' else
                                           "red" if county_data['risk_category'] == 'High' else
                                           "orange" if county_data['risk_category'] == 'Moderate' else "green"},
                            'steps': [
                                {'range': [0, 45], 'color': "lightgray"},
                                {'range': [45, 55], 'color': "lightyellow"},
                                {'range': [55, 65], 'color': "lightcoral"},
                                {'range': [65, 100], 'color': "lightpink"}
                            ],
                            'threshold': {
                                'line': {'color': "black", 'width': 4},
                                'thickness': 0.75,
                                'value': county_data['climate_fire_risk_score']
                            }
                        }
                    ))
                    
                    fig_gauge.update_layout(height=250)
                    st.plotly_chart(fig_gauge, use_container_width=True)
                    
                    st.markdown("### Component Scores")
                    st.metric("Heat Stress", f"{county_data['heat_stress']:.1f}")
                    st.metric("Drought Stress", f"{county_data['drought_stress']:.1f}")
                    st.metric("Fire History", f"{county_data['fire_history_score']:.1f}")
                    st.metric("WUI Exposure", f"{county_data['wui_exposure_score']:.1f}")
    else:
        st.warning("⚠️ Please select at least one county in the sidebar")

elif report_type == "Regional Analysis":
    st.header("🗺️ Regional Analysis Report")
    st.markdown("Comparative analysis across geographic regions")
    
    # Define regions
    eastern_counties = ['SPOKANE', 'YAKIMA', 'BENTON', 'FRANKLIN', 'WALLA WALLA', 
                       'GRANT', 'CHELAN', 'DOUGLAS', 'OKANOGAN', 'ADAMS', 'WHITMAN']
    
    if region == "Eastern Washington":
        region_df = df[df['County'].isin(eastern_counties)]
        region_name = "Eastern Washington"
    elif region == "Western Washington":
        region_df = df[~df['County'].isin(eastern_counties)]
        region_name = "Western Washington"
    elif region == "Statewide":
        region_df = df
        region_name = "Statewide"
    else:  # Custom
        if selected_counties:
            region_df = df[df['County'].isin(selected_counties)]
            region_name = "Custom Region"
        else:
            region_df = df
            region_name = "Statewide"
    
    with st.expander("📊 Regional Report", expanded=True):
        st.markdown(f"""
        # {region_name} Wildfire Risk Analysis
        
        **Analysis Date:** {datetime.now().strftime('%B %d, %Y')}  
        **Counties Included:** {len(region_df)}
        
        ---
        
        ## Regional Summary
        
        ### Risk Distribution
        - **Critical Risk:** {len(region_df[region_df['risk_category'] == 'Critical'])} counties
        - **High Risk:** {len(region_df[region_df['risk_category'] == 'High'])} counties
        - **Moderate Risk:** {len(region_df[region_df['risk_category'] == 'Moderate'])} counties
        - **Low Risk:** {len(region_df[region_df['risk_category'] == 'Low'])} counties
        
        ### Regional Averages
        - **Average Risk Score:** {region_df['climate_fire_risk_score'].mean():.1f}
        - **Total Population:** {region_df['population'].sum():,}
        - **Population at Risk:** {region_df['population_at_risk'].sum():,.0f}
        - **Average WUI Exposure:** {region_df['wui_exposure_pct'].mean():.1f}%
        
        ### Climate Trends
        - **Warming & Drying:** {len(region_df[region_df['climate_trend'] == 'Warming & Drying'])} counties
        - **Warming:** {len(region_df[region_df['climate_trend'] == 'Warming'])} counties
        - **Stable:** {len(region_df[region_df['climate_trend'] == 'Stable'])} counties
        
        ---
        
        ## Highest Risk Counties
        """)
        
        top_regional = region_df.nlargest(10, 'climate_fire_risk_score')
        for idx, row in top_regional.iterrows():
            st.markdown(f"""
            ### {row['County']} County
            - Risk Score: {row['climate_fire_risk_score']:.1f}
            - Category: {row['risk_category']}
            - Population at Risk: {row['population_at_risk']:,.0f}
            - Climate Trend: {row['climate_trend']}
            """)
        
        st.markdown("""
        ---
        
        ## Regional Recommendations
        
        ### Priority Actions
        1. Coordinate inter-county mutual aid agreements
        2. Establish regional resource sharing protocols
        3. Develop unified public education campaigns
        4. Create regional evacuation coordination plans
        5. Share best practices across jurisdictions
        
        ### Resource Allocation
        - Focus on counties with Critical and High risk classifications
        - Pre-position equipment in highest-risk areas
        - Establish regional coordination centers
        - Develop shared GIS and intelligence platforms
        """)

else:  # Custom, Mitigation Planning, Historical Analysis
    st.header(f"📋 {report_type}")
    st.info("🚧 This report type is under development. Use the sidebar to configure your custom report parameters.")

st.markdown("---")

# Generation controls
st.subheader("📤 Generate & Export Report")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("📄 Generate PDF", use_container_width=True):
        st.info("📝 PDF generation requires additional setup. Export HTML version or download data instead.")

with col2:
    if st.button("📊 Export to Excel", use_container_width=True):
        # Export filtered data
        if report_type == "County Risk Assessment" and selected_counties:
            export_df = df[df['County'].isin(selected_counties)]
        elif report_type == "Regional Analysis":
            export_df = region_df
        else:
            export_df = df
        
        st.download_button(
            label="💾 Download Data",
            data=export_df.to_csv(index=False),
            file_name=f"wa_firewatch_{report_type.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

with col3:
    if st.button("📧 Email Report", use_container_width=True):
        st.info("📧 Email functionality requires SMTP configuration. Contact your administrator.")

with col4:
    if st.button("🔗 Share Link", use_container_width=True):
        st.info("🔗 Shareable links coming soon in the next platform update.")

st.markdown("---")

# Report templates
with st.expander("📚 Available Report Templates"):
    st.markdown("""
    ### Standard Templates
    
    **Executive Summary** - High-level overview for leadership
    - Key findings and recommendations
    - Risk distribution
    - Budget implications
    
    **County Risk Assessment** - Detailed county analysis
    - Comprehensive risk factors
    - Historical context
    - Specific recommendations
    
    **Regional Analysis** - Multi-county comparison
    - Geographic patterns
    - Resource allocation guidance
    - Coordination strategies
    
    **Mitigation Planning** - Action-oriented guidance
    - Prioritized interventions
    - Cost-benefit analysis
    - Implementation timelines
    
    **Historical Analysis** - Trend identification
    - Long-term patterns
    - Climate change impacts
    - Predictive insights
    
    ### Custom Reports
    
    Build your own report by selecting specific:
    - Counties or regions
    - Time periods
    - Risk factors
    - Output formats
    """)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; font-size: 0.85rem;'>
        <b>WA FireWatch Report Generator</b><br>
        For technical support or custom report requests, contact josh.curry@wa.gov
    </div>
""", unsafe_allow_html=True)
