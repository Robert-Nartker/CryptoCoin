# 💎 CryptoCoin Dashboard

**Campus Cryptocurrency Prototype - Transaction Viewer & Analytics (Component 1)**

![Python](https://img.shields.io/badge/Python-3.9+-3776ab)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-ff4b4b)
![License](https://img.shields.io/badge/License-Educational-22c55e)

## Overview

CryptoCoin is a campus cryptocurrency prototype designed to facilitate secure peer-to-peer transactions within university ecosystems. This Streamlit dashboard provides real-time visualization of all transactions stored in a Google Sheets ledger.

## Features

- 📊 **Real-time Data** — Live transaction feed from Google Sheets
- 📈 **Analytics Dashboard** — Interactive charts and metrics
- 💎 **Modern UI** — Clean, professional dark theme
- 🔄 **Auto-refresh** — Data syncs every 60 seconds
- 📱 **Responsive** — Works on desktop and mobile
- 🔍 **Transaction Details** — View full or truncated hashes

## Live Demo

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-name.streamlit.app)

## Quick Start

### Local Development

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/CryptoCoin.git
cd CryptoCoin

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run app.py
```

### Deploy to Streamlit Cloud

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Select this repository and `app.py`
5. Click Deploy!

Your app will be live at `https://your-app-name.streamlit.app`

## Project Structure

```
CryptoCoin/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── .streamlit/
│   └── config.toml       # Streamlit theme & configuration
├── .gitignore            # Git ignore rules
└── README.md             # Documentation
```

## Data Source

Transaction data is stored in a published Google Sheet:
- [View Transaction Ledger](https://docs.google.com/spreadsheets/d/e/2PACX-1vR6tEwAfY33lPFRJESrjKTN0IQyneZj6RtvVRVUSAB_KydfhP3aVZB62ksuBGHZLlI3Hv97m_DNNz8j/pubhtml)

The dashboard automatically fetches the CSV export for real-time updates.

## Configuration

Theme settings in `.streamlit/config.toml`:

| Setting | Value | Description |
|---------|-------|-------------|
| primaryColor | `#6366f1` | Indigo accent |
| backgroundColor | `#0f172a` | Dark slate |
| textColor | `#f1f5f9` | Light gray |

## Components

This dashboard is **Component 1** of the CryptoCoin project:

| Component | Description | Status |
|-----------|-------------|--------|
| 1. Dashboard | Transaction viewer & analytics | ✅ Complete |
| 2. Governance | Risk memo & policies | 📋 Planned |
| 3. Tokenomics | Scenario analysis | 📋 Planned |
| 4. Roadmap | Reflection & future plans | 📋 Planned |

## Tech Stack

- **Frontend**: Streamlit
- **Visualization**: Plotly
- **Data**: Pandas + Google Sheets
- **Styling**: Custom CSS

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is for educational purposes.

---

💎 **CryptoCoin** — Campus Cryptocurrency Prototype
