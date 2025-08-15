# analyze.py
import pandas as pd

def commits_by_week(df_commits):
    return (df_commits
            .assign(week=df_commits["date"].dt.to_period("W").dt.start_time)
            .groupby(["repo","week"]).size()
            .rename("commits").reset_index())

def top_contributors(df_contribs, top_n=10):
    return (df_contribs.groupby(["repo","login"])["contributions"].sum()
            .reset_index()
            .sort_values(["repo","contributions"], ascending=[True, False])
            .groupby("repo").head(top_n))

def issues_trend(df_issues):
    if df_issues.empty:
        return df_issues
    by_month = df_issues.assign(month=df_issues["created_at"].dt.to_period("M").dt.start_time)
    opened = by_month.groupby(["repo","month"]).size().rename("opened")
    closed = (df_issues.dropna(subset=["closed_at"])
              .assign(month=df_issues["closed_at"].dt.to_period("M").dt.start_time)
              .groupby(["repo","month"]).size().rename("closed"))
    return pd.concat([opened, closed], axis=1).fillna(0).reset_index()
