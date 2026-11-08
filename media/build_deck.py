"""Build editable slides using the supplied deck's measured visual language."""

import argparse
import hashlib
import json
import math
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.util import Inches, Pt

from workshop_content import AGENDA, SLIDES, SOURCES, VERIFIED

BG = "0A0C10"
WHITE = "FFFFFF"
MUTED = "8B939E"
CYAN = "57CCC5"
BRIGHT_CYAN = "4DE1F5"
PURPLE = "A371F7"
BLUE = "388BFD"
GREEN = "56D364"
ORANGE = "FF8A3D"
PANEL = "171B25"


def colour(value):
    return RGBColor.from_string(value)


def box(slide, x, y, w, h, fill=PANEL, rounded=False):
    shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE,
        Inches(x), Inches(y), Inches(w), Inches(h),
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = colour(fill)
    shape.line.fill.background()
    return shape


def text(slide, x, y, w, h, value, size=20, color=WHITE, bold=False, font="Arial"):
    shape = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    shape.name = value.replace("\n", " ")[:100]
    shape._element.nvSpPr.cNvPr.set("descr", value)
    tf = shape.text_frame
    tf.clear()
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = 0
    tf.margin_top = tf.margin_bottom = 0
    for i, line in enumerate(value.split("\n")):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = line
        p.font.name = font
        p.font.size = Pt(size)
        p.font.bold = bold
        p.font.color.rgb = colour(color)
        p.space_after = Pt(5)
    return shape


def bullet_list(slide, items, x, y, width, size=20):
    def heights(font_size):
        chars = max(20, int(width * 7.5 * (20 / font_size)))
        return [
            max(0.5, max(1, math.ceil(len(item) / chars)) * font_size / 72 * 1.25 + 0.12)
            for item in items
        ]

    while y + sum(heights(size)) + len(items) * 0.12 > 5.02 and size > 14:
        size -= 1
    sizes = heights(size)
    if y + sum(sizes) + len(items) * 0.12 > 5.02:
        raise ValueError(f"Content needs a split slide: {items}")
    current = y
    for i, (item, height) in enumerate(zip(items, sizes)):
        text(slide, x, current, 0.28, 0.4, ">", size, [CYAN, PURPLE, GREEN, BLUE][i % 4], True)
        text(slide, x + 0.33, current, width - 0.33, height, item, size, WHITE)
        current += height + 0.12


def interface(slide, kind):
    box(slide, 0.45, 1.75, 9.1, 2.05, PANEL, True)
    left = "PROJECTS / SESSIONS" if kind == "app" else "SESSIONS / CUSTOMIZATIONS"
    text(slide, 0.66, 1.94, 2.15, 0.6, left, 12, CYAN, True)
    text(slide, 0.66, 2.65, 2.2, 0.8, "One goal\nBounded tasks", 15)
    box(slide, 3.0, 1.92, 3.95, 1.67, "22243B", True)
    text(slide, 3.2, 2.08, 3.45, 0.4, "ACTIVE CONVERSATION", 13, PURPLE, True)
    text(slide, 3.2, 2.6, 3.45, 0.7, "Goal -> tools -> evidence\nVerify workspace and permissions", 16)
    text(slide, 7.21, 1.94, 1.95, 0.4, "REVIEW", 13, GREEN, True)
    text(slide, 7.21, 2.6, 1.95, 0.8, "Files / Changes\nChecks / Preview", 15)
    text(slide, 0.55, 3.93, 8.9, 0.3, "Original orientation schematic; use the live product for exact controls.", 11, MUTED)


def flow(slide, dependency=False):
    labels = ["Contract", "Worker A + B", "Integrate", "Validate"] if dependency else [
        "Reader A + B", "Reports", "ONE writer", "Validate"
    ]
    for i, label in enumerate(labels):
        x = 0.52 + i * 2.38
        box(slide, x, 1.85, 2.08, 0.82, "22243B", True)
        text(slide, x + 0.12, 2.06, 1.84, 0.38, label, 17, GREEN if i == 2 else CYAN, True)
        if i < 3:
            text(slide, x + 2.1, 2.06, 0.28, 0.4, ">", 22, PURPLE, True)


def ownership(slide):
    rows = [
        ("WORKER A", "Owned module A + tests A", GREEN),
        ("WORKER B", "Owned module B + tests B", BLUE),
        ("INTEGRATOR", "Contract / UI wiring / fixtures / Git", PURPLE),
    ]
    for i, (owner, paths, color) in enumerate(rows):
        y = 1.72 + i * 0.64
        box(slide, 0.5, y, 9.0, 0.54, PANEL, True)
        text(slide, 0.67, y + 0.12, 2.0, 0.35, owner, 16, color, True)
        text(slide, 2.75, y + 0.12, 6.5, 0.35, paths, 17)


def theme_metadata(template):
    ns = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main"}
    with zipfile.ZipFile(template) as source:
        theme = source.read("ppt/theme/theme1.xml")
    root = ET.fromstring(theme)
    palette = {}
    for item in root.find("a:themeElements/a:clrScheme", ns):
        entry = next(iter(item))
        palette[item.tag.rsplit("}", 1)[-1]] = entry.attrib.get("val", entry.attrib.get("lastClr"))
    return theme, palette


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--template", type=Path, required=True)
    parser.add_argument("--out", type=Path, default=Path("deliverables"))
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    theme, palette = theme_metadata(args.template)
    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(5.625)
    prs.core_properties.title = "Advanced GitHub Copilot: From agent user to agent orchestrator"
    prs.core_properties.subject = "Three-hour workshop: custom agents, skills and safe repository orchestration"
    prs.core_properties.author = "Advanced GitHub Copilot workshop"
    prs.core_properties.keywords = "Copilot, agents, subagents, skills, worktrees, workshop"
    prs.core_properties.comments = f"Official sources verified {VERIFIED}. Original teaching content."

    for index, data in enumerate(SLIDES, 1):
        s = prs.slides.add_slide(prs.slide_layouts[6])
        s.background.fill.solid()
        s.background.fill.fore_color.rgb = colour(BG)
        if data["kind"] == "cover":
            box(s, 6.5, 0, 3.5, 5.625, "29247E")
            box(s, 8.15, 0, 1.85, 5.625, "263AA1")
            box(s, 9.6, 0, 0.4, 5.625, CYAN)
            text(s, 0.48, 0.55, 6.0, 0.35, data["section"], 12, BRIGHT_CYAN, True)
            text(s, 0.48, 1.18, 7.75, 2.2, data["title"], 36, WHITE, True)
            bullet_list(s, data["items"], 0.55, 2.45 if len(data["items"]) > 3 else 3.0, 8.1, 16)
        else:
            box(s, 0, 0, 0.10, 5.625, PURPLE)
            text(s, 0.48, 0.23, 8.9, 0.3, data["section"], 11, BRIGHT_CYAN, True)
            title_size = 29 if len(data["title"]) > 47 else 32
            text(s, 0.48, 0.65, 9.02, 0.95, data["title"], title_size, WHITE, True)
            if data["kind"] in ("app", "vscode"):
                interface(s, data["kind"])
                text(s, 0.56, 4.41, 8.88, 0.57, data["items"][1] + " / " + data["items"][-1], 15, BRIGHT_CYAN)
            elif data["kind"] == "ownership":
                ownership(s)
                text(s, 0.6, 4.09, 8.8, 0.8, "Freeze the contract. Stop before touching another owner's file.\nOwnership is advisory; validate the actual changed paths.", 18, BRIGHT_CYAN)
            elif data["kind"] == "flow":
                flow(s, data["section"] == "DEPENDENCIES")
                bullet_list(s, data["items"][1:], 0.6, 3.04, 8.8, 17)
            elif data["code"]:
                bullet_list(s, data["items"], 0.48, 1.85, 4.14, 18)
                box(s, 4.92, 1.78, 4.58, 3.22, PANEL, True)
                code_font = 12 if len(data["code"].splitlines()) <= 9 else 11
                text(s, 5.12, 1.98, 4.18, 2.89, data["code"], code_font, CYAN, False, "Consolas")
            else:
                bullet_list(s, data["items"], 0.58, 1.80, 8.8, 20)

        footer = "Advanced GitHub Copilot workshop  |  Source snapshot: 7 Nov 2026"
        text(s, 0.48, 5.27, 8.55, 0.22, footer, 9, MUTED)
        text(s, 9.18, 5.22, 0.45, 0.28, str(index), 12, WHITE)
        if data["sources"] and data["kind"] != "cover":
            text(s, 0.48, 5.04, 8.7, 0.2, "Sources: " + ", ".join(data["sources"]), 8, MUTED)
        notes = ["STANDALONE EXPLAINER NARRATION (do not read verbatim in the live event).",
                 "Live event: use concise explanations and the 60-minute timed facilitator plan.",
                 data["cue"], data["narration"], "", "OFFICIAL SOURCES:"]
        notes.extend(f"{key}: {SOURCES[key][0]}\n{SOURCES[key][1]}" for key in data["sources"])
        s.notes_slide.notes_text_frame.text = "\n\n".join(notes)

    path = args.out / "advanced-github-copilot-workshop.pptx"
    prs.save(path)
    # Carry across the actual supplied theme, but no old slide text or affiliation.
    temporary = path.with_suffix(".theme.pptx")
    with zipfile.ZipFile(path) as original, zipfile.ZipFile(temporary, "w", zipfile.ZIP_DEFLATED) as result:
        for info in original.infolist():
            result.writestr(info, theme if info.filename == "ppt/theme/theme1.xml" else original.read(info.filename))
    temporary.replace(path)
    metadata = {
        "verified": VERIFIED, "slides": len(SLIDES),
        "template_sha256": hashlib.sha256(args.template.read_bytes()).hexdigest(),
        "style": {
            "size": "16:9, 10 x 5.625 inches", "source_palette": palette,
            "fonts": "Arial / Consolas; supplied theme retained",
            "treatment": "Near-black background, bold white headings, cyan text, purple/blue panels, green/orange semantic accents, numbered footer",
            "adaptation": "Original content and schematics; no copied legacy slide text or presenter affiliation",
        },
        "agenda": AGENDA,
        "slides_data": SLIDES,
    }
    (args.out / "workshop-manifest.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    ledger = [
        "# Source ledger and freshness review",
        f"\nVerified by direct fetch of official pages: **{VERIFIED}**.",
        "This is a dated snapshot, not a guarantee of future UI or schema stability.",
        "The source deck was used for visual formatting, not as a factual source.",
        "\n| ID | Official source | Material supported | Caveat |",
        "|---|---|---|---|",
    ]
    caveats = {
        "S1": "All Copilot plans; organization app policy must be enabled. Modes are not tool permissions.",
        "S2": "Projects are public preview; core labs do not depend on them.",
        "S3": "Workspace choice controls file isolation; permissions and sandboxing are separate.",
        "S4": "Branch shares current folder; New Worktree starts from committed files. UI Commit/Create PR skip local hooks; run required checks explicitly.",
        "S5": "Copilot and Local schemas differ; target changes interpretation, not runtime. Copilot skills field vs Local agents/handoffs.",
        "S6": "Local handoffs only. Instructions alone are not a permission boundary.",
        "S7": "Local invocation stateless, not full-history inheritance. Separate context is not file isolation. Copilot lifecycle differs.",
        "S8": "Automatic selection not guaranteed. Full directory needed. Name matches directory. Skills do not grant tools.",
        "S9": "Custom subagents in CLI do not include repo instructions by default; pass relevant constraints explicitly.",
        "S10": "/fleet can increase AI usage; delegation does not inherently create worktrees.",
        "S11": "VS Code experience preview; Copilot event schema differs from Local. preToolUse timeouts fall through normal permissions, not fail-closed.",
        "S12": "Use bounded tasks, relevant context, requirement-focused checks, review and measured usage.",
        "S13": "Published 28 October 2026. Documents new-session Copilot harness default. Marketplace/connectors preview, computer use experimental.",
        "S14": "Support differs by IDE/surface; recheck client and organization policy.",
        "S15": "Worktrees are not security boundaries. Host execution location differs from model hosting.",
    }
    for key, (title, url) in SOURCES.items():
        ledger.append(f"| {key} | [{title}]({url}) | {title} | {caveats[key]} |")
    ledger += [
        "\n## Before teaching again",
        "1. Reopen all sources, record date/version, and compare agent fields and tool names.",
        "2. Check installed app, VS Code, Copilot access, harness picker and organization policy.",
        "3. Run the attendee preflight, baseline tests and all instructor solutions.",
        "4. Rehearse all three demonstrations on the actual machine.",
        "5. Keep sequential/manual fallback prompts available; do not replace missing features with claims of enforcement.",
        "\n## Original workflow guidance",
        "Task claims/leases, write-ownership matrices, one integration writer, contract freezes and changed-path review are teaching techniques, not claims of a built-in cross-agent filesystem lock.",
        "\n## Media provenance",
        "The editable deck carries the supplied theme and recreates its dark/cyan/purple visual treatment.",
        "All teaching text, task diagrams and interface schematics are original. No presenter or GitHub Expert Services affiliation is implied.",
        "The video uses local Microsoft Zira speech synthesis. It is narrated instruction with code examples, not a recording of a live product demo.",
    ]
    (args.out / "source-ledger.md").write_text("\n".join(ledger) + "\n", encoding="utf-8")
    print(json.dumps({"deck": str(path), "slides": len(SLIDES), "agenda_minutes": sum(m for _, m in AGENDA)}))


if __name__ == "__main__":
    main()
