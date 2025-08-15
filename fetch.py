# fetch.py
import os, time, requests
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Accept": "application/vnd.github+json"}

def paged_get(url, params=None):
    while url:
        r = requests.get(url, headers=HEADERS, params=params, timeout=30)
        if r.status_code == 403 and r.headers.get("X-RateLimit-Remaining") == "0":
            reset = int(r.headers.get("X-RateLimit-Reset", "0"))
            sleep_s = max(0, reset - int(time.time()) + 2)
            time.sleep(sleep_s)
            continue
        r.raise_for_status()
        yield r.json()
        # follow Link: rel="next"
        link = r.headers.get("Link", "")
        next_url = None
        for part in link.split(","):
            if 'rel="next"' in part:
                next_url = part[part.find("<")+1:part.find(">")]
        url, params = next_url, None

def list_repos(org=None, repos=None):
    if repos: return repos
    return [f"{org}/{r['name']}"
            for page in paged_get(f"https://api.github.com/orgs/{org}/repos?per_page=100")
            for r in page]

def list_commits(repo, since=None):
    url = f"https://api.github.com/repos/{repo}/commits?per_page=100"
    params = {"since": since} if since else None
    for page in paged_get(url, params): 
        for c in page: yield c

def list_contributors(repo):
    url = f"https://api.github.com/repos/{repo}/contributors?per_page=100&anon=1"
    for page in paged_get(url): 
        for u in page: yield u

def list_issues(repo, state="all", since=None):
    url = f"https://api.github.com/repos/{repo}/issues?per_page=100&state={state}"
    params = {"since": since} if since else None
    for page in paged_get(url, params):
        for i in page:
            if "pull_request" not in i:  # exclude PRs here
                yield i
