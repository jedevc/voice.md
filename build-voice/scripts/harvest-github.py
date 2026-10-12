#!/usr/bin/env python3
"""Harvest a user's GitHub PR comments, reviews, authored PR bodies and commits.

usage: harvest-github.py OUT_DIR USER ORG[,ORG...] SINCE(YYYY-MM-DD)
"""
import datetime
import json
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor

OUT, USER, ORGS, SINCE = sys.argv[1], sys.argv[2], sys.argv[3].split(","), sys.argv[4]


def gh(*args):
    for _ in range(5):
        r = subprocess.run(["gh", "api", *args], capture_output=True, text=True)
        if r.returncode == 0:
            return json.loads(r.stdout) if r.stdout.strip() else None
        if "rate limit" not in r.stderr:
            print("ERR", args, r.stderr[:200], file=sys.stderr)
            return None
        time.sleep(65)
    return None


# search caps out at 1000 results, so split into months
def months():
    d = datetime.date.fromisoformat(SINCE)
    while d <= datetime.date.today():
        n = (d.replace(day=28) + datetime.timedelta(days=4)).replace(day=1)
        yield d, n - datetime.timedelta(days=1)
        d = n


def search(kind, q):
    items = []
    for page in range(1, 11):
        r = gh("-X", "GET", f"search/{kind}", "-f", f"q={q}", "-f", "per_page=100", "-f", f"page={page}")
        if not r:
            break
        items += r["items"]
        if len(r["items"]) < 100:
            break
    return items


prs, authored, commits = {}, {}, []
for org in ORGS:
    for a, b in months():
        rng = f"{a}..{b}"
        for it in search("issues", f"org:{org} is:pr commenter:{USER} updated:{rng}") + search(
            "issues", f"org:{org} is:pr reviewed-by:{USER} updated:{rng}"
        ):
            prs[it["url"]] = it
        for it in search("issues", f"org:{org} is:pr author:{USER} created:{rng}"):
            authored[it["url"]] = {
                "repo": it["repository_url"].split("/repos/")[1],
                "number": it["number"],
                "title": it["title"],
                "body": it["body"],
                "url": it["html_url"],
                "created": it["created_at"],
            }
        for it in search("commits", f"org:{org} author:{USER} author-date:{rng}"):
            commits.append(
                {
                    "repo": it["repository"]["full_name"],
                    "sha": it["sha"],
                    "date": it["commit"]["author"]["date"],
                    "message": it["commit"]["message"],
                }
            )
print(len(prs), "prs touched;", len(authored), "authored;", len(commits), "commits", file=sys.stderr)


def fetch(it):
    repo = it["repository_url"].split("/repos/")[1]
    n = it["number"]
    out = []
    for kind, path in [
        ("review_comment", f"repos/{repo}/pulls/{n}/comments"),
        ("review", f"repos/{repo}/pulls/{n}/reviews"),
        ("issue_comment", f"repos/{repo}/issues/{n}/comments"),
    ]:
        r = subprocess.run(
            ["gh", "api", "--paginate", path, "--jq", f'.[] | select(.user.login=="{USER}")'],
            capture_output=True,
            text=True,
        )
        for line in r.stdout.splitlines():
            if not line.strip():
                continue
            c = json.loads(line)
            body = c.get("body") or ""
            date = c.get("created_at") or c.get("submitted_at") or ""
            if not body.strip() or date < SINCE:
                continue
            out.append(
                {
                    "kind": kind,
                    "repo": repo,
                    "pr": n,
                    "pr_author": it["user"]["login"],
                    "pr_title": it["title"],
                    "date": date,
                    "path": c.get("path"),
                    "diff_hunk": (c.get("diff_hunk") or "")[-600:],
                    "body": body,
                    "url": c.get("html_url"),
                }
            )
    return out


with ThreadPoolExecutor(8) as ex:
    comments = [c for res in ex.map(fetch, prs.values()) for c in res]

os.makedirs(OUT, exist_ok=True)
for name, data in [("comments.json", comments), ("authored_prs.json", list(authored.values())), ("commits.json", commits)]:
    with open(os.path.join(OUT, name), "w") as f:
        json.dump(data, f, indent=1)
print(len(comments), "comments", file=sys.stderr)
