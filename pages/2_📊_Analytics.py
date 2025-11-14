"""
Deep Analytics Page
Advanced statistical analysis, correlations, and predictive insights
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from scipy import stats
from datetime import datetime, timedelta

st.set_page_config(
    page_title="WA FireWatch - Analytics",
    page_icon="📊",
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
        fema['year'] = fema['declarationDate'].dt.year
        return fema
    except FileNotFoundError:
        return None

df = load_data()
fema_data = load_fema_data()

# Header
st.title("📊 Deep Analytics & Insights")
st.markdown("Advanced statistical analysis and predictive modeling")
st.markdown("---")

# Sidebar - Analysis Options
with st.sidebar:
    st.header("🔬 Analysis Options")
    
    analysis_type = st.selectbox(
        "Primary Analysis",
        [
            "Correlation Analysis",
            "Time Series Trends",
            "Risk Factor Decomposition",
            "Predictive Modeling",
            "Comparative Analysis",
            "Statistical Summary"
        ]
    )
    
    st.markdown("---")
    
    st.subheader("Variables")
    
    available_vars = [
        'climate_fire_risk_score',
        'heat_stress',
        'drought_stress',
        'fire_history_score',
        'wui_exposure_score',
        'population',
        'population_at_risk',
        'Fire_Count',
        'wui_exposure_pct',
        'mean_pop_density',
        'avg_housing_density'
    ]
    
    primary_var = st.selectbox("Primary Variable", available_vars, index=0)
    secondary_var = st.selectbox("Secondary Variable", available_vars, index=1)
    
    st.markdown("---")
    
    st.subheader("Filters")
    
    selected_counties = st.multiselect(
        "Focus Counties",
        sorted(df['County'].unique()),
        help="Leave empty for all counties"
    )
    
    risk_filter = st.multiselect(
        "Risk Categories",
        sorted(df['risk_category'].unique()),
        default=sorted(df['risk_category'].unique())
    )

# Apply filters
filtered_df = df.copy()
if selected_counties:
    filtered_df = filtered_df[filtered_df['County'].isin(selected_counties)]
if risk_filter:
    filtered_df = filtered_df[filtered_df['risk_category'].isin(risk_filter)]

# Main content based on analysis type
if analysis_type == "Correlation Analysis":
    st.header("🔗 Correlation Analysis")
    st.markdown("Exploring relationships between risk factors")
    
    # Correlation matrix
    st.subheader("Risk Factor Correlation Matrix")
    
    correlation_vars = [
        'climate_fire_risk_score', 'heat_stress', 'drought_stress',
        'fire_history_score', 'wui_exposure_score', 'population_at_risk',
        'Fire_Count', 'wui_exposure_pct'
    ]
    
    corr_matrix = filtered_df[correlation_vars].corr()
    
    fig_corr = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=[col.replace('_', ' ').title() for col in corr_matrix.columns],
        y=[col.replace('_', ' ').title() for col in corr_matrix.index],
        colorscale='RdBu',
        zmid=0,
        text=corr_matrix.values.round(2),
        texttemplate='%{text}',
        textfont={"size": 10},
        colorbar=dict(title="Correlation")
    ))
    
    fig_corr.update_layout(
        title="Risk Factor Correlations",
        height=600,
        xaxis_tickangle=-45
    )
    
    st.plotly_chart(fig_corr, use_container_width=True)
    
    # Scatter plot with trend line
    st.subheader(f"Relationship: {primary_var.replace('_', ' ').title()} vs {secondary_var.replace('_', ' ').title()}")
    
    # Calculate correlation
    correlation = filtered_df[primary_var].corr(filtered_df[secondary_var])
    
    fig_scatter = px.scatter(
        filtered_df,
        x=primary_var,
        y=secondary_var,
        color='risk_category',
        size='population',
        hover_data=['County', 'climate_trend'],
        trendline="ols",
        color_discrete_map={
            'Critical': '#8B0000',
            'High': '#FF4500',
            'Moderate': '#FFA500',
            'Low': '#90EE90'
        }
    )
    
    fig_scatter.update_layout(
        title=f"Correlation: {correlation:.3f}",
        height=500,
        xaxis_title=primary_var.replace('_', ' ').title(),
        yaxis_title=secondary_var.replace('_', ' ').title()
    )
    
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    # Key insights
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Correlation Coefficient", f"{correlation:.3f}")
    
    with col2:
        # R-squared
        slope, intercept, r_value, p_value, std_err = stats.linregress(
            filtered_df[primary_var].dropna(),
            filtered_df[secondary_var].dropna()
        )
        st.metric("R² Value", f"{r_value**2:.3f}")
    
    with col3:
        st.metric("P-value", f"{p_value:.4f}")

elif analysis_type == "Time Series Trends":
    st.header("📈 Time Series Analysis")
    st.markdown("Historical trends and future projections")
    
    if fema_data is not None:
        # Disaster frequency over time
        st.subheader("Federal Disaster Declarations Over Time")
        
        yearly_data = fema_data.groupby('year').agg({
            'disasterNumber': 'count',
            'County': lambda x: x.nunique()
        }).reset_index()
        yearly_data.columns = ['Year', 'Total Disasters', 'Unique Counties']
        
        # Create figure with secondary y-axis
        fig_timeline = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig_timeline.add_trace(
            go.Bar(
                x=yearly_data['Year'],
                y=yearly_data['Total Disasters'],
                name='Total Disasters',
                marker_color='#d32f2f'
            ),
            secondary_y=False
        )
        
        fig_timeline.add_trace(
            go.Scatter(
                x=yearly_data['Year'],
                y=yearly_data['Unique Counties'],
                name='Counties Affected',
                line=dict(color='#1976d2', width=3),
                mode='lines+markers'
            ),
            secondary_y=True
        )
        
        # Add trend lines
        if len(yearly_data) > 2:
            z = np.polyfit(yearly_data['Year'], yearly_data['Total Disasters'], 1)
            p = np.poly1d(z)
            
            fig_timeline.add_trace(
                go.Scatter(
                    x=yearly_data['Year'],
                    y=p(yearly_data['Year']),
                    name='Disaster Trend',
                    line=dict(color='#d32f2f', width=2, dash='dash'),
                    showlegend=True
                ),
                secondary_y=False
            )
        
        fig_timeline.update_xaxes(title_text="Year")
        fig_timeline.update_yaxes(title_text="Number of Disasters", secondary_y=False)
        fig_timeline.update_yaxes(title_text="Counties Affected", secondary_y=True)
        
        fig_timeline.update_layout(
            title="Historical Fire Disaster Trends",
            height=500,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig_timeline, use_container_width=True)
        
        # Projections
        st.subheader("🔮 5-Year Forecast")
        
        if len(yearly_data) >= 5:
            # Simple linear regression for projection
            recent_years = yearly_data.tail(10)
            z = np.polyfit(recent_years['Year'], recent_years['Total Disasters'], 1)
            p = np.poly1d(z)
            
            future_years = range(yearly_data['Year'].max() + 1, yearly_data['Year'].max() + 6)
            projected_disasters = [p(year) for year in future_years]
            
            projection_df = pd.DataFrame({
                'Year': list(future_years),
                'Projected Disasters': projected_disasters
            })
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.dataframe(
                    projection_df.style.format({'Projected Disasters': '{:.0f}'}),
                    use_container_width=True,
                    hide_index=True
                )
            
            with col2:
                avg_increase = (projected_disasters[-1] - yearly_data['Total Disasters'].iloc[-1]) / 5
                st.metric(
                    "Avg. Annual Increase",
                    f"{avg_increase:.1f} disasters/year",
                    delta=f"{(avg_increase / yearly_data['Total Disasters'].iloc[-1] * 100):.1f}%"
                )
                
                total_projected = sum(projected_disasters)
                st.metric(
                    "5-Year Total (Projected)",
                    f"{total_projected:.0f} disasters"
                )
        
        # Seasonal patterns
        st.subheader("📅 Seasonal Patterns")
        
        fema_data['month'] = fema_data['declarationDate'].dt.month
        monthly_disasters = fema_data.groupby('month').size().reset_index(name='count')
        
        month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                      'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        monthly_disasters['month_name'] = monthly_disasters['month'].apply(lambda x: month_names[x-1])
        
        fig_seasonal = px.bar(
            monthly_disasters,
            x='month_name',
            y='count',
            title='Fire Disaster Declarations by Month (1991-2024)',
            labels={'count': 'Number of Disasters', 'month_name': 'Month'},
            color='count',
            color_continuous_scale='Reds'
        )
        
        fig_seasonal.update_layout(height=400)
        st.plotly_chart(fig_seasonal, use_container_width=True)
        
        peak_month = monthly_disasters.nlargest(1, 'count')['month_name'].values[0]
        st.info(f"🔥 **Peak Fire Season:** {peak_month} with {monthly_disasters.nlargest(1, 'count')['count'].values[0]} historical declarations")

elif analysis_type == "Risk Factor Decomposition":
    st.header("🧩 Risk Factor Decomposition")
    st.markdown("Breaking down composite risk scores into components")
    
    # Component contribution
    st.subheader("Risk Score Components")
    
    components = ['heat_stress', 'drought_stress', 'fire_history_score', 'wui_exposure_score']
    component_weights = [0.25, 0.25, 0.25, 0.25]  # Adjust based on your actual calculation
    
    # Average contributions
    avg_contributions = []
    for comp in components:
        avg_contributions.append(filtered_df[comp].mean())
    
    fig_components = go.Figure(data=[
        go.Bar(
            x=[comp.replace('_', ' ').title() for comp in components],
            y=avg_contributions,
            marker_color=['#ff6b6b', '#ee5a6f', '#c44569', '#6c5ce7'],
            text=[f"{val:.1f}" for val in avg_contributions],
            textposition='auto'
        )
    ])
    
    fig_components.update_layout(
        title="Average Component Scores Across Selected Counties",
        yaxis_title="Score",
        height=400
    )
    
    st.plotly_chart(fig_components, use_container_width=True)
    
    # Component distribution by risk category
    st.subheader("Component Scores by Risk Category")
    
    fig_box = go.Figure()
    
    for comp in components:
        for category in sorted(filtered_df['risk_category'].unique()):
            category_data = filtered_df[filtered_df['risk_category'] == category][comp]
            
            fig_box.add_trace(go.Box(
                y=category_data,
                name=f"{category} - {comp.replace('_', ' ').title()}",
                boxmean='sd'
            ))
    
    fig_box.update_layout(
        title="Risk Component Distributions",
        yaxis_title="Score",
        height=500,
        showlegend=True
    )
    
    st.plotly_chart(fig_box, use_container_width=True)
    
    # County-specific breakdown
    st.subheader("County-Level Component Analysis")
    
    selected_county = st.selectbox(
        "Select County for Detailed Analysis",
        sorted(filtered_df['County'].unique())
    )
    
    county_data = filtered_df[filtered_df['County'] == selected_county].iloc[0]
    
    county_components = [county_data[comp] for comp in components]
    
    fig_radar = go.Figure(data=go.Scatterpolar(
        r=county_components,
        theta=[comp.replace('_', ' ').title() for comp in components],
        fill='toself',
        name=selected_county
    ))
    
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max(county_components) * 1.2]
            )
        ),
        title=f"{selected_county} County Risk Profile",
        height=500
    )
    
    st.plotly_chart(fig_radar, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Component Scores:**")
        for comp, val in zip(components, county_components):
            st.metric(comp.replace('_', ' ').title(), f"{val:.2f}")
    
    with col2:
        st.markdown("**County Statistics:**")
        st.metric("Overall Risk Score", f"{county_data['climate_fire_risk_score']:.1f}")
        st.metric("Risk Category", county_data['risk_category'])
        st.metric("Climate Trend", county_data['climate_trend'])

elif analysis_type == "Predictive Modeling":
    st.header("🔮 Predictive Risk Modeling")
    st.markdown("Scenario analysis and future risk projections")
    
    st.subheader("Climate Change Scenario Modeling")
    
    # User inputs for scenarios
    col1, col2 = st.columns(2)
    
    with col1:
        temp_increase = st.slider(
            "Temperature Increase (°C)",
            min_value=0.0,
            max_value=5.0,
            value=2.0,
            step=0.5,
            help="Projected temperature increase over next 25 years"
        )
    
    with col2:
        precip_change = st.slider(
            "Precipitation Change (%)",
            min_value=-50,
            max_value=50,
            value=-10,
            step=5,
            help="Projected change in annual precipitation"
        )
    
    # Calculate adjusted risk scores
    # Simplified model - in production you'd use more sophisticated climate models
    temp_factor = 1 + (temp_increase * 0.15)  # 15% increase per degree
    precip_factor = 1 - (precip_change / 100 * 0.1)  # 10% of precip change affects risk
    
    filtered_df['projected_heat_stress'] = filtered_df['heat_stress'] * temp_factor
    filtered_df['projected_drought_stress'] = filtered_df['drought_stress'] * precip_factor
    filtered_df['projected_risk_score'] = (
        filtered_df['projected_heat_stress'] * 0.25 +
        filtered_df['projected_drought_stress'] * 0.25 +
        filtered_df['fire_history_score'] * 0.25 +
        filtered_df['wui_exposure_score'] * 0.25
    )
    
    # Show changes
    st.subheader("Projected Risk Changes")
    
    risk_changes = filtered_df[['County', 'climate_fire_risk_score', 'projected_risk_score', 'risk_category']].copy()
    risk_changes['risk_change'] = risk_changes['projected_risk_score'] - risk_changes['climate_fire_risk_score']
    risk_changes['pct_change'] = (risk_changes['risk_change'] / risk_changes['climate_fire_risk_score'] * 100)
    
    # Sort by largest increase
    risk_changes = risk_changes.sort_values('risk_change', ascending=False)
    
    fig_changes = go.Figure()
    
    fig_changes.add_trace(go.Bar(
        x=risk_changes['County'][:15],
        y=risk_changes['climate_fire_risk_score'][:15],
        name='Current Risk',
        marker_color='#1976d2'
    ))
    
    fig_changes.add_trace(go.Bar(
        x=risk_changes['County'][:15],
        y=risk_changes['projected_risk_score'][:15],
        name='Projected Risk',
        marker_color='#d32f2f'
    ))
    
    fig_changes.update_layout(
        title="Top 15 Counties: Current vs Projected Risk",
        xaxis_title="County",
        yaxis_title="Risk Score",
        height=500,
        barmode='group',
        xaxis_tickangle=-45
    )
    
    st.plotly_chart(fig_changes, use_container_width=True)
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_increase = risk_changes['risk_change'].mean()
        st.metric("Avg Risk Increase", f"+{avg_increase:.1f}")
    
    with col2:
        counties_upgraded = len(risk_changes[risk_changes['risk_change'] > 5])
        st.metric("Counties w/ Major Increase", counties_upgraded)
    
    with col3:
        max_increase = risk_changes['risk_change'].max()
        st.metric("Maximum Increase", f"+{max_increase:.1f}")
    
    with col4:
        most_affected = risk_changes.nlargest(1, 'risk_change')['County'].values[0]
        st.metric("Most Affected County", most_affected)
    
    # Display table
    st.subheader("Detailed Projections")
    
    display_changes = risk_changes[['County', 'climate_fire_risk_score', 'projected_risk_score', 'risk_change', 'pct_change']].copy()
    display_changes.columns = ['County', 'Current Risk', 'Projected Risk', 'Change', '% Change']
    display_changes = display_changes.round(2)
    
    st.dataframe(display_changes, use_container_width=True, hide_index=True, height=400)

elif analysis_type == "Comparative Analysis":
    st.header("⚖️ Comparative County Analysis")
    st.markdown("Side-by-side comparison of risk factors")
    
    # County selection
    st.subheader("Select Counties to Compare")
    
    compare_counties = st.multiselect(
        "Choose 2-5 counties",
        sorted(df['County'].unique()),
        default=df.nlargest(3, 'climate_fire_risk_score')['County'].tolist()[:3]
    )
    
    if len(compare_counties) >= 2:
        compare_df = df[df['County'].isin(compare_counties)]
        
        # Radar chart comparison
        st.subheader("Risk Profile Comparison")
        
        components = ['heat_stress', 'drought_stress', 'fire_history_score', 'wui_exposure_score']
        
        fig_compare = go.Figure()
        
        colors = ['#d32f2f', '#1976d2', '#f57c00', '#7cb342', '#9c27b0']
        
        for idx, county in enumerate(compare_counties):
            county_data = compare_df[compare_df['County'] == county].iloc[0]
            values = [county_data[comp] for comp in components]
            
            fig_compare.add_trace(go.Scatterpolar(
                r=values,
                theta=[comp.replace('_', ' ').title() for comp in components],
                fill='toself',
                name=county,
                line_color=colors[idx % len(colors)]
            ))
        
        fig_compare.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 30])
            ),
            showlegend=True,
            height=500,
            title="Multi-County Risk Factor Comparison"
        )
        
        st.plotly_chart(fig_compare, use_container_width=True)
        
        # Side-by-side metrics
        st.subheader("Key Metrics Comparison")
        
        metrics_to_compare = [
            ('climate_fire_risk_score', 'Overall Risk Score'),
            ('population_at_risk', 'Population at Risk'),
            ('Fire_Count', 'Historical Fires'),
            ('wui_exposure_pct', 'WUI Exposure %')
        ]
        
        cols = st.columns(len(compare_counties))
        
        for idx, county in enumerate(compare_counties):
            with cols[idx]:
                st.markdown(f"### {county}")
                county_data = compare_df[compare_df['County'] == county].iloc[0]
                
                for metric, label in metrics_to_compare:
                    value = county_data[metric]
                    if metric == 'population_at_risk':
                        st.metric(label, f"{value:,.0f}")
                    elif metric == 'wui_exposure_pct':
                        st.metric(label, f"{value:.1f}%")
                    else:
                        st.metric(label, f"{value:.1f}")
                
                st.markdown(f"**Category:** {county_data['risk_category']}")
                st.markdown(f"**Climate:** {county_data['climate_trend']}")
        
        # Comparison table
        st.subheader("Detailed Comparison Table")
        
        comparison_vars = [
            'County', 'climate_fire_risk_score', 'risk_category', 'climate_trend',
            'population', 'population_at_risk', 'Fire_Count', 'heat_stress',
            'drought_stress', 'wui_exposure_pct'
        ]
        
        comparison_table = compare_df[comparison_vars].copy()
        comparison_table = comparison_table.round(2)
        
        st.dataframe(comparison_table, use_container_width=True, hide_index=True)
    
    else:
        st.warning("⚠️ Please select at least 2 counties to compare")

else:  # Statistical Summary
    st.header("📊 Statistical Summary")
    st.markdown("Comprehensive statistical overview of risk factors")
    
    st.subheader("Distribution Statistics")
    
    # Summary statistics
    summary_stats = filtered_df[['climate_fire_risk_score', 'heat_stress', 'drought_stress', 
                                 'fire_history_score', 'wui_exposure_score', 'population_at_risk']].describe()
    
    st.dataframe(summary_stats.T.style.format("{:.2f}"), use_container_width=True)
    
    # Histograms
    st.subheader("Risk Score Distribution")
    
    fig_hist = px.histogram(
        filtered_df,
        x='climate_fire_risk_score',
        nbins=30,
        color='risk_category',
        color_discrete_map={
            'Critical': '#8B0000',
            'High': '#FF4500',
            'Moderate': '#FFA500',
            'Low': '#90EE90'
        }
    )
    
    fig_hist.update_layout(
        title="Climate-Fire Risk Score Distribution",
        xaxis_title="Risk Score",
        yaxis_title="Frequency",
        height=400
    )
    
    st.plotly_chart(fig_hist, use_container_width=True)
    
    # Box plots for all components
    st.subheader("Component Score Distributions")
    
    components = ['heat_stress', 'drought_stress', 'fire_history_score', 'wui_exposure_score']
    
    fig_boxes = go.Figure()
    
    for comp in components:
        fig_boxes.add_trace(go.Box(
            y=filtered_df[comp],
            name=comp.replace('_', ' ').title(),
            boxmean='sd'
        ))
    
    fig_boxes.update_layout(
        title="Risk Component Statistical Distribution",
        yaxis_title="Score",
        height=500
    )
    
    st.plotly_chart(fig_boxes, use_container_width=True)
    
    # Statistical tests
    st.subheader("Statistical Significance Tests")
    
    # ANOVA for risk categories
    categories = filtered_df['risk_category'].unique()
    if len(categories) > 1:
        groups = [filtered_df[filtered_df['risk_category'] == cat]['climate_fire_risk_score'].values 
                 for cat in categories]
        f_stat, p_value = stats.f_oneway(*groups)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("F-Statistic (ANOVA)", f"{f_stat:.2f}")
        with col2:
            st.metric("P-Value", f"{p_value:.4f}")
        
        if p_value < 0.05:
            st.success("✅ Risk categories are statistically significantly different (p < 0.05)")
        else:
            st.info("ℹ️ No significant difference between risk categories detected")

st.markdown("---")

# Export analytics
st.subheader("💾 Export Analysis Results")

col1, col2, col3 = st.columns(3)

with col1:
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="📥 Download Filtered Data",
        data=csv,
        file_name=f"wa_firewatch_analytics_{pd.Timestamp.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

with col2:
    st.button("📊 Generate Analytics Report", help="Create detailed PDF report (coming soon)")

with col3:
    st.button("📧 Email Analysis", help="Send analysis via email (coming soon)")
