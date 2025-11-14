"""
Utility Functions for WA FireWatch Platform
Shared functions used across multiple pages
"""

import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

def format_population(pop):
    """Format population numbers for display"""
    if pop >= 1000000:
        return f"{pop/1000000:.2f}M"
    elif pop >= 1000:
        return f"{pop/1000:.1f}K"
    else:
        return f"{pop:.0f}"

def get_risk_color(risk_category):
    """Return color code for risk category"""
    color_map = {
        'Critical': '#8B0000',
        'High': '#FF4500',
        'Moderate': '#FFA500',
        'Low': '#90EE90'
    }
    return color_map.get(risk_category, '#CCCCCC')

def get_trend_color(climate_trend):
    """Return color code for climate trend"""
    color_map = {
        'Warming & Drying': '#d32f2f',
        'Warming': '#f57c00',
        'Stable': '#7cb342',
        'Cooling': '#1976d2'
    }
    return color_map.get(climate_trend, '#CCCCCC')

def calculate_risk_category(score):
    """Determine risk category from score"""
    if score >= 65:
        return 'Critical'
    elif score >= 55:
        return 'High'
    elif score >= 45:
        return 'Moderate'
    else:
        return 'Low'

def create_gauge_chart(value, title, max_value=100, color='#d32f2f'):
    """Create a gauge chart for risk visualization"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title},
        gauge={
            'axis': {'range': [None, max_value]},
            'bar': {'color': color},
            'steps': [
                {'range': [0, max_value * 0.45], 'color': "lightgray"},
                {'range': [max_value * 0.45, max_value * 0.55], 'color': "lightyellow"},
                {'range': [max_value * 0.55, max_value * 0.65], 'color': "lightcoral"},
                {'range': [max_value * 0.65, max_value], 'color': "lightpink"}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': value
            }
        }
    ))
    
    fig.update_layout(height=250, margin=dict(l=20, r=20, t=50, b=20))
    return fig

def filter_by_date_range(df, date_column, start_date, end_date):
    """Filter dataframe by date range"""
    mask = (df[date_column] >= start_date) & (df[date_column] <= end_date)
    return df[mask]

def export_to_csv(df, filename_prefix):
    """Prepare dataframe for CSV export with timestamp"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{filename_prefix}_{timestamp}.csv"
    return df.to_csv(index=False), filename

def calculate_percentile_rank(value, series):
    """Calculate percentile rank of a value within a series"""
    return (series < value).sum() / len(series) * 100

def get_eastern_western_counties():
    """Return lists of counties by region"""
    eastern_counties = [
        'SPOKANE', 'YAKIMA', 'BENTON', 'FRANKLIN', 'WALLA WALLA',
        'GRANT', 'CHELAN', 'DOUGLAS', 'OKANOGAN', 'ADAMS', 'WHITMAN',
        'KITTITAS', 'KLICKITAT', 'COLUMBIA', 'GARFIELD', 'ASOTIN',
        'FERRY', 'STEVENS', 'PEND OREILLE', 'LINCOLN'
    ]
    
    return eastern_counties

def format_date_for_display(date_obj):
    """Format datetime for display"""
    if pd.isna(date_obj):
        return "N/A"
    return date_obj.strftime('%B %d, %Y')

def create_risk_summary_dict(df):
    """Create summary statistics dictionary"""
    return {
        'total_counties': len(df),
        'critical_counties': len(df[df['risk_category'] == 'Critical']),
        'high_counties': len(df[df['risk_category'] == 'High']),
        'avg_risk_score': df['climate_fire_risk_score'].mean(),
        'total_population': df['population'].sum(),
        'population_at_risk': df['population_at_risk'].sum(),
        'warming_counties': len(df[df['climate_trend'].str.contains('Warming', na=False)])
    }

# Custom CSS styling
def get_custom_css():
    """Return custom CSS for consistent styling"""
    return """
    <style>
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #d32f2f;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin: 10px 0;
    }
    
    .info-box {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #1976d2;
        margin: 15px 0;
    }
    
    .warning-box {
        background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #f57c00;
        margin: 15px 0;
    }
    
    .critical-box {
        background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #c62828;
        margin: 15px 0;
    }
    
    .success-box {
        background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #388e3c;
        margin: 15px 0;
    }
    
    h1, h2, h3 {
        color: #1a237e;
        font-weight: 600;
    }
    
    .stMetric {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #d32f2f;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    </style>
    """

# Color schemes for consistent visualization
RISK_COLORS = {
    'Critical': '#8B0000',
    'High': '#FF4500',
    'Moderate': '#FFA500',
    'Low': '#90EE90'
}

TREND_COLORS = {
    'Warming & Drying': '#d32f2f',
    'Warming': '#f57c00',
    'Stable': '#7cb342',
    'Cooling': '#1976d2'
}

BRAND_COLORS = {
    'primary': '#d32f2f',
    'secondary': '#1976d2',
    'success': '#388e3c',
    'warning': '#f57c00',
    'info': '#0288d1'
}
