from create_bar_chart_race_data import CreateBarChartRaceDB
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def build_bar_chart_race(df, item_column, value_column, time_column, top_n=None, item_label="", value_label="", frame_duration: int=50):
#取得排序後的時間點，準備好資料
    times = sorted(df[time_column].unique())
    unique_items = df[item_column].unique()
    color_palette = px.colors.qualitative.Alphabet
    color_map = dict(zip(unique_items, [color_palette[i % len(color_palette)] for i in range(len(unique_items))]))
    
    def get_step_data(t):
        sub_df = df[df[time_column] == t].sort_values(value_column, ascending=True)
        return sub_df.tail(top_n) if top_n else sub_df
    
#建立動畫Frames與Slider Steps
    frames = []
    for t in times:
        df_t = get_step_data(t)
        frames.append(
            go.Frame(
                data=[go.Bar(
                    x=df_t[value_column],
                    y=df_t[item_column],
                    orientation='h',
                    text=df_t[value_column],
                    textposition='inside',
                    marker=dict(color=df_t[item_column].map(color_map))
                    )],
                    layout=go.Layout(title_text=f"{item_label} ({t})"),
                    name=str(t)
                    )
        )
#先計算好過渡時間
    transition_duration = int(frame_duration * 0.7)    
    slider_steps = [
        {
            "args": [[str(t)], {"frame": {"duration": frame_duration, "redraw": True}, "mode": "immediate", "transition": {"duration": transition_duration, "easing": "quadratic-in-out"}}],
            "label": str(t), "method": "animate"
        }
        for t in times
    ]

#建立初始圖表
    df_init = get_step_data(times[0])
    fig = go.Figure(
        data=[go.Bar(x=df_init[value_column], y=df_init[item_column], orientation='h', text=df_init[value_column], textposition='inside', marker=dict(color=df_init[item_column].map(color_map)))],
        frames=frames
    )

#建立Layout 與控制按鈕
    fig.update_layout(
        title=f"{item_label} ({times[0]})",
        xaxis=dict(title=value_label, range=[0, df[value_column].max() * 1.1]),
        yaxis=dict(title=item_label, categoryorder="trace"),
        updatemenus=[{
            "type": "buttons", "showactive": False, "x": 0.08, "y": -0.08, "xanchor": "right", "yanchor": "top", "direction": "left",
            "buttons": [
                {"label": "▶ Play", "method": "animate", "args": [None, {"frame": {"duration": frame_duration, "redraw": True}, "fromcurrent": True, "transition": {"duration": int(frame_duration * 0.7), "easing": "quadratic-in-out"}}]},
                {"label": "⏸ Pause", "method": "animate", "args": [[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate", "transition": {"duration": 0}}]}
            ]
        }],
        sliders=[{"active": 0, "x": 0.1, "y": 0, "len": 0.9, "pad": {"t": 50}, "steps": slider_steps}]
    )
    return fig

create_bar_chart_race_data = CreateBarChartRaceDB()
cumulative_votes_by_time_candidate = create_bar_chart_race_data.create_cumulative_votes_by_time_candidate()
covid_19_confirmed = create_bar_chart_race_data.create_covid_19_confirmed()
covid_19_deaths = create_bar_chart_race_data.create_covid_19_deaths()

#總統大選 Candidate votes 動態圖
fig_vote = build_bar_chart_race(cumulative_votes_by_time_candidate, "candidate", "cumulative_sum_votes", "collected_at", top_n=3, item_label="Votes collected by candidate", value_label="Cumulative votes")
fig_vote.write_html("bar_chart_race_votes_go.html")

#Covid 19 Confirmed 動態圖
fig_covid = build_bar_chart_race(covid_19_confirmed, "country", "confirmed", "reported_on", top_n=10, item_label="Confirmed by country", value_label="Number of cases")
fig_covid.write_html("bar_chart_race_confirmed_go.html")

#Covid 19 Deaths 動態圖
fig_death = build_bar_chart_race(covid_19_deaths, "country", "deaths", "reported_on", top_n=10, item_label="Deaths by country", value_label="Number of deaths")
fig_death.write_html("bar_chart_race_deaths_go.html")