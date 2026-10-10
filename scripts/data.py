"""Public GitHub data for the activity and language graphics.

Fetched through the GitHub GraphQL API with the `gh` CLI (locally, or in the scheduled workflow with the repository token).
The result is cached in data/stats.json so the artwork can be rebuilt offline.
"""
import json
import subprocess
from collections import Counter
from pathlib import Path

LOGIN = "chiragshah2357"
CACHE = Path(__file__).resolve().parent.parent / "data" / "stats.json"

QUERY = """query($login:String!){ user(login:$login){ createdAt
  contributionsCollection{ totalCommitContributions totalPullRequestContributions totalIssueContributions totalPullRequestReviewContributions
    restrictedContributionsCount contributionCalendar{ totalContributions weeks{ contributionDays{ date contributionCount } } } }
  openIssues: issues(states:OPEN){ totalCount }
  repositories(first:100, ownerAffiliations:OWNER, isFork:false, privacy:PUBLIC){ totalCount nodes{ name primaryLanguage{ name color } } } } }"""


def _fetch() -> dict:
    out = subprocess.run(["gh", "api", "graphql", "-F", f"login={LOGIN}", "-f", f"query={QUERY}"], capture_output=True, text=True, check=True, timeout=90)
    return json.loads(out.stdout)["data"]["user"]


def _summarise(u: dict) -> dict:
    c = u["contributionsCollection"]
    days = [(d["date"], d["contributionCount"]) for w in c["contributionCalendar"]["weeks"] for d in w["contributionDays"]]
    longest = run = 0
    for _, n in days:
        run = run + 1 if n > 0 else 0
        longest = max(longest, run)
    cur = 0
    for _, n in reversed(days):   # current streak: today may still be empty, so allow one empty day at the end
        if n > 0:
            cur += 1
        elif cur == 0 and _ == days[-1][0]:
            continue
        else:
            break
    best = max(days, key=lambda x: x[1])
    langs = Counter()
    colors = {}
    for r in u["repositories"]["nodes"]:
        pl = r["primaryLanguage"]
        if pl:
            langs[pl["name"]] += 1
            colors[pl["name"]] = pl["color"] or "#8a8377"
    return {
        "login": LOGIN, "joined": u["createdAt"][:10], "total": c["contributionCalendar"]["totalContributions"],
        "commits": c["totalCommitContributions"], "prs": c["totalPullRequestContributions"], "issues": c["totalIssueContributions"],
        "reviews": c["totalPullRequestReviewContributions"], "private": c["restrictedContributionsCount"],
        "days": days, "active_days": sum(1 for _, n in days if n > 0), "longest_streak": longest, "current_streak": cur,
        "busiest": {"date": best[0], "count": best[1]}, "repos": u["repositories"]["totalCount"],
        "languages": [{"name": k, "repos": v, "color": colors[k]} for k, v in langs.most_common()],
        "open_issues": u["openIssues"]["totalCount"],   # issues this account opened that are still open
    }   # no timestamp in here on purpose: an unchanged day must not make the daily workflow commit


def load(offline: bool = False) -> dict:
    if not offline:
        try:
            data = _summarise(_fetch())
            CACHE.parent.mkdir(exist_ok=True)
            CACHE.write_text(json.dumps(data, indent=1), encoding="utf-8")
            return data
        except (subprocess.SubprocessError, OSError, KeyError, ValueError) as e:
            print(f"! could not fetch GitHub data ({e}); using the cached copy")
    cached = json.loads(CACHE.read_text(encoding="utf-8"))
    cached.setdefault("open_issues", 0)
    return cached


if __name__ == "__main__":
    d = load()
    print({k: v for k, v in d.items() if k not in ("days",)})
