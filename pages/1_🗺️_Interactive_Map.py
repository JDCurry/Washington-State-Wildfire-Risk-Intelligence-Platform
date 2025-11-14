"""
Interactive Risk Map Page
Multi-layer visualization with advanced filtering and analysis
"""

import streamlit as st
import pandas as pd
import folium
from folium import plugins
from streamlit_folium import st_folium
import json

st.set_page_config(
    page_title="Washington State Wildfire Risk Intelligence Platform - Interactive Map",
    page_icon="🗺️",
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

@st.cache_data
def create_geojson():
    """Create simplified GeoJSON for Washington counties"""
    # This is a placeholder - in production you'd load actual county boundaries
    # For now, we'll work with point data
    return None

df = load_data()
fema_data = load_fema_data()

# Header
st.title("🗺️ Interactive Wildfire Risk Map")
st.markdown("Multi-layer visualization with real-time filtering and analysis")
st.markdown("---")

# Sidebar controls
with st.sidebar:
    st.header("🎛️ Map Controls")
    
    st.subheader("Base Layer")
    base_layer = st.selectbox(
        "Map Style",
        ["OpenStreetMap", "Satellite", "Terrain", "Dark"],
        help="Choose base map visualization"
    )
    
    st.markdown("---")
    st.subheader("Risk Filters")
    
    # Risk category filter
    risk_categories = ['All'] + sorted(df['risk_category'].unique().tolist())
    selected_risk = st.multiselect(
        "Risk Categories",
        risk_categories[1:],
        default=risk_categories[1:],
        help="Filter by risk level"
    )
    
    # Climate trend filter
    climate_trends = sorted(df['climate_trend'].unique().tolist())
    selected_trends = st.multiselect(
        "Climate Trends",
        climate_trends,
        default=climate_trends,
        help="Filter by climate pattern"
    )
    
    # Risk score slider
    min_score, max_score = st.slider(
        "Risk Score Range",
        min_value=float(df['climate_fire_risk_score'].min()),
        max_value=float(df['climate_fire_risk_score'].max()),
        value=(float(df['climate_fire_risk_score'].min()), float(df['climate_fire_risk_score'].max())),
        help="Filter by composite risk score"
    )
    
    # Population threshold
    min_population = st.slider(
        "Minimum County Population",
        min_value=0,
        max_value=int(df['population'].max()),
        value=0,
        step=10000,
        help="Filter out low-population counties"
    )
    
    st.markdown("---")
    st.subheader("Data Overlays")
    
    show_fema = st.checkbox("FEMA Disasters", value=True, help="Show federal disaster declarations")
    show_county_labels = st.checkbox("County Labels", value=True, help="Display county names")
    show_heatmap = st.checkbox("Risk Heatmap", value=False, help="Show risk intensity heatmap")
    
    if show_fema and fema_data is not None:
        st.markdown("**FEMA Filter**")
        fema_year_range = st.slider(
            "Year Range",
            min_value=int(fema_data['declarationDate'].dt.year.min()),
            max_value=int(fema_data['declarationDate'].dt.year.max()),
            value=(2015, int(fema_data['declarationDate'].dt.year.max()))
        )
    
    st.markdown("---")
    st.subheader("Advanced Options")
    
    cluster_markers = st.checkbox("Cluster Markers", value=True, help="Group nearby markers")
    show_legend = st.checkbox("Show Legend", value=True, help="Display map legend")

# Apply filters
filtered_df = df.copy()
if selected_risk:
    filtered_df = filtered_df[filtered_df['risk_category'].isin(selected_risk)]
if selected_trends:
    filtered_df = filtered_df[filtered_df['climate_trend'].isin(selected_trends)]
filtered_df = filtered_df[
    (filtered_df['climate_fire_risk_score'] >= min_score) &
    (filtered_df['climate_fire_risk_score'] <= max_score) &
    (filtered_df['population'] >= min_population)
]

# Display filter results
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Counties Shown", f"{len(filtered_df)}/{len(df)}")
with col2:
    st.metric("Avg Risk Score", f"{filtered_df['climate_fire_risk_score'].mean():.1f}")
with col3:
    st.metric("Total Pop. at Risk", f"{filtered_df['population_at_risk'].sum()/1000:.0f}K")
with col4:
    if show_fema and fema_data is not None:
        fema_filtered = fema_data[
            (fema_data['declarationDate'].dt.year >= fema_year_range[0]) &
            (fema_data['declarationDate'].dt.year <= fema_year_range[1])
        ]
        st.metric("FEMA Disasters", len(fema_filtered))
    else:
        st.metric("FEMA Disasters", "Disabled")

st.markdown("---")

# Create map
st.subheader("Washington State Wildfire Risk Analysis")

# Map tile options
tile_options = {
    "OpenStreetMap": "OpenStreetMap",
    "Satellite": "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
    "Terrain": "https://server.arcgisonline.com/ArcGIS/rest/services/World_Terrain_Base/MapServer/tile/{z}/{y}/{x}",
    "Dark": "CartoDB dark_matter"
}

m = folium.Map(
    location=[47.5, -120.5],
    zoom_start=7,
    tiles=tile_options.get(base_layer, "OpenStreetMap"),
    attr='WA FireWatch'
)

# Add heatmap layer if requested
if show_heatmap and len(filtered_df) > 0:
    # Create heatmap data - we'd need lat/lon for counties
    # For now, using a placeholder
    st.info("💡 Heatmap layer requires county centroid coordinates. Feature coming soon!")

# Add county markers with detailed popups
if cluster_markers:
    marker_cluster = plugins.MarkerCluster(name='County Risk Markers').add_to(m)
    marker_parent = marker_cluster
else:
    marker_parent = m

for _, row in filtered_df.iterrows():
    # Determine marker color and icon based on risk
    if row['risk_category'] == 'Critical':
        color = 'darkred'
        icon = 'fire'
    elif row['risk_category'] == 'High':
        color = 'red'
        icon = 'warning-sign'
    elif row['risk_category'] == 'Moderate':
        color = 'orange'
        icon = 'exclamation-sign'
    else:
        color = 'green'
        icon = 'ok-sign'
    
    # Count FEMA disasters for this county
    if fema_data is not None:
        county_fema = fema_data[fema_data['County'] == row['County']]
        fema_count = len(county_fema)
        recent_fires = county_fema.nlargest(3, 'declarationDate')
        fires_list = '<br>'.join([
            f"• <b>{fire['declarationTitle']}</b> ({fire['declarationDate'].strftime('%Y-%m-%d')})"
            for _, fire in recent_fires.iterrows()
        ])
    else:
        fema_count = 0
        fires_list = "No data available"
    
    # Create detailed popup
    popup_html = f"""
    <div style="font-family: Arial, sans-serif; width: 350px; max-height: 400px; overflow-y: auto;">
        <div style="background: linear-gradient(135deg, {color} 0%, {color}dd 100%); 
                    color: white; padding: 15px; margin: -10px -10px 10px -10px; border-radius: 5px 5px 0 0;">
            <h3 style="margin: 0; font-size: 1.3rem;">{row['County']} County</h3>
            <div style="font-size: 0.9rem; margin-top: 5px;">Risk Score: {row['climate_fire_risk_score']:.1f} | {row['risk_category']}</div>
        </div>
        
        <div style="padding: 5px;">
            <h4 style="color: #1976d2; margin: 10px 0 5px 0; border-bottom: 2px solid #1976d2;">
                📊 Risk Assessment
            </h4>
            <table style="width: 100%; font-size: 0.9rem;">
                <tr><td><b>Climate Trend:</b></td><td>{row['climate_trend']}</td></tr>
                <tr><td><b>Heat Stress:</b></td><td>{row['heat_stress']:.1f}</td></tr>
                <tr><td><b>Drought Stress:</b></td><td>{row['drought_stress']:.1f}</td></tr>
                <tr><td><b>Fire History Score:</b></td><td>{row['fire_history_score']:.1f}</td></tr>
                <tr><td><b>WUI Exposure:</b></td><td>{row['wui_exposure_pct']:.1f}%</td></tr>
            </table>
            
            <h4 style="color: #d32f2f; margin: 15px 0 5px 0; border-bottom: 2px solid #d32f2f;">
                👥 Population Impact
            </h4>
            <table style="width: 100%; font-size: 0.9rem;">
                <tr><td><b>Total Population:</b></td><td>{row['population']:,}</td></tr>
                <tr><td><b>At Risk (WUI):</b></td><td>{row['population_at_risk']:,.0f}</td></tr>
                <tr><td><b>% Interface:</b></td><td>{row['pct_interface']*100:.1f}%</td></tr>
                <tr><td><b>% Intermix:</b></td><td>{row['pct_intermix']*100:.1f}%</td></tr>
            </table>
            
            <h4 style="color: #f57c00; margin: 15px 0 5px 0; border-bottom: 2px solid #f57c00;">
                🔥 Disaster History
            </h4>
            <div style="font-size: 0.9rem;">
                <b>FEMA Declarations:</b> {fema_count}<br>
                <b>NOAA Fire Events:</b> {row['Fire_Count']}<br>
                <br>
                <b>Recent Major Fires:</b><br>
                {fires_list if fires_list != "No data available" else "<i>No recent disasters</i>"}
            </div>
        </div>
    </div>
    """
    
    # We need actual lat/lon - using approximate Washington center for demo
    # In production, you'd have county centroids
    lat = 47.5 + (hash(row['County']) % 1000) / 10000  # Placeholder
    lon = -120.5 + (hash(row['County']) % 2000) / 10000  # Placeholder
    
    folium.Marker(
        location=[lat, lon],
        popup=folium.Popup(popup_html, max_width=400),
        tooltip=f"{row['County']}: {row['climate_fire_risk_score']:.1f} ({row['risk_category']})",
        icon=folium.Icon(color=color, icon=icon, prefix='glyphicon')
    ).add_to(marker_parent)
    
    # Add county label if requested
    if show_county_labels:
        folium.Marker(
            location=[lat, lon],
            icon=folium.DivIcon(html=f"""
                <div style="font-size: 10px; font-weight: bold; color: #333; 
                            text-shadow: 1px 1px 2px white, -1px -1px 2px white;
                            white-space: nowrap;">
                    {row['County']}
                </div>
            """)
        ).add_to(m)

# Add FEMA disaster markers
if show_fema and fema_data is not None:
    fema_filtered = fema_data[
        (fema_data['declarationDate'].dt.year >= fema_year_range[0]) &
        (fema_data['declarationDate'].dt.year <= fema_year_range[1])
    ].dropna(subset=['lat', 'lon'])
    
    if cluster_markers:
        fema_cluster = plugins.MarkerCluster(name='FEMA Disasters', 
                                            overlay=True,
                                            control=True).add_to(m)
        fema_parent = fema_cluster
    else:
        fema_parent = m
    
    for _, row in fema_filtered.iterrows():
        popup_html = f"""
        <div style="font-family: Arial; width: 280px;">
            <div style="background: #c62828; color: white; padding: 10px; margin: -10px -10px 10px -10px;">
                <h4 style="margin: 0;">🏛️ FEMA Disaster</h4>
            </div>
            <b>{row['declarationTitle']}</b><br>
            <b>County:</b> {row['County']}<br>
            <b>Date:</b> {row['declarationDate'].strftime('%B %d, %Y')}<br>
            <b>Disaster #:</b> {row['disasterNumber']}<br>
            <hr style="margin: 8px 0;">
            <small><i>Federal assistance declaration</i></small>
        </div>
        """
        
        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=6,
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=f"{row['declarationTitle']} - {row['declarationDate'].strftime('%Y')}",
            color='#c62828',
            fill=True,
            fillColor='#ff5252',
            fillOpacity=0.7,
            weight=2
        ).add_to(fema_parent)

# Add legend if requested
if show_legend:
    legend_html = '''
    <div style="position: fixed; 
                bottom: 50px; right: 50px; width: 200px; 
                background-color: white; border:2px solid grey; z-index:9999; 
                font-size:12px; padding: 10px; border-radius: 5px;
                box-shadow: 0 0 15px rgba(0,0,0,0.2);">
        <h4 style="margin: 0 0 10px 0;">Risk Categories</h4>
        <p style="margin: 5px 0;"><span style="color: darkred;">⬤</span> Critical (>65)</p>
        <p style="margin: 5px 0;"><span style="color: red;">⬤</span> High (55-65)</p>
        <p style="margin: 5px 0;"><span style="color: orange;">⬤</span> Moderate (45-55)</p>
        <p style="margin: 5px 0;"><span style="color: green;">⬤</span> Low (<45)</p>
        <hr style="margin: 8px 0;">
        <p style="margin: 5px 0;"><span style="color: #c62828;">●</span> FEMA Disaster</p>
    </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))

# Add layer control
folium.LayerControl(position='topright').add_to(m)

# Display map
st_folium(m, width=1400, height=700, returned_objects=[])

st.markdown("---")

# Map insights
col1, col2 = st.columns(2)

with col1:
    st.subheader("📍 Geographic Insights")
    
    # Eastern vs Western Washington
    eastern_counties = ['SPOKANE', 'YAKIMA', 'BENTON', 'FRANKLIN', 'WALLA WALLA', 'GRANT', 'CHELAN', 'DOUGLAS', 'OKANOGAN']
    eastern = df[df['County'].isin(eastern_counties)]
    western = df[~df['County'].isin(eastern_counties)]
    
    st.markdown(f"""
    **Eastern Washington:**
    - Average Risk Score: {eastern['climate_fire_risk_score'].mean():.1f}
    - High/Critical Counties: {len(eastern[eastern['risk_category'].isin(['High', 'Critical'])])}
    - Warming & Drying Trend: {len(eastern[eastern['climate_trend'] == 'Warming & Drying'])} counties
    
    **Western Washington:**
    - Average Risk Score: {western['climate_fire_risk_score'].mean():.1f}
    - High/Critical Counties: {len(western[western['risk_category'].isin(['High', 'Critical'])])}
    - Warming & Drying Trend: {len(western[western['climate_trend'] == 'Warming & Drying'])} counties
    """)

with col2:
    st.subheader("🎯 Filtered View Analysis")
    
    if len(filtered_df) > 0:
        st.markdown(f"""
        **Current Selection:**
        - Counties: {len(filtered_df)}
        - Total Population: {filtered_df['population'].sum():,}
        - People at Risk: {filtered_df['population_at_risk'].sum():,.0f}
        - Avg WUI Exposure: {filtered_df['wui_exposure_pct'].mean():.1f}%
        - Highest Risk: {filtered_df.nlargest(1, 'climate_fire_risk_score')['County'].values[0]} ({filtered_df['climate_fire_risk_score'].max():.1f})
        """)
    else:
        st.warning("⚠️ No counties match current filter criteria")

st.markdown("---")

# Export options
st.subheader("💾 Export Current View")

col1, col2, col3 = st.columns(3)

with col1:
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="📥 Download Data (CSV)",
        data=csv,
        file_name=f"wa_firewatch_filtered_{pd.Timestamp.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

with col2:
    st.button("📊 Generate Report", help="Create a detailed PDF report (coming soon)")

with col3:
    st.button("📧 Email Summary", help="Send filtered data via email (coming soon)")
