"""Reads test-case-creator runs from Claude Code's saved session transcripts (step 6).

Claude Code saves each subagent run as ~/.claude/projects/<project>/<session>/subagents/agent-<id>.jsonl, with a
.meta.json beside it naming the agent type. One run = the task prompt, every tool call with its input, and the
final report (the SubagentHandback message). No agent is run again: this only parses what was recorded.
"""

import json
import re
import shlex
from dataclasses import dataclass, field
from pathlib import Path

TRANSCRIPTS = Path.home() / ".claude" / "projects" / "c--EPAM-Assignment"

# The test-case-creator's instructions entered git at 7ea9e53 (2026-10-13 00:37 +05:30). Earlier runs followed
# instructions that are not recorded, so they are not judged.
RULES_SINCE = "2026-10-12T19:07"
# Open questions moved from <Area folder>/open-questions.md to Open_Questions/open-question_<Area>.md on this day
# (commit 7c8b1e7); runs on that day may use either location.
OPEN_QUESTIONS_MOVED = "2026-10-16"

CASE_ID = r"(?:UI|API)-[A-Za-z_]+-\d{3}"


@dataclass
class RagQuery:
    text: str
    top_k: int | None


@dataclass
class Run:
    id: str
    started: str  # ISO UTC
    prompt: str
    tool_calls: list[dict] = field(default_factory=list)  # {"name", "input"} in call order
    report: str | None = None  # the SubagentHandback message; None if the run never handed back

    @property
    def kind(self) -> str:
        return "API" if re.search(r"\bAPI\b", self.prompt) else "UI"

    @property
    def complete(self) -> bool:
        return self.report is not None

    @property
    def judged(self) -> bool:
        """True if the run happened under the instructions now in git."""
        return self.started >= RULES_SINCE

    @property
    def bash(self) -> list[str]:
        return [c["input"].get("command", "") for c in self.tool_calls if c["name"] == "Bash"]

    @property
    def written(self) -> list[str]:
        """Paths of files the run created or edited, in order (forward slashes)."""
        return [c["input"].get("file_path", "").replace("\\", "/") for c in self.tool_calls if c["name"] in ("Write", "Edit")]

    @property
    def rag_queries(self) -> list[RagQuery]:
        """Every query_index.py call, including the ones inside shell `for q in "..." ...; do` loops."""
        queries = []
        for cmd in self.bash:
            lookup = re.search(r"rag_lookup\.py((?:\s+R-[A-Za-z_]+-\d+)+)", cmd)
            if lookup:  # the wrapper: one query per rule ID, always the rule's wording at top-k 3
                queries += [RagQuery(rule_id, 3) for rule_id in lookup.group(1).split()]
                continue
            if "query_index.py" not in cmd:
                continue
            k = re.search(r"--top-k[ =](\d+)", cmd)
            top_k = int(k.group(1)) if k else None
            loop = re.search(r"for \w+ in (.+?);\s*do", cmd, re.S)
            if loop:
                try:
                    texts = shlex.split(loop.group(1))
                except ValueError:
                    texts = re.findall(r'"([^"]+)"', loop.group(1))
            else:
                texts = [m.group(1) for m in re.finditer(r'query_index\.py\s+"([^"]+)"', cmd)]
            queries += [RagQuery(t, top_k) for t in texts]
        return queries

    @property
    def dedupe_runs(self) -> int:
        return sum("dedupe_cases.py" in cmd for cmd in self.bash)

    @property
    def written_case_ids(self) -> list[str]:
        """Case IDs from the case headings ('### <ID>:') in text the run wrote: Write content, Edit replacements,
        and shell writes. Empty when the run built its cases with a generator script (IDs computed at run time)."""
        texts = [c["input"].get("content", "") + c["input"].get("new_string", "") for c in self.tool_calls if c["name"] in ("Write", "Edit")]
        texts += [cmd for cmd in self.bash if "<<" in cmd]
        return sorted({m.group(1) for t in texts for m in re.finditer(rf"^### ({CASE_ID}):", t, re.M)})

    @property
    def case_ids(self) -> list[str]:
        """Case IDs the run created: the headings it wrote, or else the IDs its report lists, with ranges like
        'UI-ATT-001 to UI-ATT-012' expanded. A report can also mention existing cases, so headings come first."""
        used_generator = any(re.search(r"python\S*\s+(?:-\s+\S*\s*)?\S*gen\w*\.py|python\S*\s+\"\$\w+\"", c) for c in self.bash)
        if self.written_case_ids and not used_generator:
            return self.written_case_ids
        if not self.report:
            return self.written_case_ids
        ids = set(re.findall(CASE_ID, self.report))
        for first, last in re.findall(rf"({CASE_ID})\s*(?:to|-|–|\.\.)\s*({CASE_ID})", self.report):
            prefix, a = first.rsplit("-", 1)
            if last.rsplit("-", 1)[0] == prefix:
                ids |= {f"{prefix}-{n:03d}" for n in range(int(a), int(last.rsplit("-", 1)[1]) + 1)}
        return sorted(ids | set(self.written_case_ids))


def load_runs(agent_type: str = "test-case-creator") -> list[Run]:
    runs = []
    for meta in TRANSCRIPTS.glob("*/subagents/*.meta.json"):
        if json.loads(meta.read_text(encoding="utf-8")).get("agentType") != agent_type:
            continue
        run = None
        for line in meta.with_suffix("").with_suffix(".jsonl").read_text(encoding="utf-8").splitlines():
            entry = json.loads(line)
            message = entry.get("message", {})
            if run is None and entry.get("type") == "user" and isinstance(message.get("content"), str):
                run = Run(id=meta.stem.split(".")[0], started=entry["timestamp"], prompt=message["content"])
            if run and entry.get("type") == "assistant":
                for part in message.get("content", []):
                    if part.get("type") == "tool_use":
                        run.tool_calls.append({"name": part["name"], "input": part.get("input", {})})
                        if part["name"] == "SubagentHandback":
                            run.report = part["input"].get("message", "")
        if run:
            runs.append(run)
    return sorted(runs, key=lambda r: r.started)
