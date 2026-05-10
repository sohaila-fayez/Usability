import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------
# Seitenkonfiguration
# --------------------------------
st.set_page_config(
    page_title="Life Quality Dashboard",
    layout="wide"
)

# --------------------------------
# Titel
# --------------------------------
st.title("🌍 Städte-Ranking Dashboard")
st.subheader("Quality of Life Analyse mit Numbeo-Daten")

# --------------------------------
# CSV-Datei laden
# --------------------------------
df = pd.read_csv("zquality_of_life.csv")

# --------------------------------
# Daten anzeigen
# --------------------------------
st.header("📋 Datensatz")

st.dataframe(df)

# --------------------------------
# Sidebar Filter
# --------------------------------
st.sidebar.header("Filter")

years = df["Year"].unique()

selected_year = st.sidebar.selectbox(
    "Jahr auswählen",
    sorted(years)
)

filtered_df = df[df["Year"] == selected_year]

# --------------------------------
# Top 10 Städte nach Lebensqualität
# --------------------------------
st.header("🏆 Top Städte nach Quality of Life")

top10 = filtered_df.sort_values(
    by="Quality of Life Index",
    ascending=False
).head(10)

fig_bar = px.bar(
    top10,
    x="Country",
    y="Quality of Life Index",
    color="Quality of Life Index",
    title="Top 10 Städte"
)

st.plotly_chart(fig_bar, use_container_width=True)

# --------------------------------
# Scatter Plot
# --------------------------------
st.header("💰 Kaufkraft vs Lebensqualität")

fig_scatter = px.scatter(
    filtered_df,
    x="Purchasing Power Index",
    y="Quality of Life Index",
    size="Safety Index",
    color="Cost of Living Index",
    hover_name="Country",
    title="Zusammenhang verschiedener Faktoren"
)

st.plotly_chart(fig_scatter, use_container_width=True)

# --------------------------------
# Statistik
# --------------------------------
st.header("📈 Grundlegende Statistik")

st.write(filtered_df.describe())