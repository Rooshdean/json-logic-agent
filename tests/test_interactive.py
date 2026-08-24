from pathlib import Path

import pytest

from json_logic_agent.interactive import ACTIONS, action_target, selected_file_path
from json_logic_agent.models import ProjectScanResult


def test_v4_actions_cover_all_render_targets():
    assert {target for _, target in ACTIONS} == {"logic", "python", "javascript", "typescript", "mermaid"}


def test_action_target_maps_human_label():
    assert action_target("Explain in normal logic") == "logic"
    assert action_target("Draw as Mermaid diagram") == "mermaid"


def test_action_target_rejects_unknown_label():
    with pytest.raises(ValueError):
        action_target("Unknown")


def test_selected_file_path_joins_scan_root(tmp_path):
    scan = ProjectScanResult(root=str(tmp_path))
    assert selected_file_path(scan, "nested/workflow.json") == Path(tmp_path) / "nested/workflow.json"
