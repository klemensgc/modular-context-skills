"""
review-core / clickup_adapter — turns raw ClickUp data into normalized Item[] + a
company-health summary. Used by comms-review (ClickUp leg) and clickup-review.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from clickup_client import ClickUp
from model import from_clickup_task


def gather(cu=None, today=None):
    """Collect a ClickUp cross-section for comms-review."""
    import datetime
    cu = cu or ClickUp()
    today = datetime.date.fromisoformat(today) if today else datetime.date.today()

    # 1) my tasks (all configured workspaces)
    my = cu.get_my_tasks_all_teams(include_closed=False)
    my_items, errors = {}, {}
    for team, ts in my.items():
        if isinstance(ts, dict) and 'error' in ts:
            errors[team] = ts['error']
            continue
        my_items[team] = [from_clickup_task(t) for t in ts]

    # 2) newest planning week (optional — needs planning_doc_id)
    week = None
    if cu.c.get('planning_doc_id'):
        try:
            week = cu.latest_planning_week()
        except RuntimeError as e:
            week = {'error': str(e)}

    # 3) CRM funnel headline (optional — needs crm_list_id)
    funnel = {}
    if cu.c.get('crm_list_id'):
        try:
            tasks = cu.get_list_tasks(cu.c['crm_list_id'])
            from collections import Counter
            funnel['by_stage'] = dict(Counter(t.get('status', {}).get('status', '?') for t in tasks))
            funnel['total'] = len(tasks)
        except RuntimeError as e:
            funnel['error'] = str(e)

    return {
        'today': today.isoformat(),
        'my_tasks': {team: [i.to_dict() for i in items] for team, items in my_items.items()},
        'my_tasks_count': {team: len(items) for team, items in my_items.items()},
        'planning_week': week,
        'funnel': funnel,
        'errors': errors,
    }


def health_lines(data):
    """Short 'how is the company doing' summary from the ClickUp angle."""
    L = []
    total_my = sum(data['my_tasks_count'].values())
    L.append(f"ClickUp: {total_my} open tasks assigned to me "
             f"({', '.join(f'{k}={v}' for k, v in data['my_tasks_count'].items())})")
    wk = data.get('planning_week') or {}
    if wk and 'error' not in wk:
        L.append(f"Planning: {wk.get('name')} — {wk.get('content', '')[:140].strip()}")
    f = data.get('funnel', {})
    if 'by_stage' in f:
        L.append(f"CRM funnel: {f['total']} deals across {len(f['by_stage'])} stages")
    return L


if __name__ == '__main__':
    import json, argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--json', action='store_true')
    ap.add_argument('--today', default=None)
    a = ap.parse_args()
    d = gather(today=a.today)
    if a.json:
        print(json.dumps(d, ensure_ascii=False, indent=1))
    else:
        for line in health_lines(d):
            print('•', line)
        for team, items in d['my_tasks'].items():
            print(f"\n[{team}]")
            for it in items:
                print(f"  - {it['title'][:46]:46} | {it['status']} | {it['container']}")
