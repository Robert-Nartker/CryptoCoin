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

# === Modern Startup Theme ===
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');
    
    :root {
        --bg-dark: #0A0A0F;
        --bg-card: rgba(255, 255, 255, 0.03);
        --bg-card-hover: rgba(255, 255, 255, 0.06);
        --border-color: rgba(255, 255, 255, 0.08);
        --accent-primary: #6366f1;
        --accent-secondary: #ec4899;
        --accent-tertiary: #10b981;
        --text-primary: #f8fafc;
        --text-secondary: #94a3b8;
    }

    .stApp {
        background-color: var(--bg-dark);
        background-image: 
            radial-gradient(circle at 10% 20%, rgba(99, 102, 241, 0.12) 0%, transparent 25%),
            radial-gradient(circle at 90% 80%, rgba(236, 72, 153, 0.08) 0%, transparent 25%);
        font-family: 'Inter', sans-serif;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }

    /* Hero Typography */
    .hero-title {
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        font-size: 3.5rem;
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
        font-size: 1.15rem;
        font-weight: 400;
        max-width: 600px;
        margin: 0 auto 2rem auto;
        line-height: 1.6;
    }

    /* Cards */
    .glass-card {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 1.5rem;
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        background: var(--bg-card-hover);
        border-color: rgba(99, 102, 241, 0.2);
        transform: translateY(-2px);
    }

    /* Wallet Card */
    .wallet-card {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(236, 72, 153, 0.05) 100%);
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 16px;
        padding: 1.25rem;
        margin-bottom: 1rem;
    }
    
    .wallet-label {
        color: var(--accent-primary);
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 0.25rem;
    }
    
    .wallet-address {
        color: var(--text-secondary);
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
        margin-bottom: 0.75rem;
        word-break: break-all;
    }
    
    .wallet-balance {
        color: var(--text-primary);
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.75rem;
        font-weight: 700;
    }
    
    .wallet-balance-label {
        color: var(--text-secondary);
        font-size: 0.75rem;
        margin-top: 0.25rem;
    }

    /* Metrics */
    .metric-label {
        color: var(--text-secondary);
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .metric-value {
        color: var(--text-primary);
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.5rem;
        font-weight: 700;
    }

    /* Section Headers */
    .section-header {
        color: var(--text-primary);
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .section-subheader {
        color: var(--text-secondary);
        font-size: 0.95rem;
        margin-bottom: 1.5rem;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background-color: rgba(255,255,255,0.03);
        border-radius: 12px;
        padding: 4px;
        border: 1px solid var(--border-color);
    }

    .stTabs [data-baseweb="tab"] {
        height: 2.75rem;
        background-color: transparent;
        border: none;
        color: var(--text-secondary);
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        border-radius: 8px;
        padding: 0 1.5rem;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: var(--accent-primary) !important;
        color: white !important;
    }
    
    /* Hide Streamlit elements */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Status indicator */
    .status-dot {
        height: 8px;
        width: 8px;
        background-color: var(--accent-tertiary);
        border-radius: 50%;
        display: inline-block;
        margin-right: 6px;
        box-shadow: 0 0 10px var(--accent-tertiary);
    }
    
    /* Interpretation box */
    .interpretation-box {
        background: rgba(99, 102, 241, 0.08);
        border-left: 3px solid var(--accent-primary);
        padding: 1.25rem;
        border-radius: 0 12px 12px 0;
        margin: 1.5rem 0;
    }
    
    .interpretation-title {
        color: var(--accent-primary);
        font-weight: 600;
        font-size: 0.9rem;
        margin-bottom: 0.75rem;
    }
    
    .interpretation-text {
        color: var(--text-secondary);
        font-size: 0.95rem;
        line-height: 1.7;
    }

    /* Use case box */
    .usecase-box {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: 16px;
        padding: 2rem;
        margin: 1.5rem 0;
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
    if pd.isna(num) or num == 0:
        return "0"
    if abs(num) >= 1_000_000:
        return f"{num/1_000_000:.2f}M"
    if abs(num) >= 1_000:
        return f"{num/1_000:.2f}K"
    return f"{num:,.2f}"


def truncate_address(addr, front=6, back=4):
    if pd.isna(addr) or not isinstance(addr, str) or len(addr) <= front + back:
        return str(addr) if not pd.isna(addr) else "—"
    return f"{addr[:front]}...{addr[-back:]}"


def calculate_wallet_balances(df):
    """Calculate balances for each unique wallet from transaction history."""
    wallets = {}
    
    # Find relevant columns
    from_col = next((c for c in df.columns if 'from' in c.lower()), None)
    to_col = next((c for c in df.columns if 'to' in c.lower()), None)
    amount_col = next((c for c in df.columns if 'amount' in c.lower() or 'value' in c.lower()), None)
    
    if not all([from_col, to_col, amount_col]):
        return {}
    
    for _, row in df.iterrows():
        sender = str(row[from_col]) if not pd.isna(row[from_col]) else None
        recipient = str(row[to_col]) if not pd.isna(row[to_col]) else None
        amount = pd.to_numeric(row[amount_col], errors='coerce')
        
        if pd.isna(amount):
            amount = 0
        
        # Deduct from sender
        if sender and sender != 'nan':
            if sender not in wallets:
                wallets[sender] = {'sent': 0, 'received': 0, 'role': 'Unknown'}
            wallets[sender]['sent'] += amount
        
        # Add to recipient
        if recipient and recipient != 'nan':
            if recipient not in wallets:
                wallets[recipient] = {'sent': 0, 'received': 0, 'role': 'Unknown'}
            wallets[recipient]['received'] += amount
    
    # Calculate net balance
    for addr in wallets:
        wallets[addr]['balance'] = wallets[addr]['received'] - wallets[addr]['sent']
        
        # Assign roles based on activity
        if wallets[addr]['sent'] == 0 and wallets[addr]['received'] > 0:
            wallets[addr]['role'] = 'Treasury / Mint'
        elif wallets[addr]['received'] > wallets[addr]['sent']:
            wallets[addr]['role'] = 'Net Recipient'
        else:
            wallets[addr]['role'] = 'Net Sender'
    
    return wallets


def render_wallet_card(address, balance, role, label="Wallet"):
    st.markdown(f"""
    <div class="wallet-card">
        <div class="wallet-label">{label}</div>
        <div class="wallet-address">{address}</div>
        <div class="wallet-balance">◆ {format_number(balance)}</div>
        <div class="wallet-balance-label">{role}</div>
    </div>
    """, unsafe_allow_html=True)


def render_metric_card(label, value, prefix=""):
    st.markdown(f"""
    <div class="glass-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{prefix}{value}</div>
    </div>
    """, unsafe_allow_html=True)


def main():
    # === Top Bar ===
    col_logo, col_spacer, col_status = st.columns([1, 4, 1])
    with col_logo:
        st.markdown("<div style='font-weight:700; font-size:1.2rem; color:#fff;'>◆ CryptoCoin</div>", unsafe_allow_html=True)
    with col_status:
        st.markdown(f"<div style='text-align:right; color:#94a3b8; font-size:0.9rem;'><span class='status-dot'></span>Live</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # === Hero ===
    st.markdown('<div class="hero-title">The Future of<br>Campus Currency</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">Real-time transparency. Secure transactions. Student-first economy.</div>', unsafe_allow_html=True)

    # === Load Data ===
    df, error = load_data()

    if error:
        st.error(f"Unable to connect to ledger: {error}")
        return

    if df is None or df.empty:
        st.warning("Ledger is currently empty.")
        return

    df.columns = df.columns.str.strip()
    
    # Calculate wallet balances
    wallets = calculate_wallet_balances(df)
    
    # Find amount column
    amount_col = next((c for c in df.columns if 'amount' in c.lower() or 'value' in c.lower()), None)

    # === TWO PAGES AS TABS ===
    tab1, tab2 = st.tabs(["📋 Overview & Use-Case", "📈 Analytics & Interpretation"])

    # =====================================================
    # PAGE 1: OVERVIEW & USE-CASE
    # =====================================================
    with tab1:
        st.markdown("<br>", unsafe_allow_html=True)
        
        # --- Use Case Section (placeholder for user content) ---
        st.markdown('<div class="section-header">💡 Use Case</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-subheader">How CryptoCoin works on campus</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="usecase-box">
            <p style="color: #94a3b8; font-style: italic;">
                [Your use-case explanation will go here]<br><br>
                Describe your chosen campus use-case (e.g., student life, research/alumni rewards, 
                event ticketing, dining credits, etc.) in plain language.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Flow diagram placeholder
        st.markdown("**Transaction Flow**")
        st.info("📊 *Upload or describe your flow diagram here showing how a typical user interacts with CryptoCoin.*")
        
        st.markdown("---")
        
        # --- Wallet Addresses Section ---
        st.markdown('<div class="section-header">👛 Wallet Addresses</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-subheader">Active addresses and their current CryptoCoin balances</div>', unsafe_allow_html=True)
        
        if wallets:
            # Get top wallets by absolute balance
            sorted_wallets = sorted(wallets.items(), key=lambda x: abs(x[1]['balance']), reverse=True)
            
            # Display at least 2 wallets (requirement)
            num_wallets = min(4, len(sorted_wallets))  # Show up to 4
            cols = st.columns(2)
            
            wallet_labels = ["Primary Wallet", "Secondary Wallet", "Wallet #3", "Wallet #4"]
            
            for i, (addr, data) in enumerate(sorted_wallets[:num_wallets]):
                with cols[i % 2]:
                    render_wallet_card(
                        address=addr,
                        balance=data['balance'],
                        role=data['role'],
                        label=wallet_labels[i]
                    )
        else:
            st.warning("Unable to calculate wallet balances from transaction data.")
        
        st.markdown("---")
        
        # --- Recent Transactions Section ---
        st.markdown('<div class="section-header">🔄 Recent Transactions</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-subheader">Latest confirmed transactions on the network</div>', unsafe_allow_html=True)
        
        # Format for display
        display_df = df.copy()
        
        # Truncate addresses for cleaner display
        for col in display_df.columns:
            if any(x in col.lower() for x in ['hash', 'from', 'to', 'addr']):
                display_df[col] = display_df[col].astype(str).apply(lambda x: truncate_address(x))
        
        st.dataframe(
            display_df,
            use_container_width=True,
            height=300,
            column_config={
                amount_col: st.column_config.NumberColumn(
                    "Amount",
                    format="◆ %.2f"
                )
            } if amount_col else None
        )
        
        # Link to view full data
        st.markdown("[View full transaction ledger →](https://docs.google.com/spreadsheets/d/e/2PACX-1vR6tEwAfY33lPFRJESrjKTN0IQyneZj6RtvVRVUSAB_KydfhP3aVZB62ksuBGHZLlI3Hv97m_DNNz8j/pubhtml)")

    # =====================================================
    # PAGE 2: ANALYTICS & INTERPRETATION
    # =====================================================
    with tab2:
        st.markdown("<br>", unsafe_allow_html=True)
        
        # --- Metrics Overview ---
        if amount_col:
            amounts = pd.to_numeric(df[amount_col], errors='coerce').fillna(0)
            total_vol = amounts.sum()
            avg_tx = amounts.mean()
            tx_count = len(df)
            unique_wallets = len(wallets)
            
            m1, m2, m3, m4 = st.columns(4)
            with m1:
                render_metric_card("Total Transactions", f"{tx_count:,}")
            with m2:
                render_metric_card("Total Volume", format_number(total_vol), "◆ ")
            with m3:
                render_metric_card("Avg Transaction", format_number(avg_tx), "◆ ")
            with m4:
                render_metric_card("Unique Wallets", f"{unique_wallets}")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # --- Chart Section ---
        st.markdown('<div class="section-header">📊 Token Distribution</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-subheader">Visualization of transaction activity and token flow</div>', unsafe_allow_html=True)
        
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            if amount_col:
                # Transaction volume over index (proxy for time)
                fig = px.area(
                    df.reset_index(), 
                    y=amount_col,
                    title="Transaction Volume",
                    color_discrete_sequence=['#6366f1']
                )
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='#94a3b8',
                    title_font_color='#f8fafc',
                    margin=dict(l=20, r=20, t=40, b=20),
                    xaxis=dict(showgrid=False, title=None),
                    yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', title=None),
                    height=280,
                    showlegend=False
                )
                fig.update_traces(fillcolor='rgba(99, 102, 241, 0.2)', line=dict(width=2))
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
        with chart_col2:
            if amount_col:
                # Distribution histogram
                fig2 = px.histogram(
                    df, 
                    x=amount_col, 
                    nbins=10,
                    title="Value Distribution",
                    color_discrete_sequence=['#ec4899']
                )
                fig2.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='#94a3b8',
                    title_font_color='#f8fafc',
                    margin=dict(l=20, r=20, t=40, b=20),
                    xaxis=dict(showgrid=False, title=None),
                    yaxis=dict(showgrid=False, title=None),
                    height=280,
                    showlegend=False,
                    bargap=0.1
                )
                st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})
        
        st.markdown("---")
        
        # --- Transaction Table ---
        st.markdown('<div class="section-header">📋 Transaction Details</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-subheader">Complete record with sender/recipient roles, amounts, fees, and types</div>', unsafe_allow_html=True)
        
        # Show full transaction table with more detail
        st.dataframe(
            display_df,
            use_container_width=True,
            height=350
        )
        
        st.markdown("---")
        
        # --- Interpretation Section (placeholder for user content) ---
        st.markdown('<div class="section-header">📝 Interpretation</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="interpretation-box">
            <div class="interpretation-title">What the Data Tells Us</div>
            <div class="interpretation-text">
                [Your interpretation will go here]<br><br>
                Explain what the transaction data reveals about how CryptoCoin is being used, 
                and whether this feels viable for the university at a larger scale.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Viability assessment placeholder
        st.markdown("""
        <div class="interpretation-box" style="background: rgba(16, 185, 129, 0.08); border-color: #10b981;">
            <div class="interpretation-title" style="color: #10b981;">Viability Assessment</div>
            <div class="interpretation-text">
                [Your viability analysis will go here]<br><br>
                Is this viable for the university at larger scale? Why or why not?
            </div>
        </div>
        """, unsafe_allow_html=True)

    # === Footer ===
    st.markdown("---")
    f1, f2, f3 = st.columns([1, 2, 1])
    with f2:
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
        st.markdown("<div style='text-align:center; color: #64748b; font-size: 0.8rem; margin-top: 1rem;'>CryptoCoin Protocol v1.0 • Component 1: Streamlit Dashboard</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
