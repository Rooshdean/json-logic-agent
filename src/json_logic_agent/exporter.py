from __future__ import annotations

from pathlib import Path
from xml.sax.saxutils import escape

from .models import TranslationResult
from .n8n import format_n8n_report


def build_markdown_report(result: TranslationResult) -> str:
    lines: list[str] = [
        f"# JSON Logic Agent Report: {result.source_name}",
        "",
        f"- **Source format:** {result.metadata.get('source_format', 'unknown')}",
        f"- **Provider:** {result.metadata.get('provider', 'local/unknown')}",
        f"- **Model:** {result.metadata.get('model', 'n/a')}",
        f"- **Target view:** {result.target}",
        f"- **Fidelity score:** {result.metadata.get('fidelity_score', 'n/a')}/100",
        "",
    ]

    if result.n8n_report:
        lines.extend([
            "## n8n Workflow Intelligence",
            "",
            "```text",
            format_n8n_report(result.n8n_report),
            "```",
            "",
        ])

    lines.extend(["## Semantic Deep Dive", ""])
    if result.target == "mermaid":
        lines.extend(["```mermaid", result.rendered_output, "```", ""])
    elif result.target == "python":
        lines.extend(["```python", result.rendered_output, "```", ""])
    elif result.target == "javascript":
        lines.extend(["```javascript", result.rendered_output, "```", ""])
    elif result.target == "typescript":
        lines.extend(["```typescript", result.rendered_output, "```", ""])
    else:
        lines.extend([result.rendered_output, ""])

    if result.warnings:
        lines.extend(["## Assumptions / Warnings", ""])
        for warning in result.warnings:
            lines.append(f"- {warning}")
        lines.append("")

    if result.trace:
        lines.extend([
            "## Pipeline Metadata",
            "",
            f"- Inspector classification: `{result.trace.inspection.json_kind}`",
            f"- Inspector confidence: `{result.trace.inspection.confidence}`",
            f"- Critic verdict: `{result.trace.critique.verdict}`",
            f"- Reviewer verdict: `{result.trace.review.verdict if result.trace.review else 'n/a'}`",
            "",
        ])

    return "\n".join(lines).rstrip() + "\n"


def export_markdown(result: TranslationResult, path: str | Path) -> Path:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(build_markdown_report(result), encoding="utf-8")
    return output


def _pdf_paragraphs_from_text(text: str, styles):
    from reportlab.platypus import Paragraph, Spacer

    story = []
    for raw in text.splitlines():
        line = raw.rstrip()
        if not line:
            story.append(Spacer(1, 6))
            continue
        if line.startswith("### "):
            story.append(Paragraph(escape(line[4:]), styles["Heading3"]))
        elif line.startswith("## "):
            story.append(Paragraph(escape(line[3:]), styles["Heading2"]))
        elif line.startswith("# "):
            story.append(Paragraph(escape(line[2:]), styles["Heading1"]))
        elif line.startswith("- "):
            story.append(Paragraph("- " + escape(line[2:]), styles["BodyText"]))
        else:
            story.append(Paragraph(escape(line), styles["BodyText"]))
    return story


def export_pdf(result: TranslationResult, path: str | Path) -> Path:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_LEFT
    from reportlab.lib.units import mm
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted, PageBreak

    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="Small", parent=styles["BodyText"], fontSize=8.5, leading=11, alignment=TA_LEFT))
    code_style = ParagraphStyle(name="Code", parent=styles["Code"], fontSize=7.3, leading=9)

    doc = SimpleDocTemplate(
        str(output),
        pagesize=A4,
        rightMargin=16 * mm,
        leftMargin=16 * mm,
        topMargin=16 * mm,
        bottomMargin=16 * mm,
        title=f"JSON Logic Agent Report - {result.source_name}",
        author="JSON Logic Agent",
    )

    story = [
        Paragraph(f"JSON Logic Agent Report: {escape(result.source_name)}", styles["Title"]),
        Spacer(1, 8),
        Paragraph(f"Source format: {escape(str(result.metadata.get('source_format', 'unknown')))}", styles["Small"]),
        Paragraph(f"Provider: {escape(str(result.metadata.get('provider', 'local/unknown')))}", styles["Small"]),
        Paragraph(f"Model: {escape(str(result.metadata.get('model', 'n/a')))}", styles["Small"]),
        Paragraph(f"Target view: {escape(result.target)}", styles["Small"]),
        Paragraph(f"Fidelity score: {escape(str(result.metadata.get('fidelity_score', 'n/a')))}/100", styles["Small"]),
        Spacer(1, 12),
    ]

    if result.n8n_report:
        story.append(Paragraph("n8n Workflow Intelligence", styles["Heading1"]))
        story.append(Preformatted(format_n8n_report(result.n8n_report), code_style, maxLineLength=100))
        story.append(PageBreak())

    story.append(Paragraph("Semantic Deep Dive", styles["Heading1"]))
    if result.target in {"python", "javascript", "typescript", "mermaid"}:
        story.append(Preformatted(result.rendered_output, code_style, maxLineLength=110))
    else:
        story.extend(_pdf_paragraphs_from_text(result.rendered_output, styles))

    if result.warnings:
        story.append(Spacer(1, 12))
        story.append(Paragraph("Assumptions / Warnings", styles["Heading1"]))
        for warning in result.warnings:
            story.append(Paragraph("- " + escape(warning), styles["Small"]))

    if result.trace:
        story.append(Spacer(1, 12))
        story.append(Paragraph("Pipeline Metadata", styles["Heading1"]))
        story.append(Paragraph(f"Inspector classification: {escape(result.trace.inspection.json_kind)}", styles["Small"]))
        story.append(Paragraph(f"Inspector confidence: {result.trace.inspection.confidence}", styles["Small"]))
        story.append(Paragraph(f"Critic verdict: {escape(result.trace.critique.verdict)}", styles["Small"]))
        story.append(Paragraph(f"Reviewer verdict: {escape(result.trace.review.verdict if result.trace.review else 'n/a')}", styles["Small"]))

    doc.build(story)
    return output


def export_report(result: TranslationResult, path: str | Path) -> Path:
    output = Path(path)
    suffix = output.suffix.lower()
    if suffix == ".md":
        return export_markdown(result, output)
    if suffix == ".pdf":
        return export_pdf(result, output)
    raise ValueError("Export path must end in .md or .pdf")
