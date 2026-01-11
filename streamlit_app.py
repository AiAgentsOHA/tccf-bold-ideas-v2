"""
TCCF Bold Ideas - Science Innovation Dashboard
Streamlit Application

Run with: streamlit run streamlit_dashboard.py

Requirements:
    pip install streamlit pandas plotly openpyxl
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

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');
    
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
    
    p, span, div, label {
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
    
    div[data-testid="stExpander"] {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        margin-bottom: 0.5rem;
    }
    
    div[data-testid="stExpander"] summary {
        color: #ffffff !important;
    }
    
    .eval-box {
        background: linear-gradient(135deg, rgba(0, 212, 170, 0.15), rgba(255, 107, 74, 0.08));
        border: 1px solid rgba(0, 212, 170, 0.3);
        border-radius: 12px;
        padding: 1.25rem;
        margin-bottom: 1rem;
    }
    
    .eval-title {
        color: #00d4aa;
        font-weight: 600;
        font-size: 1rem;
        margin-bottom: 0.5rem;
    }
    
    .eval-text {
        color: #ffffff;
        line-height: 1.6;
        font-size: 0.9rem;
    }
    
    .score-box {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 8px;
        padding: 0.75rem;
        text-align: center;
    }
    
    .score-value {
        color: #00d4aa;
        font-size: 1.5rem;
        font-weight: 700;
    }
    
    .score-label {
        color: #8ba3c7;
        font-size: 0.7rem;
        text-transform: uppercase;
    }
    
    .section-title {
        color: #8ba3c7;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        padding-bottom: 0.5rem;
        margin: 1.5rem 0 1rem;
    }
    
    .stSelectbox > div > div, .stMultiSelect > div > div {
        background: rgba(255, 255, 255, 0.05) !important;
        border-color: rgba(255, 255, 255, 0.1) !important;
    }
    
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.05) !important;
        border-color: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
    }
    
    .stCheckbox label {
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    """Load evaluation data and merge with original application data."""
    # Try multiple paths for the evaluation file
    eval_paths = [
        'TCCF_Bold_Ideas_FINAL.csv',
        '/mnt/user-data/outputs/TCCF_Bold_Ideas_FINAL.csv',
        './TCCF_Bold_Ideas_FINAL.csv'
    ]
    
    eval_df = None
    for path in eval_paths:
        try:
            eval_df = pd.read_csv(path)
            break
        except FileNotFoundError:
            continue
    
    if eval_df is None:
        st.error("Evaluation data file not found. Please ensure TCCF_Bold_Ideas_FINAL.csv is in the same directory.")
        return None
    
    # Try to load original application data for extended fields
    orig_paths = [
        'Bold_Ideas_Database_2e27323557b980b0bd23d3d58431f8c5_all.csv',
        '/mnt/user-data/uploads/Bold_Ideas_Database_2e27323557b980b0bd23d3d58431f8c5_all.csv'
    ]
    
    orig_df = None
    for path in orig_paths:
        try:
            orig_df = pd.read_csv(path, encoding='utf-8-sig')
            break
        except FileNotFoundError:
            continue
    
    # Merge if original data is available
    if orig_df is not None:
        for idx, row in eval_df.iterrows():
            email = row['Email']
            orig_match = orig_df[orig_df['Email'] == email]
            if len(orig_match) > 0:
                orig = orig_match.iloc[0]
                eval_df.loc[idx, 'Science_Inputs'] = str(orig.get('Science Inputs', ''))[:1000] if pd.notna(orig.get('Science Inputs', '')) else ''
                eval_df.loc[idx, 'Bold_Characteristics'] = str(orig.get('Bold Characteristics', ''))[:600] if pd.notna(orig.get('Bold Characteristics', '')) else ''
                eval_df.loc[idx, 'Problem_Addressed'] = str(orig.get('Problem Addressed', ''))[:500] if pd.notna(orig.get('Problem Addressed', '')) else ''
                eval_df.loc[idx, 'Beneficiaries'] = str(orig.get('Beneficiaries', ''))[:400] if pd.notna(orig.get('Beneficiaries', '')) else ''
                eval_df.loc[idx, 'Team_Info'] = str(orig.get('Team', ''))[:600] if pd.notna(orig.get('Team', '')) else ''
                eval_df.loc[idx, 'LinkedIn'] = str(orig.get('LinkedIn', '')) if pd.notna(orig.get('LinkedIn', '')) else ''
                eval_df.loc[idx, 'Website'] = str(orig.get('Website / app link', '')) if pd.notna(orig.get('Website / app link', '')) else ''
    
    return eval_df


def get_recommendation_color(rec):
    """Get color for recommendation."""
    if 'STRONGLY' in str(rec):
        return '#00d4aa'
    elif rec == '★ RECOMMEND':
        return '#4fffdb'
    elif rec == 'SHORTLIST':
        return '#7dd3fc'
    elif rec == 'CONSIDER':
        return '#fbbf24'
    elif 'MAYBE' in str(rec):
        return '#fb923c'
    elif rec == 'LOW PRIORITY':
        return '#f87171'
    return '#ef4444'


def get_science_emoji(level):
    """Get emoji for science level."""
    if '★★★' in str(level):
        return '🔬'
    elif '★★☆' in str(level):
        return '⚗️'
    elif '★☆☆' in str(level):
        return '🔧'
    elif '☆☆☆' in str(level):
        return '📦'
    return '❓'


def generate_eval_summary(row):
    """Generate evaluation summary text for an applicant."""
    rec = row['RECOMMENDATION']
    name = row['Venture_Name']
    what = row['WHAT_THEY_DO']
    score = row['WEIGHTED_SCORE']
    innovation = row['Score_Innovation_30%']
    plastic = row.get('Plastic_Tonnes', 0)
    
    if 'STRONGLY' in rec or rec == '★ RECOMMEND':
        summary = f"**{name}** demonstrates **strong scientific innovation** in their approach to plastic waste management. "
        summary += f"Their solution involves *{what}*. "
        summary += f"With a weighted score of **{score}/5.0**, this applicant shows excellent potential for the TCCF Bold Ideas program. "
        summary += f"Their innovation score of **{innovation}/5** reflects genuine science-based differentiation. "
        try:
            if plastic and float(plastic) > 100:
                summary += f"Projected plastic impact of **{plastic} tonnes** aligns well with program targets."
        except:
            pass
    elif rec == 'SHORTLIST':
        summary = f"**{name}** presents a **promising science-enabled solution**. "
        summary += f"Core offering: *{what}*. "
        summary += f"Weighted score: **{score}/5.0**. Worth interviewing to assess technical depth and scalability. "
        summary += f"Innovation score ({innovation}/5) suggests meaningful technical differentiation."
    elif rec == 'CONSIDER':
        summary = f"**{name}** shows **some scientific elements** in their approach. "
        summary += f"Service: *{what}*. "
        summary += f"Weighted score: **{score}/5.0**. "
        summary += f"May warrant further review if stronger candidates don't fill cohort. Innovation score: {innovation}/5."
    elif 'MAYBE' in rec:
        summary = f"**{name}** has **limited scientific differentiation**. "
        summary += f"Offering: *{what}*. "
        summary += f"Weighted score: **{score}/5.0**. "
        summary += f"Innovation score ({innovation}/5) indicates conventional approach. Consider only if science capacity can be demonstrated."
    else:
        summary = f"**{name}** does not meet the **science-based innovation threshold** for this program. "
        summary += f"Approach: *{what}*. "
        summary += f"Weighted score: **{score}/5.0**. "
        summary += f"Innovation score ({innovation}/5) reflects generic or conventional methodology. Not recommended for TCCF Bold Ideas."
    
    return summary


def main():
    # Sidebar
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
        
        st.metric("Total Applicants", len(df))
        st.metric("Science Innovations", len(df[df['SCIENCE_LEVEL'].str.contains('★★', na=False)]))
        st.metric("Top Recommendations", len(df[df['RECOMMENDATION'].str.contains('RECOMMEND', na=False)]))
    
    # Main content header
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0 2rem;">
        <span style="background: rgba(0, 212, 170, 0.2); border: 1px solid rgba(0, 212, 170, 0.3); 
              padding: 0.5rem 1.5rem; border-radius: 100px; color: #00d4aa; font-size: 0.85rem;
              text-transform: uppercase; letter-spacing: 0.1em;">
            🔬 Science-Based Innovation Evaluation
        </span>
        <h1 style="font-size: 2.5rem; margin: 1rem 0 0.5rem; background: linear-gradient(135deg, #ff6b4a, #00d4aa);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 700;">
            Africa's Boldest Plastic Solutions
        </h1>
        <p style="color: #8ba3c7; font-size: 1rem; max-width: 700px; margin: 0 auto;">
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
    
    # Summary metrics row
    col1, col2, col3, col4, col5 = st.columns(5)
    
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
        if len(filtered_df) > 0:
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
                font=dict(color='white', size=10),
                showlegend=True,
                legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(size=9)),
                margin=dict(t=20, b=20, l=20, r=20),
                height=300
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### Score Distribution")
        if len(filtered_df) > 0:
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
                margin=dict(t=20, b=40, l=40, r=20),
                height=300
            )
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Applicants section
    st.markdown(f"### 🏆 Applicants ({len(filtered_df)} shown)")
    
    # Sort options
    sort_col = st.selectbox(
        "Sort by",
        ['WEIGHTED_SCORE', 'Score_Innovation_30%', 'Score_Impact_25%', 'Venture_Name'],
        index=0
    )
    
    sorted_df = filtered_df.sort_values(sort_col, ascending=(sort_col == 'Venture_Name'))
    
    # Display each applicant
    for idx, row in sorted_df.iterrows():
        science_emoji = get_science_emoji(row['SCIENCE_LEVEL'])
        
        with st.expander(
            f"{science_emoji} **{row['Venture_Name']}** — Score: {row['WEIGHTED_SCORE']:.2f} | {row['RECOMMENDATION']}"
        ):
            # Evaluation Summary Box
            st.markdown("""
            <div class="eval-box">
                <div class="eval-title">📋 Evaluation Summary</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(generate_eval_summary(row))
            
            # Score Breakdown
            st.markdown('<p class="section-title">Score Breakdown</p>', unsafe_allow_html=True)
            
            score_cols = st.columns(5)
            scores = [
                ('Innovation', '30%', row['Score_Innovation_30%']),
                ('Impact', '25%', row['Score_Impact_25%']),
                ('Social', '20%', row['Score_Social_20%']),
                ('Commercial', '15%', row['Score_Commercial_15%']),
                ('Team', '10%', row['Score_Team_10%'])
            ]
            
            for i, (label, weight, score) in enumerate(scores):
                with score_cols[i]:
                    pct = float(score) * 20
                    st.markdown(f"""
                    <div class="score-box">
                        <div class="score-value">{score}</div>
                        <div class="score-label">{label} ({weight})</div>
                        <div style="background: rgba(255,255,255,0.1); height: 4px; border-radius: 2px; margin-top: 0.5rem;">
                            <div style="width: {pct}%; height: 100%; background: #00d4aa; border-radius: 2px;"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Contact & Basic Info
            st.markdown('<p class="section-title">Contact & Basic Information</p>', unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown(f"**Contact:** {row['Contact']}")
                st.markdown(f"**Email:** {row['Email']}")
            with col2:
                st.markdown(f"**Location:** {row['Location']}")
                st.markdown(f"**Stage:** {row['Stage']}")
            with col3:
                st.markdown(f"**Legal Status:** {row['Legal_Status']}")
                if 'LinkedIn' in row and pd.notna(row.get('LinkedIn')) and row.get('LinkedIn'):
                    st.markdown(f"[LinkedIn Profile]({row['LinkedIn']})")
            with col4:
                st.markdown(f"**Target Countries:** {row['Target_Countries']}")
                if 'Website' in row and pd.notna(row.get('Website')) and row.get('Website'):
                    st.markdown(f"[Website]({row['Website']})")
            
            # Impact Metrics
            st.markdown('<p class="section-title">Impact Metrics</p>', unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Plastic Impact", f"{row['Plastic_Tonnes']} tonnes")
            with col2:
                st.metric("Livelihoods", f"{row['Livelihoods']} people")
            with col3:
                if 'Beneficiaries' in row and pd.notna(row.get('Beneficiaries')) and row.get('Beneficiaries'):
                    ben = str(row['Beneficiaries'])[:200]
                    st.markdown(f"**Beneficiaries:** {ben}...")
            
            # Application Content
            has_content = False
            for field in ['Science_Inputs', 'Bold_Characteristics', 'Problem_Addressed', 'Team_Info']:
                if field in row and pd.notna(row.get(field)) and row.get(field):
                    has_content = True
                    break
            
            if has_content:
                st.markdown('<p class="section-title">Application Content</p>', unsafe_allow_html=True)
                
                if 'Science_Inputs' in row and pd.notna(row.get('Science_Inputs')) and row.get('Science_Inputs'):
                    st.markdown("**🔬 Science & Technical Inputs:**")
                    st.info(str(row['Science_Inputs'])[:800])
                
                if 'Bold_Characteristics' in row and pd.notna(row.get('Bold_Characteristics')) and row.get('Bold_Characteristics'):
                    st.markdown("**💡 Bold Characteristics:**")
                    st.info(str(row['Bold_Characteristics'])[:500])
                
                if 'Problem_Addressed' in row and pd.notna(row.get('Problem_Addressed')) and row.get('Problem_Addressed'):
                    st.markdown("**🎯 Problem Addressed:**")
                    st.info(str(row['Problem_Addressed'])[:400])
                
                if 'Team_Info' in row and pd.notna(row.get('Team_Info')) and row.get('Team_Info'):
                    st.markdown("**👥 Team Information:**")
                    st.info(str(row['Team_Info'])[:500])
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #8ba3c7; font-size: 0.85rem; padding: 2rem 0;">
        <p><strong>TCCF Bold Ideas Project</strong> | The Coca-Cola Foundation × OceanHub Africa</p>
        <p>Applications close: February 15, 2026</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
