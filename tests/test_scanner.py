import json

from json_logic_agent.scanner import scan_project


def test_scan_project_classifies_json(tmp_path):
    (tmp_path / "workflow.json").write_text(
        json.dumps({"trigger": "created", "rules": []}), encoding="utf-8"
    )
    (tmp_path / "package.json").write_text(
        json.dumps({"name": "demo", "scripts": {}}), encoding="utf-8"
    )

    result = scan_project(tmp_path)
    by_name = {item.path: item for item in result.files}

    assert by_name["workflow.json"].likely_kind == "workflow-or-automation"
    assert by_name["package.json"].likely_kind == "node-package-manifest"


def test_scan_project_ignores_node_modules(tmp_path):
    node_modules = tmp_path / "node_modules" / "pkg"
    node_modules.mkdir(parents=True)
    (node_modules / "package.json").write_text(json.dumps({"name": "pkg"}), encoding="utf-8")

    result = scan_project(tmp_path)
    assert result.files == []


def test_scan_project_reports_invalid_json(tmp_path):
    (tmp_path / "broken.json").write_text("{not-json", encoding="utf-8")
    result = scan_project(tmp_path)
    assert result.skipped_invalid_json == ["broken.json"]
