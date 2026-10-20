"""Create DRAFT Kit broadcasts for newly added opted-in Jekyll posts. Never send."""
import datetime as dt
import html
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

import markdown
import yaml

API = "https://api.kit.com/v4/broadcasts"

def git(*args):
    return subprocess.check_output(["git", *args], text=True).strip()

def parse(path):
    raw = Path(path).read_text(encoding="utf-8-sig").lstrip()
    match = re.match(r"\A---\s*\n(.*?)\n---\s*\n(.*)\Z", raw, flags=re.S)
    if not match:
        raise ValueError(f"{path}: missing YAML front matter")
    meta = yaml.safe_load(match.group(1)) or {}
    if not isinstance(meta, dict):
        raise ValueError(f"{path}: invalid YAML front matter")
    return meta, match.group(2)

def main():
    if os.environ.get("EVENT_NAME") == "workflow_dispatch":
        print("Manual run disabled to avoid drafting old posts.")
        return
    before = os.environ.get("BEFORE_SHA", "")
    if not re.fullmatch(r"[a-f0-9]{40}", before) or before == "0" * 40:
        print("Missing baseline commit; skipping safely.")
        return
    added = git("diff", "--diff-filter=A", "--name-only", before, "HEAD").splitlines()
    posts = [p for p in added if re.fullmatch(r"_posts/\d{4}-\d{2}-\d{2}-.+\.(md|markdown)", p)]
    print(f"New post files: {len(posts)}")
    for filename in posts:
        meta, body = parse(filename)
        if meta.get("email") is not True:
            print(f"Skipping {filename}: email is not true")
            continue
        today = dt.datetime.now(dt.timezone.utc).date()
        date = dt.date.fromisoformat(Path(filename).name[:10])
        if abs((today - date).days) > 2:
            print(f"Skipping {filename}: post date not within 2 days of today")
            continue
        title, subtitle = meta.get("title"), meta.get("subtitle")
        if not isinstance(title, str) or not title.strip():
            raise ValueError(f"{filename}: title is required")
        if not isinstance(subtitle, str) or not subtitle.strip():
            raise ValueError(f"{filename}: subtitle is required")
        if len(subtitle) > 150:
            raise ValueError(f"{filename}: subtitle must be 150 characters or fewer")
        api_key = os.environ.get("KIT_API_KEY")
        if not api_key:
            raise ValueError("KIT_API_KEY secret is missing")
        slug = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", Path(filename).stem)
        link = f"https://learningfreelance.com/{slug}/"
        body_html = markdown.markdown(body, extensions=["extra", "sane_lists"])
        body_html += f'\n<p><a href="{html.escape(link, quote=True)}">Read on Learning Freelance →</a></p>'
        payload = {
            "subject": title,
            "preview_text": subtitle,
            "content": body_html,
            "description": f"GitHub draft: {filename}",
            "public": False,
            "send_at": None
        }
        request = urllib.request.Request(API, data=json.dumps(payload).encode(), headers={
            "Content-Type": "application/json",
            "X-Kit-Api-Key": api_key,
        }, method="POST")
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                result = json.load(response)
        except urllib.error.HTTPError as exc:
            print("Kit returned HTTP", exc.code, exc.read().decode()[:1200], file=sys.stderr)
            raise
        print(f"Created Kit draft {result.get('broadcast', {}).get('id')}. No email sent.")

if __name__ == "__main__":
    main()
