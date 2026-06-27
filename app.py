import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from streamlit_option_menu import option_menu

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Quality of Life Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# APP STYLING — all usability fixes applied:
#   - Min font 0.82rem (WCAG readable)
#   - Improved contrast ratios (4.5:1 text, 3:1 graphical)
#   - Responsive columns via CSS grid
#   - Accessible focus styles
#   - Skip-link for keyboard users
#   - Consistent border-radius, spacing
# ============================================================

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=DM+Sans:wght@400;500;700&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/icon?family=Material+Icons+Round" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">

<style>

/* ============================================================
   GLOBAL LAYOUT
============================================================ */
.block-container {
    max-width: 1380px;
    padding-top: 1.4rem;
    padding-bottom: 2.2rem;
}

/* Skip-link for keyboard accessibility */
.skip-link {
    position: absolute;
    top: -40px;
    left: 0;
    background: #003366;
    color: #ffffff;
    padding: 8px 16px;
    z-index: 10000;
    font-size: 0.9rem;
    border-radius: 0 0 8px 0;
    transition: top 0.2s;
}
.skip-link:focus {
    top: 0;
}

/* ============================================================
   TYPOGRAPHY — min 0.82rem for WCAG readability
============================================================ */
html, body, [class*="css"] {
    color: #001F3F;
    font-family: "Inter", "Segoe UI", sans-serif;
}

.app-title {
    font-size: 2.35rem;
    font-weight: 800;
    line-height: 1.1;
    letter-spacing: -0.03em;
    color: #001F3F;
    margin-bottom: 0.35rem;
}

.app-subtitle {
    font-size: 1.02rem;
    line-height: 1.6;
    color: #003366;
    margin-top: 0;
    margin-bottom: 0.8rem;
    max-width: 980px;
}

h1 {
    font-size: 2rem !important;
    font-weight: 800 !important;
    margin-bottom: 0.4rem !important;
    color: #001F3F;
}

h2 {
    font-size: 1.35rem !important;
    font-weight: 700 !important;
    margin-top: 0.2rem !important;
    margin-bottom: 0.6rem !important;
    color: #001F3F;
}

h3 {
    font-size: 1.05rem !important;
    font-weight: 700 !important;
    color: #003366;
}

.small-note {
    font-size: 0.92rem;
    line-height: 1.5;
    color: #003366;
    background: #EAEDED;
    padding: 0.55rem 1rem;
    border-radius: 10px;
    border-left: 4px solid #005B99;
}

.small-note b {
    color: #0096D6;
}

.tab-desc {
    font-size: 0.93rem;
    line-height: 1.5;
    color: #1a1a1a;
    margin-top: -0.3rem;
    margin-bottom: 0.6rem;
}

/* Contextual help tooltip */
.help-tip {
    display: inline-block;
    cursor: help;
    color: #005B99;
    font-size: 0.85rem;
    border-bottom: 1px dashed #005B99;
    margin-left: 0.3rem;
}

/* ============================================================
   SIDEBAR — improved font sizes for readability
============================================================ */
section[data-testid="stSidebar"] {
    background: #EAEDED;
    color: #003366;
    border-right: 1px solid #d0d5d9;
}

section[data-testid="stSidebar"] .block-container {
    padding-top: 1.2rem;
    padding-bottom: 1.4rem;
}

section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stSlider label,
section[data-testid="stSidebar"] .stCheckbox label {
    color: #003366 !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
}

section[data-testid="stSidebar"] .stCaption,
section[data-testid="stSidebar"] small {
    color: #444444 !important;
    font-size: 0.82rem !important;
}

section[data-testid="stSidebar"] hr {
    border-color: #c0c5c9 !important;
}

.sidebar-title {
    font-family: "Inter", sans-serif;
    font-size: 1.25rem;
    font-weight: 700;
    line-height: 1.3;
    color: #003366;
    margin-bottom: 1.3rem;
    letter-spacing: -0.01em;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.sidebar-filter-group {
    border-top: 1px solid #c0c5c9;
    padding-top: 0.75rem;
    margin-top: 0.3rem;
    margin-bottom: 0.15rem;
}

.sidebar-group-header {
    font-family: "Inter", sans-serif;
    font-size: 0.82rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    color: #4B8B3B;
    margin-bottom: 0.1rem;
    display: flex;
    align-items: center;
    gap: 0.4rem;
}

.sidebar-group-header i {
    font-size: 0.88rem;
}

.sidebar-section-label {
    font-family: "Inter", sans-serif;
    font-size: 0.82rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    color: #4B8B3B;
    margin-bottom: 0.35rem;
    display: flex;
    align-items: center;
    gap: 0.4rem;
}

.sidebar-section-label i {
    font-size: 0.88rem;
}

.sidebar-help {
    font-family: "Inter", sans-serif;
    font-size: 0.88rem;
    line-height: 1.65;
    color: #333333;
}

.sidebar-help b {
    color: #555555;
    font-weight: 600;
}

/* ============================================================
   SIDEBAR INPUTS — larger touch targets (min 44px)
============================================================ */

div[data-testid="stPopover"] > div > button {
    width: 100%;
    min-height: 44px;
    border-radius: 10px !important;
    border: 1px solid #c0c5c9 !important;
    background: #ffffff !important;
    color: #003366 !important;
    justify-content: flex-start !important;
    padding: 0.65rem 0.85rem !important;
    font-weight: 500 !important;
    font-size: 0.88rem !important;
    box-shadow: none !important;
    transition: background 0.15s ease, border-color 0.15s ease;
}

div[data-testid="stPopover"] > div > button:hover {
    background: #f5f5f5 !important;
    border-color: #003366 !important;
}

section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
    min-height: 44px;
    border: 1px solid #c0c5c9 !important;
    background: #ffffff !important;
    color: #003366 !important;
    border-radius: 10px !important;
    box-shadow: none !important;
}

section[data-testid="stSidebar"] div[data-baseweb="select"] > div:hover {
    border-color: #003366 !important;
}

section[data-testid="stSidebar"] div[data-baseweb="select"] svg {
    fill: #555555 !important;
}

section[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] div[role="slider"] {
    background: #003366 !important;
}

section[data-testid="stSidebar"] .stCheckbox label,
section[data-testid="stSidebar"] .stCheckbox label span,
section[data-testid="stSidebar"] .stCheckbox label p {
    color: #333333 !important;
}

section[data-testid="stSidebar"] div[data-baseweb="select"] span,
section[data-testid="stSidebar"] div[data-baseweb="select"] div[class*="valueContainer"] {
    color: #003366 !important;
}

section[data-testid="stSidebar"] .stSlider div[data-testid="stTickBarMin"],
section[data-testid="stSidebar"] .stSlider div[data-testid="stTickBarMax"],
section[data-testid="stSidebar"] .stSlider [data-testid="stThumbValue"] {
    color: #444444 !important;
}


/* ============================================================
   INPUTS / CONTROLS
============================================================ */

div[data-baseweb="select"] > div,
div[data-testid="stTextInput"] input,
div[data-testid="stNumberInput"] input {
    border-radius: 12px !important;
}

div[data-baseweb="tag"] {
    background-color: #e8edf5 !important;
    border: 1px solid #d6dee9 !important;
    border-radius: 999px !important;
}

div[data-baseweb="tag"] span {
    color: #344054 !important;
    font-weight: 500 !important;
}

div[data-baseweb="select"] > div {
    min-height: 46px;
    border: 1px solid #d8dee8 !important;
    box-shadow: none !important;
    background-color: #ffffff !important;
}

/* Focus ring for keyboard accessibility */
div[data-baseweb="select"] > div:focus-within {
    outline: 2px solid #005B99 !important;
    outline-offset: 2px;
}

input:focus, button:focus-visible {
    outline: 2px solid #005B99 !important;
    outline-offset: 2px;
}

/* ============================================================
   CARDS / BOXES
============================================================ */
.section-box {
    background: #EAEDED;
    border: 1px solid #d8dee8;
    padding: 1rem 1.15rem;
    border-radius: 14px;
    margin-bottom: 1rem;
    color: #001F3F;
    font-size: 0.93rem;
    line-height: 1.6;
}

.kpi-card {
    border-radius: 14px;
    padding: 1rem 1rem 0.95rem 1rem;
    min-height: 150px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    box-shadow: 0 2px 8px rgba(0, 31, 63, 0.18);
    border: none;
    background: linear-gradient(135deg, #001F3F 0%, #005B99 100%);
}

.kpi-card-outline {
    background: #ffffff;
    border: 2px solid #4B8B3B;
    box-shadow: none;
}

.kpi-card-outline .kpi-title {
    color: #4B8B3B;
}

.kpi-card-outline .kpi-value {
    color: #1a1a1a;
}

.kpi-card-outline .kpi-sub {
    color: #333333;
}

/* Primary KPI card — highlighted via Restorff Effect */
.kpi-card-primary {
    background: linear-gradient(135deg, #003366 0%, #0096D6 100%);
    box-shadow: 0 4px 16px rgba(0, 51, 102, 0.35);
    transform: scale(1.02);
}

.kpi-title {
    font-size: 0.88rem;
    color: rgba(255,255,255,0.85);
    margin-bottom: 0.45rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.02em;
}

.kpi-value {
    font-size: 1.55rem;
    font-weight: 800;
    line-height: 1.2;
    color: #ffffff;
    margin-bottom: 0.3rem;
}

.kpi-sub {
    font-size: 0.88rem;
    color: rgba(255,255,255,0.75);
    line-height: 1.45;
}

.good-box {
    background: linear-gradient(135deg, #EDF7E8 0%, #f8fbf5 100%);
    border-left: 4px solid #4B8B3B;
    padding: 0.9rem 1rem;
    border-radius: 12px;
    margin-bottom: 1rem;
    color: #003366;
}

.warn-box {
    background: linear-gradient(135deg, #EDF7E8 0%, #f8fbf5 100%);
    border-left: 4px solid #4B8B3B;
    padding: 0.9rem 1rem;
    border-radius: 12px;
    margin-bottom: 1rem;
    color: #001F3F;
}

.concern-box {
    background: linear-gradient(135deg, #FDECEC 0%, #fef5f5 100%);
    border-left: 4px solid #D94F4F;
    padding: 0.9rem 1rem;
    border-radius: 12px;
    margin-bottom: 1rem;
    color: #001F3F;
}

.insight-box {
    background: linear-gradient(135deg, #E3F0FA 0%, #f5f9fd 100%);
    border: 1px solid #0096D6;
    padding: 0.9rem 1rem;
    border-radius: 12px;
    margin-bottom: 1rem;
    color: #001F3F;
    font-size: 0.93rem;
    line-height: 1.55;
}

.success-box {
    background: linear-gradient(135deg, #E8F5E9 0%, #f1f8f2 100%);
    border: 1px solid #4B8B3B;
    padding: 0.9rem 1rem;
    border-radius: 12px;
    margin-bottom: 1rem;
    color: #1a1a1a;
    font-size: 0.93rem;
    line-height: 1.55;
    text-align: center;
}

.footer-note {
    font-size: 0.88rem;
    color: #003366;
    margin-top: 2rem;
}

/* ============================================================
   TABS
============================================================ */
button[data-baseweb="tab"] {
    font-weight: 600 !important;
    color: #003366 !important;
    padding-left: 0.4rem !important;
    padding-right: 0.4rem !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #005B99 !important;
}

div[data-testid="stHorizontalBlock"] ul.nav {
    border-bottom: 2px solid #d0d5d9;
}

.nav-link i,
.nav-link .icon {
    background: linear-gradient(135deg, #003366, #A4D65E) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
}

.nav-link.active {
    border-bottom: none !important;
    border-image: none !important;
    position: relative !important;
}

.nav-link.active::after {
    content: '';
    position: absolute;
    bottom: -2px;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, #003366, #A4D65E);
    border-radius: 2px;
}

/* ============================================================
   MAIN CONTENT POPOVER BUTTONS
============================================================ */
.stMainBlockContainer div[data-testid="stPopover"] > div > button {
    background: #EAEDED !important;
    color: #003366 !important;
    border: 1px solid #c0c5c9 !important;
}

.stMainBlockContainer div[data-testid="stPopover"] > div > button:hover {
    background: #dde1e4 !important;
    border-color: #003366 !important;
}

/* ============================================================
   DATAFRAME / TABLE
============================================================ */
div[data-testid="stDataFrame"] {
    border: 1px solid #e5e7eb;
    border-radius: 14px;
    overflow: hidden;
}

/* ============================================================
   PLOT CONTAINERS
============================================================ */
div[data-testid="stPlotlyChart"] {
    background: #ffffff;
    border: 1px solid #EAEDED;
    border-radius: 16px;
    padding: 0.35rem 0.35rem 0.2rem 0.35rem;
    box-shadow: 0 2px 8px rgba(0, 31, 63, 0.06);
}

.stCaption {
    color: #005B99 !important;
}

/* Download button — green */
.stDownloadButton > button {
    background-color: #4B8B3B !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 10px !important;
}

.stDownloadButton > button:hover {
    background-color: #3d7331 !important;
}

/* ============================================================
   RESPONSIVE — mobile friendly
============================================================ */
@media (max-width: 768px) {
    .block-container {
        padding-top: 0.8rem;
        padding-bottom: 1rem;
    }
    .app-title {
        font-size: 1.6rem;
    }
    .app-subtitle {
        font-size: 0.9rem;
    }
    .kpi-card {
        min-height: 120px;
    }
    .kpi-card-primary {
        transform: none;
    }
    .nav-link {
        font-size: 12px !important;
        padding: 8px 10px !important;
    }
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# CONFIG
# ============================================================

INDICES = [
    "Quality of Life Index",
    "Purchasing Power Index",
    "Safety Index",
    "Health Care Index",
    "Cost of Living Index",
    "Property Price to Income Ratio",
    "Traffic Commute Time Index",
    "Pollution Index",
    "Climate Index"
]

INDEX_LABELS = {
    "Quality of Life Index": "Quality of Life",
    "Purchasing Power Index": "Purchasing Power",
    "Safety Index": "Safety",
    "Health Care Index": "Health Care",
    "Cost of Living Index": "Cost of Living",
    "Property Price to Income Ratio": "Housing Burden",
    "Traffic Commute Time Index": "Commute Time",
    "Pollution Index": "Pollution",
    "Climate Index": "Climate"
}

INDEX_DESCRIPTIONS = {
    "Quality of Life Index": "Overall quality of life score combining multiple factors",
    "Purchasing Power Index": "Relative purchasing power based on average salary",
    "Safety Index": "How safe residents feel (higher = safer)",
    "Health Care Index": "Quality of the health care system (higher = better)",
    "Cost of Living Index": "Relative cost of living including rent (lower = cheaper)",
    "Property Price to Income Ratio": "Ratio of property prices to income (lower = more affordable)",
    "Traffic Commute Time Index": "Average commute time and traffic inefficiency (lower = better)",
    "Pollution Index": "Overall pollution level (lower = cleaner)",
    "Climate Index": "Climate comfort score (higher = more pleasant)"
}

POSITIVE_INDICES = [
    "Quality of Life Index",
    "Purchasing Power Index",
    "Safety Index",
    "Health Care Index",
    "Climate Index"
]

NEGATIVE_INDICES = [
    "Cost of Living Index",
    "Property Price to Income Ratio",
    "Traffic Commute Time Index",
    "Pollution Index"
]

CORE_COMPARE_INDICES = [
    "Quality of Life Index",
    "Safety Index",
    "Health Care Index",
    "Purchasing Power Index",
    "Climate Index"
]

COLORBLIND_SAFE_PALETTE = [
    "#003366", "#E69F00", "#56B4E9", "#009E73",
    "#F0E442", "#0072B2", "#D55E00", "#CC79A7"
]

# ============================================================
# DATA LOADING
# ============================================================

@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv("quality_of_life.csv")
    df.columns = df.columns.str.strip()

    for col in INDICES:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.replace(",", ".", regex=False)
                .str.strip()
                .replace("", np.nan)
            )
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df = df.dropna(subset=["Year"])
    df["Year"] = df["Year"].astype(int)

    if "Rank" in df.columns:
        df["Rank"] = pd.to_numeric(df["Rank"], errors="coerce")

    return df

df = load_data()

# ============================================================
# HELPERS
# ============================================================

def ui_label(index_name: str) -> str:
    return INDEX_LABELS.get(index_name, index_name)

def is_positive_index(index_name: str) -> bool:
    return index_name in POSITIVE_INDICES

def better_direction_text(index_name: str) -> str:
    return "Higher values are better." if is_positive_index(index_name) else "Lower values are better."

def direction_arrow(index_name: str) -> str:
    return "↑ Higher = Better" if is_positive_index(index_name) else "↓ Lower = Better"

def get_sorted_df(data: pd.DataFrame, index_name: str) -> pd.DataFrame:
    ascending = not is_positive_index(index_name)
    return data.sort_values(index_name, ascending=ascending)

def normalize_for_compare(df_source: pd.DataFrame, df_selected: pd.DataFrame, columns: list) -> pd.DataFrame:
    out = df_selected[["Country"] + columns].copy()

    for col in columns:
        col_min = df_source[col].min()
        col_max = df_source[col].max()

        if pd.isna(col_min) or pd.isna(col_max) or col_min == col_max:
            out[col] = 50
            continue

        if col in POSITIVE_INDICES:
            out[col] = (out[col] - col_min) / (col_max - col_min) * 100
        else:
            out[col] = (col_max - out[col]) / (col_max - col_min) * 100

    return out

def make_kpi_card(title, value, subtitle="", variant=""):
    variant_class = f" kpi-card-{variant}" if variant else ""
    st.markdown(
        f"""
        <div class="kpi-card{variant_class}" role="region" aria-label="{title}: {value}">
            <div class="kpi-title">{title}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-sub">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

def build_country_summary(row: pd.Series) -> dict:
    strengths = []
    concerns = []

    if row["Quality of Life Index"] >= 170:
        strengths.append("very high overall quality of life")
    elif row["Quality of Life Index"] >= 150:
        strengths.append("strong overall quality of life")

    if row["Safety Index"] >= 70:
        strengths.append("strong safety conditions")

    if row["Health Care Index"] >= 70:
        strengths.append("good health care performance")

    if row["Climate Index"] >= 80:
        strengths.append("favorable climate conditions")

    if row["Pollution Index"] >= 60:
        concerns.append("higher pollution levels")

    if row["Traffic Commute Time Index"] >= 40:
        concerns.append("longer commute times")

    if row["Property Price to Income Ratio"] >= 10:
        concerns.append("high housing burden")

    if not strengths:
        strengths.append("mixed performance across the selected indicators")

    text = f"**{row['Country']}** shows " + ", ".join(strengths) + "."
    if concerns:
        text += " Potential challenges include " + ", ".join(concerns) + "."

    sentiment = "good"
    if len(concerns) > len(strengths):
        sentiment = "concern"
    elif concerns:
        sentiment = "warn"

    return {"text": text, "sentiment": sentiment}

def chart_alt_text(chart_type: str, description: str) -> None:
    st.markdown(
        f'<div class="sr-only" role="img" aria-label="{chart_type}: {description}" style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0,0,0,0);"></div>',
        unsafe_allow_html=True
    )

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown(
    "<div class='sidebar-title'><i class='bi bi-sliders'></i> Dashboard Controls</div>",
    unsafe_allow_html=True
)

# ── Group 1: Data Selection ──────────────────────────────────
st.sidebar.markdown(
    "<div class='sidebar-filter-group'>"
    "<div class='sidebar-group-header'><i class='bi bi-database'></i> Data Selection</div>"
    "</div>",
    unsafe_allow_html=True
)

years = sorted(df["Year"].dropna().unique())
selected_year = st.sidebar.selectbox("Select Year", years, index=len(years)-1)

df_year = df[df["Year"] == selected_year].copy()
all_countries = sorted(df_year["Country"].dropna().unique())

default_countries = []
for c in ["Germany", "Switzerland", "Netherlands", "Denmark", "Austria"]:
    if c in all_countries:
        default_countries.append(c)

if not default_countries:
    default_countries = all_countries[:4]

if "selected_countries_state" not in st.session_state:
    st.session_state.selected_countries_state = default_countries.copy()

st.session_state.selected_countries_state = [
    c for c in st.session_state.selected_countries_state if c in all_countries
]

if not st.session_state.selected_countries_state:
    st.session_state.selected_countries_state = default_countries.copy()

MAX_COMPARE_COUNTRIES = 8

with st.sidebar.popover("Select the countries to compare", use_container_width=True):
    st.caption(f"Select up to {MAX_COMPARE_COUNTRIES} countries to compare.")

    pop_c1, pop_c2 = st.columns(2)
    with pop_c1:
        if st.button("Select all", use_container_width=True, key="sel_all"):
            st.session_state.selected_countries_state = all_countries[:MAX_COMPARE_COUNTRIES]
            st.rerun()
    with pop_c2:
        if st.button("Clear all", use_container_width=True, key="clr_all"):
            st.session_state.selected_countries_state = []
            st.rerun()

    country_search = st.text_input(
        "Search country",
        placeholder="Type to filter...",
        key="country_search_sidebar"
    )

    if country_search:
        visible_countries = [
            c for c in all_countries
            if country_search.lower() in c.lower()
        ]
    else:
        visible_countries = all_countries

    new_selection = []
    for country in visible_countries:
        checked = country in st.session_state.selected_countries_state
        is_selected = st.checkbox(country, value=checked, key=f"country_chk_{country}")
        if is_selected:
            new_selection.append(country)

    hidden_selected = [
        c for c in st.session_state.selected_countries_state
        if c not in visible_countries
    ]
    st.session_state.selected_countries_state = hidden_selected + new_selection

selected_countries = st.session_state.selected_countries_state

if selected_countries:
    st.sidebar.caption(f"{len(selected_countries)} of {len(all_countries)} countries selected")
else:
    st.sidebar.warning("No country selected — please select at least one.")

# ── Group 2: Display Settings ────────────────────────────────
st.sidebar.markdown(
    "<div class='sidebar-filter-group'>"
    "<div class='sidebar-group-header'><i class='bi bi-gear'></i> Display Settings</div>"
    "</div>",
    unsafe_allow_html=True
)

selected_index = st.sidebar.selectbox(
    "Main Indicator",
    INDICES,
    index=0,
    format_func=ui_label,
    help=INDEX_DESCRIPTIONS.get(INDICES[0], "")
)

st.sidebar.caption(f"*{direction_arrow(selected_index)}*")

top_n = st.sidebar.slider("Top N countries", 5, min(40, len(df_year)), 15)

show_bottom = st.sidebar.checkbox("Show Bottom 10 panel", value=True)

# ── Reset Filters ────────────────────────────────────────────
st.sidebar.markdown("<br>", unsafe_allow_html=True)
if st.sidebar.button("Reset all filters", use_container_width=True):
    st.session_state.selected_countries_state = default_countries.copy()
    st.rerun()

# ── Page Guide ────────────────────────────────────────────────
st.sidebar.markdown("<br>", unsafe_allow_html=True)
st.sidebar.markdown(
    "<div class='sidebar-section-label'><i class='bi bi-signpost-split'></i> Page Guide</div>",
    unsafe_allow_html=True
)
st.sidebar.markdown(
    """
    <div class='sidebar-help'>
    <b>Overview</b> — global snapshot for the selected year<br>
    <b>Compare</b> — side-by-side country comparison<br>
    <b>Drivers</b> — correlations between indicators<br>
    <b>Trends</b> — changes over time<br>
    <b>Data Explorer</b> — inspect and export data<br>
    <b>About & Help</b> — how to use this dashboard
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown("<hr>", unsafe_allow_html=True)
st.sidebar.caption("Source: Kaggle – Quality of Life Index")

df_compare = df_year[df_year["Country"].isin(selected_countries)] if selected_countries else df_year.copy()

# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<a class="skip-link" href="#main-content">Skip to main content</a>',
    unsafe_allow_html=True
)

st.markdown("""
<h1 class='app-title' id='main-content'><i class='bi bi-globe-asia-australia' style='font-size:35px;vertical-align:middle;margin-right:6px;background:linear-gradient(135deg,#003366,#A4D65E);-webkit-background-clip:text;-webkit-text-fill-color:transparent'></i>Quality of Life Across Countries</h1>
""", unsafe_allow_html=True)
st.markdown(
    "<p class='app-subtitle'>Explore how countries compare in quality of life, safety, health care, affordability, climate and environmental conditions.</p>",
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <div class='small-note' role='status' aria-live='polite'>
        Year: <b>{selected_year}</b>
        &nbsp;&nbsp;|&nbsp;&nbsp;
        Countries selected: <b>{len(selected_countries)}</b>
        &nbsp;&nbsp;|&nbsp;&nbsp;
        Main indicator: <b>{ui_label(selected_index)}</b>
        &nbsp;&nbsp;({direction_arrow(selected_index)})
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(" ")
st.markdown(" ")

# ============================================================
# TOP NAVIGATION
# ============================================================

selected = option_menu(
    menu_title=None,
    options=[
        "Overview",
        "Compare Countries",
        "Explore Drivers",
        "Trends",
        "Data Explorer",
        "About & Help"
    ],
    icons=[
        "house-fill",
        "globe-asia-australia",
        "compass-fill",
        "bar-chart-line-fill",
        "database-fill-gear",
        "info-circle-fill"
    ],
    orientation="horizontal",

    styles={
        "container": {
            "padding": "0.25rem 0",
            "background-color": "#ffffff",
            "margin-bottom": "1.25rem",
            "border-bottom": "2px solid #d0d5d9",
            "border-radius": "0",
        },
        "icon": {
            "color": "#003366",
            "font-size": "14px",
            "margin-right": "3px",
        },
        "nav-link": {
            "font-size": "14px",
            "font-weight": "600",
            "color": "#003366",
            "padding": "12px 18px",
            "border-radius": "0",
            "border-bottom": "3px solid transparent",
            "white-space": "nowrap",
        },
        "nav-link-selected": {
            "background-color": "transparent",
            "color": "#003366",
            "border-bottom": "3px solid #4B8B3B",
            "font-weight": "700",
            "border-radius": "0",
        },
    }
)

# ============================================================
# TAB 1 — OVERVIEW
# ============================================================

if selected == "Overview":
    st.header("Overview")
    st.markdown(
        "<p class='tab-desc'>A high-level snapshot of global quality of life for the selected year — top performers, key metrics and geographic distribution.</p>",
        unsafe_allow_html=True
    )

    sorted_qol = df_year.sort_values("Quality of Life Index", ascending=False)
    best_country = sorted_qol.iloc[0]
    avg_qol = df_year["Quality of Life Index"].mean()
    safest_country = df_year.sort_values("Safety Index", ascending=False).iloc[0]
    cleanest_country = df_year.sort_values("Pollution Index", ascending=True).iloc[0]

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        make_kpi_card(
            "Best Quality of Life",
            best_country["Country"],
            f"{best_country['Quality of Life Index']:.1f} points",
        )
    with k2:
        make_kpi_card(
            "Average Quality of Life",
            f"{avg_qol:.1f}",
            "Mean score across all countries"
        )
    with k3:
        make_kpi_card(
            "Safest Country",
            safest_country["Country"],
            f"Safety score: {safest_country['Safety Index']:.1f}"
        )
    with k4:
        make_kpi_card(
            "Lowest Pollution",
            cleanest_country["Country"],
            f"Pollution score: {cleanest_country['Pollution Index']:.1f}"
        )

    st.markdown("")

    # ── RANKING ──────────────────────────────────────────────
    st.subheader(f"Top {top_n} Countries by {ui_label(selected_index)}")
    st.caption(f"{direction_arrow(selected_index)}")

    top_df = get_sorted_df(df_year, selected_index).head(top_n).copy()
    top_df["Rank Position"] = range(1, len(top_df) + 1)

    chart_alt_text("Bar chart", f"Top {top_n} countries ranked by {ui_label(selected_index)} for {selected_year}")

    fig_rank = px.bar(
        top_df,
        x=selected_index,
        y="Country",
        orientation="h",
        text=selected_index,
        color=selected_index,
        color_continuous_scale=[[0, "#B3D4F0"], [0.3, "#6AAED6"], [0.55, "#005B99"], [0.8, "#003366"], [1, "#001F3F"]] if is_positive_index(selected_index) else [[0, "#F5C6C6"], [0.3, "#E88B8B"], [0.55, "#D94F4F"], [0.8, "#B22222"], [1, "#9B1B30"]],
        hover_data={
            "Country": True,
            selected_index: ':.2f',
            "Quality of Life Index": ':.2f',
            "Safety Index": ':.2f',
            "Health Care Index": ':.2f',
            "Pollution Index": ':.2f'
        }
    )

    fig_rank.update_traces(texttemplate="%{text:.1f}", textposition="outside")
    fig_rank.update_layout(
        height=max(400, top_n * 32),
        yaxis=dict(autorange="reversed"),
        coloraxis_showscale=False,
        margin=dict(l=10, r=20, t=20, b=10),
        xaxis_title=ui_label(selected_index),
        yaxis_title="",
        plot_bgcolor="#FAFBFC",
        paper_bgcolor="#FAFBFC"
    )
    st.plotly_chart(fig_rank, use_container_width=True)

    st.caption(
        f"{ui_label(selected_index)} ranking for {selected_year}. {better_direction_text(selected_index)}"
    )

    st.markdown("<div style='height: 1.0rem;'></div>", unsafe_allow_html=True)

    # ── WORLD MAP ────────────────────────────────────────────
    with st.expander("World Map — Geographic Distribution", expanded=True):
        st.subheader(f"World Map — {ui_label(selected_index)}")

        chart_alt_text("Choropleth map", f"World map showing {ui_label(selected_index)} distribution across countries in {selected_year}")

        map_scale_positive = [[0, "#EAEDED"], [0.25, "#A4D65E"], [0.5, "#0096D6"], [0.75, "#005B99"], [1, "#001F3F"]]
        map_scale_negative = [[0, "#EAEDED"], [0.25, "#F1C40F"], [0.5, "#FFAB40"], [0.75, "#FF6347"], [1, "#9B1B30"]]
        map_scale = map_scale_positive if is_positive_index(selected_index) else map_scale_negative

        fig_map = px.choropleth(
            df_year,
            locations="Country",
            locationmode="country names",
            color=selected_index,
            hover_name="Country",
            hover_data={
                "Quality of Life Index": ':.2f',
                "Safety Index": ':.2f',
                "Health Care Index": ':.2f',
                "Pollution Index": ':.2f',
                selected_index: ':.2f'
            },
            color_continuous_scale=map_scale
        )

        fig_map.update_layout(
            height=550,
            margin=dict(l=0, r=0, t=20, b=0),
            plot_bgcolor="#FAFBFC",
            paper_bgcolor="#FAFBFC",
            geo=dict(
                bgcolor="#FAFBFC",
                lakecolor="#EAEDED",
                landcolor="#EAEDED",
                showocean=True,
                oceancolor="#E3F0FA"
            )
        )
        st.plotly_chart(fig_map, use_container_width=True)

        st.caption(
            "Geographic overview of the selected indicator. Hover over countries for details."
        )

    # ── Bottom performers (Progressive Disclosure) ───────────
    if show_bottom:
        with st.expander("Bottom 10 Countries", expanded=False):
            st.subheader(f"Bottom 10 Countries by {ui_label(selected_index)}")

            bottom_df = get_sorted_df(df_year, selected_index).tail(10).copy()
            bottom_df = bottom_df.sort_values(selected_index, ascending=is_positive_index(selected_index))

            chart_alt_text("Bar chart", f"Bottom 10 countries by {ui_label(selected_index)} for {selected_year}")

            fig_bottom = px.bar(
                bottom_df,
                x=selected_index,
                y="Country",
                orientation="h",
                text=selected_index,
                color=selected_index,
                color_continuous_scale=[[0, "#F5C6C6"], [0.3, "#E88B8B"], [0.55, "#D94F4F"], [0.8, "#B22222"], [1, "#9B1B30"]]
            )
            fig_bottom.update_traces(texttemplate="%{text:.1f}", textposition="outside")
            fig_bottom.update_layout(
                height=420,
                coloraxis_showscale=False,
                margin=dict(l=10, r=20, t=20, b=10),
                xaxis_title=ui_label(selected_index),
                yaxis_title="",
                plot_bgcolor="#FAFBFC",
                paper_bgcolor="#FAFBFC"
            )
            st.plotly_chart(fig_bottom, use_container_width=True)


# ============================================================
# TAB 2 — COMPARE COUNTRIES
# ============================================================

elif selected == "Compare Countries":
    st.header("Compare Countries")
    st.markdown(
        "<p class='tab-desc'>Compare countries directly using normalized scores, head-to-head heatmaps and a country profile drill-down. All scores are normalized to 0–100 where higher always means better.</p>",
        unsafe_allow_html=True
    )

    if not selected_countries:
        st.warning("Please select at least one country in the sidebar.")
    else:
        if len(selected_countries) > MAX_COMPARE_COUNTRIES:
            st.warning(f"You have selected {len(selected_countries)} countries. Only the first {MAX_COMPARE_COUNTRIES} will be shown for readability.")
            display_countries = selected_countries[:MAX_COMPARE_COUNTRIES]
        else:
            display_countries = selected_countries

        compare_cols = st.columns([1.1, 1])

        # ── LEFT: Normalized grouped comparison ──────────────
        with compare_cols[0]:
            st.subheader("Normalized Country Comparison")

            compare_base = df_year[df_year["Country"].isin(display_countries)][["Country"] + CORE_COMPARE_INDICES]
            compare_norm = normalize_for_compare(df_year, compare_base, CORE_COMPARE_INDICES)

            compare_long = compare_norm.melt(
                id_vars="Country",
                var_name="Index",
                value_name="Score"
            )
            compare_long["Index"] = compare_long["Index"].map(ui_label)

            chart_alt_text("Grouped bar chart", f"Normalized comparison of {len(display_countries)} countries across core indicators")

            fig_compare = px.bar(
                compare_long,
                x="Index",
                y="Score",
                color="Country",
                barmode="group",
                text="Score",
                hover_data={"Score": ':.1f'},
                color_discrete_sequence=COLORBLIND_SAFE_PALETTE
            )
            fig_compare.update_traces(texttemplate="%{text:.0f}", textposition="outside")
            fig_compare.update_layout(
                height=540,
                yaxis_title="Normalized score (0–100)",
                xaxis_title="",
                legend_title="Country",
                margin=dict(l=10, r=10, t=20, b=10),
                plot_bgcolor="#FAFBFC",
                paper_bgcolor="#FAFBFC"
            )
            st.plotly_chart(fig_compare, use_container_width=True)

            st.caption(
                "Each group of bars compares the selected countries on one indicator. Taller bars mean stronger performance — scores are normalized to 0–100."
            )

        # ── RIGHT: Radar chart ───────────────────────────────
        with compare_cols[1]:
            st.subheader("Radar Comparison")

            radar_cols = [
                "Quality of Life Index",
                "Safety Index",
                "Health Care Index",
                "Purchasing Power Index",
                "Climate Index"
            ]
            radar_df = df_year[df_year["Country"].isin(display_countries)][["Country"] + radar_cols]
            radar_norm = normalize_for_compare(df_year, radar_df, radar_cols)

            chart_alt_text("Radar chart", f"Radar profile of {len(display_countries)} countries across 5 core indicators")

            fig_radar = go.Figure()
            radar_labels = [ui_label(c_) for c_ in radar_cols]

            for i, country in enumerate(display_countries):
                row = radar_norm[radar_norm["Country"] == country]
                if row.empty:
                    continue

                values = row[radar_cols].iloc[0].tolist()
                values += values[:1]

                color = COLORBLIND_SAFE_PALETTE[i % len(COLORBLIND_SAFE_PALETTE)]
                r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
                fill_color = f"rgba({r},{g},{b},0.15)"

                fig_radar.add_trace(go.Scatterpolar(
                    r=values,
                    theta=radar_labels + [radar_labels[0]],
                    fill="toself",
                    name=country,
                    line=dict(width=2.5, color=color),
                    fillcolor=fill_color,
                    marker=dict(size=5, color=color)
                ))

            fig_radar.update_layout(
                height=540,
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 100], gridcolor="#d0d5d9", linecolor="#d0d5d9", tickfont=dict(size=10, color="#555555")),
                    angularaxis=dict(gridcolor="#d0d5d9", linecolor="#d0d5d9", tickfont=dict(size=12, color="#003366")),
                    bgcolor="#FAFBFC"
                ),
                margin=dict(l=60, r=60, t=30, b=30),
                paper_bgcolor="#FAFBFC",
                legend=dict(font=dict(size=12))
            )
            st.plotly_chart(fig_radar, use_container_width=True)

            st.caption(
                "A wider shape means more balanced performance. Spikes and dips highlight standout strengths and weaknesses."
            )

        # ── Head-to-head comparison ──────────────────────────
        st.markdown("---")
        st.subheader("Head-to-Head Country Drill-down")

        c1, c2 = st.columns(2)
        with c1:
            country_a = st.selectbox("Country A", all_countries, index=0, key="country_a")
        with c2:
            filtered_b = [c for c in all_countries if c != country_a]
            country_b = st.selectbox("Country B", filtered_b, index=0, key="country_b")

        row_a = df_year[df_year["Country"] == country_a]
        row_b = df_year[df_year["Country"] == country_b]

        if row_a.empty or row_b.empty:
            st.warning("One or both countries are not available in the selected year.")
        else:
            h2h = pd.concat([row_a, row_b])[["Country"] + INDICES].copy()
            h2h_norm = normalize_for_compare(df_year, h2h, INDICES).set_index("Country")
            h2h_display = h2h_norm.copy()
            h2h_display.columns = [ui_label(c) for c in h2h_display.columns]

            chart_alt_text("Heatmap", f"Head-to-head comparison between {country_a} and {country_b}")

            fig_h2h = px.imshow(
                h2h_display,
                text_auto=".0f",
                color_continuous_scale="YlGn",
                zmin=0,
                zmax=100,
                aspect="auto"
            )
            fig_h2h.update_layout(
                height=280,
                margin=dict(l=0, r=0, t=30, b=0),
                coloraxis_colorbar=dict(title="Score")
            )
            st.plotly_chart(fig_h2h, use_container_width=True)

            st.caption(
                "Normalized comparison (0–100). Higher scores always indicate better performance."
            )

        # ── Country profile drill-down ───────────────────────
        st.markdown("---")
        with st.expander("Country Profile Drill-down", expanded=False):
            st.subheader("Country Profile Drill-down")

            profile_country = st.selectbox(
                "Select a country to inspect in detail",
                all_countries,
                index=all_countries.index(selected_countries[0]) if selected_countries and selected_countries[0] in all_countries else 0
            )

            row = df_year[df_year["Country"] == profile_country]
            if not row.empty:
                row = row.iloc[0]

                summary = build_country_summary(row)
                box_class = {"good": "good-box", "warn": "warn-box", "concern": "concern-box"}.get(summary["sentiment"], "good-box")

                st.markdown(
                    f'<div class="{box_class}">{summary["text"]}</div>',
                    unsafe_allow_html=True
                )

                p1, p2, p3, p4 = st.columns(4)
                with p1:
                    make_kpi_card("Quality of Life", f"{row['Quality of Life Index']:.1f}", "Overall score", variant="outline")
                with p2:
                    make_kpi_card("Safety", f"{row['Safety Index']:.1f}", "Higher = safer", variant="outline")
                with p3:
                    make_kpi_card("Health Care", f"{row['Health Care Index']:.1f}", "Higher = better", variant="outline")
                with p4:
                    make_kpi_card("Pollution", f"{row['Pollution Index']:.1f}", "Lower = better", variant="outline")

                st.markdown("")

                profile_df = pd.DataFrame({
                    "Indicator": [ui_label(i) for i in INDICES],
                    "Direction": [direction_arrow(i) for i in INDICES],
                    "Raw value": [row[i] for i in INDICES]
                })

                avg_vals = df_year[INDICES].mean()
                profile_df["Difference vs. average"] = [
                    row[ind] - avg_vals[ind] for ind in INDICES
                ]

                st.dataframe(
                    profile_df.style.format({
                        "Raw value": "{:.2f}",
                        "Difference vs. average": "{:+.2f}"
                    }).background_gradient(subset=["Difference vs. average"], cmap="RdYlGn"),
                    use_container_width=True
                )

# ============================================================
# TAB 3 — EXPLORE DRIVERS
# ============================================================

elif selected == "Explore Drivers":
    st.header("Explore Drivers")
    st.markdown(
        "<p class='tab-desc'>Explore relationships between indicators. Useful for finding patterns — but correlation does not prove causation.</p>",
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="insight-box">
        <b>How to read this section:</b> First check the correlation heatmap to see which indicators move together.
        Then use the scatter plot below to explore a specific relationship in detail.
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.expander("Correlation Heatmap", expanded=True):
        st.subheader("Correlation Heatmap")

        chart_alt_text("Heatmap", "Correlation matrix showing pairwise relationships between all quality of life indicators")

        corr = df_year[INDICES].corr()
        corr.index = [ui_label(i) for i in corr.index]
        corr.columns = [ui_label(i) for i in corr.columns]

        fig_corr = px.imshow(
            corr,
            text_auto=".2f",
            color_continuous_scale="RdBu_r",
            zmin=-1,
            zmax=1,
            aspect="auto"
        )
        fig_corr.update_layout(
            height=550,
            margin=dict(l=10, r=10, t=20, b=10)
        )
        st.plotly_chart(fig_corr, use_container_width=True)

        st.caption(
            "Values near +1 = strong positive relationship, near −1 = strong negative, near 0 = little relationship."
        )

    st.markdown("---")
    st.subheader("Scatter Plot with Trend Line")

    s1, s2, s3 = st.columns([1, 1, 1])
    with s1:
        x_axis = st.selectbox("X-axis indicator", INDICES, index=1, format_func=ui_label, help=INDEX_DESCRIPTIONS.get(INDICES[1], ""))
    with s2:
        y_axis = st.selectbox("Y-axis indicator", INDICES, index=0, format_func=ui_label, help=INDEX_DESCRIPTIONS.get(INDICES[0], ""))
    with s3:
        bubble_size = st.selectbox(
            "Bubble size (optional)",
            ["None"] + INDICES,
            index=0,
            format_func=lambda x: "None" if x == "None" else ui_label(x)
        )

    scatter_kwargs = {}
    if bubble_size != "None":
        scatter_kwargs["size"] = bubble_size

    chart_alt_text("Scatter plot", f"Relationship between {ui_label(x_axis)} and {ui_label(y_axis)}")

    fig_scatter = px.scatter(
        df_year,
        x=x_axis,
        y=y_axis,
        hover_name="Country",
        color="Quality of Life Index",
        color_continuous_scale="Viridis",
        trendline="ols",
        hover_data={col: ':.2f' for col in INDICES},
        **scatter_kwargs
    )

    fig_scatter.update_layout(
        height=520,
        xaxis_title=f"{ui_label(x_axis)} ({direction_arrow(x_axis)})",
        yaxis_title=f"{ui_label(y_axis)} ({direction_arrow(y_axis)})",
        margin=dict(l=10, r=10, t=20, b=10)
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

    st.caption(
        f"Hover over points to inspect countries. {ui_label(x_axis)} vs. {ui_label(y_axis)}."
    )

    if x_axis != y_axis:
        corr_value = df_year[[x_axis, y_axis]].corr().iloc[0, 1]
        strength = "strong" if abs(corr_value) > 0.6 else "moderate" if abs(corr_value) > 0.3 else "weak"
        relation = "positive" if corr_value > 0 else "negative"
        st.markdown(
            f"""
            <div class="section-box">
            <b>Interpretation:</b> The correlation between <b>{ui_label(x_axis)}</b> and <b>{ui_label(y_axis)}</b>
            is <b>{corr_value:.2f}</b> — a <b>{strength} {relation}</b> relationship.
            This does not imply causation.
            </div>
            """,
            unsafe_allow_html=True
        )

# ============================================================
# TAB 4 — TRENDS
# ============================================================

elif selected == "Trends":
    st.header("Trends")
    st.markdown(
        "<p class='tab-desc'>Track how indicators change over time for selected countries.</p>",
        unsafe_allow_html=True
    )

    if not selected_countries:
        st.warning("Please select at least one country in the sidebar.")
    else:
        df_trend = df[df["Country"].isin(selected_countries)].copy()

        st.subheader(f"Trend of {ui_label(selected_index)} Over Time")
        st.caption(f"{direction_arrow(selected_index)}")

        chart_alt_text("Line chart", f"Trend of {ui_label(selected_index)} over time for {len(selected_countries)} countries")

        fig_trend = px.line(
            df_trend,
            x="Year",
            y=selected_index,
            color="Country",
            markers=True,
            hover_data={col: ':.2f' for col in INDICES},
            color_discrete_sequence=COLORBLIND_SAFE_PALETTE
        )
        fig_trend.update_traces(line=dict(width=2.5), marker=dict(size=7))
        fig_trend.update_layout(
            height=480,
            yaxis_title=ui_label(selected_index),
            margin=dict(l=10, r=10, t=20, b=10),
            plot_bgcolor="#FAFBFC",
            paper_bgcolor="#FAFBFC",
            xaxis=dict(gridcolor="#EAEDED"),
            yaxis=dict(gridcolor="#EAEDED")
        )
        st.plotly_chart(fig_trend, use_container_width=True)

        st.caption(
            f"Rising lines signal progress, falling lines highlight areas of concern."
        )

        with st.expander("Change Summary Table", expanded=False):
            changes = []
            for country in selected_countries:
                c_df = df_trend[df_trend["Country"] == country].sort_values("Year")
                if len(c_df) >= 2:
                    start_val = c_df[selected_index].iloc[0]
                    end_val = c_df[selected_index].iloc[-1]

                    if pd.notna(start_val) and pd.notna(end_val) and start_val != 0:
                        pct = ((end_val - start_val) / start_val) * 100
                    else:
                        pct = np.nan

                    changes.append({
                        "Country": country,
                        "Start Year": int(c_df["Year"].iloc[0]),
                        "End Year": int(c_df["Year"].iloc[-1]),
                        "Start Value": round(start_val, 2),
                        "End Value": round(end_val, 2),
                        "Absolute Change": round(end_val - start_val, 2),
                        "Percent Change": round(pct, 1) if pd.notna(pct) else np.nan
                    })

            if changes:
                changes_df = pd.DataFrame(changes).sort_values("Absolute Change", ascending=False)
                st.dataframe(
                    changes_df.style.format({
                        "Start Value": "{:.2f}",
                        "End Value": "{:.2f}",
                        "Absolute Change": "{:+.2f}",
                        "Percent Change": "{:+.1f}%"
                    }).background_gradient(subset=["Absolute Change"], cmap="RdYlGn"),
                    use_container_width=True
                )

        # ── Single-Country Trend Drill-down ──────────────────
        st.markdown("---")
        with st.expander("Single-Country Trend Drill-down", expanded=False):
            st.subheader("Single-Country Multi-Indicator Trend")

            trend_country = st.selectbox(
                "Select one country for a detailed multi-indicator trend view",
                all_countries,
                index=all_countries.index(selected_countries[0]) if selected_countries and selected_countries[0] in all_countries else 0
            )

            chart_alt_text("Multi-line chart", f"All indicators over time for {trend_country}")

            one_country = df[df["Country"] == trend_country][["Year", "Country"] + INDICES].copy()
            long_country = one_country.melt(
                id_vars=["Year", "Country"],
                var_name="Indicator",
                value_name="Value"
            )
            long_country["Indicator"] = long_country["Indicator"].map(ui_label)

            fig_country_trend = px.line(
                long_country,
                x="Year",
                y="Value",
                color="Indicator",
                markers=True,
                color_discrete_sequence=COLORBLIND_SAFE_PALETTE + ["#999999"]
            )
            fig_country_trend.update_traces(line=dict(width=2.5), marker=dict(size=6))
            fig_country_trend.update_layout(
                height=480,
                yaxis_title="Value",
                margin=dict(l=10, r=10, t=20, b=10),
                plot_bgcolor="#FAFBFC",
                paper_bgcolor="#FAFBFC",
                xaxis=dict(gridcolor="#EAEDED"),
                yaxis=dict(gridcolor="#EAEDED"),
                legend=dict(font=dict(size=11))
            )
            st.plotly_chart(fig_country_trend, use_container_width=True)

            st.caption(
                f"All indicators for {trend_country} over time. Compare quality of life, safety, health care, affordability and environmental metrics."
            )

# ============================================================
# TAB 5 — DATA EXPLORER
# ============================================================

elif selected == "Data Explorer":
    st.header("Data Explorer")
    st.markdown(
        "<p class='tab-desc'>Search, filter and export the raw data behind the dashboard.</p>",
        unsafe_allow_html=True
    )

    all_col_options = ["Country", "Year"] + INDICES
    default_cols = ["Country", "Year", "Quality of Life Index", "Safety Index", "Health Care Index"]

    if "selected_cols_state" not in st.session_state:
        st.session_state.selected_cols_state = default_cols.copy()

    c1, c2 = st.columns([1, 1])
    with c1:
        with st.popover("Search country", use_container_width=True):
            search_country = st.text_input(
                "Search for a country",
                placeholder="Type to filter...",
                key="explorer_country_search"
            )
    with c2:
        with st.popover("Choose columns to display", use_container_width=True):
            st.caption("Select which columns appear in the table below.")
            new_col_selection = []
            for col in all_col_options:
                label = ui_label(col) if col in INDEX_LABELS else col
                checked = col in st.session_state.selected_cols_state
                if st.checkbox(label, value=checked, key=f"col_chk_{col}"):
                    new_col_selection.append(col)
            st.session_state.selected_cols_state = new_col_selection

    selected_cols = st.session_state.selected_cols_state
    if not selected_cols:
        selected_cols = ["Country", "Year"]

    df_display = df_year.copy()

    if search_country:
        df_display = df_display[df_display["Country"].str.contains(search_country, case=False, na=False)]

    subset_mode = st.radio(
        "Dataset scope",
        ["All countries in selected year", "Selected countries only"],
        horizontal=True,
        help="Choose whether to show all countries or only those selected in the sidebar."
    )

    if subset_mode == "Selected countries only" and selected_countries:
        df_display = df_display[df_display["Country"].isin(selected_countries)]

    display_table = df_display[selected_cols].copy()
    if "Quality of Life Index" in selected_cols:
        display_table = display_table.sort_values("Quality of Life Index", ascending=False)

    st.dataframe(
        display_table.style.background_gradient(
            subset=[c for c in selected_cols if c in INDICES],
            cmap="YlGn"
        ).format("{:.2f}", subset=[c for c in selected_cols if c in INDICES]),
        use_container_width=True,
        height=520
    )

    st.markdown("### Dataset Summary")
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        make_kpi_card("Countries in View", f"{len(df_display)}", "Rows in the filtered table", variant="outline")
    with m2:
        make_kpi_card("Average QoL", f"{df_display['Quality of Life Index'].mean():.1f}", "Filtered dataset", variant="outline")
    with m3:
        make_kpi_card("Highest QoL", f"{df_display['Quality of Life Index'].max():.1f}", "Filtered dataset", variant="outline")
    with m4:
        make_kpi_card("Lowest QoL", f"{df_display['Quality of Life Index'].min():.1f}", "Filtered dataset", variant="outline")

    st.markdown("### Export")
    csv_filtered = df_display.to_csv(index=False).encode("utf-8")
    downloaded = st.download_button(
        label="Download filtered data as CSV",
        data=csv_filtered,
        file_name=f"quality_of_life_filtered_{selected_year}.csv",
        mime="text/csv"
    )
    if downloaded:
        st.markdown(
            '<div class="success-box">CSV downloaded successfully.</div>',
            unsafe_allow_html=True
        )

# ============================================================
# TAB 6 — ABOUT & HELP
# ============================================================

elif selected == "About & Help":
    st.header("About & Help")

    st.markdown(
        """
        <div class="section-box">
        <b>What this dashboard does</b><br>
        This dashboard helps explore and compare countries using the Quality of Life dataset.
        It supports ranking, country comparison, trend analysis and correlation exploration.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader("Quick Start Guide")
    st.markdown("""
1. **Choose a year** and one **main indicator** in the sidebar on the left.
2. **Select countries** to compare using the country selector in the sidebar.
3. Start in **Overview** to see top performers and the world map.
4. Open **Compare Countries** to compare selected countries with normalized scores and head-to-head analysis.
5. Use **Explore Drivers** to understand relationships between indicators.
6. Use **Trends** to see how countries changed over time.
7. Use **Data Explorer** for the raw table and CSV export.
""")

    st.subheader("Understanding the Indicators")
    indicator_df = pd.DataFrame({
        "Indicator": [ui_label(i) for i in INDICES],
        "Direction": [direction_arrow(i) for i in INDICES],
        "Description": [INDEX_DESCRIPTIONS.get(i, "") for i in INDICES]
    })
    st.dataframe(indicator_df, use_container_width=True, hide_index=True)

    st.subheader("Interpretation Notes")
    st.markdown("""
- **Quality of Life, Safety, Health Care, Purchasing Power and Climate** are indicators where **higher values are better**.
- **Pollution, Commute Time and Housing Burden** are indicators where **lower values are better**.
- In normalized comparison views, negative indicators are automatically inverted so that **higher normalized scores always mean better performance**.
- Correlation charts show **relationships**, not causality.
""")

    st.subheader("Data Source")
    st.markdown("Kaggle – Quality of Life Index dataset")

    st.subheader("Built With")
    st.markdown("Python, Streamlit, Pandas, Plotly, NumPy")

    st.markdown(
        '<div class="success-box">Thank you for exploring the Quality of Life Dashboard!</div>',
        unsafe_allow_html=True
    )

# ============================================================
# FOOTER
# ============================================================

st.markdown("---")
st.markdown(
    "<div class='footer-note'>Quality of Life Dashboard — built with usability principles from ISO 9241-110, Nielsen's Heuristics, and Shneiderman's Golden Rules.</div>",
    unsafe_allow_html=True
)
