# main.py
import yaml, pandas as pd
from fetch import list_repos, list_commits, list_contributors, list_issues
from transform import commits_df, contributors_df, issues_df
from analyze import commits_by_week, top_contributors, issues_trend
from visualize import plot_commits_weekly, plot_issues

def run():
    cfg = yaml.safe_load(open("config.yaml"))
    repos = list_repos(org=cfg.get("org"), repos=cfg.get("repos"))
    since = cfg.get("since")

    commits_frames, contrib_frames, issue_frames = [], [], []

    # >>> Replace your old loop with THIS try/except loop <<<
    for repo in repos:
        print(f"\nFetching: {repo} (since={since})")
        try:
            cdf = commits_df(list_commits(repo, since), repo)
            idf = issues_df(list_issues(repo, since=since), repo)
            udf = contributors_df(list_contributors(repo), repo)
        except Exception as e:
            print(f"  ERROR fetching {repo}: {e}")
            continue

        print(f"  commits: {len(cdf)} | issues: {len(idf)} | contributors: {len(udf)}")
        if not cdf.empty: commits_frames.append(cdf)
        if not idf.empty: issue_frames.append(idf)
        if not udf.empty: contrib_frames.append(udf)

    dfc = pd.concat(commits_frames, ignore_index=True) if commits_frames else pd.DataFrame()
    dfi = pd.concat(issue_frames,   ignore_index=True) if issue_frames   else pd.DataFrame()
    dfu = pd.concat(contrib_frames, ignore_index=True) if contrib_frames else pd.DataFrame()

    wk = commits_by_week(dfc) if not dfc.empty else pd.DataFrame()
    it = issues_trend(dfi)    if not dfi.empty else pd.DataFrame()
    tc = top_contributors(dfu, top_n=10) if not dfu.empty else pd.DataFrame()

    print("\nCommits/week sample:\n", wk.head(10))
    print("\nTop contributors sample:\n", tc.head(10))
    print("\nIssues trend sample:\n", it.head(10))

    if not wk.empty: plot_commits_weekly(wk)
    if not it.empty: plot_issues(it)

    import matplotlib.pyplot as plt
    if not wk.empty or not it.empty:
        plt.show()
    else:
        print("\nNo data to plot. Check your repos and 'since' in config.yaml.")

if __name__ == "__main__":
    run()
