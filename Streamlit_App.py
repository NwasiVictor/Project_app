
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns


import streamlit as st
from datetime import date

df = pd.read_csv("victor.csv")

# Sidebar
st.sidebar.header("Filters")

# State selection
states = st.sidebar.multiselect(
    "Select State(s)",
    options=sorted(df["State"].dropna().unique())
)

# Start date
start_date = st.sidebar.date_input("Start Date", value=date(2026, 1, 1))

# End date
end_date = st.sidebar.date_input("End Date", value=date.today())

# Display selections in main app
#st.write("### Selected Filters")
#st.write(f"**State:** {state}")
#st.write(f"**Start Date:** {start_date}")
#st.write(f"**End Date:** {end_date}")


df['Start date'] = pd.to_datetime(df['Start date'])
df['End date'] = pd.to_datetime(df['End date'])
df['Duration'] = (df['End date'] - df['Start date']).dt.days

st.title("Incident Analysis Dashboard")


# Q1: How have incidents changed over the years?
st.subheader("1. How have incidents changed over the years?")
incidents_per_year = df.groupby(df['Start date'].dt.year).size().reset_index(name='count')
incidents_per_year.rename(columns={'Start date': 'year'}, inplace=True)

fig1 = px.line(
    incidents_per_year,
    x='year',
    y='count',
    markers=True,
    color_discrete_sequence=px.colors.qualitative.Set2,
    title="Incidents per Year"
)
st.plotly_chart(fig1, use_container_width=True)

# Q2: Which states recorded the most fatalities?
st.subheader("2. Which states recorded the most fatalities?")
deaths_by_state = df.groupby('State')['Number of deaths'].sum().reset_index().sort_values('Number of deaths', ascending=False)

fig2 = px.bar(
    deaths_by_state,
    x='Number of deaths',
    y='State',
    orientation='h',
    color='Number of deaths',
    color_continuous_scale='Reds',
    title="Total Deaths by State"
)
st.plotly_chart(fig2, use_container_width=True)

# Q3:Which states had the highest incident frequency?
st.subheader("3. Which states had the highest incident frequency?")
fig3 = alt.Chart(df).mark_bar().encode(
    x='State',
    y='count()',
    tooltip=['State','count()']
).properties(title='Incident Frequency by State')
st.altair_chart(fig3, use_container_width=True)

# Q4: Do incidents cluster in certain months?
st.subheader("4. Do incidents cluster in certain months?")
incidents_per_month = df.groupby(df['Start date'].dt.month).size().reset_index(name='count')
incidents_per_month.rename(columns={'Start date': 'month'}, inplace=True)

fig4 = px.line(
    incidents_per_month,
    x='month',
    y='count',
    markers=True,
    color_discrete_sequence=px.colors.qualitative.Bold,
    title="Incidents per Month"
)
st.plotly_chart(fig4, use_container_width=True)

# Q5: Which incident types are most deadly?
st.subheader("5. Which incident types are most deadly?")
avg_deaths_by_incident = df.groupby('Incident')['Number of deaths'].mean().reset_index()

fig5 = px.bar(
    avg_deaths_by_incident,
    x='Incident',
    y='Number of deaths',
    color='Number of deaths',
    color_continuous_scale='Viridis',
    title="Average Deaths per Incident Type"
)
st.plotly_chart(fig5, use_container_width=True)

# Q6: Has the severity of incidents increased or decreased?
st.subheader("6. Has the severity of incidents increased or decreased?")
avg_deaths_per_year = df.groupby(df['Start date'].dt.year)['Number of deaths'].mean().reset_index()
avg_deaths_per_year.rename(columns={'Start date': 'year'}, inplace=True)

fig6 = px.line(
    avg_deaths_per_year,
    x='year',
    y='Number of deaths',
    markers=True,
    color_discrete_sequence=px.colors.qualitative.Dark2,
    title="Average Deaths per Year"
)
st.plotly_chart(fig6, use_container_width=True)

df['Start date'] = pd.to_datetime(df['Start date'])
df['End date'] = pd.to_datetime(df['End date'])

# Create derived columns
df['Duration'] = (df['End date'] - df['Start date']).dt.days
df['Year'] = df['Start date'].dt.year
df['Month'] = df['Start date'].dt.month

# Q7: Top 10 deadliest incidents
st.subheader("Q9: Top 10 deadliest incidents")
top10 = df.nlargest(10, 'Number of deaths')[['Identifier','Incident','State','Number of deaths']]
fig9 = px.bar(top10, x='Incident', y='Number of deaths',
              color='State', title="Top 10 Deadliest Incidents")
st.plotly_chart(fig9, use_container_width=True)
st.dataframe(top10)
