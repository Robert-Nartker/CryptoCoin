"""
CryptoCoin Dashboard - Streamlit UI
Component 1: Transaction Viewer & Analytics Dashboard

Campus Cryptocurrency Prototype
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import requests
from io import StringIO

# === Configuration ===
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR6tEwAfY33lPFRJESrjKTN0IQyneZj6RtvVRVUSAB_KydfhP3aVZB62ksuBGHZLlI3Hv97m_DNNz8j/pub?output=csv"

# === Page Config ===
st.set_page_config(
    page_title="CryptoCoin",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# === AI Startup Theme (Glassmorphism + Modern Gradients) ===
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    :root {
        --bg-dark: #0A0A0F; /* Deep space black */
        --bg-card: rgba(255, 255, 255, 0.03);
        --bg-card-hover: rgba(255, 255, 255, 0.06);
        --border-color: rgba(255, 255, 255, 0.08);
        --accent-primary: #6366f1; /* Indigo */
        --accent-secondary: #ec4899; /* Pink */
        --accent-tertiary: #10b981; /* Emerald */
        --text-primary: #f8fafc;
        --text-secondary: #94a3b8;
    }

    /* Global Reset & Base */
    .stApp {
        background-color: var(--bg-dark);
        background-image: 
            radial-gradient(circle at 10% 20%, rgba(99, 102, 241, 0.15) 0%, transparent 20%),
            radial-gradient(circle at 90% 80%, rgba(236, 72, 153, 0.1) 0%, transparent 20%);
        font-family: 'Inter', sans-serif;
    }

    /* Remove Streamlit default padding */
    .block-container {
        padding-top: 3rem;
        padding-bottom: 5rem;
        max-width: 1200px;
    }

    /* Hero Section Typography */
    .hero-title {
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        font-size: 4rem;
        text-align: center;
        background: linear-gradient(135deg, #fff 30%, #a5b4fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -0.03em;
        margin-bottom: 0.5rem;
        line-height: 1.1;
    }
    
    .hero-subtitle {
        font-family: 'Inter', sans-serif;
        color: var(--text-secondary);
        text-align: center;
        font-size: 1.25rem;
        font-weight: 400;
        max-width: 600px;
        margin: 0 auto 3rem auto;
        line-height: 1.6;
    }

    /* Custom Cards (Glassmorphism) */
    .css-card {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 1.5rem;
        transition: all 0.3s ease;
    }
    
    .css-card:hover {
        background: var(--bg-card-hover);
        border-color: rgba(99, 102, 241, 0.3);
        transform: translateY(-2px);
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
    }

    /* Metrics Styling */
    .metric-label {
        color: var(--text-secondary);
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .metric-value {
        color: var(--text-primary);
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.75rem;
        font-weight: 700;
        letter-spacing: -0.02em;
    }
    
    /* Styled DataFrame */
    .stDataFrame {
        border: 1px solid var(--border-color) !important;
        border-radius: 12px !important;
    }
    
    div[data-testid="stDataFrame"] {
        background: rgba(0,0,0,0.2);
    }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, var(--accent-primary) 0%, #4f46e5 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s;
        width: 100%;
    }
    
    .stButton>button:hover {
        opacity: 0.9;
        transform: scale(1.02);
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background-color: transparent;
        border-bottom: 1px solid var(--border-color);
    }

    .stTabs [data-baseweb="tab"] {
        height: 3rem;
        white-space: pre-wrap;
        background-color: transparent;
        border: none;
        color: var(--text-secondary);
        font-family: 'Inter', sans-serif;
    }
    
    .stTabs [aria-selected="true"] {
        color: var(--accent-primary) !important;
        border-bottom: 2px solid var(--accent-primary) !important;
    }
    
    /* Hide Streamlit Cruft */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .viewerBadge_container__1QSob {display: none;}
    
    /* Status Badge */
    .status-dot {
        height: 8px;
        width: 8px;
        background-color: var(--accent-tertiary);
        border-radius: 50%;
        display: inline-block;
        margin-right: 6px;
        box-shadow: 0 0 10px var(--accent-tertiary);
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=60)
def load_data():
    try:
        response = requests.get(SHEET_CSV_URL, timeout=10)
        response.raise_for_status()
        df = pd.read_csv(StringIO(response.text))
        return df, None
    except Exception as e:
        return None, str(e)

def format_number(num):
    if num >= 1_000_000:
        return f"{num/1_000_000:.2f}M"
    if num >= 1_000:
        return f"{num/1_000:.2f}K"
    return f"{num:,.2f}"

def render_metric_card(label, value, prefix=""):
    st.markdown(f"""
    <div class="css-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{prefix}{value}</div>
    </div>
    """, unsafe_allow_html=True)

def main():
    # === Navbar / Top Bar ===
    col_logo, col_spacer, col_status = st.columns([1, 4, 1])
    with col_logo:
        st.markdown("<div style='font-weight:700; font-size:1.2rem; color:#fff;'>◆ CryptoCoin</div>", unsafe_allow_html=True)
    with col_status:
        st.markdown(f"<div style='text-align:right; color:#94a3b8; font-size:0.9rem;'><span class='status-dot'></span>Live Sync</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # === Hero Section ===
    st.markdown('<div class="hero-title">The Future of<br>Campus Currency</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">Real-time transparency. Secure transactions. Student-first economy.<br>View the live ledger below.</div>', unsafe_allow_html=True)

    # === Load Data ===
    df, error = load_data()

    if error:
        st.error(f"Unable to connect to ledger: {error}")
        return

    if df is None or df.empty:
        st.warning("Ledger is currently empty.")
        return

    # Clean columns
    df.columns = df.columns.str.strip()

    # Calculate Metrics
    total_tx = len(df)
    amount_col = next((c for c in df.columns if 'amount' in c.lower() or 'value' in c.lower()), None)
    
    total_vol = 0
    avg_tx = 0
    max_tx = 0
    
    if amount_col:
        amounts = pd.to_numeric(df[amount_col], errors='coerce').fillna(0)
        total_vol = amounts.sum()
        avg_tx = amounts.mean()
        max_tx = amounts.max()

    # === Metrics Grid ===
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        render_metric_card("Total Transactions", f"{total_tx:,}")
    with m2:
        render_metric_card("Total Volume", format_number(total_vol), "◆ ")
    with m3:
        render_metric_card("Average Value", format_number(avg_tx), "◆ ")
    with m4:
        render_metric_card("Largest Single Tx", format_number(max_tx), "◆ ")

    st.markdown("<br><br>", unsafe_allow_html=True)

    # === Main Content Area ===
    c1, c2 = st.columns([2, 1])

    with c1:
        st.markdown("### 📋 Live Ledger", unsafe_allow_html=True)
        st.markdown("<div style='margin-bottom: 1rem; color: var(--text-secondary);'>Real-time stream of all confirmed transactions.</div>", unsafe_allow_html=True)
        
        # Table Styling
        display_df = df.copy()
        
        # Truncate hashes for cleaner UI
        for col in display_df.columns:
            if any(x in col.lower() for x in ['hash', 'from', 'to', 'addr']):
                display_df[col] = display_df[col].astype(str).apply(lambda x: x[:6] + '...' + x[-4:] if len(x) > 10 else x)
        
        st.dataframe(
            display_df,
            use_container_width=True,
            height=400,
            column_config={
                amount_col: st.column_config.NumberColumn(
                    "Amount",
                    format="◆ %.2f"
                )
            } if amount_col else None
        )

    with c2:
        st.markdown("### 📈 Network Activity", unsafe_allow_html=True)
        
        if amount_col:
            # 1. Volume Trend (Area Chart)
            # Create a synthetic index or use date if available
            df_chart = df.copy()
            df_chart = df_chart.reset_index()
            
            # Minimalist Area Chart
            fig = px.area(
                df_chart, 
                y=amount_col, 
                title=None,
                color_discrete_sequence=['#6366f1']
            )
            
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=0, r=0, t=0, b=0),
                xaxis=dict(showgrid=False, showticklabels=False),
                yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', showticklabels=True),
                height=200,
                showlegend=False
            )
            # Add gradient fill
            fig.update_traces(fillcolor='rgba(99, 102, 241, 0.2)', line=dict(width=2))
            
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # 2. Distribution (Histogram)
            fig2 = px.histogram(
                df, 
                x=amount_col, 
                nbins=10,
                color_discrete_sequence=['#ec4899']
            )
            fig2.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=0, r=0, t=0, b=20),
                xaxis=dict(showgrid=False, title=None, tickfont=dict(color='#64748b')),
                yaxis=dict(showgrid=False, showticklabels=False),
                height=150,
                showlegend=False,
                bargap=0.1
            )
            st.markdown("<div style='font-size: 0.85rem; color: var(--text-secondary); margin-bottom:0.5rem;'>Value Distribution</div>", unsafe_allow_html=True)
            st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})
            
        else:
            st.info("Insufficient data for analytics.")

    # === Footer / Actions ===
    st.markdown("---")
    
    f1, f2, f3 = st.columns([1, 2, 1])
    with f2:
        if st.button("Refresh Network Data"):
            st.cache_data.clear()
            st.rerun()
        st.markdown("<div style='text-align:center; color: var(--text-secondary); font-size: 0.8rem; margin-top: 1rem;'>CryptoCoin Protocol v1.0 • Component 1</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
