#!/usr/bin/env python3
"""
ClickUp Review — review a CRM/sales funnel list in ClickUp: count per stage,
deals near close, stale leads, value sums. Read-only.

Stages are derived dynamically from the list definition (orderindex) — works with ANY
ClickUp list, not a fixed funnel. Configure your list + fields in
~/.modular-context/clickup/credentials.json (see review-core/references/credentials.example.json).

Shared client: review-core/lib/clickup_client.py.

Usage:
    python3 audit.py                 # text report
    python3 audit.py --json          # raw data
    python3 audit.py --stale 14      # stale threshold (days)
    python3 audit.py --today 2026-01-01
"""
import sys, os, json, argparse, datetime

_CORE = os.path.join(os.path.dirname(__file__), '..', '..', 'review-core', 'lib')
sys.path.insert(0, os.path.abspath(_CORE))
from clickup_client import ClickUp  # noqa: E402


def to_date(ms):
    try:
        return datetime.date.fromtimestamp(int(ms) / 1000)
    except (TypeError, ValueError):
        return None


def build(today):
    cu = ClickUp()
    list_id = cu.c['crm_list_id']
    F = cu.c.get('field_ids', {})
    val_field = F.get('estimated_value')
    lo_field = F.get('last_outreach_date')

    # stages + which are 'done' (type done/closed) — straight from the list definition
    meta = cu.list_status_meta(list_id)
    meta.sort(key=lambda x: x.get('orderindex', 0))
    stage_order = [s['status'] for s in meta]
    done = {s['status'] for s in meta if s.get('type') in ('done', 'closed')}
    # "near close" = last 1-3 active (non-done) stages
    active_stages = [s for s in stage_order if s not in done]
    hot = active_stages[-3:] if len(active_stages) >= 3 else active_stages

    tasks = cu.get_list_tasks(list_id)
    groups = {}
    for t in tasks:
        groups.setdefault(t.get('status', {}).get('status', '?'), []).append(t)

    def rows(stage):
        out = []
        for t in groups.get(stage, []):
            lo = to_date(cu.custom_field(t, lo_field)) if lo_field else None
            val = cu.custom_field(t, val_field) if val_field else None
            try:
                valf = float(val) if val not in (None, '') else None
            except (TypeError, ValueError):
                valf = None
            out.append({'name': t.get('name', '?'),
                        'outreach_age': (today - lo).days if lo else None,
                        'value': valf, 'url': t.get('url')})
        return out

    return {
        'fetched': len(tasks), 'today': today.isoformat(),
        'stage_order': stage_order, 'done': sorted(done), 'hot': hot,
        'stages': {st: rows(st) for st in stage_order},
        'unmapped': {st: rows(st) for st in groups if st not in stage_order},
    }


def render(report, stale_days):
    L = [f"# ClickUp Review (as of {report['today']})",
         f"Fetched {report['fetched']} tasks.\n", f"{'STAGE':28} {'#':>3} {'sum value':>10}", '-' * 45]
    active = 0
    for st in report['stage_order']:
        rs = report['stages'][st]
        s = sum(r['value'] for r in rs if r['value'])
        if st not in report['done']:
            active += len(rs)
        L.append(f"{st[:28]:28} {len(rs):>3} {s:>10,.0f}")
    for st, rs in report['unmapped'].items():
        L.append(f"[UNMAPPED] {st[:17]:17} {len(rs):>3}")
    L.append('-' * 45)
    L.append(f"{'ACTIVE PIPELINE':28} {active:>3}\n")
    for st in report['hot']:
        rs = report['stages'].get(st, [])
        if not rs:
            continue
        L.append(f"## {st} ({len(rs)})")
        for r in sorted(rs, key=lambda x: (x['outreach_age'] is None, -(x['outreach_age'] or 0))):
            age = f"{r['outreach_age']}d ago" if r['outreach_age'] is not None else "no outreach date"
            L.append(f"  - {r['name'][:45]:45} | {age}")
        L.append("")
    L.append(f"## Stale (>{stale_days}d, active stages)")
    flagged = False
    for st in report['stage_order']:
        if st in report['done']:
            continue
        for r in report['stages'][st]:
            if r['outreach_age'] is not None and r['outreach_age'] > stale_days:
                L.append(f"  - {r['name'][:40]:40} | {st[:22]:22} | {r['outreach_age']}d")
                flagged = True
    if not flagged:
        L.append("  (none / outreach dates not set)")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--json', action='store_true')
    ap.add_argument('--stale', type=int, default=14)
    ap.add_argument('--today', default=None)
    a = ap.parse_args()
    today = datetime.date.fromisoformat(a.today) if a.today else datetime.date.today()
    report = build(today)
    print(json.dumps(report, ensure_ascii=False, indent=1) if a.json else render(report, a.stale))


if __name__ == '__main__':
    main()
