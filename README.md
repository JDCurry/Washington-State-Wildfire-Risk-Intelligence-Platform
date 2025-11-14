# WA FireWatch - Washington State Wildfire Risk Intelligence Platform

## 🔥 Overview

**WA FireWatch** is a comprehensive wildfire risk intelligence platform designed for emergency management professionals, policymakers, and researchers in Washington State. The platform integrates climate data, historical fire records, demographic information, and wildland-urban interface analysis to provide actionable insights for wildfire mitigation and preparedness.

## ✨ Key Features

### 🗺️ Interactive Risk Mapping
- Multi-layer visualization with county-level risk scoring
- Historical FEMA disaster overlay with detailed popups
- Dynamic filtering by risk category, climate trend, and population
- Multiple base map styles (street, satellite, terrain)
- Clustered markers for improved performance

### 📊 Advanced Analytics
- **Correlation Analysis** - Explore relationships between risk factors
- **Time Series Trends** - Historical patterns and 5-year projections
- **Risk Factor Decomposition** - Component-level analysis
- **Predictive Modeling** - Climate change scenario testing
- **Comparative Analysis** - Side-by-side county comparison
- **Statistical Summary** - Comprehensive distribution statistics

### 📄 Report Generation
- **Executive Summaries** - High-level overviews for leadership
- **County Risk Assessments** - Detailed single-county analysis
- **Regional Analysis** - Multi-county comparisons
- **Mitigation Planning** - Action-oriented guidance
- **Custom Reports** - Flexible report builder

### 📈 Decision Support
- Evidence-based prioritization
- Resource allocation guidance
- Risk scenario modeling
- Export capabilities (CSV, PDF, HTML)

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone or download the repository**
```bash
cd wa_firewatch
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Prepare data files**
Place the following files in the `data/` directory:
- `WA_Climate_Fire_Dashboard_Data.csv`
- `FEMA_Disasters_Geocoded.csv`
- `wa_counties.geojson` (optional, for enhanced mapping)

4. **Run the application**
```bash
streamlit run Home.py
```

5. **Access the platform**
Open your web browser to `http://localhost:8501`

## 📁 Project Structure

```
wa_firewatch/
├── Home.py                          # Main dashboard entry point
├── pages/
│   ├── 1_🗺️_Interactive_Map.py      # Interactive mapping interface
│   ├── 2_📊_Analytics.py            # Advanced analytics suite
│   ├── 3_📄_Reports.py              # Report generation
│   └── 4_ℹ️_About.py                # Documentation & methodology
├── data/
│   ├── WA_Climate_Fire_Dashboard_Data.csv
│   ├── FEMA_Disasters_Geocoded.csv
│   └── wa_counties.geojson (optional)
├── utils/                           # Utility functions (future)
├── assets/                          # Images and static files (future)
├── requirements.txt                 # Python dependencies
└── README.md                        # This file
```

## 📊 Data Sources

The platform integrates multiple authoritative data sources:

1. **NOAA Climate Normals (2019-2024)**
   - Temperature and precipitation anomalies
   - County-level climate trends

2. **FEMA Disaster Declarations (1991-2024)**
   - Federal fire disaster declarations
   - 126 historical events

3. **NOAA Storm Events (1996-2024)**
   - 482 wildfire events
   - Property damage estimates

4. **USDA Forest Service WUI Data (2020)**
   - Wildland-Urban Interface mapping
   - Housing density in fire-prone areas

5. **U.S. Census Bureau (2020)**
   - Population demographics
   - Housing unit counts

## 🔬 Methodology

### Risk Score Calculation

The **Climate-Fire Risk Score** is a weighted composite:

```
Risk Score = (Heat Stress × 0.25) + 
             (Drought Stress × 0.25) + 
             (Fire History Score × 0.25) + 
             (WUI Exposure Score × 0.25)
```

### Risk Categories

| Category | Score Range | Description |
|----------|-------------|-------------|
| Critical | 65-100 | Extreme risk requiring immediate action |
| High | 55-64 | Elevated risk requiring urgent mitigation |
| Moderate | 45-54 | Moderate risk requiring proactive measures |
| Low | 0-44 | Lower risk requiring routine preparedness |

For detailed methodology, see the "About & Methodology" page in the platform.

## 💡 Use Cases

### Emergency Management
- Risk assessment and prioritization
- Resource deployment planning
- Grant application support
- Mitigation strategy development

### Policy & Planning
- Evidence for policy decisions
- Budget justification
- Long-term strategic planning
- Interagency coordination

### Community Engagement
- Public education materials
- Stakeholder presentations
- Risk communication
- Firewise program support

### Research & Analysis
- Academic research
- Climate change impact studies
- Vulnerability assessments
- Trend analysis

## 🛠️ Technical Stack

- **Frontend Framework:** Streamlit 1.28+
- **Mapping:** Folium 0.14+
- **Visualizations:** Plotly 5.17+
- **Data Processing:** Pandas 2.0+, NumPy 1.24+
- **Statistical Analysis:** SciPy 1.11+
- **Python Version:** 3.8+

## 📖 User Guide

### Navigation
- **Home:** Executive dashboard with key metrics and insights
- **Interactive Map:** Multi-layer risk visualization
- **Analytics:** Deep statistical analysis tools
- **Reports:** Custom report generation
- **About:** Methodology and documentation

### Tips for Effective Use
1. Start with the Home dashboard to identify priorities
2. Use the Interactive Map for geographic context
3. Conduct deep-dive analysis in the Analytics section
4. Generate reports for stakeholder communication
5. Export data for offline analysis and presentation

## 🤝 Contributing

This is a professional emergency management tool. For contributions, enhancements, or bug reports:

**Contact:** Josh Curry  
**Email:** josh.curry@wa.gov  
**Organization:** Washington State Emergency Management Division

## 📜 Citation

If you use WA FireWatch in research or publications, please cite:

```
Curry, J. (2025). WA FireWatch: Washington State Wildfire Risk Intelligence Platform. 
Washington State Emergency Management Division. https://wa.gov/firewatch
```

## ⚠️ Disclaimer

WA FireWatch provides risk assessment tools based on historical data and statistical modeling. Users should be aware that:

- Risk scores are estimates, not guarantees
- Local conditions may vary significantly
- Platform should inform, not replace, professional judgment
- Real-time operational decisions require additional data

## 📄 License

© 2025 Washington State Emergency Management Division

**Platform Code:** MIT License  
**Data:** Subject to original source licenses and terms

See data source documentation for specific usage restrictions.

## 🔄 Version History

**Version 2.0** (November 2025) - Current
- Complete platform redesign with multi-page architecture
- Advanced analytics suite
- Report generation capabilities
- Enhanced data integration
- Professional branding and UI

**Version 1.0** (November 2024)
- Initial release with basic dashboard functionality

## 📞 Support

For technical support, training, or questions:

- **Technical Support:** firewatch-support@wa.gov
- **Training Inquiries:** firewatch-training@wa.gov
- **General Questions:** josh.curry@wa.gov

---

**WA FireWatch** - Empowering evidence-based wildfire mitigation through data science
