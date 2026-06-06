#!/usr/bin/env python3
"""Build the requirements Markdown files into a linked PDF.

The script uses only the Python standard library by default. It also writes a
linked HTML file and can optionally ask a local headless Chromium browser, such
as Microsoft Edge or Google Chrome, to print the HTML to PDF.
"""

from __future__ import annotations

import argparse
import html
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
REQUIREMENTS_DIR = REPO_ROOT / "requirements"
DEFAULT_OUTPUT = REPO_ROOT / "build" / "requirements.pdf"
DEFAULT_HTML_OUTPUT = REPO_ROOT / "build" / "requirements.html"

DOC_ORDER = [
    "overview.md",
    "features.md",
    "user-roles.md",
    "api.md",
    "security-auth.md",
    "ui-ux.md",
    "architecture.md",
    "deployment.md",
    "reporting.md",
    "integrations.md",
    "mobile-app.md",
    "open-questions.md",
]

DOC_LINK_LABELS = {
    "api": "API",
    "architecture": "Architecture",
    "deployment": "Deployment",
    "features": "Features",
    "integrations": "Integrations",
    "mobile-app": "Mobile App",
    "open-questions": "Open Questions",
    "overview": "Overview",
    "reporting": "Reporting",
    "security-auth": "Security Auth",
    "ui-ux": "UI/UX",
    "user-roles": "User Roles",
}

HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
LIST_ITEM_RE = re.compile(r"^(\s*)([-+*]|\d+\.)\s+(.*)$")
FENCE_RE = re.compile(r"^\s*(```+|~~~+)(.*)$")
MARKDOWN_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
CODE_SPAN_RE = re.compile(r"`([^`]+)`")
URL_RE = re.compile(r"(?<![\"'=])(https?://[^\s<]+)")


@dataclass
class Heading:
    level: int
    text: str
    anchor: str


@dataclass
class Document:
    path: Path
    rel_path: str
    anchor: str
    title: str
    link_label: str
    text: str
    headings: list[Heading]


@dataclass
class InlineRun:
    text: str
    link: str | None = None
    external: bool = False


@dataclass
class PdfBlock:
    kind: str
    runs: list[InlineRun]
    text: str = ""
    level: int = 0
    anchor: str | None = None
    indent: int = 0


@dataclass
class PdfLink:
    target: str
    external: bool
    rect: tuple[float, float, float, float]


@dataclass
class PdfPage:
    content: list[str]
    links: list[PdfLink]


def strip_inline_markdown(value: str) -> str:
    value = MARKDOWN_LINK_RE.sub(r"\1", value)
    value = CODE_SPAN_RE.sub(r"\1", value)
    return value.replace("*", "").replace("_", "").strip()


def clean_heading(value: str) -> str:
    value = re.sub(r"\s+#+\s*$", "", value).strip()
    return strip_inline_markdown(value)


def slugify(value: str) -> str:
    value = strip_inline_markdown(value)
    value = unicodedata.normalize("NFKD", value)
    value = value.encode("ascii", "ignore").decode("ascii")
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value or "section"


def unique_anchor(base: str, used: set[str]) -> str:
    anchor = base
    counter = 2
    while anchor in used:
        anchor = f"{base}-{counter}"
        counter += 1
    used.add(anchor)
    return anchor


def reference_label(path: Path) -> str:
    stem = path.stem
    if stem in DOC_LINK_LABELS:
        return DOC_LINK_LABELS[stem]
    return " ".join(part.capitalize() for part in re.split(r"[-_]+", stem))


def collect_document_paths() -> list[Path]:
    ordered = [REQUIREMENTS_DIR / name for name in DOC_ORDER]
    ordered = [path for path in ordered if path.exists()]
    seen = {path.resolve() for path in ordered}
    extras = sorted(
        path
        for path in REQUIREMENTS_DIR.glob("*.md")
        if path.resolve() not in seen
    )
    return ordered + extras


def collect_headings(path: Path, text: str, doc_anchor: str, used: set[str]) -> tuple[str, list[Heading]]:
    headings: list[Heading] = []
    title = reference_label(path)
    first_h1_seen = False

    for line in text.splitlines():
        match = HEADING_RE.match(line)
        if not match:
            continue

        level = len(match.group(1))
        heading_text = clean_heading(match.group(2))

        if level == 1 and not first_h1_seen:
            anchor = doc_anchor
            used.add(anchor)
            title = heading_text
            first_h1_seen = True
        else:
            anchor = unique_anchor(f"{doc_anchor}-{slugify(heading_text)}", used)

        headings.append(Heading(level=level, text=heading_text, anchor=anchor))

    return title, headings


def load_documents() -> list[Document]:
    if not REQUIREMENTS_DIR.exists():
        raise FileNotFoundError(f"Missing requirements directory: {REQUIREMENTS_DIR}")

    used: set[str] = set()
    documents: list[Document] = []

    for path in collect_document_paths():
        text = path.read_text(encoding="utf-8")
        doc_anchor = slugify(path.stem)
        title, headings = collect_headings(path, text, doc_anchor, used)
        documents.append(
            Document(
                path=path,
                rel_path=path.relative_to(REPO_ROOT).as_posix(),
                anchor=doc_anchor,
                title=title,
                link_label=reference_label(path),
                text=text,
                headings=headings,
            )
        )

    return documents


def build_document_maps(documents: list[Document]) -> tuple[dict[Path, Document], dict[str, Document]]:
    by_abs = {document.path.resolve(): document for document in documents}
    by_rel: dict[str, Document] = {}

    for document in documents:
        by_rel[document.rel_path] = document
        by_rel[document.path.name] = document

    return by_abs, by_rel


def split_target(target: str) -> tuple[str, str | None]:
    target = target.strip().strip("<>")
    path_part, _, fragment = target.partition("#")
    path_part = path_part.partition("?")[0]
    return path_part, fragment or None


def resolve_requirement_target(
    target: str,
    current_document: Document,
    by_abs: dict[Path, Document],
    by_rel: dict[str, Document],
) -> tuple[Document, str | None] | None:
    if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target):
        return None

    normalized = target.replace("\\", "/").strip()
    path_part, fragment = split_target(normalized)
    if not path_part.lower().endswith(".md"):
        return None

    if path_part in by_rel:
        return by_rel[path_part], fragment

    if path_part.startswith("requirements/"):
        candidate = REPO_ROOT / path_part
    else:
        candidate = current_document.path.parent / path_part

    try:
        return by_abs[candidate.resolve()], fragment
    except KeyError:
        return None


def resolve_fragment(document: Document, fragment: str | None) -> str:
    if not fragment:
        return document.anchor

    normalized_fragment = slugify(fragment)
    for heading in document.headings:
        if heading.anchor == fragment:
            return heading.anchor
        if heading.anchor == normalized_fragment:
            return heading.anchor
        if slugify(heading.text) == normalized_fragment:
            return heading.anchor
        if heading.anchor.endswith(f"-{normalized_fragment}"):
            return heading.anchor

    return document.anchor


def render_internal_reference(document: Document, anchor: str, text: str | None = None) -> str:
    label = document.link_label if text is None else strip_inline_markdown(text)
    return f'<a href="#{html.escape(anchor, quote=True)}">{html.escape(label, quote=False)}</a>'


def render_inline(
    text: str,
    current_document: Document,
    by_abs: dict[Path, Document],
    by_rel: dict[str, Document],
) -> str:
    tokens: list[str] = []

    def stash(fragment: str) -> str:
        token = f"@@HTML_TOKEN_{len(tokens)}@@"
        tokens.append(fragment)
        return token

    def markdown_link(match: re.Match[str]) -> str:
        label = match.group(1)
        target = match.group(2)
        resolved = resolve_requirement_target(target, current_document, by_abs, by_rel)
        if resolved:
            document, fragment = resolved
            anchor = resolve_fragment(document, fragment)
            return stash(render_internal_reference(document, anchor, label))

        safe_target = html.escape(target, quote=True)
        safe_label = html.escape(strip_inline_markdown(label), quote=False)
        return stash(f'<a href="{safe_target}">{safe_label}</a>')

    def code_span(match: re.Match[str]) -> str:
        content = match.group(1).strip()
        resolved = resolve_requirement_target(content, current_document, by_abs, by_rel)
        if resolved:
            document, fragment = resolved
            anchor = resolve_fragment(document, fragment)
            return stash(render_internal_reference(document, anchor))
        return stash(f"<code>{html.escape(match.group(1), quote=False)}</code>")

    def bare_url(match: re.Match[str]) -> str:
        url = match.group(1)
        trailing = ""
        while url and url[-1] in ".,;:)":
            trailing = url[-1] + trailing
            url = url[:-1]
        safe_url = html.escape(url, quote=True)
        return stash(f'<a href="{safe_url}">{html.escape(url, quote=False)}</a>{html.escape(trailing, quote=False)}')

    text = MARKDOWN_LINK_RE.sub(markdown_link, text)
    text = CODE_SPAN_RE.sub(code_span, text)
    text = URL_RE.sub(bare_url, text)

    rendered = html.escape(text, quote=False)
    for index, fragment in enumerate(tokens):
        rendered = rendered.replace(f"@@HTML_TOKEN_{index}@@", fragment)

    return rendered


def close_paragraph(
    output: list[str],
    paragraph_lines: list[str],
    current_document: Document,
    by_abs: dict[Path, Document],
    by_rel: dict[str, Document],
) -> None:
    if not paragraph_lines:
        return

    paragraph = " ".join(line.strip() for line in paragraph_lines)
    output.append(f"<p>{render_inline(paragraph, current_document, by_abs, by_rel)}</p>")
    paragraph_lines.clear()


def close_lists(output: list[str], list_stack: list[dict[str, object]]) -> None:
    while list_stack:
        item = list_stack.pop()
        output.append("</li>")
        output.append(f"</{item['tag']}>")


def render_markdown_document(
    document: Document,
    by_abs: dict[Path, Document],
    by_rel: dict[str, Document],
) -> str:
    output: list[str] = []
    paragraph_lines: list[str] = []
    list_stack: list[dict[str, object]] = []
    heading_index = 0
    lines = document.text.splitlines()
    index = 0

    while index < len(lines):
        line = lines[index]

        fence = FENCE_RE.match(line)
        if fence:
            close_paragraph(output, paragraph_lines, document, by_abs, by_rel)
            close_lists(output, list_stack)

            marker = fence.group(1)
            code_lines: list[str] = []
            index += 1
            while index < len(lines) and not lines[index].lstrip().startswith(marker):
                code_lines.append(lines[index])
                index += 1
            output.append(f"<pre><code>{html.escape(chr(10).join(code_lines), quote=False)}</code></pre>")
            index += 1
            continue

        if not line.strip():
            close_paragraph(output, paragraph_lines, document, by_abs, by_rel)
            close_lists(output, list_stack)
            index += 1
            continue

        heading_match = HEADING_RE.match(line)
        if heading_match:
            close_paragraph(output, paragraph_lines, document, by_abs, by_rel)
            close_lists(output, list_stack)
            heading = document.headings[heading_index]
            heading_index += 1
            output.append(
                f'<h{heading.level} id="{html.escape(heading.anchor, quote=True)}">'
                f"{render_inline(heading.text, document, by_abs, by_rel)}"
                f"</h{heading.level}>"
            )
            index += 1
            continue

        list_match = LIST_ITEM_RE.match(line)
        if list_match:
            close_paragraph(output, paragraph_lines, document, by_abs, by_rel)
            indent = len(list_match.group(1).replace("\t", "    "))
            marker = list_match.group(2)
            tag = "ol" if marker.endswith(".") else "ul"

            if not list_stack:
                output.append(f"<{tag}>")
                list_stack.append({"indent": indent, "tag": tag})
            elif indent > int(list_stack[-1]["indent"]):
                output.append(f"<{tag}>")
                list_stack.append({"indent": indent, "tag": tag})
            else:
                while list_stack and indent < int(list_stack[-1]["indent"]):
                    item = list_stack.pop()
                    output.append("</li>")
                    output.append(f"</{item['tag']}>")

                if list_stack and indent == int(list_stack[-1]["indent"]):
                    if list_stack[-1]["tag"] == tag:
                        output.append("</li>")
                    else:
                        item = list_stack.pop()
                        output.append("</li>")
                        output.append(f"</{item['tag']}>")
                        output.append(f"<{tag}>")
                        list_stack.append({"indent": indent, "tag": tag})
                else:
                    output.append(f"<{tag}>")
                    list_stack.append({"indent": indent, "tag": tag})

            content = list_match.group(3)
            output.append(f"<li>{render_inline(content, document, by_abs, by_rel)}")
            index += 1
            continue

        close_lists(output, list_stack)
        paragraph_lines.append(line)
        index += 1

    close_paragraph(output, paragraph_lines, document, by_abs, by_rel)
    close_lists(output, list_stack)
    return "\n".join(output)


def build_index(documents: list[Document]) -> str:
    output = ['<nav class="toc" id="index">', "<h1>Index</h1>", "<ol>"]

    for document in documents:
        output.append(
            f'<li><a href="#{html.escape(document.anchor, quote=True)}">'
            f"{html.escape(document.title, quote=False)}</a>"
        )
        child_headings = [heading for heading in document.headings if heading.level > 1]
        if child_headings:
            output.append("<ol>")
            for heading in child_headings:
                css_class = f' class="toc-level-{heading.level}"'
                output.append(
                    f'<li{css_class}><a href="#{html.escape(heading.anchor, quote=True)}">'
                    f"{html.escape(heading.text, quote=False)}</a></li>"
                )
            output.append("</ol>")
        output.append("</li>")

    output.extend(["</ol>", "</nav>"])
    return "\n".join(output)


def build_html(title: str, documents: list[Document]) -> str:
    by_abs, by_rel = build_document_maps(documents)
    sections = []

    for document in documents:
        sections.append(
            '<section class="document" data-source="{}">\n{}\n</section>'.format(
                html.escape(document.rel_path, quote=True),
                render_markdown_document(document, by_abs, by_rel),
            )
        )

    return "\n".join(
        [
            "<!doctype html>",
            '<html lang="en">',
            "<head>",
            '<meta charset="utf-8">',
            f"<title>{html.escape(title, quote=False)}</title>",
            "<style>",
            CSS,
            "</style>",
            "</head>",
            "<body>",
            '<header class="cover">',
            f"<h1>{html.escape(title, quote=False)}</h1>",
            "<p>Generated from the living requirements Markdown files.</p>",
            "</header>",
            build_index(documents),
            "\n".join(sections),
            "</body>",
            "</html>",
        ]
    )


CSS = """
@page {
  size: A4;
  margin: 18mm 16mm;
}

html {
  color: #172033;
  font-family: "Segoe UI", Arial, sans-serif;
  font-size: 11pt;
  line-height: 1.45;
}

body {
  margin: 0;
}

a {
  color: #075985;
  text-decoration: underline;
}

.cover {
  align-content: center;
  min-height: 230mm;
  page-break-after: always;
}

.cover h1 {
  border: 0;
  font-size: 28pt;
  margin: 0 0 8mm;
}

.cover p {
  color: #475569;
  font-size: 12pt;
}

.toc {
  page-break-after: always;
}

.toc ol {
  list-style-position: outside;
  padding-left: 6mm;
}

.toc li {
  margin: 1.8mm 0;
}

.toc .toc-level-3 {
  margin-left: 4mm;
}

.toc .toc-level-4,
.toc .toc-level-5,
.toc .toc-level-6 {
  margin-left: 8mm;
}

.document {
  page-break-before: always;
}

.document:first-of-type {
  page-break-before: auto;
}

h1,
h2,
h3,
h4,
h5,
h6 {
  color: #0f172a;
  line-height: 1.2;
  page-break-after: avoid;
}

h1 {
  border-bottom: 1px solid #cbd5e1;
  font-size: 22pt;
  margin: 0 0 8mm;
  padding-bottom: 3mm;
}

h2 {
  font-size: 15pt;
  margin: 8mm 0 3mm;
}

h3 {
  font-size: 12.5pt;
  margin: 5mm 0 2mm;
}

p {
  margin: 0 0 3.5mm;
}

ul,
ol {
  margin: 0 0 3.5mm;
  padding-left: 6mm;
}

li {
  margin: 1.2mm 0;
}

li > ul,
li > ol {
  margin-top: 1.2mm;
}

code {
  background: #f1f5f9;
  border: 1px solid #e2e8f0;
  border-radius: 3px;
  color: #334155;
  font-family: "Cascadia Mono", Consolas, monospace;
  font-size: 0.92em;
  padding: 0 2px;
}

pre {
  background: #f8fafc;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  margin: 0 0 4mm;
  overflow-wrap: anywhere;
  padding: 3mm;
  white-space: pre-wrap;
}

pre code {
  background: transparent;
  border: 0;
  padding: 0;
}
"""


def parse_inline_runs(
    text: str,
    current_document: Document,
    by_abs: dict[Path, Document],
    by_rel: dict[str, Document],
) -> list[InlineRun]:
    runs: list[InlineRun] = []
    token_re = re.compile(r"\[([^\]]+)\]\(([^)]+)\)|`([^`]+)`")

    def append_plain(value: str) -> None:
        position = 0
        for match in URL_RE.finditer(value):
            if match.start() > position:
                runs.append(InlineRun(value[position:match.start()]))

            url = match.group(1)
            trailing = ""
            while url and url[-1] in ".,;:)":
                trailing = url[-1] + trailing
                url = url[:-1]

            runs.append(InlineRun(url, link=url, external=True))
            if trailing:
                runs.append(InlineRun(trailing))
            position = match.end()

        if position < len(value):
            runs.append(InlineRun(value[position:]))

    position = 0
    for match in token_re.finditer(text):
        if match.start() > position:
            append_plain(text[position:match.start()])

        if match.group(1) is not None:
            label = strip_inline_markdown(match.group(1))
            target = match.group(2)
            resolved = resolve_requirement_target(target, current_document, by_abs, by_rel)
            if resolved:
                document, fragment = resolved
                runs.append(InlineRun(label, link=resolve_fragment(document, fragment)))
            elif re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target):
                runs.append(InlineRun(label, link=target, external=True))
            else:
                runs.append(InlineRun(label))
        else:
            content = match.group(3).strip()
            resolved = resolve_requirement_target(content, current_document, by_abs, by_rel)
            if resolved:
                document, fragment = resolved
                runs.append(
                    InlineRun(
                        document.link_label,
                        link=resolve_fragment(document, fragment),
                    )
                )
            else:
                runs.append(InlineRun(match.group(3)))

        position = match.end()

    if position < len(text):
        append_plain(text[position:])

    return runs


def markdown_blocks_for_document(
    document: Document,
    by_abs: dict[Path, Document],
    by_rel: dict[str, Document],
) -> list[PdfBlock]:
    blocks: list[PdfBlock] = []
    paragraph_lines: list[str] = []
    heading_index = 0
    lines = document.text.splitlines()
    index = 0

    def close_paragraph_block() -> None:
        if not paragraph_lines:
            return
        paragraph = " ".join(line.strip() for line in paragraph_lines)
        blocks.append(
            PdfBlock(
                kind="paragraph",
                runs=parse_inline_runs(paragraph, document, by_abs, by_rel),
            )
        )
        paragraph_lines.clear()

    while index < len(lines):
        line = lines[index]

        fence = FENCE_RE.match(line)
        if fence:
            close_paragraph_block()
            marker = fence.group(1)
            code_lines: list[str] = []
            index += 1
            while index < len(lines) and not lines[index].lstrip().startswith(marker):
                code_lines.append(lines[index])
                index += 1
            blocks.append(PdfBlock(kind="code", runs=[], text="\n".join(code_lines)))
            index += 1
            continue

        if not line.strip():
            close_paragraph_block()
            index += 1
            continue

        heading_match = HEADING_RE.match(line)
        if heading_match:
            close_paragraph_block()
            heading = document.headings[heading_index]
            heading_index += 1
            blocks.append(
                PdfBlock(
                    kind="heading",
                    runs=[InlineRun(heading.text)],
                    level=heading.level,
                    anchor=heading.anchor,
                )
            )
            index += 1
            continue

        list_match = LIST_ITEM_RE.match(line)
        if list_match:
            close_paragraph_block()
            indent = len(list_match.group(1).replace("\t", "    "))
            content = list_match.group(3)
            blocks.append(
                PdfBlock(
                    kind="list",
                    runs=parse_inline_runs(content, document, by_abs, by_rel),
                    indent=max(0, indent // 2),
                )
            )
            index += 1
            continue

        paragraph_lines.append(line)
        index += 1

    close_paragraph_block()
    return blocks


def fmt_pdf_number(value: float) -> str:
    return f"{value:.2f}".rstrip("0").rstrip(".")


def pdf_escape_text(value: str) -> str:
    raw = value.encode("cp1252", errors="replace")
    escaped = bytearray()
    for byte in raw:
        if byte in (40, 41, 92):
            escaped.append(92)
            escaped.append(byte)
        elif byte == 10:
            escaped.extend(b"\\n")
        elif byte == 13:
            escaped.extend(b"\\r")
        else:
            escaped.append(byte)
    return escaped.decode("latin1")


def pdf_text_width(text: str, size: float, font: str = "normal") -> float:
    if font == "mono":
        return len(text) * size * 0.6

    width = 0.0
    for char in text:
        if char == " ":
            width += 0.28
        elif char in ".,:;|!/\\'`iIl[]()":
            width += 0.26
        elif char in "mwMW@#%&":
            width += 0.82
        elif char.isupper():
            width += 0.64
        elif char.isdigit():
            width += 0.56
        else:
            width += 0.52
    return width * size


def split_run_tokens(runs: list[InlineRun]) -> list[InlineRun]:
    tokens: list[InlineRun] = []
    for run in runs:
        for part in re.split(r"(\s+)", run.text):
            if not part:
                continue
            if part.isspace():
                tokens.append(InlineRun(" ", link=run.link, external=run.external))
            else:
                tokens.append(InlineRun(part, link=run.link, external=run.external))
    return tokens


def trim_line_tokens(tokens: list[InlineRun]) -> list[InlineRun]:
    while tokens and tokens[-1].text == " ":
        tokens.pop()
    return tokens


def split_oversized_token(token: InlineRun, max_width: float, size: float, font: str) -> list[InlineRun]:
    chunks: list[InlineRun] = []
    current = ""
    for char in token.text:
        if current and pdf_text_width(current + char, size, font) > max_width:
            chunks.append(InlineRun(current, link=token.link, external=token.external))
            current = char
        else:
            current += char
    if current:
        chunks.append(InlineRun(current, link=token.link, external=token.external))
    return chunks


def wrap_runs(
    runs: list[InlineRun],
    max_width: float,
    size: float,
    font: str = "normal",
) -> list[list[InlineRun]]:
    lines: list[list[InlineRun]] = []
    current: list[InlineRun] = []
    current_width = 0.0

    for token in split_run_tokens(runs):
        if token.text == " " and not current:
            continue

        token_width = pdf_text_width(token.text, size, font)
        if token_width > max_width:
            parts = split_oversized_token(token, max_width, size, font)
        else:
            parts = [token]

        for part in parts:
            part_width = pdf_text_width(part.text, size, font)
            if current and current_width + part_width > max_width:
                lines.append(trim_line_tokens(current))
                current = []
                current_width = 0.0
                if part.text == " ":
                    continue

            current.append(part)
            current_width += part_width

    if current:
        lines.append(trim_line_tokens(current))

    return lines or [[InlineRun("")]]


class DirectPdfRenderer:
    page_width = 595.28
    page_height = 841.89
    margin_left = 54.0
    margin_right = 54.0
    margin_top = 54.0
    margin_bottom = 54.0
    link_color = (0.03, 0.35, 0.53)
    text_color = (0.09, 0.13, 0.20)
    muted_color = (0.35, 0.42, 0.51)

    def __init__(self) -> None:
        self.pages: list[PdfPage] = []
        self.anchors: dict[str, tuple[int, float]] = {}
        self.y = 0.0
        self.new_page()

    @property
    def current_page(self) -> PdfPage:
        return self.pages[-1]

    @property
    def content_width(self) -> float:
        return self.page_width - self.margin_left - self.margin_right

    def new_page(self) -> None:
        self.pages.append(PdfPage(content=[], links=[]))
        self.y = self.page_height - self.margin_top

    def ensure_space(self, height: float) -> None:
        if self.y - height < self.margin_bottom:
            self.new_page()

    def add_anchor(self, anchor: str | None, top: float | None = None) -> None:
        if anchor:
            self.anchors[anchor] = (len(self.pages) - 1, top if top is not None else self.y + 8)

    def draw_text(
        self,
        x: float,
        y: float,
        text: str,
        size: float,
        font_name: str,
        color: tuple[float, float, float],
    ) -> None:
        if not text:
            return
        r, g, b = color
        self.current_page.content.append(
            "{} {} {} rg\nBT /{} {} Tf 1 0 0 1 {} {} Tm ({}) Tj ET".format(
                fmt_pdf_number(r),
                fmt_pdf_number(g),
                fmt_pdf_number(b),
                font_name,
                fmt_pdf_number(size),
                fmt_pdf_number(x),
                fmt_pdf_number(y),
                pdf_escape_text(text),
            )
        )

    def draw_line(
        self,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        color: tuple[float, float, float],
        width: float = 0.5,
    ) -> None:
        r, g, b = color
        self.current_page.content.append(
            "{} {} {} RG {} w {} {} m {} {} l S".format(
                fmt_pdf_number(r),
                fmt_pdf_number(g),
                fmt_pdf_number(b),
                fmt_pdf_number(width),
                fmt_pdf_number(x1),
                fmt_pdf_number(y1),
                fmt_pdf_number(x2),
                fmt_pdf_number(y2),
            )
        )

    def draw_wrapped_runs(
        self,
        runs: list[InlineRun],
        x: float,
        max_width: float,
        size: float,
        font: str = "normal",
        bold: bool = False,
        after: float = 4.0,
        first_line_prefix: tuple[str, float] | None = None,
    ) -> None:
        lines = wrap_runs(runs, max_width, size, font)
        line_height = size * 1.35
        font_name = "F2" if font == "mono" else ("F3" if bold else "F1")

        for line_index, line in enumerate(lines):
            self.ensure_space(line_height)
            if first_line_prefix and line_index == 0:
                prefix, prefix_x = first_line_prefix
                self.draw_text(prefix_x, self.y, prefix, size, "F1", self.text_color)

            cursor = x
            for token in line:
                width = pdf_text_width(token.text, size, font)
                color = self.link_color if token.link else self.text_color
                self.draw_text(cursor, self.y, token.text, size, font_name, color)

                if token.link and token.text.strip():
                    self.current_page.links.append(
                        PdfLink(
                            target=token.link,
                            external=token.external,
                            rect=(cursor, self.y - 2, cursor + width, self.y + size + 2),
                        )
                    )
                    self.draw_line(cursor, self.y - 1.2, cursor + width, self.y - 1.2, self.link_color, 0.4)

                cursor += width

            self.y -= line_height

        self.y -= after

    def draw_heading(self, text: str, level: int, anchor: str | None = None) -> None:
        if level <= 1:
            size = 21.0
            before = 0.0
            after = 12.0
        elif level == 2:
            size = 15.0
            before = 10.0
            after = 6.0
        elif level == 3:
            size = 12.5
            before = 7.0
            after = 4.0
        else:
            size = 11.5
            before = 5.0
            after = 3.0

        self.ensure_space(before + size * 1.5 + after)
        self.y -= before
        self.add_anchor(anchor, self.y + size + 4)
        start_y = self.y
        self.draw_wrapped_runs(
            [InlineRun(text)],
            self.margin_left,
            self.content_width,
            size,
            bold=True,
            after=after,
        )

        if level == 1:
            self.draw_line(
                self.margin_left,
                start_y - size * 1.65,
                self.page_width - self.margin_right,
                start_y - size * 1.65,
                (0.75, 0.80, 0.87),
                0.6,
            )

    def draw_paragraph(self, runs: list[InlineRun]) -> None:
        self.draw_wrapped_runs(runs, self.margin_left, self.content_width, 10.5, after=5.0)

    def draw_list_item(self, runs: list[InlineRun], indent: int) -> None:
        indent_width = min(indent, 6) * 14.0
        bullet_x = self.margin_left + indent_width
        text_x = bullet_x + 12.0
        max_width = self.page_width - self.margin_right - text_x
        self.draw_wrapped_runs(
            runs,
            text_x,
            max_width,
            10.2,
            after=2.2,
            first_line_prefix=("-", bullet_x),
        )

    def draw_code(self, text: str) -> None:
        for line in text.splitlines() or [""]:
            self.draw_wrapped_runs(
                [InlineRun(line)],
                self.margin_left + 8,
                self.content_width - 16,
                9.0,
                font="mono",
                after=1.0,
            )
        self.y -= 4.0

    def draw_cover(self, title: str) -> None:
        self.y = self.page_height - 230.0
        self.draw_wrapped_runs(
            [InlineRun(title)],
            self.margin_left,
            self.content_width,
            27.0,
            bold=True,
            after=12.0,
        )
        self.draw_text(
            self.margin_left,
            self.y,
            "Generated from the living requirements Markdown files.",
            12.0,
            "F1",
            self.muted_color,
        )

    def draw_index_entry(self, text: str, target: str, level: int) -> None:
        size = 11.0 if level == 0 else 9.5
        indent = min(level, 4) * 14.0
        self.draw_wrapped_runs(
            [InlineRun(text, link=target)],
            self.margin_left + indent,
            self.content_width - indent,
            size,
            bold=level == 0,
            after=2.0,
        )

    def render_block(self, block: PdfBlock) -> None:
        if block.kind == "heading":
            self.draw_heading(block.runs[0].text, block.level, block.anchor)
        elif block.kind == "paragraph":
            self.draw_paragraph(block.runs)
        elif block.kind == "list":
            self.draw_list_item(block.runs, block.indent)
        elif block.kind == "code":
            self.draw_code(block.text)


class PdfWriter:
    def __init__(self) -> None:
        self.objects: list[bytes | None] = [None]

    def reserve(self) -> int:
        self.objects.append(None)
        return len(self.objects) - 1

    def set_object(self, object_id: int, content: bytes) -> None:
        self.objects[object_id] = content

    def write(self, path: Path, root_id: int) -> None:
        output = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
        offsets: list[int] = []

        for object_id, content in enumerate(self.objects[1:], start=1):
            if content is None:
                raise RuntimeError(f"PDF object {object_id} was reserved but not written")
            offsets.append(len(output))
            output.extend(f"{object_id} 0 obj\n".encode("ascii"))
            output.extend(content)
            output.extend(b"\nendobj\n")

        xref_start = len(output)
        output.extend(f"xref\n0 {len(self.objects)}\n".encode("ascii"))
        output.extend(b"0000000000 65535 f \n")
        for offset in offsets:
            output.extend(f"{offset:010d} 00000 n \n".encode("ascii"))

        output.extend(
            (
                f"trailer\n<< /Size {len(self.objects)} /Root {root_id} 0 R >>\n"
                f"startxref\n{xref_start}\n%%EOF\n"
            ).encode("ascii")
        )
        path.write_bytes(bytes(output))


def stream_object(content: bytes) -> bytes:
    return b"<< /Length " + str(len(content)).encode("ascii") + b" >>\nstream\n" + content + b"\nendstream"


def pdf_rect(rect: tuple[float, float, float, float]) -> str:
    return "[{} {} {} {}]".format(*(fmt_pdf_number(value) for value in rect))


def build_direct_pdf(title: str, documents: list[Document], output: Path) -> None:
    by_abs, by_rel = build_document_maps(documents)
    renderer = DirectPdfRenderer()

    renderer.draw_cover(title)
    renderer.new_page()
    renderer.draw_heading("Index", 1, "index")
    for document in documents:
        renderer.draw_index_entry(document.title, document.anchor, 0)
        for heading in document.headings:
            if heading.level > 1:
                renderer.draw_index_entry(heading.text, heading.anchor, heading.level - 1)

    for document in documents:
        renderer.new_page()
        for block in markdown_blocks_for_document(document, by_abs, by_rel):
            renderer.render_block(block)

    writer = PdfWriter()
    catalog_id = writer.reserve()
    pages_id = writer.reserve()
    font_regular_id = writer.reserve()
    font_mono_id = writer.reserve()
    font_bold_id = writer.reserve()

    page_ids = [writer.reserve() for _ in renderer.pages]
    content_ids = [writer.reserve() for _ in renderer.pages]

    writer.set_object(
        font_regular_id,
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>",
    )
    writer.set_object(
        font_mono_id,
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Courier /Encoding /WinAnsiEncoding >>",
    )
    writer.set_object(
        font_bold_id,
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>",
    )

    for page_index, page in enumerate(renderer.pages):
        content = "\n".join(page.content).encode("latin1", errors="replace")
        writer.set_object(content_ids[page_index], stream_object(content))

    for page_index, page in enumerate(renderer.pages):
        annotation_ids: list[int] = []
        for link in page.links:
            rect = pdf_rect(link.rect)

            if link.external:
                action = (
                    f"<< /S /URI /URI ({pdf_escape_text(link.target)}) >>"
                )
            else:
                if link.target not in renderer.anchors:
                    continue
                target_page_index, target_y = renderer.anchors[link.target]
                target_page_id = page_ids[target_page_index]
                action = (
                    f"<< /S /GoTo /D [{target_page_id} 0 R /XYZ 0 "
                    f"{fmt_pdf_number(target_y)} 0] >>"
                )

            annotation_id = writer.reserve()
            annotation_ids.append(annotation_id)
            writer.set_object(
                annotation_id,
                (
                    "<< /Type /Annot /Subtype /Link "
                    f"/Rect {rect} /Border [0 0 0] /A {action} >>"
                ).encode("latin1"),
            )

        annotations = ""
        if annotation_ids:
            annotations = " /Annots [{}]".format(
                " ".join(f"{annotation_id} 0 R" for annotation_id in annotation_ids)
            )

        writer.set_object(
            page_ids[page_index],
            (
                f"<< /Type /Page /Parent {pages_id} 0 R "
                f"/MediaBox [0 0 {fmt_pdf_number(renderer.page_width)} {fmt_pdf_number(renderer.page_height)}] "
                f"/Resources << /Font << /F1 {font_regular_id} 0 R /F2 {font_mono_id} 0 R /F3 {font_bold_id} 0 R >> >> "
                f"/Contents {content_ids[page_index]} 0 R{annotations} >>"
            ).encode("ascii"),
        )

    writer.set_object(
        pages_id,
        (
            f"<< /Type /Pages /Count {len(page_ids)} /Kids ["
            + " ".join(f"{page_id} 0 R" for page_id in page_ids)
            + "] >>"
        ).encode("ascii"),
    )
    writer.set_object(catalog_id, f"<< /Type /Catalog /Pages {pages_id} 0 R >>".encode("ascii"))

    output.parent.mkdir(parents=True, exist_ok=True)
    writer.write(output, catalog_id)




def find_browser(explicit_browser: str | None) -> Path | None:
    candidates: list[str | Path] = []

    if explicit_browser:
        candidates.append(explicit_browser)

    for env_name in ("CHROME_BIN", "MSEDGE_BIN", "BROWSER"):
        if os.environ.get(env_name):
            candidates.append(os.environ[env_name])

    for executable in (
        "msedge",
        "chrome",
        "google-chrome",
        "chromium",
        "chromium-browser",
    ):
        found = shutil.which(executable)
        if found:
            candidates.append(found)

    candidates.extend(
        [
            Path("C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"),
            Path("C:/Program Files/Microsoft/Edge/Application/msedge.exe"),
            Path("C:/Program Files/Google/Chrome/Application/chrome.exe"),
            Path("/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"),
            Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
        ]
    )

    for candidate in candidates:
        path = Path(candidate)
        if path.exists():
            return path

    return None


def print_pdf(browser: Path, html_output: Path, pdf_output: Path, timeout_seconds: int) -> None:
    common_flags = [
        "--disable-background-networking",
        "--disable-breakpad",
        "--disable-extensions",
        "--disable-gpu",
        "--disable-gpu-compositing",
        "--disable-gpu-sandbox",
        "--disable-software-rasterizer",
        "--disable-sync",
        "--no-default-browser-check",
        "--no-first-run",
        "--no-pdf-header-footer",
        "--print-to-pdf-no-header",
        f"--print-to-pdf={pdf_output}",
        html_output.resolve().as_uri(),
    ]

    attempts: list[list[str]] = []
    with tempfile.TemporaryDirectory(prefix="requirements-pdf-browser-") as user_data_dir:
        for headless_flag in ("--headless=new", "--headless"):
            attempts.append(
                [
                    str(browser),
                    headless_flag,
                    f"--user-data-dir={user_data_dir}",
                    *common_flags,
                ]
            )

        result = None
        for command in attempts:
            result = subprocess.run(
                command,
                check=False,
                capture_output=True,
                text=True,
                timeout=timeout_seconds,
            )
            if result.returncode == 0 and pdf_output.exists():
                break

    if result is None:
        raise RuntimeError("Browser PDF generation failed: browser did not run")

    if result.returncode != 0:
        stderr = result.stderr.strip()
        stdout = result.stdout.strip()
        details = stderr or stdout or f"exit code {result.returncode}"
        raise RuntimeError(f"Browser PDF generation failed: {details}")

    if not pdf_output.exists():
        raise RuntimeError(f"Browser finished but did not create {pdf_output}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build requirements/*.md into a linked PDF with an index."
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"PDF output path. Default: {DEFAULT_OUTPUT}",
    )
    parser.add_argument(
        "--html-output",
        type=Path,
        default=DEFAULT_HTML_OUTPUT,
        help=f"Intermediate linked HTML output path. Default: {DEFAULT_HTML_OUTPUT}",
    )
    parser.add_argument(
        "--title",
        default="Municipal Energy Management Requirements",
        help="Document title used on the cover page.",
    )
    parser.add_argument(
        "--browser",
        help="Path to a Chromium-based browser executable.",
    )
    parser.add_argument(
        "--engine",
        choices=("direct", "browser", "auto"),
        default="direct",
        help="PDF engine. direct uses the built-in renderer, browser prints the HTML, auto tries browser then direct. Default: direct.",
    )
    parser.add_argument(
        "--browser-timeout",
        type=int,
        default=20,
        help="Seconds to wait for browser PDF generation before failing or falling back. Default: 20.",
    )
    parser.add_argument(
        "--html-only",
        action="store_true",
        help="Only write the linked HTML file and skip PDF generation.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    documents = load_documents()
    rendered_html = build_html(args.title, documents)

    args.html_output.parent.mkdir(parents=True, exist_ok=True)
    args.html_output.write_text(rendered_html, encoding="utf-8", newline="\n")
    print(f"Wrote {args.html_output}")

    if args.html_only:
        return 0

    args.output.parent.mkdir(parents=True, exist_ok=True)
    if args.engine in ("browser", "auto"):
        browser = find_browser(args.browser)
        if not browser:
            message = (
                "Could not find Microsoft Edge, Google Chrome, or Chromium. "
                "The linked HTML was written; pass --browser or use --html-only."
            )
            if args.engine == "browser":
                print(message, file=sys.stderr)
                return 2
            print(f"{message} Falling back to direct PDF generation.", file=sys.stderr)
        else:
            try:
                print_pdf(browser, args.html_output, args.output, args.browser_timeout)
                print(f"Wrote {args.output}")
                return 0
            except (RuntimeError, subprocess.TimeoutExpired) as error:
                if args.engine == "browser":
                    raise
                print(
                    f"Browser PDF generation failed ({error}). Falling back to direct PDF generation.",
                    file=sys.stderr,
                )

    build_direct_pdf(args.title, documents, args.output)
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
