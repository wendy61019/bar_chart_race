from create_bar_chart_race_data import CreateBarChartRaceDB
import pandas as pd
from raceplotly.plots import barplot
import streamlit as st

#設定網頁標題與排版
st.set_page_config(page_title="Bar Chart Race", layout="wide")
st.title("📊 Bar Chart Race")

#載入資料
@st.cache_data
def prepare_data():
    create_bar_chart_race_data = CreateBarChartRaceDB()
    votes = create_bar_chart_race_data.create_cumulative_votes_by_time_candidate()
    confirmed = create_bar_chart_race_data.create_covid_19_confirmed()
    deaths = create_bar_chart_race_data.create_covid_19_deaths()
    return votes, confirmed, deaths
cumulative_votes_by_time_candidate, covid_19_confirmed, covid_19_deaths = prepare_data()

#建立3個頁籤
tab_vote, tab_covid_confirmed, tab_covid_death = st.tabs(["🗳️ Taiwan Presidential Election 2024", "🦠 Global COVID-19 Cases",  "💀 Global COVID-19 Deaths"])

#繪製總統大選動態圖
with tab_vote:
    st.subheader("🗳️ Taiwan Presidential Election 2024 Bar Chart Race")
    votes_df = cumulative_votes_by_time_candidate.copy()
    votes_df["collected_at"] = votes_df["collected_at"].astype(str)
    vote_raceplot = barplot(votes_df, item_column="candidate", value_column="cumulative_sum_votes",
                            time_column="collected_at", top_entries=3)
    fig_vote = vote_raceplot.plot(item_label="Votes collected by candidate", value_label="Cumulative votes",
                            frame_duration=50)
    st.plotly_chart(fig_vote, width="stretch")

#繪製Covid 19確診動態圖
with tab_covid_confirmed:
    st.subheader("🦠 The Evolution of Global COVID-19 Case Numbers")
    confirmed_df = covid_19_confirmed.copy()
    confirmed_df["reported_on"] = confirmed_df["reported_on"].astype(str)
    confirmed_raceplot = barplot(confirmed_df, item_column="country", value_column="confirmed",
                                time_column="reported_on")
    fig_confirmed = confirmed_raceplot.plot(item_label="Confirmed by country", value_label="Number of cases",
                                frame_duration=50)
    st.plotly_chart(fig_confirmed, width="stretch")

#繪製Covid 19死亡動態圖
with tab_covid_death:
    st.subheader("💀 The Fatal Trajectory of Global COVID-19 Deaths")
    death_df = covid_19_deaths.copy()
    death_df["reported_on"] = death_df["reported_on"].astype(str)
    death_raceplot = barplot(death_df, item_column="country", value_column="deaths",
                             time_column="reported_on")
    fig_death = death_raceplot.plot(item_label="Death toll by country", value_label="Number of deaths",
                                    frame_duration=50)
    st.plotly_chart(fig_death, width="stretch")