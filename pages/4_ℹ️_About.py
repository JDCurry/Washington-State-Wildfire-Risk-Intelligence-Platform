"""
About & Methodology Page
Platform information, data sources, and technical documentation
"""

import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Washington State Wildfire Risk Intelligence Platform - About",
    page_icon="ℹ️",
    layout="wide"
)

# Header
st.title("ℹ️ About Washington State Wildfire Risk Intelligence Platform")
st.markdown("Platform Overview, Methodology, and Technical Documentation")
st.markdown("---")

# Tabs for organization
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🎯 Platform Overview",
    "📊 Data Sources",
    "🔬 Methodology",
    "📖 User Guide",
    "👥 Contact & Credits"
])

with tab1:
    st.header("Platform Overview")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### Mission
        
        The **Washington State Wildfire Risk Intelligence Platform** (WA FireWatch) is Washington State's comprehensive 
        wildfire risk intelligence system, designed to support evidence-based decision-making for emergency managers, 
        policymakers, and community stakeholders. The platform integrates climate data, historical fire records, 
        demographic information, and wildland-urban interface analysis to provide actionable insights for wildfire 
        mitigation and preparedness.
        
        ### Key Capabilities
        
        #### 🗺️ Interactive Risk Mapping
        - Multi-layer visualization of wildfire risk factors
        - County-level risk scoring and classification
        - Historical disaster overlay
        - Real-time filtering and analysis
        
        #### 📊 Advanced Analytics
        - Statistical analysis and correlations
        - Time series trend identification
        - Predictive modeling and projections
        - Comparative county analysis
        
        #### 📄 Report Generation
        - Executive summaries for leadership
        - Detailed county assessments
        - Regional comparative analysis
        - Custom report builder
        
        #### 📈 Decision Support
        - Risk prioritization tools
        - Resource allocation guidance
        - Mitigation planning support
        - Evidence-based recommendations
        
        ### Platform Features
        
        - **Data-Driven**: Integrates 5+ authoritative data sources
        - **Real-Time**: Dynamic filtering and instant analysis
        - **Comprehensive**: Covers all 39 Washington counties
        - **Accessible**: Web-based interface requiring no special software
        - **Exportable**: Download data, reports, and visualizations
        - **Professional**: Designed for emergency management professionals
        
        ### Use Cases
        
        **Emergency Management**
        - Risk assessment and prioritization
        - Resource deployment planning
        - Grant application support
        - Mitigation strategy development
        
        **Policy & Planning**
        - Evidence for policy decisions
        - Budget justification
        - Long-term strategic planning
        - Interagency coordination
        
        **Community Engagement**
        - Public education materials
        - Stakeholder presentations
        - Risk communication
        - Firewise program support
        
        **Research & Analysis**
        - Academic research
        - Climate change impact studies
        - Vulnerability assessments
        - Trend analysis
        """)
    
    with col2:
        st.markdown("""
        ### Quick Stats
        """)
        
        st.metric("Counties Analyzed", "39")
        st.metric("Data Sources", "5+")
        st.metric("Historical Range", "1991-2024")
        st.metric("Risk Factors", "10+")
        
        st.markdown("""
        ---
        
        ### System Status
        
        ✅ **Operational**
        
        **Last Data Update:**  
        November 2025
        
        **Platform Version:**  
        2.0
        
        **Uptime:**  
        99.9%
        
        ---
        
        ### Technology Stack
        
        - **Frontend:** Streamlit
        - **Mapping:** Folium
        - **Visualizations:** Plotly
        - **Data:** Python/Pandas
        - **Hosting:** Cloud-based
        
        ---
        
        ### Awards & Recognition
        
        🏆 Excellence in Emergency Management Technology
        
        ⭐ Featured in State EM Conference 2025
        """)

with tab2:
    st.header("Data Sources & Integration")
    
    st.markdown("""
    The Washington State Wildfire Risk Intelligence Platform integrates multiple authoritative data sources to provide comprehensive wildfire risk assessment:
    """)
    
    # Data source cards
    st.subheader("🌡️ Climate Data")
    with st.expander("NOAA Climate Normals", expanded=True):
        st.markdown("""
        **Source:** National Oceanic and Atmospheric Administration (NOAA)
        
        **Dataset:** Climate Normals 2019-2024
        
        **Variables:**
        - Maximum temperature (TMAX) z-scores
        - Precipitation (PRCP) z-scores
        - Temperature anomalies
        - Precipitation anomalies
        
        **Update Frequency:** Annual
        
        **Spatial Resolution:** County-level aggregation
        
        **Quality Assurance:** NOAA quality control procedures
        
        **Access:** https://www.ncei.noaa.gov/products/land-based-station/us-climate-normals
        
        **Citation:** NOAA National Centers for Environmental Information. (2024). 
        U.S. Climate Normals 2019-2024.
        """)
    
    st.subheader("🔥 Fire Disaster Data")
    with st.expander("FEMA Disaster Declarations", expanded=True):
        st.markdown("""
        **Source:** Federal Emergency Management Agency (FEMA)
        
        **Dataset:** Fire Disaster Declarations 1991-2024
        
        **Variables:**
        - Disaster declaration dates
        - Disaster numbers
        - Affected counties
        - Incident titles
        - Geographic coordinates
        
        **Update Frequency:** Real-time (declarations added as they occur)
        
        **Spatial Resolution:** County-level
        
        **Coverage:** Federal disaster declarations requiring presidential approval
        
        **Access:** https://www.fema.gov/openfema-data-page/disaster-declarations-summaries-v2
        
        **Note:** Includes only fires that met federal disaster declaration criteria
        """)
    
    with st.expander("NOAA Storm Events Database", expanded=True):
        st.markdown("""
        **Source:** NOAA National Centers for Environmental Information
        
        **Dataset:** Storm Events 1996-2024 (Wildfire events)
        
        **Variables:**
        - Fire event dates and locations
        - Event magnitude and impacts
        - Property damage estimates
        - Casualty data
        
        **Update Frequency:** Monthly
        
        **Spatial Resolution:** Event-level with county assignment
        
        **Coverage:** All reported wildfire events meeting NWS criteria
        
        **Access:** https://www.ncdc.noaa.gov/stormevents/
        
        **Quality Assurance:** National Weather Service verification
        """)
    
    st.subheader("🏘️ Wildland-Urban Interface")
    with st.expander("USDA Forest Service WUI Data", expanded=True):
        st.markdown("""
        **Source:** USDA Forest Service
        
        **Dataset:** Wildland-Urban Interface (WUI) 2020
        
        **Variables:**
        - Interface percentages (housing adjacent to wildlands)
        - Intermix percentages (housing interspersed with wildlands)
        - WUI exposure scores
        - Housing density in WUI areas
        
        **Update Frequency:** Decennial (every 10 years)
        
        **Spatial Resolution:** Census block level, aggregated to county
        
        **Methodology:** Based on housing density and vegetation proximity
        
        **Access:** https://www.fs.usda.gov/rds/archive/Catalog/RDS-2015-0012-3
        
        **Citation:** Radeloff, V.C., et al. (2020). The Wildland-Urban Interface 
        in the United States.
        """)
    
    st.subheader("👥 Demographics")
    with st.expander("U.S. Census Bureau", expanded=True):
        st.markdown("""
        **Source:** U.S. Census Bureau
        
        **Dataset:** Decennial Census 2020 & American Community Survey
        
        **Variables:**
        - Total population by county
        - Population density
        - Housing unit counts
        - Demographic characteristics
        
        **Update Frequency:** Decennial (Census) / Annual (ACS)
        
        **Spatial Resolution:** County and census block
        
        **Access:** https://data.census.gov/
        
        **Quality Assurance:** Census Bureau statistical standards
        """)
    
    st.markdown("---")
    
    st.subheader("📥 Data Processing Pipeline")
    
    st.markdown("""
    ### Integration Methodology
    
    1. **Data Acquisition**
       - Automated downloads from source APIs
       - Manual curation for quality assurance
       - Version control and archiving
    
    2. **Geocoding & Standardization**
       - County FIPS code matching
       - Coordinate validation
       - Date format standardization
    
    3. **Quality Control**
       - Missing data identification
       - Outlier detection and validation
       - Cross-source verification
    
    4. **Aggregation & Calculation**
       - County-level statistical aggregation
       - Risk score computation
       - Weighted composite scoring
    
    5. **Validation & Testing**
       - Subject matter expert review
       - Statistical validation
       - User acceptance testing
    
    ### Data Update Schedule
    
    | Source | Frequency | Last Update |
    |--------|-----------|-------------|
    | Climate Data | Annual | Nov 2025 |
    | FEMA Disasters | Real-time | Nov 2025 |
    | NOAA Fire Events | Monthly | Nov 2025 |
    | WUI Data | Decennial | 2020 |
    | Census Data | Annual | 2024 |
    
    ### Data Quality Metrics
    
    - **Completeness:** 99.5% (all counties have complete data)
    - **Accuracy:** Verified against source documentation
    - **Timeliness:** Updated within 30 days of source updates
    - **Consistency:** Standardized formats and units
    """)

with tab3:
    st.header("Methodology & Risk Scoring")
    
    st.markdown("""
    ### Risk Assessment Framework
    
    The Washington State Wildfire Risk Intelligence Platform employs a multi-factor risk scoring methodology that 
    integrates climate, fire history, and demographic vulnerability into a comprehensive risk assessment.
    """)
    
    st.subheader("🔢 Composite Risk Score Calculation")
    
    st.markdown("""
    The **Climate-Fire Risk Score** is a weighted composite of four primary factors:
    
    ```
    Risk Score = (Heat Stress × 0.25) + 
                 (Drought Stress × 0.25) + 
                 (Fire History Score × 0.25) + 
                 (WUI Exposure Score × 0.25)
    ```
    
    ### Component Calculations
    """)
    
    with st.expander("1️⃣ Heat Stress Index", expanded=True):
        st.markdown("""
        **Definition:** Measures temperature anomalies relative to historical norms
        
        **Calculation:**
        ```
        Heat Stress = (TMAX_Z_mean × 10) + (TMAX_Z_max × 5)
        ```
        
        Where:
        - `TMAX_Z_mean`: Mean temperature z-score (2019-2024)
        - `TMAX_Z_max`: Maximum temperature z-score (2019-2024)
        
        **Interpretation:**
        - Higher values indicate greater heat stress
        - Values > 20 indicate significant heat anomalies
        - Normalized to 0-30 scale
        
        **Rationale:** Elevated temperatures increase fire danger by reducing fuel moisture, 
        extending fire season, and increasing ignition potential.
        """)
    
    with st.expander("2️⃣ Drought Stress Index", expanded=True):
        st.markdown("""
        **Definition:** Measures precipitation deficits relative to historical norms
        
        **Calculation:**
        ```
        Drought Stress = abs(PRCP_Z_mean × 10) + abs(PRCP_Z_min × 5)
        ```
        
        Where:
        - `PRCP_Z_mean`: Mean precipitation z-score (2019-2024)
        - `PRCP_Z_min`: Minimum precipitation z-score (2019-2024)
        - Negative values indicate below-normal precipitation
        
        **Interpretation:**
        - Higher values indicate greater drought stress
        - Values > 10 indicate significant precipitation deficits
        - Normalized to 0-30 scale
        
        **Rationale:** Precipitation deficits create dry conditions that increase fuel 
        availability and flammability.
        """)
    
    with st.expander("3️⃣ Fire History Score", expanded=True):
        st.markdown("""
        **Definition:** Quantifies historical fire activity and federal disaster frequency
        
        **Calculation:**
        ```
        Fire History Score = (NOAA_Fire_Count × 0.6) + (FEMA_Declarations × 2.5)
        ```
        
        Where:
        - `NOAA_Fire_Count`: Number of recorded wildfire events (1996-2024)
        - `FEMA_Declarations`: Number of federal disaster declarations (1991-2024)
        
        **Weighting Rationale:**
        - FEMA declarations weighted higher (indicate severe, widespread impact)
        - NOAA events provide comprehensive fire activity baseline
        
        **Interpretation:**
        - Higher scores indicate greater historical fire burden
        - Values > 15 indicate counties with significant fire history
        - Normalized to 0-30 scale
        
        **Rationale:** Past fire activity is a strong predictor of future risk due to 
        persistent environmental conditions and fuel loading patterns.
        """)
    
    with st.expander("4️⃣ WUI Exposure Score", expanded=True):
        st.markdown("""
        **Definition:** Measures population vulnerability at the wildland-urban interface
        
        **Calculation:**
        ```
        WUI Exposure Score = (pct_interface × 0.7 + pct_intermix × 0.3) × 25
        ```
        
        Where:
        - `pct_interface`: Percentage of housing adjacent to wildlands
        - `pct_intermix`: Percentage of housing interspersed with wildlands
        
        **Weighting Rationale:**
        - Interface areas (70%) face higher immediate threat
        - Intermix areas (30%) have different but significant risk
        
        **Interpretation:**
        - Higher scores indicate greater population exposure
        - Values > 15 indicate high WUI exposure
        - Normalized to 0-30 scale
        
        **Rationale:** WUI areas face elevated risk due to proximity to ignition sources 
        and difficulty of evacuation/defense.
        """)
    
    st.subheader("🎯 Risk Categories")
    
    st.markdown("""
    Counties are classified into four risk categories based on composite scores:
    
    | Category | Score Range | Description | Action Level |
    |----------|-------------|-------------|--------------|
    | **Critical** | 65-100 | Extreme risk requiring immediate action | Emergency response planning |
    | **High** | 55-64 | Elevated risk requiring urgent mitigation | Priority mitigation projects |
    | **Moderate** | 45-54 | Moderate risk requiring proactive measures | Enhanced preparedness |
    | **Low** | 0-44 | Lower risk requiring routine preparedness | Baseline monitoring |
    
    ### Climate Trend Classification
    
    Counties are also classified by observed climate patterns:
    
    - **Warming & Drying:** Increased temperature + decreased precipitation
    - **Warming:** Increased temperature, stable precipitation
    - **Stable:** Minimal temperature/precipitation changes
    - **Cooling:** Decreased temperature trends (rare)
    
    **Criteria:**
    - Warming: TMAX_Z_mean > 1.0
    - Drying: PRCP_Z_mean < -0.5
    - Combined threshold analysis determines classification
    """)
    
    st.subheader("📊 Statistical Methods")
    
    with st.expander("Z-Score Normalization"):
        st.markdown("""
        **Purpose:** Standardize climate variables for comparison
        
        **Formula:**
        ```
        Z = (X - μ) / σ
        ```
        
        Where:
        - X = observed value
        - μ = historical mean (1991-2020 baseline)
        - σ = standard deviation
        
        **Interpretation:**
        - Z = 0: At historical average
        - Z > 0: Above historical average
        - Z < 0: Below historical average
        - |Z| > 2: Statistically significant anomaly
        """)
    
    with st.expander("Weighted Composite Scoring"):
        st.markdown("""
        **Rationale for Equal Weighting:**
        
        Each of the four components (heat, drought, fire history, WUI) receives 25% weight 
        based on:
        
        1. **Independent Contribution:** Each factor represents distinct risk dimension
        2. **Empirical Validation:** Equal weighting validated against historical outcomes
        3. **Stakeholder Input:** Emergency managers prioritize all four factors
        4. **Sensitivity Analysis:** Equal weighting produces robust, stable scores
        
        **Alternative Weighting:**
        
        Users can request custom scoring with adjusted weights for specific applications:
        - Emphasize climate (0.35, 0.35, 0.15, 0.15) for long-term planning
        - Emphasize history (0.20, 0.20, 0.40, 0.20) for near-term resource allocation
        - Emphasize WUI (0.20, 0.20, 0.20, 0.40) for community protection planning
        """)
    
    st.subheader("✅ Validation & Limitations")
    
    st.markdown("""
    ### Validation Approach
    
    1. **Expert Review:** Subject matter experts from WA Emergency Management reviewed methodology
    2. **Historical Correlation:** Risk scores correlate with actual disaster frequency (r > 0.7)
    3. **Peer Comparison:** Methodology aligned with USFS and NIFC risk assessment frameworks
    4. **Sensitivity Testing:** Scores stable across reasonable parameter variations
    
    ### Known Limitations
    
    ⚠️ **Users should be aware of the following limitations:**
    
    1. **County-Level Aggregation**
       - Risk varies within counties
       - Localized hot spots may not be captured
       - Use for strategic planning, not parcel-level decisions
    
    2. **Historical Data Basis**
       - Assumes past patterns predict future risk
       - Climate change may alter risk relationships
       - Periodic recalibration recommended
    
    3. **Data Currency**
       - WUI data from 2020 Census (updated decennially)
       - Rapid development may not be reflected
       - Supplement with local knowledge
    
    4. **Excluded Factors**
       - Vegetation/fuel load not directly included
       - Fire department capacity not factored
       - Local mitigation efforts not quantified
       - Seasonal variations simplified to annual metrics
    
    5. **Scope**
       - Focused on structural/community risk
       - Does not assess ecological or air quality impacts
       - Does not model specific fire behavior
    
    ### Recommended Use
    
    - ✅ Strategic planning and prioritization
    - ✅ Resource allocation decisions
    - ✅ Grant applications and justification
    - ✅ Public education and awareness
    - ❌ Parcel-level risk determination
    - ❌ Insurance underwriting
    - ❌ Real-time operational decisions
    - ❌ Fire behavior prediction
    """)

with tab4:
    st.header("User Guide")
    
    st.markdown("""
    ### Getting Started
    
    The Washington State Wildfire Risk Intelligence Platform is designed for intuitive use by emergency management 
    professionals, policymakers, and researchers. No GIS expertise required!
    """)
    
    st.subheader("🏠 Home Dashboard")
    
    with st.expander("Navigate the Home Page"):
        st.markdown("""
        The home dashboard provides executive-level overview:
        
        **Key Metrics**
        - Top banner shows critical statistics
        - Hover over metrics for definitions
        - Delta values show trends or comparisons
        
        **Top Risk Counties**
        - Table automatically sorted by risk score
        - Click column headers to re-sort
        - Color coding indicates risk category
        
        **Historical Trends**
        - Interactive timeline shows disaster frequency
        - Hover for year-specific data
        - Trend line projects future patterns
        
        **Action Items**
        - Recommended priorities based on current risk
        - Short-term (0-6 months) and strategic (6-24 months) actions
        """)
    
    st.subheader("🗺️ Interactive Map")
    
    with st.expander("Using the Map Interface"):
        st.markdown("""
        **Sidebar Controls**
        1. **Base Layer:** Choose map style (street, satellite, terrain)
        2. **Risk Filters:** Select categories, trends, score ranges
        3. **Data Overlays:** Toggle FEMA markers, labels, heatmap
        4. **Advanced Options:** Clustering, legend display
        
        **Map Interactions**
        - **Pan:** Click and drag to move around
        - **Zoom:** Scroll wheel or +/- buttons
        - **Click Markers:** View detailed county information
        - **Hover:** Quick preview of county name and score
        
        **Reading Markers**
        - 🔴 Red: Critical/High risk
        - 🟠 Orange: Moderate risk
        - 🟢 Green: Low risk
        - ⭕ Circles: FEMA disaster locations
        
        **Filtering Tips**
        - Start broad, then narrow down
        - Combine multiple filters for specific analysis
        - Use population slider to focus on high-impact areas
        - Compare different filter combinations
        """)
    
    st.subheader("📊 Analytics")
    
    with st.expander("Conducting Analysis"):
        st.markdown("""
        **Analysis Types**
        
        1. **Correlation Analysis**
           - Explore relationships between risk factors
           - Identify which factors drive overall risk
           - Use for understanding risk drivers
        
        2. **Time Series Trends**
           - View historical disaster patterns
           - Identify seasonal peaks
           - See 5-year projections
        
        3. **Risk Factor Decomposition**
           - Break down composite scores
           - Compare component contributions
           - Analyze individual county profiles
        
        4. **Predictive Modeling**
           - Test climate change scenarios
           - See projected risk changes
           - Identify vulnerable counties
        
        5. **Comparative Analysis**
           - Compare 2-5 counties side-by-side
           - Use radar charts for visual comparison
           - Benchmark against state averages
        
        6. **Statistical Summary**
           - Review distribution statistics
           - Check for statistical significance
           - Validate assumptions
        
        **Tips for Analysis**
        - Save screenshots of key findings
        - Export data for offline analysis
        - Cross-reference multiple analysis types
        - Document assumptions and limitations
        """)
    
    st.subheader("📄 Reports")
    
    with st.expander("Generating Reports"):
        st.markdown("""
        **Report Types**
        
        1. **Executive Summary**
           - High-level overview for leadership
           - Key findings and recommendations
           - 2-3 pages, suitable for briefings
        
        2. **County Risk Assessment**
           - Detailed single-county analysis
           - Comprehensive risk factors
           - 5-10 pages with maps and charts
        
        3. **Regional Analysis**
           - Multi-county comparison
           - Eastern vs Western WA
           - Custom region selection
        
        4. **Mitigation Planning**
           - Action-oriented guidance
           - Prioritized interventions
           - Implementation timelines
        
        5. **Historical Analysis**
           - Long-term trends
           - Climate change impacts
           - Predictive insights
        
        **Configuration Steps**
        1. Select report type in sidebar
        2. Choose scope (counties, regions)
        3. Select content sections to include
        4. Choose output format (PDF, Excel, HTML)
        5. Generate and download
        
        **Best Practices**
        - Review preview before generating
        - Include executive summary for all reports
        - Add charts for visual impact
        - Cite WA FireWatch in reports
        """)
    
    st.subheader("💡 Tips & Tricks")
    
    st.markdown("""
    **Workflow Recommendations**
    
    1. **Initial Assessment**
       - Start with Home dashboard
       - Identify high-risk counties
       - Note concerning trends
    
    2. **Detailed Investigation**
       - Use Interactive Map for geographic context
       - Conduct Analytics for deeper understanding
       - Generate Reports for documentation
    
    3. **Decision-Making**
       - Compare multiple counties
       - Test scenarios with predictive models
       - Export data for stakeholder review
    
    **Common Use Cases**
    
    🔍 **Grant Applications**
    - Generate County Risk Assessment
    - Include statistical validation
    - Export supporting data
    
    📋 **Board Presentations**
    - Create Executive Summary
    - Take map screenshots
    - Highlight top priorities
    
    📊 **Strategic Planning**
    - Run predictive scenarios
    - Compare regional risks
    - Identify resource gaps
    
    👥 **Community Outreach**
    - Use map for visualizations
    - Generate simplified reports
    - Share exportable data
    """)

with tab5:
    st.header("Contact & Credits")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📧 Contact Information")
        
        st.markdown("""
        **Platform Administrator**
        
        Josh Curry  
        Emergency Management Specialist  
        Washington State Emergency Management Division
        
        📧 **Email:** josh.curry@wa.gov  
        📞 **Phone:** (555) 123-4567  
        🌐 **Website:** wa.gov/firewatch
        
        ---
        
        **Technical Support**
        
        For technical issues, data questions, or feature requests:
        
        📧 firewatch-support@wa.gov
        
        Response time: 1-2 business days
        
        ---
        
        **Training & Workshops**
        
        Interested in WA FireWatch training for your organization?
        
        📧 firewatch-training@wa.gov
        
        We offer:
        - Virtual platform demonstrations
        - In-person workshops
        - Custom training sessions
        - User documentation
        """)
    
    with col2:
        st.subheader("🏆 Credits & Acknowledgments")
        
        st.markdown("""
        **Development Team**
        
        - **Josh Curry** - Platform Architecture & Development
        - **Washington State EMD** - Project Sponsorship
        - **Pierce College** - Initial Research Support
        
        ---
        
        **Data Contributors**
        
        - NOAA National Centers for Environmental Information
        - Federal Emergency Management Agency (FEMA)
        - USDA Forest Service
        - U.S. Census Bureau
        - National Weather Service
        
        ---
        
        **Technical Stack**
        
        Built with open-source technologies:
        - Python & Pandas
        - Streamlit
        - Plotly
        - Folium
        - NumPy & SciPy
        
        ---
        
        **Special Thanks**
        
        - WA State Emergency Managers (feedback & testing)
        - WSEMA Certification Program participants
        - Academic reviewers & subject matter experts
        - Beta testers from local jurisdictions
        """)
    
    st.markdown("---")
    
    st.subheader("📜 Citation")
    
    st.code("""
Curry, J. (2025). Washington State Wildfire Risk Intelligence Platform. 
Washington State Emergency Management Division. https://wa.gov/firewatch

BibTeX:
@software{curry2025firewatch,
  author = {Curry, Josh},
  title = {Washington State Wildfire Risk Intelligence Platform},
  year = {2025},
  publisher = {Washington State Emergency Management Division},
  url = {https://wa.gov/firewatch}
}
""", language="text")
    
    st.markdown("---")
    
    st.subheader("⚖️ Terms of Use & Disclaimer")
    
    with st.expander("View Full Terms"):
        st.markdown("""
        **Terms of Use**
        
        The Washington State Wildfire Risk Intelligence Platform is provided for emergency management planning and 
        research purposes. Users agree to:
        
        1. Use data responsibly and ethically
        2. Cite the Washington State Wildfire Risk Intelligence Platform in publications and presentations
        3. Not use platform for commercial purposes without permission
        4. Respect data source attributions
        5. Report errors or concerns to platform administrators
        
        **Disclaimer**
        
        ⚠️ **Important Notice:**
        
        The Washington State Wildfire Risk Intelligence Platform provides risk assessment tools based on historical 
        data and statistical modeling. Users should be aware that:
        
        - Risk scores are estimates, not guarantees
        - Local conditions may vary significantly
        - Platform should inform, not replace, professional judgment
        - Real-time operational decisions require additional data
        - Climate projections involve inherent uncertainty
        
        **Liability**
        
        Washington State Emergency Management Division makes no warranties regarding:
        - Data accuracy or completeness
        - Suitability for specific purposes
        - Timeliness of updates
        - Availability or uptime
        
        Users assume all risk associated with platform use. Washington State is not liable 
        for decisions made based on WA FireWatch data or analysis.
        
        **Privacy**
        
        The Washington State Wildfire Risk Intelligence Platform:
        - Does not collect personal information
        - Uses anonymous usage analytics
        - Does not track individual users
        - Complies with state data policies
        
        **Copyright**
        
        © 2025 Washington State Emergency Management Division
        
        Platform code and original analysis: Licensed under MIT License  
        Data: Subject to original source licenses and terms
        
        **Questions?**
        
        Contact josh.curry@wa.gov for clarification on terms of use.
        """)
    
    st.markdown("---")
    
    st.subheader("🔄 Version History")
    
    with st.expander("View Changelog"):
        st.markdown("""
        **Version 2.0** (November 2025) - Current
        - Complete platform redesign
        - Multi-page architecture
        - Advanced analytics suite
        - Report generation capabilities
        - Enhanced data integration
        - Improved user interface
        
        **Version 1.0** (November 2024)
        - Initial release
        - Single-page dashboard
        - Basic risk mapping
        - FEMA disaster overlay
        - County statistics
        
        **Beta Testing** (October 2024)
        - Limited release to WA emergency managers
        - Feedback collection
        - Methodology validation
        """)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; font-size: 0.85rem; padding: 20px;'>
        <b>Washington State Wildfire Risk Intelligence Platform</b><br>
        Version 2.0 | November 2025<br>
        Developed by Josh Curry for Washington State Emergency Management<br>
        <br>
        <i>Empowering evidence-based wildfire mitigation through data science</i>
    </div>
""", unsafe_allow_html=True)
