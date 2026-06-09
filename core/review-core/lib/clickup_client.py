"""
review-core / clickup_client — shared ClickUp client for the *-review skill family
(clickup-review, comms-review, tasklist auto-read).

Read-first. Write functions (create/update/comment/set_field) exist but call them ONLY
after explicit user approval — review skills are read-only by default.

Config: ~/.modular-context/clickup/credentials.json (outside any repo, NEVER commit).
See references/credentials.example.json for the schema. Get a personal token at
ClickUp → Settings → Apps → API Token.

  v2 — tasks, lists, statuses, custom fields, comments, my-tasks per workspace
  v3 — Docs (planning doc) — works with a personal token, but slow → retry 90s
"""
import json, os, time, urllib.request, urllib.error, urllib.parse

CREDS_PATH = os.path.expanduser('~/.modular-context/clickup/credentials.json')
V2 = 'https://api.clickup.com/api/v2'
V3 = 'https://api.clickup.com/api/v3'


def load_creds():
    if not os.path.exists(CREDS_PATH):
        raise SystemExit(
            f"Missing credentials: {CREDS_PATH}\n"
            "Copy references/credentials.example.json there and fill in your values.")
    return json.load(open(CREDS_PATH))


class ClickUp:
    def __init__(self, creds=None):
        self.c = creds or load_creds()
        self.token = self.c['api_token']
        self.me = self.c.get('me_user_id')
        self.teams = self.c.get('teams', {})

    # ---- low level ----
    def _req(self, url, method='GET', body=None, retries=4, timeout=90):
        data = json.dumps(body).encode() if body is not None else None
        headers = {'Authorization': self.token}
        if body is not None:
            headers['Content-Type'] = 'application/json'
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        for attempt in range(retries):
            try:
                with urllib.request.urlopen(req, timeout=timeout) as r:
                    return json.load(r)
            except urllib.error.HTTPError as e:
                raise RuntimeError(f"ClickUp {e.code}: {e.read()[:300].decode(errors='replace')}")
            except (urllib.error.URLError, TimeoutError) as e:
                if attempt == retries - 1:
                    raise RuntimeError(f"ClickUp unreachable ({retries}x): {e}")
                time.sleep(2 * (attempt + 1))

    # ---- reads ----
    def list_statuses(self, list_id):
        """Funnel stages in canonical order (orderindex)."""
        sts = self._req(f'{V2}/list/{list_id}')['statuses']
        return [s['status'] for s in sorted(sts, key=lambda x: x.get('orderindex', 0))]

    def list_status_meta(self, list_id):
        return self._req(f'{V2}/list/{list_id}')['statuses']

    def get_list_tasks(self, list_id, include_closed=True, subtasks=True):
        tasks, page = [], 0
        while True:
            q = f'include_closed={"true" if include_closed else "false"}&subtasks={"true" if subtasks else "false"}&page={page}'
            d = self._req(f'{V2}/list/{list_id}/task?{q}')
            batch = d.get('tasks', [])
            tasks += batch
            if d.get('last_page') or not batch:
                break
            page += 1
        return tasks

    def get_my_tasks(self, team_id, include_closed=False, subtasks=True):
        """All tasks assigned to me_user_id in a workspace (cross-list)."""
        tasks, page = [], 0
        while True:
            q = (f'assignees%5B%5D={self.me}&include_closed={"true" if include_closed else "false"}'
                 f'&subtasks={"true" if subtasks else "false"}&page={page}')
            d = self._req(f'{V2}/team/{team_id}/task?{q}')
            batch = d.get('tasks', [])
            tasks += batch
            if d.get('last_page') or not batch:
                break
            page += 1
        return tasks

    def get_my_tasks_all_teams(self, include_closed=False):
        out = {}
        for name, tid in self.teams.items():
            try:
                out[name] = self.get_my_tasks(tid, include_closed=include_closed)
            except RuntimeError as e:
                out[name] = {'error': str(e)}
        return out

    @staticmethod
    def custom_field(task, field_id):
        for cf in task.get('custom_fields', []):
            if cf.get('id') == field_id:
                return cf.get('value')
        return None

    # ---- v3 docs (planning) ----
    def doc_pages(self, doc_id, fmt='text/md'):
        team = next(iter(self.teams.values()), None)
        d = self._req(f'{V3}/workspaces/{team}/docs/{doc_id}/pages?content_format={urllib.parse.quote(fmt)}')
        return d if isinstance(d, list) else d.get('pages', [])

    def latest_planning_week(self, doc_id=None, page_prefix=r'^W\d+'):
        """
        Newest weekly page (e.g. W{N}) from a Planning doc.
        'Newest on the list' = page with the highest numeric page-id suffix
        (ClickUp assigns increasing ids on creation) among pages matching page_prefix.
        Returns {name, id, content, subpages} or None.
        """
        import re
        doc_id = doc_id or self.c.get('planning_doc_id')
        if not doc_id:
            return None
        pages = self.doc_pages(doc_id)
        candidates = []

        def walk(ps):
            for p in ps:
                nm = (p.get('name') or '').strip()
                if re.match(page_prefix, nm):
                    suffix = (p.get('id', '')).rsplit('-', 1)[-1]
                    try:
                        candidates.append((int(suffix), p))
                    except ValueError:
                        candidates.append((0, p))
                walk(p.get('pages') or p.get('children') or [])
        walk(pages)
        if not candidates:
            return None
        candidates.sort(key=lambda x: x[0], reverse=True)
        page = candidates[0][1]
        subs = page.get('pages') or page.get('children') or []
        return {
            'name': page.get('name'),
            'id': page.get('id'),
            'content': page.get('content') or '',
            'subpages': [{'name': s.get('name'), 'content': s.get('content') or ''} for s in subs],
        }

    # ---- writes (ONLY after explicit user approval) ----
    def create_task(self, list_id, name, status=None, **extra):
        body = {'name': name}
        if status:
            body['status'] = status
        body.update(extra)
        return self._req(f'{V2}/list/{list_id}/task', 'POST', body)

    def update_task(self, task_id, **fields):
        return self._req(f'{V2}/task/{task_id}', 'PUT', fields)

    def set_field(self, task_id, field_id, value):
        return self._req(f'{V2}/task/{task_id}/field/{field_id}', 'POST', {'value': value})

    def comment(self, task_id, text, notify_all=False):
        return self._req(f'{V2}/task/{task_id}/comment', 'POST',
                         {'comment_text': text, 'notify_all': notify_all})
