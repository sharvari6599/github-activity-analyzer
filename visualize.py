# visualize.py
import matplotlib.pyplot as plt

def plot_commits_weekly(df):
    for repo, g in df.groupby("repo"):
        g = g.sort_values("week")
        plt.figure()
        plt.plot(g["week"], g["commits"])
        plt.title(f"Weekly commits – {repo}")
        plt.xlabel("Week"); plt.ylabel("Commits"); plt.tight_layout()

def plot_issues(df):
    for repo, g in df.groupby("repo"):
        g = g.sort_values("month")
        plt.figure()
        plt.plot(g["month"], g["opened"], label="Opened")
        plt.plot(g["month"], g["closed"], label="Closed")
        plt.title(f"Issues opened vs closed – {repo}")
        plt.xlabel("Month"); plt.ylabel("Count"); plt.legend(); plt.tight_layout()
