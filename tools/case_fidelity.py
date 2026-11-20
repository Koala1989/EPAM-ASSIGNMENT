"""Case-fidelity check: does a Playwright UI spec match its Approved manual case? Deterministic, no LLM.

It checks the rules automation/CONVENTIONS.md (UI) already sets for a spec, against the case its first line names:
  - the `// case:` line points to the case, the case is Approved or Changed, and the file is <case id>.spec.ts;
  - the test title is `<case ID>: <case title>` and the tags are the case's Tags;
  - one `test.step` per case step, numbered `<n>.` in order, each with at least one `expect` when the step has an
    Expected result;
  - every `QA-<suffix> <name>` record in the Prerequisites (Data) is created with the matching `data.*` call, and
    where the Prerequisites state a parent or category, the spec uses it. Recognised wordings: `A` > `B` > `C`,
    `X` and `Y` under `Z`, one part in each of A and B, named `X`, `Y`, and `X` in `Z`;
  - every `QA-<suffix> <name>` in a step's Test data or Expected result is used in the spec (`data.name('<name>')`).
Names are read from `data.name('<name>')` written in place, through a variable, or through an array of them
(`[data.name('A'), ...]` or `['A', ...].map((l) => data.name(l))`, then `x[0]`).

It checks shape (names, counts, parents, steps), not meaning: whether an assertion proves its Expected result stays
with playwright-test-reviewer. Prerequisites are prose, so a relationship worded another way is not checked.
Problems fail the check; warnings (step wording, records the case does not list) are for the reader only.

Used by tools/generator_gate.py (the PreToolUse hook that refuses a generator's spec write) and from the repo root:
  python tools/case_fidelity.py <spec.ts> ...      check these specs
  python tools/case_fidelity.py --all              every UI spec (not the seeds)
Exit code 1 if any spec has a problem.
"""

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
UI_TESTS = REPO / "automation" / "tests" / "ui"
SPEC_PATH = re.compile(r"automation/tests/ui/(?!seeds/)[^/]+/[^/]+\.spec\.ts$")
# The case Tags (references/seed-manual-test-case.md) and the spec tag each one becomes (CONVENTIONS.md UI)
TAG_OF = {"Smoke": "@smoke", "Regression": "@regression", "Cross-functional": "@cross-functional",
          "Permissions": "@permissions", "Settings-dependent": "@settings"}
DATA_CALLS = ("category", "part", "company", "parameterTemplate", "location")
KIND_OF_WORD = {"category": "category", "categories": "category", "part": "part", "parts": "part",
                "company": "company", "companies": "company", "parameter template": "parameterTemplate",
                "parameter templates": "parameterTemplate", "location": "location", "locations": "location"}
LINK_FIELD = {"category": "parent", "part": "category", "location": "parent"}  # the field that names the parent

QA = r"`QA-<suffix> ([^`]+)`"
QA_LIST = r"((?:`QA-<suffix> [^`]+`(?:\s*,\s*|\s+and\s+)?)+)"
KIND_WORD = r"\b(parameter templates?|categor(?:y|ies)|parts?|compan(?:y|ies)|locations?)\b"
STOP_WORDS = {"the", "a", "an", "and", "of", "in", "to", "its", "it", "on", "for", "with", "then", "is", "at", "from"}


@dataclass
class Issue:
    line: int | None
    text: str

    def __str__(self) -> str:
        return f"line {self.line}: {self.text}" if self.line else self.text


@dataclass
class Result:
    spec: str
    case_id: str | None = None
    case_file: str | None = None
    problems: list[Issue] = field(default_factory=list)
    warnings: list[Issue] = field(default_factory=list)
    not_approved: bool = False  # the case may not be automated at all: nothing in the spec to fix

    @property
    def ok(self) -> bool:
        return not self.problems


# --- the case -----------------------------------------------------------------------------------------------------

@dataclass
class Step:
    n: int
    action: str
    test_data: str
    expected: str


@dataclass
class Case:
    id: str
    title: str
    functionality: str
    fields: dict[str, str]
    steps: list[Step]

    @property
    def tag_words(self) -> list[str]:
        return [t.strip() for t in plain(self.fields.get("Tags", "")).split(",") if t.strip() and t.strip() != "None"]

    @property
    def data(self) -> str:
        """The Data part of the Prerequisites, up to Pre-steps."""
        m = re.search(r"Data:\s*(.*?)(?:;\s*Pre-steps:|$)", self.fields.get("Prerequisites", ""), re.S)
        return m.group(1).strip() if m else ""


def _cells(row: str) -> list[str]:
    return [c.strip() for c in re.split(r"(?<!\\)\|", row.strip().strip("|"))]


def plain(text: str) -> str:
    """Markdown emphasis and code marks removed, whitespace collapsed."""
    return re.sub(r"\s+", " ", re.sub(r"[*`]", "", text)).strip()


def find_case(path: Path, case_id: str) -> Case | None:
    text = path.read_text(encoding="utf-8")
    m = re.search(rf"^### {re.escape(case_id)}: (.+?)\s*$(.*?)(?=^### |^---\s*$|\Z)", text, re.M | re.S)
    if not m:
        return None
    title, body = m.group(1), m.group(2)
    fields = {}
    for row in re.findall(r"^\| \*\*(.+?)\*\* \|(.*)\|\s*$", body, re.M):
        fields[row[0]] = row[1].strip()
    steps = []
    after = body.split("**Steps**", 1)[1] if "**Steps**" in body else ""
    for line in after.splitlines():
        cells = _cells(line) if line.startswith("|") else []
        if len(cells) >= 4 and cells[0].isdigit():
            steps.append(Step(int(cells[0]), cells[1], cells[2], cells[3]))
    h1 = re.search(r"^# (.+?)\s*$", text, re.M)
    functionality = re.sub(r":\s*\S+ test cases$", "", h1.group(1)) if h1 else ""
    return Case(case_id, title, functionality, fields, steps)


@dataclass
class CaseData:
    kinds: dict[str, str] = field(default_factory=dict)  # label -> data call (category, part, ...)
    links: list[tuple[str, str]] = field(default_factory=list)  # (child label, parent label)
    warnings: list[str] = field(default_factory=list)


def case_data(data: str) -> CaseData:
    """The QA records the Prerequisites name, their kind, and the parents and categories they state."""
    out = CaseData()
    # other code spans (users, endpoints, file names) emptied; spans are paired left to right
    clean = re.sub(r"`[^`]*`", lambda m: m.group(0) if m.group(0).startswith("`QA-<suffix> ") else "``", data)
    kind = None
    for m in re.finditer(rf"{QA}|{KIND_WORD}", clean, re.I):
        if m.group(1):
            out.kinds.setdefault(m.group(1), kind or "record")
        else:
            kind = KIND_OF_WORD[m.group(2).lower()]

    def link(child: str, parent: str) -> None:
        if (child, parent) not in out.links:
            out.links.append((child, parent))

    for m in re.finditer(rf"`QA-<suffix> [^`]+`(?:\s*>\s*`QA-<suffix> [^`]+`)+", clean):  # A > B > C
        names = re.findall(QA, m.group(0))
        for parent, child in zip(names, names[1:]):
            link(child, parent)
    for m in re.finditer(rf"{QA_LIST}\s+under\s+{QA}", clean):  # X and Y under Z
        for child in re.findall(QA, m.group(1)):
            link(child, m.group(2))
    for m in re.finditer(rf"{QA}\s+in\s+(?:the\s+)?(?:category\s+|location\s+)?{QA}", clean):  # X in Z
        link(m.group(1), m.group(2))
    for m in re.finditer(rf"in each of ([^`;]+?),?\s+named\s+{QA_LIST}", clean):  # one part in each of A and B, named
        parents = [p for p in re.split(r"\s*,\s*|\s+and\s+", m.group(1).strip()) if p]
        children = re.findall(QA, m.group(2))
        if len(parents) != len(children):
            out.warnings.append(f"Prerequisites: {len(children)} names for {len(parents)} parents in "
                                f"'in each of {m.group(1)}'; these links were not checked")
            continue
        for parent, child in zip(parents, children):
            link(child, parent)
    return out


# --- the spec -----------------------------------------------------------------------------------------------------

def blank(text: str) -> tuple[str, str]:
    """(text without comments, text without comments or string contents): same length, same line breaks."""
    no_comments, skeleton = list(text), list(text)
    i, n = 0, len(text)

    def clear(a: int, b: int, comment: bool) -> None:
        for k in range(a, b):
            if text[k] != "\n":
                skeleton[k] = " "
                if comment:
                    no_comments[k] = " "

    while i < n:
        if text.startswith("//", i):
            j = text.find("\n", i)
            j = n if j < 0 else j
            clear(i, j, True)
            i = j
        elif text.startswith("/*", i):
            j = text.find("*/", i + 2)
            j = n if j < 0 else j + 2
            clear(i, j, True)
            i = j
        elif text[i] in "'\"`":
            quote, j = text[i], i + 1
            while j < n and text[j] != quote:
                j += 2 if text[j] == "\\" else 1
            clear(i + 1, min(j, n), False)
            i = j + 1
        else:
            i += 1
    return "".join(no_comments), "".join(skeleton)


def closing(skeleton: str, open_at: int) -> int:
    """Index of the bracket closing the one at open_at (strings and comments already blanked)."""
    depth = 0
    for k in range(open_at, len(skeleton)):
        if skeleton[k] in "([{":
            depth += 1
        elif skeleton[k] in ")]}":
            depth -= 1
            if depth == 0:
                return k
    return len(skeleton)


def unescape(s: str) -> str:
    return re.sub(r"\\(.)", r"\1", s)


STRING = r"""(['"`])((?:\\.|(?!\1)[^\\])*)\1"""
NAME_CALL = r"""data\.name\(\s*['"`]([^'"`]+)['"`]\s*\)"""


@dataclass
class SpecStep:
    n: int | None
    title: str
    line: int
    expects: int


@dataclass
class Record:
    call: str
    label: str | None
    var: str | None
    link_field: str | None
    link_var: str | None
    line: int


@dataclass
class Spec:
    case_line: tuple[str, str] | None
    titles: list[tuple[str, int]]
    tags: set[str]
    describe: str | None
    steps: list[SpecStep]
    records: list[Record]
    used: set[str]  # every data.name('<label>')


def parse_spec(text: str) -> Spec:
    nc, sk = blank(text)

    def line(at: int) -> int:
        return text.count("\n", 0, at) + 1

    first = next((ln for ln in text.splitlines() if ln.strip()), "")
    m = re.match(r"\s*// case: (\S+) \(([^)]+)\)", first)
    case_line = (m.group(1), m.group(2)) if m else None

    titles, tags = [], set()
    for m in re.finditer(rf"(?<![\w.])test(?:\.fixme)?\(\s*{STRING}", nc):
        titles.append((plain(unescape(m.group(2))), line(m.start())))
        args = nc[m.start(): closing(sk, nc.index("(", m.start()))]
        t = re.search(r"\btag\s*:\s*(\[[^\]]*\]|['\"][^'\"]*['\"])", args)
        if t:
            tags |= set(re.findall(r"['\"]([^'\"]+)['\"]", t.group(1)))
    d = re.search(rf"\btest\.describe\(\s*{STRING}", nc)

    steps = []
    for m in re.finditer(rf"\btest\.step\(\s*{STRING}", nc):
        open_at = nc.index("(", m.start())
        body = sk[open_at: closing(sk, open_at)]
        title = plain(unescape(m.group(2)))
        n = re.match(r"(\d+)\.\s", title)
        steps.append(SpecStep(int(n.group(1)) if n else None, title, line(m.start()),
                              len(re.findall(r"\bexpect(?:\.\w+)?\s*\(", body))))

    names = {}  # variable -> label, for `const x = <expression with one data.name('<label>')>`
    for m in re.finditer(r"\b(?:const|let)\s+(\w+)\s*=\s*([^;\n]*)", nc):
        labels = re.findall(NAME_CALL, m.group(2))
        if len(labels) == 1 and "await data." not in m.group(2):
            names[m.group(1)] = labels[0]

    # variable -> labels, for `const x = [data.name('A'), ...]` and `const x = ['A', ...].map((l) => data.name(l))`,
    # so that `data.part(x[0], ...)` resolves to 'A'
    arrays, used = {}, set(re.findall(NAME_CALL, nc))
    for m in re.finditer(r"\b(?:const|let)\s+(\w+)\s*=\s*\[", nc):
        open_at = m.end() - 1
        close = closing(sk, open_at)
        items = split_top(nc, sk, open_at + 1, close)
        if re.match(r"\s*\.map\(\s*\(?\s*(\w+)\s*\)?\s*=>\s*data\.name\(\s*\1\s*\)\s*\)", nc[close + 1: close + 200]):
            labels = [unescape(s.group(2)) if (s := re.fullmatch(rf"\s*{STRING}\s*", item)) else None for item in items]
            used |= {label for label in labels if label}
        else:
            labels = [found[0] if len(found := re.findall(NAME_CALL, item)) == 1 else None for item in items]
        arrays[m.group(1)] = labels

    def label_of(arg: str) -> str | None:
        call = re.search(NAME_CALL, arg)
        if call:
            return call.group(1)
        index = re.fullmatch(r"\s*(\w+)\s*\[\s*(\d+)\s*\]\s*", arg)
        if index and index.group(1) in arrays and int(index.group(2)) < len(arrays[index.group(1)]):
            return arrays[index.group(1)][int(index.group(2))]
        return names.get(arg.strip())

    records = []
    for m in re.finditer(rf"(?:\b(?:const|let)\s+(\w+)\s*=\s*)?await\s+data\.({'|'.join(DATA_CALLS)})\s*\(", nc):
        open_at = m.end() - 1
        args = split_top(nc, sk, open_at + 1, closing(sk, open_at))
        rest = ",".join(args[1:])
        ref = re.search(r"\b(parent|category|location)\s*:\s*(\w+)\.pk\b", rest)
        records.append(Record(m.group(2), label_of(args[0]) if args else None, m.group(1), ref.group(1) if ref else None,
                              ref.group(2) if ref else None, line(m.start())))
    return Spec(case_line, titles, tags, plain(unescape(d.group(2))) if d else None, steps, records, used)


def split_top(nc: str, sk: str, start: int, end: int) -> list[str]:
    """The comma-separated items of nc[start:end] at bracket depth 0 (sk: the same text with strings blanked)."""
    items, depth, last = [], 0, start
    for k in range(start, end):
        depth += sk[k] in "([{"
        depth -= sk[k] in ")]}"
        if sk[k] == "," and depth == 0:
            items.append(nc[last:k])
            last = k + 1
    items.append(nc[last:end])
    return [item for item in items if item.strip()]


# --- the check ----------------------------------------------------------------------------------------------------

def _words(text: str) -> set[str]:
    return {w for w in re.findall(r"[a-z0-9]+", plain(text).lower()) if w not in STOP_WORDS}


def check(text: str, spec_path: str) -> Result:
    """Check one spec's text (spec_path: where it is or will be written, for the file-name rule)."""
    rel = spec_path.replace("\\", "/")
    result = Result(spec=rel)
    problems, warnings = result.problems, result.warnings
    spec = parse_spec(text)

    if not spec.case_line:
        problems.append(Issue(1, "the first line must be `// case: test-cases/<Area folder>/<file>.md (<case ID>)`"))
        return result
    case_path, case_id = spec.case_line
    result.case_id, result.case_file = case_id, case_path
    path = REPO / case_path
    case = find_case(path, case_id) if path.is_file() else None
    if case is None:
        where = "does not exist" if not path.is_file() else f"has no `### {case_id}:` heading"
        problems.append(Issue(1, f"the `// case:` line names {case_path}, which {where}"))
        return result

    review = case.fields.get("Review", "")
    if not re.match(r"(Approved|Changed)\b", review):
        problems.append(Issue(None, f"{case_id} is not Approved or Changed (Review: {plain(review)[:60]}); "
                                    "only Approved or Changed cases are automated"))
        result.not_approved = True
        return result
    if Path(rel).name != f"{case_id.lower()}.spec.ts":
        problems.append(Issue(None, f"the file must be named {case_id.lower()}.spec.ts"))

    # title and tags
    want = f"{case_id}: {plain(case.title)}"
    if len(spec.titles) != 1:
        problems.append(Issue(spec.titles[1][1] if len(spec.titles) > 1 else None,
                              f"one test per spec; found {len(spec.titles)}"))
    for title, ln in spec.titles[:1]:
        if title != want and not re.fullmatch(rf"{re.escape(case_id)} \[.*\]: {re.escape(plain(case.title))}", title):
            problems.append(Issue(ln, f"the test title must be '{want}', not '{title}'"))
    unknown = [t for t in case.tag_words if t not in TAG_OF]
    if unknown:
        warnings.append(Issue(None, f"case tags not in the seed format: {', '.join(unknown)}; not checked"))
    wanted_tags = {TAG_OF[t] for t in case.tag_words if t in TAG_OF}
    if spec.tags != wanted_tags and spec.titles:
        missing, extra = wanted_tags - spec.tags, spec.tags - wanted_tags
        parts = ([f"missing {', '.join(sorted(missing))}"] if missing else []) + \
                ([f"not in the case: {', '.join(sorted(extra))}"] if extra else [])
        problems.append(Issue(spec.titles[0][1], f"tags must be the case's Tags ({', '.join(sorted(wanted_tags)) or 'none'}): "
                                                 + "; ".join(parts)))
    if case.functionality and spec.describe and plain(case.functionality) != spec.describe:
        warnings.append(Issue(None, f"test.describe is '{spec.describe}'; the case file's functionality is "
                                    f"'{plain(case.functionality)}'"))

    # steps
    if len(spec.steps) != len(case.steps):
        problems.append(Issue(None, f"the case has {len(case.steps)} step(s); the spec has {len(spec.steps)} "
                                    "`test.step` block(s) (one per case step, in order)"))
    for i, (s, c) in enumerate(zip(spec.steps, case.steps), start=1):
        if s.n != i:
            problems.append(Issue(s.line, f"step '{s.title}' must be numbered '{i}.' (case step {i}: {plain(c.action)})"))
        if s.expects == 0 and plain(c.expected) not in ("", "None", "-"):
            problems.append(Issue(s.line, f"step {i} has no `expect`; the case's Expected result: {plain(c.expected)[:160]}"))
        overlap = _words(c.action) & _words(s.title)
        if _words(c.action) and len(overlap) / len(_words(c.action)) < 0.5:
            warnings.append(Issue(s.line, f"step {i} title '{s.title}' differs from the case action '{plain(c.action)}'"))

    # prerequisite records and their parents
    wanted = case_data(case.data)
    warnings += [Issue(None, w) for w in wanted.warnings]
    by_label = {}
    for r in spec.records:
        if r.label is None:
            warnings.append(Issue(r.line, f"data.{r.call}(...) with a name the check cannot read; not checked"))
        else:
            by_label.setdefault(r.label, r)
    by_var = {r.var: r for r in spec.records if r.var}
    last_setup = max((r.line for r in spec.records), default=None)
    for label, kind in wanted.kinds.items():
        r = by_label.get(label)
        if r is None:
            parent = next((p for c, p in wanted.links if c == label), None)
            parent_rec = by_label.get(parent) if parent else None
            note = ""
            if parent and parent_rec and not parent_rec.var:
                note = f"; store the \"{parent}\" {parent_rec.call} created on line {parent_rec.line} in a variable for this"
            ref = parent_rec.var if parent_rec and parent_rec.var else f"<the \"{parent}\" {wanted.kinds.get(parent, 'record')}>"
            fields = f", {{ {LINK_FIELD.get(kind, 'parent')}: {ref}.pk }}" if parent else ""
            call = kind if kind in DATA_CALLS else "<call>"
            where = f" with the other prerequisites (after line {last_setup})" if last_setup else ""
            problems.append(Issue(None, f"the case's Prerequisites create {kind} `QA-<suffix> {label}`; the spec does not. "
                                        f"Add `await data.{call}(data.name('{label}'){fields});`{where}{note}"))
        elif kind in DATA_CALLS and r.call != kind:
            problems.append(Issue(r.line, f"`QA-<suffix> {label}` is a {kind} in the case's Prerequisites; the spec "
                                          f"creates it with data.{r.call}"))
    for child, parent in wanted.links:
        r = by_label.get(child)
        if r is None:
            continue  # reported above as missing
        field_name = LINK_FIELD.get(wanted.kinds.get(child, ""), "parent")
        if r.link_var is None:
            problems.append(Issue(r.line, f"{wanted.kinds.get(child, 'record')} \"{child}\" is created without "
                                          f"`{field_name}`; the case's Prerequisites put it in \"{parent}\""))
            continue
        target = by_var.get(r.link_var)
        if target is None or target.label is None:
            warnings.append(Issue(r.line, f"cannot tell which record `{r.link_var}` is; link of \"{child}\" not checked"))
        elif target.label != parent:
            problems.append(Issue(r.line, f"{wanted.kinds.get(child, 'record')} \"{child}\" is created in \"{target.label}\" "
                                          f"(`{r.link_field}: {r.link_var}.pk`); the case's Prerequisites put it in "
                                          f"\"{parent}\""))
    for r in spec.records:
        if r.label and r.label not in wanted.kinds:
            warnings.append(Issue(r.line, f"creates {r.call} \"{r.label}\", which the case's Prerequisites do not list"))

    # names the steps use
    step_line = {i: s.line for i, s in enumerate(spec.steps, start=1)}
    for i, c in enumerate(case.steps, start=1):
        for label in dict.fromkeys(re.findall(QA, c.test_data + " " + c.expected)):
            if label not in spec.used:
                problems.append(Issue(step_line.get(i), f"step {i} of the case uses `QA-<suffix> {label}`; the spec "
                                                        f"never uses data.name('{label}')"))
    return result


def check_file(path: Path) -> Result:
    return check(path.read_text(encoding="utf-8"), path.resolve().relative_to(REPO.resolve()).as_posix())


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("specs", nargs="*", type=Path, help="spec files to check")
    parser.add_argument("--all", action="store_true", help="every UI spec under automation/tests/ui (not the seeds)")
    parser.add_argument("--quiet", action="store_true", help="problems only, no warnings")
    args = parser.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    specs = list(args.specs) + (sorted(p for p in UI_TESTS.glob("*/*.spec.ts") if p.parent.name != "seeds") if args.all else [])
    if not specs:
        parser.print_help()
        return
    failed = 0
    for path in specs:
        r = check_file(path)
        failed += not r.ok
        print(f"{'FAIL' if r.problems else 'ok  '}  {r.case_id or '?':22} {r.spec}")
        for p in r.problems:
            print(f"      problem: {p}")
        for w in [] if args.quiet else r.warnings:
            print(f"      warning: {w}")
    print(f"\n{len(specs) - failed} of {len(specs)} specs match their case")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
