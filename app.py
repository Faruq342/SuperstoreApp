import streamlit as st
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Nigeria Incidents Dashboard", layout="wide")

sns.set_style("whitegrid")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("incidents_updated.csv")
    df["Start date"] = pd.to_datetime(df["Start date"],  errors="coerce")
    df["End date"] = pd.to_datetime(df["End date"], errors="coerce")
    return df

df = load_data()

st.title("Incidents, Accidents and Violence in Nigeria")
st.markdown("An exploratory dashboard analyzing recorded incidents across Nigeria.")

# Sidebar filters
st.sidebar.header("Filters")
states = st.sidebar.multiselect(
    "Select State(S)",
    options=sorted(df["State"].dropna().unique()),
    default=None
)
categories = st.sidebar.multiselect(
    "Select Incident Category",
    options=sorted(df["Incident category"].dropna().unique()),
    default=None
)

filtered_df = df.copy()
if states:
    filtered_df = filtered_df[filtered_df["State"].isin(states)]
if categories:
    filtered_df = filtered_df[filtered_df["Incident category"].isin(categories)]

# key metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Incidents", f"{len(filtered_df):,}")
col2.metric("Total Deaths", f"{int(filtered_df['Number of deaths'].sum()):,}")
col3.metric("State Affected", filtered_df["State"].nunique())

st.divider()

# Chart 1: Top states by deaths
st.subheader("Top 10 States by Total Deaths")
top_states = filtered_df.groupby("State")["Number of deaths"].sum().sort_values(ascending=False).head(10)
fig1, ax1 = plt.subplots(figsize=(10, 5))
sns.barplot(x=top_states.values, y=top_states.index, hue=top_states.index, palette="Reds_r", legend=False, ax=ax1)
ax1.set_xlabel("Total Deaths")
ax1.set_ylabel("State")
st.pyplot(fig1)

# Chart 2: Deaths by category
st.subheader("Total Deaths by Incident Category")
cat_deaths = filtered_df.groupby("Incident category")["Number of deaths"].sum().sort_values(ascending=False)
fig2, ax2 = plt.subplots(figsize=(10, 6))
sns.barplot(x=cat_deaths.values, y=cat_deaths.index, hue=cat_deaths.index, palette="viridis", legend=False, ax=ax2)
ax2.set_xlabel("Total Deaths")
ax2.set_ylabel("Incident Category")
st.pyplot(fig2)

# Chart 3: Trend over time
st.subheader("Deaths by Year")
yearly = filtered_df.groupby(filtered_df["Start date"].dt.year)["Number of deaths"].sum()
fig3, ax3 = plt.subplots(figsize=(10, 5))
sns.lineplot(x=yearly.index, y=yearly.values, marker="o", ax=ax3)
ax3.set_xlabel("Year")
ax3.set_ylabel("Total Deaths")
st.pyplot(fig3)

# Chart 4: Severity by category
st.subheader("Average Deaths per Incidents by Category (Severity)")
avg_severity = filtered_df.groupby("Incident category")["Number of deaths"].mean().sort_values(ascending=False)
fig4, ax4 = plt.subplots(figsize=(10, 6))
sns.barplot(x=avg_severity.values, y=avg_severity.index, hue=avg_severity.index, palette="magma", legend=False, ax=ax4)
ax4.set_xlabel("Average Deaths per Incident")
ax4.set_ylabel("Incident Category")
st.pyplot(fig4)

st.divider()
st.subheader("Raw Data")
st.dataframe(filtered_df)
