"""Export the prompts used to drive the agents into agents/prompts.md.

Reads the Claude Code session transcripts for this project. By default it writes the architect's selected
prompts (tools/prompts_selection.json) grouped by theme, every skill command, and how the agents are briefed.
With --all it writes the full log instead: every prompt the architect typed, every skill command and the exact
prompt each agent was started with, by day. Built-in commands, background-task notices and tool results are
left out; long pastes are shortened and demo passwords masked.

Usage (from the repository root):
    python tools/export_prompts.py [--transcripts <dir>] [--out agents/prompts.md]
    python tools/export_prompts.py --all --out <file>
"""
import argparse, glob, json, os, re, sys
from collections import Counter, OrderedDict

MAIN = '71e523c9'  # the architect's main working session (continued across compactions)
SKIP_COMMANDS = {'/usage', '/usage-credits'}


def extract(D):
    out = []
    def clean(t):
        t = re.sub(r'<system-reminder>.*?</system-reminder>', '', t, flags=re.S)
        t = re.sub(r'<ide_[a-z_]+>.*?</ide_[a-z_]+>', '', t, flags=re.S)
        return t.strip()
    for f in glob.glob(os.path.join(D, '*.jsonl')):
        sid = os.path.basename(f)[:8]
        for line in open(f, encoding='utf-8'):
            try: d = json.loads(line)
            except: continue
            ts = d.get('timestamp', '')
            m = d.get('message') or {}
            c = m.get('content')
            if d.get('type') == 'user' and not d.get('isMeta') and not d.get('isCompactSummary'):
                texts = [c] if isinstance(c, str) else [b.get('text', '') for b in (c or []) if isinstance(b, dict) and b.get('type') == 'text']
                for t in texts:
                    if not t or 'tool_use_id' in t: continue
                    if t.startswith('This session is being continued') or '<local-command-caveat>' in t or '<local-command-stdout>' in t: continue
                    cm = re.search(r'<command-name>(.*?)</command-name>.*?<command-args>(.*?)</command-args>', t, re.S)
                    if cm:
                        name = cm.group(1).strip()
                        if name in ('/model', '/compact', '/clear', '/mcp', '/agents', '/context', '/cost', '/exit', '/resume', '/login', '/config', '/help', '/status', '/memory', '/init', '/ide', '/doctor', '/plugin', '/permissions', '/hooks', '/add-dir'): continue
                        out.append((ts, sid, 'command', (name + ' ' + cm.group(2).strip()).strip()))
                        continue
                    t = clean(t)
                    if not t or t.startswith('[Request interrupted'): continue
                    out.append((ts, sid, 'user', t))
            if d.get('type') == 'assistant':
                for b in (c or []) if isinstance(c, list) else []:
                    if isinstance(b, dict) and b.get('type') == 'tool_use' and b.get('name') in ('Agent', 'Task'):
                        i = b.get('input', {})
                        out.append((ts, sid, 'agent:' + str(i.get('subagent_type', 'general-purpose')), i.get('prompt', '')))
    out.sort()
    seen = set(); res = []
    for ts, sid, kind, t in out:
        k = (kind, t)
        if k in seen: continue
        seen.add(k); res.append({'ts': ts, 'sid': sid, 'kind': kind, 'text': t})
    return [e for e in res if keep(e)]


def keep(e):
    t = e['text']
    if e['kind'] == 'user' and t.lstrip().startswith('<task-notification>'):
        return False  # background-task completion notices, not prompts
    if e['kind'] == 'user' and t.lstrip().startswith('<command-message>'):
        return False  # the slash command itself is listed separately
    if e['kind'] == 'command' and t.split()[0] in SKIP_COMMANDS:
        return False
    return True


def key(e):
    return f"{e['sid']}@{e['ts']}"


def redact(t):
    return re.sub(r"(admin|allaccess|engineer|reader|noaccess|steven):(inventree|nolimits|partsonly|readonly|youshallnotpass|wizardstaff)", r"\1:<password>", t)


def shorten_pastes(t):
    def rep(m):
        body = m.group(1).strip()
        if len(body) <= 1500:
            return '[pasted]\n' + body + '\n[end of paste]'
        head = re.sub(r'\s+', ' ', body)[:280]
        return f"[pasted, {len(body):,} characters; starts: \"{head}…\"]"
    t = re.sub(r'<pasted_content[^>]*>(.*?)</pasted_content[^>]*>', rep, t, flags=re.S)
    if len(t) > 6000:  # an unwrapped paste (e.g. a long agent trace)
        t = t[:1200].rstrip() + f"\n[… {len(t) - 1200:,} more characters of pasted output omitted]"
    return t


def fence(t):
    return "````text\n" + shorten_pastes(redact(t)).rstrip() + "\n````"


FIXED_PROMPTS = [
    '| Skill | Agent | Prompt |',
    '|---|---|---|',
    '| `/gen-test-cases <UI\\|API> <functionality>` | `test-case-creator` | `Generate <UI\\|API> test cases for <functionality>.` |',
    '| | `test-case-reviewer` | `Review <UI\\|API> test cases for <functionality>: <every case ID created>.` |',
    '| `/automate-cases <case IDs>` | `playwright-test-generator` | `Automate test case <case ID>.` |',
    '| | `playwright-test-healer` (only if lint, types or the first run fail) | `Run and stabilise <spec path>.` plus any lint and type errors |',
    '| | `playwright-test-reviewer` | `Review <spec path>.` |',
    '| `/automate-api-cases <case IDs>` | `api-test-generator` | `Automate test case <case ID>.` |',
    '| | `api-test-reviewer` | `Review <spec path>.` |',
]


def stamp(e):
    return f"{e['ts'][:10]} {e['ts'][11:16]} UTC"


def write_selected(rows, sel, out_path):
    by_key = {key(e): e for e in rows}
    users = [e for e in rows if e['kind'] == 'user']
    commands = [e for e in rows if e['kind'] == 'command']
    agents = [e for e in rows if e['kind'].startswith('agent:')]
    chosen = [k for t in sel['themes'] for k in t['prompts']]
    missing = [k for k in chosen + sel['agent_examples'] if k not in by_key]
    unreviewed = [e for e in users if e['ts'] > sel['reviewed_until']]
    reviewed_total = len(users) - len(unreviewed)
    n_kept = len(chosen) - len([k for k in chosen if k in missing])

    L = ['# Agent prompts', '']
    L.append(f"Selected prompts from my Claude Code sessions (10–16 October 2026): the {n_kept} of my {reviewed_total} prompts that show how I directed the agents. That means designing and refining their instructions, the case formats and conventions, the duplicate rules, the project structure, and cutting tokens and run time. Routine prompts are left out (below). The instructions the agents work under are in [`system-instructions.md`](system-instructions.md).")
    L.append('')
    L.append('## What is in this file')
    L.append('')
    L.append('| Section | Contents |')
    L.append('|---|---|')
    L.append(f"| [Prompts by theme](#prompts-by-theme) | {n_kept} prompts I typed, grouped by theme, in time order within each theme. Verbatim, typos included. |")
    L.append(f"| [Skill runs](#skill-runs) | All {len(commands)} skill commands I ran. They generated the test cases and the automation. |")
    L.append(f"| [How the agents are briefed](#how-the-agents-are-briefed) | The fixed prompts the skills send to each agent, and {len(sel['agent_examples'])} early briefings written in full before the skills existed. |")
    L.append('')
    L.append('**Left out:**')
    L.append('- routine operations: run this, delete that spec, mark cases approved, git, commands to run tests;')
    L.append('- questions about the generated code or tools ("what does this fixture do?"), and token or cost look-ups;')
    L.append('- prompts that fixed individual cases from review findings. The review files and each case\'s Review field record those changes;')
    L.append('- prompts for recording the demo videos;')
    L.append(f"- the other {len(agents) - len(sel['agent_examples'])} agent prompts. They are the fixed prompts in the table below, with only the case IDs or paths changing.")
    L.append('')
    L.append('**How it was produced.** [`tools/export_prompts.py`](../tools/export_prompts.py) reads the session transcripts in `~/.claude/projects/c--EPAM-Assignment/` and keeps the prompts listed in [`tools/prompts_selection.json`](../tools/prompts_selection.json). `python tools/export_prompts.py --all --out <file>` writes the full log instead: every prompt, skill command and agent prompt, by day. Pasted text up to 1,500 characters is kept whole; longer pastes are shortened, with their length noted, and demo passwords are masked. The planning before 10 October happened in a separate claude.ai chat and is not in the transcripts.')
    L.append('')
    L.append('## Prompts by theme')
    L.append('')
    L.append('| Theme | Prompts | What they show |')
    L.append('|---|---|---|')
    for t in sel['themes']:
        anchor = re.sub(r'[^a-z0-9 -]', '', t['title'].lower()).replace(' ', '-')
        L.append(f"| [{t['title']}](#{anchor}) | {len([k for k in t['prompts'] if k in by_key])} | {t['summary']} |")
    L.append('')
    n = 0
    for t in sel['themes']:
        L.append(f"### {t['title']}")
        L.append('')
        L.append(t['summary'])
        L.append('')
        for e in sorted((by_key[k] for k in t['prompts'] if k in by_key), key=lambda e: e['ts']):
            n += 1
            where = '' if e['sid'] == MAIN else ' · separate session'
            L.append(f"**{n}. {stamp(e)}**{where}")
            L.append('')
            L.append(fence(e['text']))
            L.append('')
    L.append('## Skill runs')
    L.append('')
    L.append('Every skill command, in order. Each one ran the agents for one stage: test cases, UI automation or API automation.')
    L.append('')
    L.append('| Date (UTC) | Command |')
    L.append('|---|---|')
    for e in commands:
        command = e['text'].replace('|', '\\|')
        L.append(f"| {stamp(e)[:-4]} | `{command}` |")
    L.append('')
    L.append('## How the agents are briefed')
    L.append('')
    L.append("The skills send short, fixed prompts on purpose: each agent reads its instructions from its own file, and reviewers get only IDs or paths, never another agent's reasoning.")
    L.append('')
    L.extend(FIXED_PROMPTS)
    L.append('')
    counts = Counter(e['kind'].split(':', 1)[1] for e in agents)
    L.append(f"Agent prompts in the transcripts: {len(agents)} (" + ', '.join(f'`{a}` {c}' for a, c in counts.most_common()) + '). `duplicate-judge` was later merged into `test-case-reviewer`.')
    L.append('')
    L.append('### Early briefings, before the skills')
    L.append('')
    L.append('On 11 and 12 October the agents were started with prompts written in full. They carried context that later moved into the agent files, which is why the skills\' prompts are now one line.')
    L.append('')
    for k in sel['agent_examples']:
        if k not in by_key:
            continue
        e = by_key[k]
        L.append(f"**`{e['kind'].split(':', 1)[1]}`, {stamp(e)}**")
        L.append('')
        L.append(fence(e['text']))
        L.append('')
    open(out_path, 'w', encoding='utf-8', newline='\n').write('\n'.join(L).rstrip() + '\n')
    print(f"selected prompts written: {n} of {reviewed_total}; skill commands: {len(commands)}; agent briefings: {len(sel['agent_examples'])}")
    for k in missing:
        print('  not found in the transcripts:', k)
    if unreviewed:
        print(f"  {len(unreviewed)} newer prompt(s) not classified yet; add the keys to keep to {SELECTION}:")
        for e in unreviewed:
            preview = re.sub(r'\s+', ' ', e['text'])[:90]
            print(f"    {key(e)}  {preview}")


def write_all(rows, out_path):
    DAYS = OrderedDict([
        ('2026-10-10', 'Requirements snapshot, seed case formats, duplicate checker, the test-case-creator agent and the requirements inventory'),
        ('2026-10-11', 'Guardrails and the Review field; first case generation; manual runs through Playwright MCP; the /gen-test-cases skill; revisions'),
        ('2026-10-12', 'Playwright generator, healer and reviewer agents; CONVENTIONS.md; first UI automation; real-form login; local RAG; prompt caching; /automate-cases; CLAUDE.md; API agents'),
        ('2026-10-13', 'API automation layers; API CRUD cases and automation; schema findings; shared config; workflow diagrams; reviewer merged with the duplicate judge; bulk case generation'),
        ('2026-10-14', 'Units, parameters and API VAL/LST/REL cases; one automation project; full Area folder names; demo environment; Expected-result rule for open questions'),
        ('2026-10-15', 'BOM, detail view, categories, templates, stock, creation and API SEC/conflict cases; review fixes and reviewer-catches.md; UI automation for the video; generator fixes; cross-functional scenarios'),
        ('2026-10-16', 'Submission gaps, README, data-driven (parameterised) API cases, common folders for questions and reviews'),
    ])

    def label(e):
        k = e['kind']
        if k == 'user':
            return 'Architect' if e['sid'] == MAIN else 'Architect (separate session)'
        if k == 'command':
            return 'Skill command'
        via = 'started by the main session' if e['sid'] == MAIN else 'started by the skill'
        return f"Agent prompt → `{k.split(':', 1)[1]}` ({via})"

    cnt = Counter('user' if e['kind'] == 'user' else 'command' if e['kind'] == 'command' else 'agent' for e in rows)
    L = ['# Agent prompts: full log', '']
    L.append(f"Every prompt from the Claude Code sessions (10–16 October 2026), in time order: {cnt['user']} architect prompts, {cnt['command']} skill commands and {cnt['agent']} agent prompts. Written by `python tools/export_prompts.py --all`; the curated selection is [`agents/prompts.md`](prompts.md).")
    L.append('')
    n = 0
    for day, summary in DAYS.items():
        day_rows = [e for e in rows if e['ts'].startswith(day)]
        if not day_rows:
            continue
        L.append(f'## {day}: {summary}')
        L.append('')
        for e in day_rows:
            n += 1
            L.append(f"**{n}. {e['ts'][11:16]} UTC · {label(e)}** · session `{e['sid']}`")
            L.append('')
            L.append(fence(e['text']))
            L.append('')
    open(out_path, 'w', encoding='utf-8', newline='\n').write('\n'.join(L).rstrip() + '\n')
    print('entries written:', n, dict(cnt))


SELECTION = 'tools/prompts_selection.json'

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--transcripts", default=os.path.expanduser("~/.claude/projects/c--EPAM-Assignment"))
    ap.add_argument("--out", default="agents/prompts.md")
    ap.add_argument("--all", action="store_true", help="write the full log instead of the selection")
    ap.add_argument("--selection", default=SELECTION)
    a = ap.parse_args()
    SELECTION = a.selection
    rows = extract(a.transcripts)
    if a.all:
        write_all(rows, a.out)
    else:
        write_selected(rows, json.load(open(a.selection, encoding='utf-8')), a.out)
