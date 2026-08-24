from json_logic_agent.n8n import analyze_n8n_workflow, is_n8n_workflow


def sample_workflow():
    return {
        "name": "Test",
        "active": False,
        "nodes": [
            {"name": "Webhook", "type": "n8n-nodes-base.webhook", "parameters": {}},
            {"name": "Check", "type": "n8n-nodes-base.if", "parameters": {"value": "={{$json.ok}}"}},
            {"name": "API", "type": "n8n-nodes-base.httpRequest", "parameters": {"url": "https://example.invalid"}},
            {"name": "Unused", "type": "n8n-nodes-base.set", "parameters": {}},
        ],
        "connections": {
            "Webhook": {"main": [[{"node": "Check", "type": "main", "index": 0}]]},
            "Check": {"main": [[{"node": "API", "type": "main", "index": 0}], []]},
        },
    }


def test_detects_n8n_export():
    assert is_n8n_workflow(sample_workflow()) is True
    assert is_n8n_workflow({"nodes": [], "connections": {}}) is False


def test_builds_n8n_graph_report():
    report = analyze_n8n_workflow(sample_workflow())
    assert report.node_count == 4
    assert report.connection_count == 2
    assert report.trigger_nodes == ["Webhook"]
    assert report.decision_nodes == ["Check"]
    assert "API" in report.terminal_nodes
    assert "Unused" in report.disconnected_nodes


def test_detects_expressions_and_external_error_risk():
    report = analyze_n8n_workflow(sample_workflow())
    check = next(node for node in report.nodes if node.name == "Check")
    assert check.expression_count == 1
    assert any(risk.node == "API" and risk.severity == "medium" for risk in report.risks)
