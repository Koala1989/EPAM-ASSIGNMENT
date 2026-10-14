"""Draws the workflow diagrams in agents/diagrams/ as SVG, in the style of references/ai-workflow.svg.

Usage: python tools/diagrams/build_diagrams.py
Then render PNGs and check text fits: node tools/diagrams/render.js (needs automation/ installed).
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parents[2] / "agents" / "diagrams"

INK, SUB, ARROW = "#3B3226", "#6B5D47", "#5B4D3A"
KIND = {  # fill, stroke
    "file": ("#FBF8F0", "#8A7A5E"),
    "tool": ("#B9C48F", "#6F7D3E"),
    "agent": ("#E2B08F", "#B5663C"),
    "human": ("#F1DDB0", "#A9822F"),
}
LANE = {"ai": ("#EDE5D3", "#7A6A4F"), "human": ("#E4E8D9", "#6C7A4A"), "result": ("#EFE9DA", "#7A6A4F")}


class Diagram:
    def __init__(self, width, height, title, subtitle):
        self.w, self.h = width, height
        self.parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" '
            'font-family="Segoe UI, Helvetica, Arial, sans-serif">',
            '<defs><marker id="arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="8" markerHeight="8" '
            f'orient="auto-start-reverse"><path d="M1 1 L9 5 L1 9 z" fill="{ARROW}"/></marker></defs>',
            f'<rect width="{width}" height="{height}" fill="#F6F1E7"/>',
            f'<text x="30" y="46" font-size="26" font-weight="700" fill="{INK}">{escape(title)}</text>',
            f'<text x="30" y="74" font-size="15" fill="{SUB}">{escape(subtitle)}</text>',
        ]
        self.n = 0

    def lane(self, kind, y, h, label):
        fill, ink = LANE[kind]
        self.parts.append(f'<rect x="20" y="{y}" width="{self.w - 40}" height="{h}" rx="14" fill="{fill}"/>')
        self.parts.append(f'<text x="40" y="{y + 25}" font-size="13" font-weight="700" letter-spacing="1.5" fill="{ink}">{escape(label)}</text>')

    def box(self, kind, x, y, w, h, title, lines=(), title2=None):
        """A box; returns its (left, top, right, bottom). Titles 17px bold, lines 14px, 22px apart."""
        fill, stroke = KIND[kind]
        self.n += 1
        bid = f"b{self.n}"
        self.parts.append(f'<rect data-box="{bid}" x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
        ty = y + 32
        self.parts.append(f'<text data-in="{bid}" x="{x + 15}" y="{ty}" font-size="17" font-weight="700" fill="{INK}">{escape(title)}</text>')
        if title2:
            ty += 22
            self.parts.append(f'<text data-in="{bid}" x="{x + 15}" y="{ty}" font-size="17" font-weight="700" fill="{INK}">{escape(title2)}</text>')
        ty += 26
        for line in lines:
            self.parts.append(f'<text data-in="{bid}" x="{x + 15}" y="{ty}" font-size="14" fill="{INK}">{escape(line)}</text>')
            ty += 22
        return x, y, x + w, y + h

    def arrow(self, x1, y1, x2, y2, dashed=False, both=False):
        extra = ' stroke-dasharray="7 5"' if dashed else ""
        start = ' marker-start="url(#arr)"' if both else ""
        self.parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{ARROW}" stroke-width="2.5" fill="none"{extra}{start} marker-end="url(#arr)"/>')

    def right(self, a, b):
        """Horizontal arrow from box a to box b (same row)."""
        y = (max(a[1], b[1]) + min(a[3], b[3])) // 2
        self.arrow(a[2] + 2, y, b[0] - 4, y)

    def gate(self, upper, lower, x=None):
        """Dashed two-way arrow between an AI box and the architect's box below it."""
        x = x if x is not None else (upper[0] + upper[2]) // 2
        self.arrow(x, upper[3] + 2, x, lower[1] - 2, dashed=True, both=True)

    def legend(self, x, y, note):
        items = [("agent", "AI agent"), ("tool", "Script or skill"), ("human", "Human step"), ("file", "Files and data")]
        for i, (kind, label) in enumerate(items):
            fill, stroke = KIND[kind]
            lx = x + i * 150
            self.parts.append(f'<rect x="{lx}" y="{y}" width="20" height="20" rx="4" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
            self.parts.append(f'<text x="{lx + 28}" y="{y + 16}" font-size="14" fill="{INK}">{escape(label)}</text>')
        for i, line in enumerate(note):
            self.parts.append(f'<text x="{x}" y="{y + 48 + 22 * i}" font-size="14" fill="{SUB}">{escape(line)}</text>')

    def save(self, name):
        OUT.mkdir(parents=True, exist_ok=True)
        (OUT / f"{name}.svg").write_text("\n".join(self.parts + ["</svg>"]) + "\n", encoding="utf-8")


def test_case_generation():
    d = Diagram(1500, 600, "AI-assisted manual test case workflow",
                "InvenTree 1.5.6 Parts module · UI and API cases · requirements in, reviewed cases out, the architect approves")
    top, bottom = 95, 500
    panels = [(20, 440, "ai", "1 · REQUIREMENTS & RAG"), (500, 500, "ai", "2 · AI FLOW (/gen-test-cases)"),
              (1040, 440, "human", "3 · HUMAN APPROVAL")]
    for x, w, kind, label in panels:
        fill, ink = LANE[kind]
        d.parts.append(f'<rect x="{x}" y="{top}" width="{w}" height="{bottom - top}" rx="14" fill="{fill}"/>')
        d.parts.append(f'<text x="{x + 20}" y="{top + 27}" font-size="13" font-weight="700" letter-spacing="1.5" fill="{ink}">{label}</text>')

    d.box("file", 45, 145, 390, 150, "Requirements", [
        "InvenTree 1.5.6 docs + OpenAPI schema slice", "inventory: UI 227 rules · API 71 rules",
        "answered open questions count too"])
    d.box("tool", 45, 325, 390, 150, "RAG", [
        "local index: ChromaDB + MiniLM over the docs", "confirms each rule's exact wording",
        "API rules: the schema is read directly"])
    creator = d.box("agent", 525, 145, 450, 150, "test-case-creator · Sonnet 5.5", [
        "writes UI or API cases from the inventory, as Draft", "raises open questions instead of assuming",
        "runs the duplicate check"])
    reviewer = d.box("agent", 525, 325, 450, 150, "test-case-reviewer · Opus 5.5", [
        "independent: rule coverage vs the inventory", "case quality, open-question marking",
        "duplicate verdict only when score is 50+"])
    d.arrow(750, creator[3] + 2, 750, reviewer[1] - 4)
    d.box("human", 1065, 145, 390, 330, "Human approval", [
        "answer open questions", "act on the review: gaps, Majors,", "duplicate verdicts",
        "run the cases (UI or API)", "set Review: Draft to Approved", "", "Approved cases feed",
        "UI + API automation"])

    d.arrow(440, 310, 495, 310)
    d.arrow(1000, 310, 1035, 310)
    d.parts.append(f'<path d="M 1260 {bottom + 2} L 1260 535 L 750 535 L 750 {bottom + 6}" stroke="{ARROW}" stroke-width="2.5" '
                   f'fill="none" stroke-dasharray="7 5" marker-end="url(#arr)"/>')
    d.parts.append(f'<text x="840" y="527" font-size="14" fill="{SUB}">answers and gaps go back: rerun /gen-test-cases</text>')
    d.legend(40, 560, [])
    d.save("test-case-generation")


def automation_generation():
    d = Diagram(1500, 870, "AI-assisted automation workflow",
                "Approved manual cases to Playwright + TypeScript specs · UI and API lanes · writers on Sonnet, independent reviewers on Opus")
    d.lane("ai", 95, 385, "AI AND TOOLS")
    d.lane("human", 500, 190, "ARCHITECT (HUMAN)")
    d.lane("result", 710, 140, "RESULT")

    xs, w = [40, 282, 524, 766, 1008, 1250], 210
    ui = [
        d.box("file", xs[0], 140, w, 140, "Approved UI case", ["UI-<Area>-NNN", "Review: Approved", "or Changed"]),
        d.box("tool", xs[1], 140, w, 140, "/automate-cases", ["skill: one trigger", "pre-check, lint, 3 runs", "one case at a time"]),
        d.box("agent", xs[2], 140, w, 140, "Generator", ["playwright-test-generator", "Sonnet 5.5 · live browser", "page objects + fixtures"]),
        d.box("agent", xs[3], 140, w, 140, "Healer", ["playwright-test-healer", "Sonnet 5.5", "fixes how a test runs,", "never what it checks"]),
        d.box("tool", xs[4], 140, w, 140, "Stability check", ["3 green runs in a row", "--repeat-each=3", "run by the skill"]),
        d.box("agent", xs[5], 140, w, 140, "Reviewer", ["playwright-test-reviewer", "Opus 5.5 · independent", "gets the spec path only"]),
    ]
    api = [
        d.box("file", xs[0], 310, w, 150, "Approved API case", ["API-<Area>-NNN", "Review: Approved", "or Changed"]),
        d.box("tool", xs[1], 310, w, 150, "/automate-api-cases", ["skill: one trigger", "pre-check, lint, 3 runs", "one case at a time"]),
        d.box("agent", xs[2], 310, w, 150, "Generator", ["api-test-generator", "Sonnet 5.5 · clients", "writes, runs, stabilises", "status hard, schema soft"]),
        d.box("tool", xs[3], 310, w, 150, "Lint + type check", ["independent re-check", "no healer: the generator", "stabilised it already"]),
        d.box("tool", xs[4], 310, w, 150, "Stability check", ["3 green runs, or failing", "only on known defects", "(soft schema check, F-11)"]),
        d.box("agent", xs[5], 310, w, 150, "Reviewer", ["api-test-reviewer", "Opus 5.5 · independent", "gets the spec path only"]),
    ]
    for row in (ui, api):
        for a, b in zip(row, row[1:]):
            d.right(a, b)

    appr = d.box("human", xs[0], 550, w, 110, "Approve cases", ["only Approved or Changed", "cases are automated"])
    code = d.box("human", xs[2], 550, w, 110, "Review shared code", ["new page-object members", "and client methods"])
    find = d.box("human", xs[4], 550, w, 110, "Decide on findings", ["fixme + // FINDING:", "known defects (F-xx)"])
    rev = d.box("human", xs[5], 550, w, 110, "Act on the review", ["Blockers and Majors", "decide what to fix"])
    d.gate(api[0], appr, x=xs[0] + w - 20)  # off-centre: clear of the lane label
    for upper, lower in [(api[2], code), (api[4], find), (api[5], rev)]:
        d.gate(upper, lower)

    done = d.box("human", xs[4], 740, w, 80, "Done", ["lint, types, 3 runs, verdict"])
    suite = d.box("file", xs[5], 740, w, 80, "Regression suite", ["npm test · @smoke"])
    d.arrow((find[0] + find[2]) // 2, find[3] + 2, (find[0] + find[2]) // 2, done[1] - 4)
    d.right(done, suite)
    d.legend(40, 752, ["Dashed arrows: output goes to the architect, decisions come back.",
                       "Each gate applies to both lanes. One project: automation/tests/ui|api/, reviews/ui|api/."])
    d.save("automation-generation")


if __name__ == "__main__":
    test_case_generation()
    automation_generation()
    print(f"wrote SVGs to {OUT}")
