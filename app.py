# app.py
import streamlit as st
import pandas as pd

# Load your cleaned dataset
df = pd.read_csv("cleaned_recruits.csv")

st.set_page_config(page_title="NCAA Gymnastics Recruits", layout="wide")
st.title("🤸 NCAA Gymnastics Recruit Database (2024–2027)")

# Sidebar filters
st.sidebar.header("Filters")
region = st.sidebar.multiselect("Select Region(s):", sorted(df['region'].dropna().unique()))
level = st.sidebar.multiselect("Select Level(s):", sorted(df['level'].dropna().unique()))
school = st.sidebar.multiselect("Select School(s):", sorted(df['school'].dropna().unique()))

# Apply filters
filtered_df = df.copy()
if region:
    filtered_df = filtered_df[filtered_df['region'].isin(region)]
if level:
    filtered_df = filtered_df[filtered_df['level'].isin(level)]
if school:
    filtered_df = filtered_df[filtered_df['school'].isin(school)]

# Show dataframe
st.subheader("Recruit Data")
st.dataframe(filtered_df)

# Show top 10 AA ranking
st.subheader("🏆 Top 10 Recruits by All-Around Score")
top_aa = filtered_df.nlargest(10, 'aa_high')[['athlete', 'school', 'aa_high']]
st.table(top_aa)

# Simple chart
st.subheader("📊 Distribution of Recruits by Region")
st.bar_chart(filtered_df['region'].value_counts().sort_index())

