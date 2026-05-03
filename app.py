import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Titel
st.title("City Quality of Life Dashboard")

# Daten laden
df = pd.read_csv("city_quality.csv")

# Tabelle anzeigen
st.subheader("Raw Data")
st.write(df)

# Auswahl Stadt
city = st.selectbox("Select a City", df["City"])

# Daten der Stadt anzeigen
st.subheader("City Details")
st.write(df[df["City"] == city])

# Einfaches Diagramm
st.subheader("Quality of Life Comparison")

fig, ax = plt.subplots()
sns.barplot(x="City", y="Quality_of_Life", data=df, ax=ax)
plt.xticks(rotation=45)

st.pyplot(fig)

# Scatter Plot
st.subheader("Cost vs Quality")

fig2, ax2 = plt.subplots()
sns.scatterplot(
    x="Cost_of_Living",
    y="Quality_of_Life",
    hue="City",
    data=df,
    ax=ax2
)

st.pyplot(fig2)