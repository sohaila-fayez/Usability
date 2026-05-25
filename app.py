import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff

# --------------------------------
# Seitenkonfiguration
# --------------------------------
st.set_page_config(
    page_title="Life Quality Dashboard",
    page_icon="🌍",
    layout="wide"
)

# --------------------------------
# Titel
# --------------------------------
st.title("🌍 Länder-Ranking Dashboard")
st.subheader("Quality of Life Analyse")

# --------------------------------
# CSV-Datei laden
# --------------------------------
df = pd.read_csv("quality_of_life.csv")

# --------------------------------
# Sidebar
# --------------------------------
st.sidebar.header("🔍 Filter")

# Jahr Filter
years = sorted(df["Year"].unique())

selected_year = st.sidebar.selectbox(
    "Jahr auswählen",
    years
)

# Länder Filter
countries = sorted(df["Country"].unique())

selected_countries = st.sidebar.multiselect(
    "Länder auswählen",
    countries,
    default=countries[:5]
)

# Daten filtern
filtered_df = df[
    (df["Year"] == selected_year)
]

# --------------------------------
# Suchfunktion
# --------------------------------
search_country = st.sidebar.text_input(
    "Land suchen"
)

if search_country:
    filtered_df = filtered_df[
        filtered_df["Country"].str.contains(
            search_country,
            case=False
        )
    ]

# --------------------------------
# KPI Karten
# --------------------------------
st.header("📊 KPI Übersicht")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Durchschnitt Quality of Life",
    round(filtered_df["Quality of Life Index"].mean(), 2)
)

col2.metric(
    "Durchschnitt Sicherheit",
    round(filtered_df["Safety Index"].mean(), 2)
)

col3.metric(
    "Durchschnitt Kaufkraft",
    round(filtered_df["Purchasing Power Index"].mean(), 2)
)

col4.metric(
    "Anzahl Länder",
    filtered_df["Country"].nunique()
)

# --------------------------------
# Tabs
# --------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📋 Datensatz",
    "🏆 Rankings",
    "📈 Diagramme",
    "🔥 Heatmap",
    "📊 Statistik"
])

# --------------------------------
# TAB 1 - Datensatz
# --------------------------------
with tab1:

    st.header("Datensatz")

    st.dataframe(filtered_df)

    # CSV Download
    csv = filtered_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇ CSV herunterladen",
        csv,
        "filtered_data.csv",
        "text/csv"
    )

# --------------------------------
# TAB 2 - Rankings
# --------------------------------
with tab2:

    st.header("Top 10 Länder")

    top10 = filtered_df.sort_values(
        by="Quality of Life Index",
        ascending=False
    ).head(10)

    st.dataframe(top10)

    fig_bar = px.bar(
        top10,
        x="Country",
        y="Quality of Life Index",
        color="Quality of Life Index",
        title="Top 10 Länder nach Lebensqualität",
        text_auto=True
    )

    st.plotly_chart(fig_bar, use_container_width=True)

# --------------------------------
# TAB 3 - Diagramme
# --------------------------------
with tab3:

    st.header("Visualisierungen")

    # Scatterplot
    fig_scatter = px.scatter(
        filtered_df,
        x="Purchasing Power Index",
        y="Quality of Life Index",
        size="Safety Index",
        color="Cost of Living Index",
        hover_name="Country",
        title="Kaufkraft vs Lebensqualität"
    )

    st.plotly_chart(fig_scatter, use_container_width=True)

    # Line Chart
    st.subheader("Entwicklung über Jahre")

    selected_country = st.selectbox(
        "Land auswählen",
        countries
    )

    country_df = df[df["Country"] == selected_country]

    fig_line = px.line(
        country_df,
        x="Year",
        y="Quality of Life Index",
        markers=True,
        title=f"Entwicklung des Quality of Life Index: {selected_country}"
    )

    st.plotly_chart(fig_line, use_container_width=True)

# --------------------------------
# TAB 4 - Heatmap
# --------------------------------
with tab4:

    st.header("Korrelations-Heatmap")

    correlation = filtered_df.select_dtypes(
        include=["number"]
    ).corr()

    fig_heatmap = ff.create_annotated_heatmap(
        z=correlation.values,
        x=list(correlation.columns),
        y=list(correlation.index),
        annotation_text=correlation.round(2).values,
        colorscale="Viridis"
    )

    st.plotly_chart(fig_heatmap, use_container_width=True)

# --------------------------------
# TAB 5 - Statistik
# --------------------------------
with tab5:

    st.header("Statistische Analyse")

    st.write(filtered_df.describe())

    st.subheader("Top Länder nach Sicherheit")

    safety_df = filtered_df.sort_values(
        by="Safety Index",
        ascending=False
    ).head(10)

    fig_safety = px.bar(
        safety_df,
        x="Country",
        y="Safety Index",
        color="Safety Index",
        title="Sicherste Länder"
    )

    st.plotly_chart(fig_safety, use_container_width=True)

# --------------------------------
# Footer
# --------------------------------
st.markdown("---")
st.caption("Life Quality Dashboard • Datenquelle: Kaggle")