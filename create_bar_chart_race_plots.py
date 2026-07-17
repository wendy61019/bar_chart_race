from create_bar_chart_race_data import CreateBarChartRaceDB
import plotly.express as px
import pandas as pd
from raceplotly.plots import barplot

create_bar_chart_race_data = CreateBarChartRaceDB()
cumulative_votes_by_time_candidate = create_bar_chart_race_data.create_cumulative_votes_by_time_candidate()
covid_19_confirmed = create_bar_chart_race_data.create_covid_19_confirmed()

#繪製plotly.express動態圖
early_collected = cumulative_votes_by_time_candidate[cumulative_votes_by_time_candidate["collected_at"] < pd.to_datetime("2024-01-13 17:30:30")]
max_cumulative_votes = early_collected["cumulative_sum_votes"].max()
fig = px.bar(early_collected,
             x="cumulative_sum_votes", y="candidate", color="candidate",
             animation_frame="collected_at", animation_group="candidate",
             range_x=[0, max_cumulative_votes])
fig.show()
max_confirmed = covid_19_confirmed["confirmed"].max()
fig = px.bar(covid_19_confirmed,
             x="confirmed", y="country", color="country",
             animation_frame="reported_on", animation_group="country",
             range_x=[0, max_confirmed])
fig.update_yaxes(categoryorder="total ascending")
fig.show()

#繪製barplot動態圖
vote_raceplot = barplot(cumulative_votes_by_time_candidate, item_column="candidate", value_column="cumulative_sum_votes",
                        time_column="collected_at", top_entries=3)
fig = vote_raceplot.plot(item_label="Votes collected by candidate", value_label="Cumulative votes",
                         frame_duration=50)
fig.write_html("bar_chart_race_votes.html")

confirmed_raceplot = barplot(covid_19_confirmed, item_column="country", value_column="confirmed",
                             time_column="reported_on")
fig = confirmed_raceplot.plot(item_label="Confirmed by country", value_label="Number of cases",
                              frame_duration=50)
fig.write_html("bar_chart_race_confirmed.html")