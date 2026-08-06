#!/usr/bin/env python3
"""Find workflow precedents in local Claude Code session transcripts.

Scans ~/.claude/projects/<project>/*.jsonl for calls to the Workflow tool, extracts the
script meta (name, description, phases) and matches it against the given keywords.

Usage:
  python3 find_precedents.py recon audit        # search the project matching the current cwd
  python3 find_precedents.py --all review       # search every project on this machine
  python3 find_precedents.py --extract my-flow  # print the newest full script with that name
  python3 find_precedents.py --list             # catalogue every workflow (no keyword filter)

Stdlib only. Output: one row per workflow (date | name | call sites | runs | phases | description).
Exits cleanly with a message when there is no session history to search.
"""
import glob
import json
import os
import re
import sys

BASE = os.path.expanduser("~/.claude/projects")


def project_dirs(all_projects):
    if not os.path.isdir(BASE):
        return []
    if all_projects:
        return [d for d in glob.glob(os.path.join(BASE, "*")) if os.path.isdir(d)]
    cur = os.getcwd().replace("/", "-")
    d = os.path.join(BASE, cur)
    return [d] if os.path.isdir(d) else []


def iter_workflow_calls(dirs):
    """Yield dicts: {ts, session, name, description, phases, agents, script}."""
    for d in dirs:
        for path in glob.glob(os.path.join(d, "*.jsonl")):
            try:
                fh = open(path, encoding="utf-8", errors="replace")
            except OSError:
                continue
            with fh:
                for line in fh:
                    if '"Workflow"' not in line or '"tool_use"' not in line:
                        continue
                    try:
                        obj = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    content = obj.get("message", {}).get("content")
                    if not isinstance(content, list):
                        continue
                    for c in content:
                        if not (isinstance(c, dict) and c.get("type") == "tool_use"
                                and c.get("name") == "Workflow"):
                            continue
                        script = (c.get("input") or {}).get("script") or ""
                        if not script:
                            continue
                        m_name = re.search(r"name:\s*['\"]([^'\"]+)['\"]", script)
                        m_desc = re.search(r"description:\s*['\"]([^'\"]+)['\"]", script)
                        yield {
                            "ts": (obj.get("timestamp") or "")[:10],
                            "session": os.path.basename(path)[:8],
                            "name": m_name.group(1) if m_name else "(unnamed)",
                            "description": m_desc.group(1) if m_desc else "",
                            "phases": re.findall(r"title:\s*['\"]([^'\"]+)['\"]", script),
                            "agents": script.count("agent("),
                            "script": script,
                        }


def main():
    argv = sys.argv[1:]
    all_projects = "--all" in argv
    list_all = "--list" in argv
    extract = None
    if "--extract" in argv:
        i = argv.index("--extract")
        if i + 1 >= len(argv):
            sys.exit("--extract requires a workflow name")
        extract = argv[i + 1]
        argv = argv[:i] + argv[i + 2:]
    keywords = [a.lower() for a in argv if not a.startswith("--")]

    if not os.path.isdir(BASE):
        print("No Claude Code session history at " + BASE
              + " — skipping the precedent step (nothing to search).")
        return

    dirs = project_dirs(all_projects)
    if not dirs:
        print("No session transcripts for the current directory — try --all.")
        return

    calls = list(iter_workflow_calls(dirs))
    if not calls:
        print("No Workflow calls found in the scanned sessions"
              + ("." if all_projects else " — try --all."))
        return

    if extract:
        hits = sorted((c for c in calls if c["name"] == extract), key=lambda c: c["ts"])
        if not hits:
            print("No script named '" + extract + "'")
            return
        print(hits[-1]["script"])
        return

    # dedup by name: keep the newest call, count how many times it ran
    by_name = {}
    for c in calls:
        prev = by_name.get(c["name"])
        if prev is None:
            c["runs"] = 1
            by_name[c["name"]] = c
        else:
            prev["runs"] += 1
            if c["ts"] >= prev["ts"]:
                c["runs"] = prev["runs"]
                by_name[c["name"]] = c

    rows = list(by_name.values())
    if keywords and not list_all:
        def score(c):
            hay = (c["name"] + " " + c["description"] + " " + " ".join(c["phases"])).lower()
            return sum(1 for k in keywords if k in hay)
        rows = [c for c in rows if score(c) > 0]
        rows.sort(key=lambda c: (score(c), c["ts"]), reverse=True)
        if not rows:
            print("No precedents for: " + ", ".join(keywords)
                  + ("" if all_projects else "  (try --all)"))
            return
    else:
        rows.sort(key=lambda c: c["ts"], reverse=True)

    limit = len(rows) if list_all else 10
    for c in rows[:limit]:
        phases = ", ".join(c["phases"][:4]) or "-"
        desc = c["description"][:80]
        print(f"{c['ts']} | {c['name']} | call sites: {c['agents']} | {c['runs']}x | "
              f"phases: {phases} | {desc}")
    if len(rows) > limit:
        print(f"... and {len(rows) - limit} more (--list shows everything)")


if __name__ == "__main__":
    main()
