import pandas as pd

def commits_df(items, repo):
    rows = []
    for c in items:
        rows.append({
            "repo": repo,
            "sha": c.get("sha"),
            "author_login": (c.get("author") or {}).get("login"),
            "committer_login": (c.get("committer") or {}).get("login"),
            "date": (c.get("commit") or {}).get("author", {}).get("date"),
        })
    df = pd.DataFrame(rows, columns=["repo","sha","author_login","committer_login","date"])
    if not df.empty:
        df["date"] = pd.to_datetime(df["date"], errors="coerce", utc=True)
        df = df.dropna(subset=["date"])
    return df

def contributors_df(items, repo):
    df = pd.DataFrame([
        {"repo": repo,
         "login": (i.get("login") or i.get("name")),
         "contributions": i.get("contributions", 0)}
        for i in items
    ], columns=["repo","login","contributions"])
    return df

def issues_df(items, repo):
    rows = []
    for i in items:
        rows.append({
            "repo": repo,
            "number": i.get("number"),
            "state": i.get("state"),
            "created_at": i.get("created_at"),
            "closed_at": i.get("closed_at"),
            "user": (i.get("user") or {}).get("login"),
        })
    # Build DF and FORCE required columns to exist
    df = pd.DataFrame(rows)
    required = ["repo","number","state","created_at","closed_at","user"]
    for col in required:
        if col not in df.columns:
            df[col] = pd.NA
    df = df[required]

    if df.empty:
        return df

    df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce", utc=True)
    df["closed_at"]  = pd.to_datetime(df["closed_at"],  errors="coerce", utc=True)
    df = df.dropna(subset=["created_at"])
    return df
