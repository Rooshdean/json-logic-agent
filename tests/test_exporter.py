from json_logic_agent.exporter import build_markdown_report, export_report
from json_logic_agent.models import LogicModel, TranslationResult


def sample_result(target="logic"):
    return TranslationResult(
        source_name="workflow.json",
        target=target,
        logic=LogicModel(summary="Test workflow", json_kind="n8n-workflow"),
        rendered_output="flowchart TD\nA --> B" if target == "mermaid" else "This workflow does a thing.",
        warnings=["Review the external API error path."],
        metadata={"source_format": "n8n-workflow", "provider": "openrouter", "model": "test/model", "fidelity_score": 97},
    )


def test_markdown_report_contains_complete_sections():
    text = build_markdown_report(sample_result("mermaid"))
    assert "# JSON Logic Agent Report: workflow.json" in text
    assert "**Fidelity score:** 97/100" in text
    assert "```mermaid" in text
    assert "flowchart TD" in text
    assert "## Assumptions / Warnings" in text


def test_export_markdown(tmp_path):
    output = export_report(sample_result(), tmp_path / "report.md")
    assert output.exists()
    assert "Semantic Deep Dive" in output.read_text(encoding="utf-8")


def test_export_pdf(tmp_path):
    output = export_report(sample_result(), tmp_path / "report.pdf")
    assert output.exists()
    assert output.read_bytes().startswith(b"%PDF")


def test_export_rejects_unknown_extension(tmp_path):
    try:
        export_report(sample_result(), tmp_path / "report.txt")
    except ValueError as exc:
        assert ".md or .pdf" in str(exc)
    else:
        raise AssertionError("Expected ValueError")
