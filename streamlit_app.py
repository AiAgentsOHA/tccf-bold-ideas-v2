"""
TCCF Bold Ideas - Science Innovation Dashboard
Streamlit wrapper for interactive applicant evaluation viewer

Run with: streamlit run streamlit_dashboard.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# Page config
st.set_page_config(
    page_title="TCCF Bold Ideas | Science Innovation Dashboard",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for ocean theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');
    
    :root {
        --ocean-deep: #0a1628;
        --ocean-mid: #0f2847;
        --eco-green: #00d4aa;
        --coral: #ff6b4a;
    }
    
    .stApp {
        background: linear-gradient(180deg, #0a1628 0%, #0f2847 100%);
    }
    
    .main .block-container {
        padding-top: 2rem;
        max-width: 1400px;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'DM Sans', sans-serif !important;
        color: #ffffff !important;
    }
    
    p, span, div {
        font-family: 'DM Sans', sans-serif !important;
    }
    
    .stMetric {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1rem;
    }
    
    .stMetric label {
        color: #8ba3c7 !important;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        color: #00d4aa !important;
        font-weight: 700;
    }
    
    .stDataFrame {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
    }
    
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: white;
    }
    
    .stMultiSelect > div > div {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    div[data-testid="stExpander"] {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
    }
    
    .highlight-card {
        background: linear-gradient(135deg, rgba(0, 212, 170, 0.2), rgba(255, 107, 74, 0.1));
        border: 1px solid rgba(0, 212, 170, 0.3);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .science-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 100px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    
    .badge-strong { background: #00d4aa; color: #0a1628; }
    .badge-good { background: #4fffdb; color: #0a1628; }
    .badge-some { background: #fbbf24; color: #0a1628; }
    .badge-low { background: #f87171; color: white; }
    
    .sidebar .stImage {
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    """Load evaluation data from CSV."""
    try:
        df = pd.read_csv('/mnt/user-data/outputs/TCCF_Bold_Ideas_FINAL.csv')
        return df
    except FileNotFoundError:
        st.error("Data file not found. Please run the evaluation script first.")
        return None


def get_recommendation_color(rec):
    """Get color for recommendation badge."""
    colors = {
        '★ STRONGLY RECOMMEND': '#00d4aa',
        '★ RECOMMEND': '#4fffdb',
        'SHORTLIST': '#7dd3fc',
        'CONSIDER': '#fbbf24',
        'MAYBE - Limited science': '#fb923c',
        'LOW PRIORITY': '#f87171',
        'NOT RECOMMENDED': '#ef4444'
    }
    for key, color in colors.items():
        if key in str(rec):
            return color
    return '#94a3b8'


def get_science_emoji(level):
    """Get emoji indicator for science level."""
    if '★★★' in str(level):
        return '🔬'
    elif '★★☆' in str(level):
        return '⚗️'
    elif '★☆☆' in str(level):
        return '🔧'
    elif '☆☆☆' in str(level):
        return '📦'
    return '❓'


def main():
    # Sidebar with logos and filters
    with st.sidebar:
        # Logos
        col1, col2 = st.columns(2)
        with col1:
            st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/ce/Coca-Cola_logo.svg/512px-Coca-Cola_logo.svg.png", width=100)
        with col2:
            st.image("https://images.squarespace-cdn.com/content/v1/5e4f59b94c9f0c23ad33a098/1603788289325-8KXVK1YXVG2PPQR3JZLD/OHA+Logo.png", width=100)
        
        st.markdown("---")
        st.markdown("### 🎯 Filters")
        
        # Load data
        df = load_data()
        if df is None:
            return
        
        # Recommendation filter
        recommendations = ['All'] + sorted(df['RECOMMENDATION'].unique().tolist())
        selected_rec = st.selectbox("Recommendation", recommendations)
        
        # Science level filter
        science_levels = ['All'] + sorted(df['SCIENCE_LEVEL'].unique().tolist())
        selected_science = st.selectbox("Science Level", science_levels)
        
        # Stage filter
        stages = ['All'] + sorted(df['Stage'].dropna().unique().tolist())
        selected_stage = st.selectbox("Stage", stages)
        
        # Search
        search = st.text_input("🔍 Search ventures", "")
        
        # Science only toggle
        science_only = st.checkbox("🔬 Strong science only (★★★ or ★★☆)")
        
        st.markdown("---")
        st.markdown("### 📊 Quick Stats")
        
        # Quick stats
        st.metric("Total Applicants", len(df))
        st.metric("Science Innovations", len(df[df['SCIENCE_LEVEL'].str.contains('★★', na=False)]))
        st.metric("Top Recommendations", len(df[df['RECOMMENDATION'].str.contains('RECOMMEND', na=False)]))
    
    # Main content
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0 2rem;">
        <span style="background: rgba(0, 212, 170, 0.2); border: 1px solid rgba(0, 212, 170, 0.3); 
              padding: 0.5rem 1.5rem; border-radius: 100px; color: #00d4aa; font-size: 0.9rem;
              text-transform: uppercase; letter-spacing: 0.1em;">
            🔬 Science-Based Innovation Evaluation
        </span>
        <h1 style="font-size: 3rem; margin: 1rem 0 0.5rem; background: linear-gradient(135deg, #ff6b4a, #00d4aa);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 700;">
            Africa's Boldest Plastic Solutions
        </h1>
        <p style="color: #8ba3c7; font-size: 1.1rem; max-width: 700px; margin: 0 auto;">
            Identifying scientists, innovators, and startups for $120K in funding
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Apply filters
    filtered_df = df.copy()
    
    if selected_rec != 'All':
        filtered_df = filtered_df[filtered_df['RECOMMENDATION'] == selected_rec]
    
    if selected_science != 'All':
        filtered_df = filtered_df[filtered_df['SCIENCE_LEVEL'] == selected_science]
    
    if selected_stage != 'All':
        filtered_df = filtered_df[filtered_df['Stage'] == selected_stage]
    
    if search:
        mask = (
            filtered_df['Venture_Name'].str.contains(search, case=False, na=False) |
            filtered_df['WHAT_THEY_DO'].str.contains(search, case=False, na=False) |
            filtered_df['Location'].str.contains(search, case=False, na=False)
        )
        filtered_df = filtered_df[mask]
    
    if science_only:
        filtered_df = filtered_df[filtered_df['SCIENCE_LEVEL'].str.contains('★★', na=False)]
    
    # Summary metrics
    st.markdown("### 📈 Overview")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    rec_counts = filtered_df['RECOMMENDATION'].value_counts()
    
    with col1:
        count = len(filtered_df[filtered_df['RECOMMENDATION'].str.contains('STRONGLY', na=False)])
        st.metric("★ Strongly Recommend", count)
    
    with col2:
        count = len(filtered_df[filtered_df['RECOMMENDATION'] == '★ RECOMMEND'])
        st.metric("★ Recommend", count)
    
    with col3:
        count = len(filtered_df[filtered_df['RECOMMENDATION'] == 'SHORTLIST'])
        st.metric("Shortlist", count)
    
    with col4:
        count = len(filtered_df[filtered_df['RECOMMENDATION'] == 'CONSIDER'])
        st.metric("Consider", count)
    
    with col5:
        avg_score = filtered_df['WEIGHTED_SCORE'].mean() if len(filtered_df) > 0 else 0
        st.metric("Avg Score", f"{avg_score:.2f}")
    
    st.markdown("---")
    
    # Charts row
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Science Level Distribution")
        science_counts = filtered_df['SCIENCE_LEVEL'].value_counts()
        
        fig = px.pie(
            values=science_counts.values,
            names=science_counts.index,
            color_discrete_sequence=['#00d4aa', '#4fffdb', '#fbbf24', '#f87171', '#94a3b8'],
            hole=0.4
        )
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            showlegend=True,
            legend=dict(
                bgcolor='rgba(0,0,0,0)',
                font=dict(size=10)
            ),
            margin=dict(t=20, b=20, l=20, r=20)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### Score Distribution")
        fig = px.histogram(
            filtered_df,
            x='WEIGHTED_SCORE',
            nbins=20,
            color_discrete_sequence=['#00d4aa']
        )
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            xaxis=dict(gridcolor='rgba(255,255,255,0.1)', title='Weighted Score'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.1)', title='Count'),
            margin=dict(t=20, b=40, l=40, r=20)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Applicants list
    st.markdown(f"### 🏆 Applicants ({len(filtered_df)} shown)")
    
    # Sort options
    sort_col = st.selectbox(
        "Sort by",
        ['WEIGHTED_SCORE', 'Score_Innovation_30%', 'Score_Impact_25%', 'Venture_Name'],
        index=0
    )
    
    sorted_df = filtered_df.sort_values(sort_col, ascending=False)
    
    # Display applicants as expandable cards
    for idx, row in sorted_df.iterrows():
        rec_color = get_recommendation_color(row['RECOMMENDATION'])
        science_emoji = get_science_emoji(row['SCIENCE_LEVEL'])
        
        with st.expander(
            f"{science_emoji} **{row['Venture_Name']}** — Score: {row['WEIGHTED_SCORE']:.2f} | {row['RECOMMENDATION']}"
        ):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**🔬 What They Do:**")
                st.markdown(f"_{row['WHAT_THEY_DO']}_")
                
                st.markdown(f"**📊 Science Level:** {row['SCIENCE_LEVEL']}")
                
                st.markdown(f"**📍 Location:** {row['Location']}")
                st.markdown(f"**🌍 Target Countries:** {row['Target_Countries']}")
                st.markdown(f"**📋 Stage:** {row['Stage']}")
                st.markdown(f"**⚖️ Legal Status:** {row['Legal_Status']}")
            
            with col2:
                st.markdown("**Score Breakdown:**")
                
                scores = {
                    'Innovation (30%)': float(row['Score_Innovation_30%']),
                    'Impact (25%)': float(row['Score_Impact_25%']),
                    'Social (20%)': float(row['Score_Social_20%']),
                    'Commercial (15%)': float(row['Score_Commercial_15%']),
                    'Team (10%)': float(row['Score_Team_10%'])
                }
                
                for label, score in scores.items():
                    pct = score / 5 * 100
                    st.markdown(f"""
                    <div style="margin-bottom: 0.5rem;">
                        <div style="display: flex; justify-content: space-between; font-size: 0.8rem; color: #8ba3c7;">
                            <span>{label}</span>
                            <span style="color: #00d4aa; font-weight: 600;">{score}</span>
                        </div>
                        <div style="background: rgba(255,255,255,0.1); height: 6px; border-radius: 3px; overflow: hidden;">
                            <div style="width: {pct}%; height: 100%; background: #00d4aa; border-radius: 3px;"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("---")
                st.markdown(f"**📧 Contact:** {row['Contact']}")
                st.markdown(f"**✉️ Email:** {row['Email']}")
                st.markdown(f"**🌊 Plastic Impact:** {row['Plastic_Tonnes']} tonnes")
                st.markdown(f"**👥 Livelihoods:** {row['Livelihoods']} people")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #8ba3c7; font-size: 0.9rem; padding: 2rem 0;">
        <p>TCCF Bold Ideas Project | The Coca-Cola Foundation × OceanHub Africa</p>
        <p>Applications close: February 15, 2026</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
