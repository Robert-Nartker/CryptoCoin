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
    page_title="CryptoCoin Dashboard",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# === Custom Styling - Modern Professional Theme ===
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    :root {
        --primary: #6366f1;
        --primary-light: #818cf8;
        --primary-dark: #4f46e5;
        --accent: #22d3ee;
        --success: #10b981;
        --warning: #f59e0b;
        --danger: #ef4444;
        --bg-dark: #0f172a;
        --bg-card: #1e293b;
        --bg-elevated: #334155;
        --text-primary: #f1f5f9;
        --text-secondary: #94a3b8;
        --text-muted: #64748b;
        --border: #334155;
    }
    
    .stApp {
        background: linear-gradient(135deg, var(--bg-dark) 0%, #1a1f35 50%, var(--bg-dark) 100%);
    }
    
    .main-header {
        font-family: 'Inter', sans-serif;
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 50%, var(--primary-light) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        letter-spacing: -0.02em;
        margin-bottom: 0;
    }
    
    .sub-header {
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        color: var(--text-secondary);
        text-align: center;
        margin-top: 8px;
        margin-bottom: 2rem;
        letter-spacing: 0.05em;
        font-weight: 400;
    }
    
    .metric-card {
        background: linear-gradient(145deg, var(--bg-card) 0%, var(--bg-elevated) 100%);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.2);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 32px rgba(99, 102, 241, 0.15);
    }
    
    .stDataFrame {
        background: var(--bg-card) !important;
        border-radius: 12px !important;
        border: 1px solid var(--border) !important;
    }
    
    div[data-testid="stMetricValue"] {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.75rem;
        font-weight: 600;
        color: var(--text-primary);
    }
    
    div[data-testid="stMetricLabel"] {
        font-family: 'Inter', sans-serif;
        font-size: 0.875rem;
        color: var(--text-secondary);
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', sans-serif;
        color: var(--text-primary);
        font-weight: 600;
    }
    
    p, span, div {
        font-family: 'Inter', sans-serif;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
        color: white;
        border: none;
        border-radius: 10px;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        padding: 0.625rem 1.25rem;
        letter-spacing: 0.02em;
        transition: all 0.2s ease;
        box-shadow: 0 2px 8px rgba(99, 102, 241, 0.3);
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, var(--primary-light) 0%, var(--primary) 100%);
        transform: translateY(-1px);
        box-shadow: 0 4px 16px rgba(99, 102, 241, 0.4);
    }
    
    .block-container {
        padding-top: 2rem;
        max-width: 1400px;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: var(--bg-card);
        border-right: 1px solid var(--border);
    }
    
    section[data-testid="stSidebar"] .block-container {
        padding-top: 2rem;
    }
    
    /* Alert styling */
    .stAlert {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 12px;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: var(--bg-card);
        border-radius: 10px;
    }
    
    /* Hide footer */
    footer {visibility: hidden;}
    
    /* Custom badge */
    .status-badge {
        display: inline-block;
        background: linear-gradient(135deg, var(--success) 0%, #059669 100%);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        color: white;
        font-weight: 600;
        letter-spacing: 0.05em;
    }
    
    /* Crypto icon styling */
    .crypto-icon {
        font-size: 1.5rem;
        margin-right: 0.5rem;
    }
    
    /* Table header */
    thead tr th {
        background: var(--bg-elevated) !important;
        color: var(--text-primary) !important;
        font-weight: 600 !important;
    }
    
    /* Links */
    a {
        color: var(--primary-light);
        text-decoration: none;
    }
    
    a:hover {
        color: var(--accent);
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data(ttl=60)  # Cache for 60 seconds
def load_data():
    """Load transaction data from Google Sheets"""
    try:
        response = requests.get(SHEET_CSV_URL, timeout=10)
        response.raise_for_status()
        df = pd.read_csv(StringIO(response.text))
        return df, None
    except Exception as e:
        return None, str(e)


def format_crypto_amount(amount):
    """Format amount with crypto symbol"""
    if amount >= 1_000_000:
        return f"◆ {amount/1_000_000:,.2f}M"
    elif amount >= 1_000:
        return f"◆ {amount/1_000:,.2f}K"
    return f"◆ {amount:,.2f}"


def format_hash(hash_str, length=8):
    """Format transaction hash for display"""
    if pd.isna(hash_str) or not isinstance(hash_str, str):
        return "—"
    if len(hash_str) > length * 2:
        return f"{hash_str[:length]}...{hash_str[-length:]}"
    return hash_str


def main():
    # === Header ===
    st.markdown('<h1 class="main-header">CryptoCoin</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Campus Cryptocurrency • Transaction Dashboard</p>', unsafe_allow_html=True)
    
    # === Sidebar ===
    with st.sidebar:
        st.markdown("### 💎 CryptoCoin")
        st.markdown('<span class="status-badge">LIVE</span>', unsafe_allow_html=True)
        st.markdown("---")
        
        st.markdown("#### About")
        st.markdown("""
        CryptoCoin is a campus cryptocurrency prototype designed 
        to facilitate secure peer-to-peer transactions within 
        university ecosystems.
        """)
        
        st.markdown("---")
        
        st.markdown("#### Data Source")
        st.markdown("📊 [View Transaction Ledger](https://docs.google.com/spreadsheets/d/e/2PACX-1vR6tEwAfY33lPFRJESrjKTN0IQyneZj6RtvVRVUSAB_KydfhP3aVZB62ksuBGHZLlI3Hv97m_DNNz8j/pubhtml)")
        
        st.markdown("---")
        
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
        
        st.markdown("---")
        
        # Stats card
        st.markdown("#### System Status")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Network**")
            st.markdown("🟢 Online")
        with col2:
            st.markdown("**Sync**")
            st.markdown("✓ Live")
        
        st.markdown("---")
        st.caption("Component 1: Streamlit Dashboard")
        st.caption(f"Last refresh: {datetime.now().strftime('%H:%M:%S')}")
    
    # === Load Data ===
    df, error = load_data()
    
    if error:
        st.error(f"❌ Failed to load data: {error}")
        st.info("Please check your internet connection or verify the spreadsheet is published.")
        return
    
    if df is None or df.empty:
        st.warning("⚠️ No transaction data found in the spreadsheet.")
        st.info("Add transactions to the Google Sheet to see them here.")
        return
    
    # === Data Processing ===
    df.columns = df.columns.str.strip()
    
    # Success notification
    st.success(f"✅ Connected to ledger • {len(df)} transactions loaded")
    
    # === Key Metrics ===
    st.markdown("---")
    st.markdown("### 📊 Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    total_transactions = len(df)
    
    # Find amount column
    amount_col = None
    for col in df.columns:
        if 'amount' in col.lower() or 'value' in col.lower() or 'total' in col.lower():
            amount_col = col
            break
    
    with col1:
        st.metric(
            label="Total Transactions",
            value=f"{total_transactions:,}",
            delta=None
        )
    
    if amount_col and pd.to_numeric(df[amount_col], errors='coerce').notna().any():
        amounts = pd.to_numeric(df[amount_col], errors='coerce')
        total_volume = amounts.sum()
        avg_transaction = amounts.mean()
        max_transaction = amounts.max()
        
        with col2:
            st.metric(
                label="Total Volume",
                value=format_crypto_amount(total_volume)
            )
        
        with col3:
            st.metric(
                label="Avg Transaction",
                value=format_crypto_amount(avg_transaction)
            )
        
        with col4:
            st.metric(
                label="Largest Tx",
                value=format_crypto_amount(max_transaction)
            )
    else:
        with col2:
            st.metric(label="Data Columns", value=len(df.columns))
        with col3:
            st.metric(label="Data Points", value=f"{df.size:,}")
        with col4:
            st.metric(label="Status", value="Active ✓")
    
    # === Transaction Table ===
    st.markdown("---")
    st.markdown("### 📋 Transaction Ledger")
    
    # Display options
    col_options, col_search = st.columns([1, 2])
    with col_options:
        show_full = st.checkbox("Show full transaction hashes", value=False)
    
    # Format data for display
    display_df = df.copy()
    
    # Format hash columns if not showing full
    if not show_full:
        for col in display_df.columns:
            if 'hash' in col.lower() or 'from' in col.lower() or 'to' in col.lower():
                if display_df[col].dtype == 'object':
                    display_df[col] = display_df[col].apply(lambda x: format_hash(x, 10))
    
    st.dataframe(
        display_df,
        use_container_width=True,
        height=350
    )
    
    # === Analytics ===
    if amount_col and pd.to_numeric(df[amount_col], errors='coerce').notna().any():
        st.markdown("---")
        st.markdown("### 📈 Analytics")
        
        amounts = pd.to_numeric(df[amount_col], errors='coerce')
        
        # Create tabs for different views
        tab1, tab2, tab3 = st.tabs(["📊 Distribution", "📈 Volume Trend", "🔍 Details"])
        
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                # Transaction amounts bar chart
                fig_bar = px.bar(
                    df,
                    y=amount_col,
                    title="Transaction Amounts",
                    labels={amount_col: "Amount (CryptoCoin)", "index": "Transaction #"},
                    color_discrete_sequence=['#6366f1']
                )
                fig_bar.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='#94a3b8',
                    title_font_color='#f1f5f9',
                    title_font_size=16,
                    showlegend=False,
                    xaxis=dict(showgrid=False),
                    yaxis=dict(gridcolor='rgba(51, 65, 85, 0.5)')
                )
                st.plotly_chart(fig_bar, use_container_width=True)
            
            with col2:
                # Distribution histogram
                fig_hist = px.histogram(
                    df,
                    x=amount_col,
                    nbins=max(5, len(df)//2),
                    title="Value Distribution",
                    labels={amount_col: "Amount (CryptoCoin)"},
                    color_discrete_sequence=['#22d3ee']
                )
                fig_hist.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='#94a3b8',
                    title_font_color='#f1f5f9',
                    title_font_size=16,
                    showlegend=False,
                    xaxis=dict(showgrid=False),
                    yaxis=dict(gridcolor='rgba(51, 65, 85, 0.5)')
                )
                st.plotly_chart(fig_hist, use_container_width=True)
        
        with tab2:
            # Cumulative volume chart
            cumulative = amounts.cumsum()
            
            fig_cumulative = go.Figure()
            fig_cumulative.add_trace(go.Scatter(
                y=cumulative,
                mode='lines+markers',
                name='Cumulative Volume',
                line=dict(color='#6366f1', width=3),
                marker=dict(size=10, color='#6366f1', line=dict(width=2, color='#22d3ee')),
                fill='tozeroy',
                fillcolor='rgba(99, 102, 241, 0.15)'
            ))
            fig_cumulative.update_layout(
                title="Cumulative Transaction Volume",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#94a3b8',
                title_font_color='#f1f5f9',
                title_font_size=16,
                xaxis_title="Transaction #",
                yaxis_title="Cumulative Volume",
                xaxis=dict(showgrid=False),
                yaxis=dict(gridcolor='rgba(51, 65, 85, 0.5)'),
                hovermode='x unified'
            )
            st.plotly_chart(fig_cumulative, use_container_width=True)
        
        with tab3:
            # Summary statistics
            st.markdown("#### Summary Statistics")
            
            stats_col1, stats_col2, stats_col3 = st.columns(3)
            
            with stats_col1:
                st.markdown("**Volume Metrics**")
                st.markdown(f"- Total: `{total_volume:,.2f}`")
                st.markdown(f"- Average: `{avg_transaction:,.2f}`")
                st.markdown(f"- Median: `{amounts.median():,.2f}`")
            
            with stats_col2:
                st.markdown("**Range**")
                st.markdown(f"- Minimum: `{amounts.min():,.2f}`")
                st.markdown(f"- Maximum: `{amounts.max():,.2f}`")
                st.markdown(f"- Std Dev: `{amounts.std():,.2f}`")
            
            with stats_col3:
                st.markdown("**Records**")
                st.markdown(f"- Total Tx: `{len(df)}`")
                st.markdown(f"- Columns: `{len(df.columns)}`")
                st.markdown(f"- Data Points: `{df.size}`")
    
    # === Raw Data ===
    st.markdown("---")
    with st.expander("🔧 Technical Details"):
        st.markdown("**Data Schema**")
        schema_df = pd.DataFrame({
            'Column': df.columns,
            'Type': df.dtypes.astype(str).values,
            'Non-Null': df.count().values,
            'Sample': [str(df[col].iloc[0])[:50] + '...' if len(str(df[col].iloc[0])) > 50 else str(df[col].iloc[0]) for col in df.columns]
        })
        st.dataframe(schema_df, use_container_width=True, hide_index=True)
        
        st.markdown("**Data Source**")
        st.code(SHEET_CSV_URL, language=None)
    
    # === Footer ===
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #64748b; padding: 1.5rem;'>
            <p style='font-size: 1rem; margin-bottom: 0.5rem;'>
                💎 <strong style='color: #f1f5f9;'>CryptoCoin</strong> — Campus Cryptocurrency Dashboard
            </p>
            <p style='font-size: 0.8rem; color: #475569;'>
                Real-time data from Google Sheets • Auto-refresh every 60 seconds<br>
                Component 1: Transaction Viewer & Analytics
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
