import sqlite3
import pandas as pd

#整理程式碼為一個類別
class CreateBarChartRaceDB:
#調整日期時間格式為 ISO-8601
#定義調整格式的函數 adjust_datetime_format() 並以 map() 方法應用。
    def adjust_datetime_format(self, x):
        date_part, time_part = x.split()
        date_part = "2024-01-13"
        datetime_iso_8601 = f"{date_part} {time_part}"
        return datetime_iso_8601

    def create_cumulative_votes_by_time_candidate(self):
#以pandas模組載入taiwan_presidential_election_2024.db資料
      connection = sqlite3.connect("data/taiwan_presidential_election_2024.db")
      sql_query = """
      SELECT polling_places.county,
            polling_places.polling_place,
            candidates.candidate,
            SUM(votes.votes) as sum_votes
        FROM votes
        JOIN candidates
          ON votes.candidate_id = candidates.id
        JOIN polling_places
          ON votes.polling_place_id = polling_places.id
      GROUP BY polling_places.county,
                polling_places.polling_place,
                candidates.candidate;
      """
      votes_by_county_polling_place_candidate = pd.read_sql(sql_query, con=connection)
      connection.close()
#以pandas模組載入113全國投開票所完成時間.xlsx
      votes_collected = pd.read_excel("data/113全國投開票所完成時間.xlsx", skiprows=[0, 1, 2])
      votes_collected.columns = ["county", "town", "polling_place", "collected_at", "number_of_voters"]
      votes_collected = votes_collected[["county", "town", "polling_place", "collected_at"]]
#連結候選人得票數與投開票所完成時間
      merged = pd.merge(votes_by_county_polling_place_candidate, votes_collected,
                        left_on=["county", "polling_place"], right_on=["county", "polling_place"],
                        how="left")
#以候選人和完成時間做為分組依據加總票數
      votes_by_collected_at_candidate = merged.groupby(["collected_at", "candidate"])["sum_votes"].sum().reset_index()
#以候選人作為分組依據累計加總票數
#使用 cumsum()（cumulative sum）方法
      cum_sum = votes_by_collected_at_candidate.groupby("candidate")["sum_votes"].cumsum()
      votes_by_collected_at_candidate["cumulative_sum_votes"] = cum_sum
#使用 pd.to_datetime() 函數將文字格式轉為日期時間格式
      votes_by_collected_at_candidate["collected_at"] = votes_by_collected_at_candidate["collected_at"].map(self.adjust_datetime_format)
      votes_by_collected_at_candidate["collected_at"] = pd.to_datetime(votes_by_collected_at_candidate["collected_at"])
      return votes_by_collected_at_candidate

    def create_covid_19_confirmed(self):
#以pandas模組載入covid_19.db資料
      connection = sqlite3.connect("data/covid_19.db")
      sql_query = """
      SELECT reported_on,
            country,
            confirmed
        FROM time_series
      WHERE reported_on <= "2020-12-31";
      """
      covid_19_confirmed = pd.read_sql(sql_query, con=connection)
      connection.close()
#將每個日期前 10 大累積確診的國家找出來
#使用 nlargest() 方法
      nlargest_index = covid_19_confirmed.groupby("reported_on")["confirmed"].nlargest(10).reset_index()["level_1"]
      covid_19_confirmed = covid_19_confirmed.loc[nlargest_index, :].reset_index(drop=True)
      return covid_19_confirmed

    def create_covid_19_deaths(self):
#以pandas模組載入covid_19.db資料
      connection = sqlite3.connect("data/covid_19.db")
      sql_query = """
      SELECT reported_on,
             country,
             deaths
        FROM time_series;
      """
      covid_19_deaths = pd.read_sql(sql_query, con=connection)
      connection.close()
#將每個日期前 10 大累積死亡的國家找出來
#使用 nlargest() 方法
      nlargest_index = covid_19_deaths.groupby("reported_on")["deaths"].nlargest(10).reset_index()["level_1"]
      covid_19_deaths = covid_19_deaths.loc[nlargest_index, :].reset_index(drop=True)
      return covid_19_deaths