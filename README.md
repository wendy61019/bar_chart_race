# 練習專案六：奔跑的長條圖

## 簡介

這個專案「奔跑的長條圖」透過中選會選舉及公投資料庫的 `113全國投開票所完成時間.xlsx` 、練習專案四建立好的 `taiwan_presidential_election_2024.db` 以及練習專案五建立好的 `covid_19.db` 資料製作出了奔跑的長條圖。我們使用了 `pandas` 整合連結 Excel 活頁簿試算表與 SQLite 資料庫資料表的內容，利用 `plotly.express` 進行概念驗證並以 `raceplotly` 與 `streamlit` 做出成品。

 - `streamlit` 可以點選 [Streamlit Community Cloud的連結](https://barchartracest.streamlit.app/) 參考成品。

## 如何重現

 - 安裝 [Miniconda](https://docs.anaconda.com/miniconda)
 - 依據 `environment_local.yml` 建立環境：
 
 ```bash
 conda env create -f environment_local.yml`
```

 - 將 `data/` 資料夾中的 `113全國投開票所完成時間.xlsx` 、`taiwan_presidential_election_2024.db` 與 `covid_19.db` 放置於專案資料夾的 `data/` 資料夾中
 - 將專案資料夾的 `create_bar_chart_race_data.py` 放置於專案資料夾中
 - 啟動環境並執行 `python create_bar_chart_race_plots.py` 就能在專案資料夾建立 `bar_chart_race_votes.html` 與 `bar_chart_race_confirmed.html`
 - 啟動環境並執行 `python create_bar_chart_race_go.py` 就能在專案資料夾建立 `bar_chart_race_votes_go.html` 與 `bar_chart_race_confirmed_go.html` 與 `bar_chart_race_deaths_go.html`
 - 啟動環境並執⾏ `streamlit run app_streamlit.py` 並前往 http://192.168.1.103:8501 瀏覽成品