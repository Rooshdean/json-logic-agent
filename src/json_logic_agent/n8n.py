import json
import re
from typing import Any

from .models import (
    N8nConnectionSummary,
    N8nNodeSummary,
    N8nRiskFinding,
    N8nWorkflowReport,
)


TRIGGER_MARKERS = ("trigger", "webhook")
DECISION_MARKERS = ("if", "switch", "filter")
CODE_MARKERS = ("code", "function")
AI_MARKERS = ("openai", "anthropic", "langchain", "agent", "chatmodel", "llm", "embeddings")
BUILTIN_MARKERS = (
    "n8n-nodes-base.set",
    "n8n-nodes-base.if",
    "n8n-nodes-base.switch",
    "n8n-nodes-base.code",
    "n8n-nodes-base.function",
    "n8n-nodes-base.merge",
    "n8n-nodes-base.noop",
    "n8n-nodes-base.wait",
    "n8n-nodes-base.splitinbatches",
)


def is_n8n_workflow(data: Any) -> bool:
    if not isinstance(data, dict):
        return False
    nodes = data.get("nodes")
    connections = data.get("connections")
    if not isinstance(nodes, list) or not isinstance(connections, dict):
        return False
    return any(
        isinstance(node, dict)
        and isinstance(node.get("type"), str)
        and ("n8n-nodes" in node["type"] or node["type"].startswith("@n8n/"))
        for node in nodes
    )


def _category(node_type: str) -> str:
    lowered = node_type.lower()
    if any(marker in lowered for marker in TRIGGER_MARKERS):
        return "trigger"
    if any(marker in lowered for marker in DECISION_MARKERS):
        return "decision"
    if any(marker in lowered for marker in CODE_MARKERS):
        return "code"
    if any(marker in lowered for marker in AI_MARKERS):
        return "ai"
    if "httprequest" in lowered:
        return "http"
    if "executeworkflow" in lowered:
        return "sub-workflow"
    return "integration" if not any(marker in lowered for marker in BUILTIN_MARKERS) else "utility"


def _integration_name(node_type: str) -> str | None:
    lowered = node_type.lower()
    if _category(node_type) in {"trigger", "decision", "code", "utility"}:
        return None
    tail = node_type.split(".")[-1].split("/")[-1]
    if tail.lower() in {"httprequest", "executeworkflow"}:
        return "HTTP/API" if tail.lower() == "httprequest" else "n8n sub-workflow"
    return tail


def _count_expressions(value: Any) -> int:
    if isinstance(value, str):
        return len(re.findall(r"\{\{.*?\}\}", value, flags=re.DOTALL))
    if isinstance(value, dict):
        return sum(_count_expressions(v) for v in value.values())
    if isinstance(value, list):
        return sum(_count_expressions(v) for v in value)
    return 0


def _flatten_connections(connections: dict[str, Any]) -> list[N8nConnectionSummary]:
    result: list[N8nConnectionSummary] = []
    for source, by_type in connections.items():
        if not isinstance(by_type, dict):
            continue
        for connection_type, outputs in by_type.items():
            if not isinstance(outputs, list):
                continue
            for output_index, targets in enumerate(outputs):
                if not isinstance(targets, list):
                    continue
                for target in targets:
                    if isinstance(target, dict) and isinstance(target.get("node"), str):
                        result.append(
                            N8nConnectionSummary(
                                source=source,
                                target=target["node"],
                                output_index=output_index,
                                connection_type=connection_type,
                            )
                        )
    return result


def analyze_n8n_workflow(data: dict[str, Any]) -> N8nWorkflowReport:
    if not is_n8n_workflow(data):
        raise ValueError("Input does not look like an exported n8n workflow")

    nodes_raw = [node for node in data.get("nodes", []) if isinstance(node, dict)]
    connections = _flatten_connections(data.get("connections", {}))
    nodes: list[N8nNodeSummary] = []
    integrations: set[str] = set()
    credential_types: set[str] = set()
    trigger_nodes: list[str] = []
    decision_nodes: list[str] = []
    code_nodes: list[str] = []
    ai_nodes: list[str] = []
    risks: list[N8nRiskFinding] = []

    for raw in nodes_raw:
        name = str(raw.get("name", "Unnamed node"))
        node_type = str(raw.get("type", "unknown"))
        category = _category(node_type)
        credentials = raw.get("credentials") if isinstance(raw.get("credentials"), dict) else {}
        creds = sorted(str(key) for key in credentials.keys())
        credential_types.update(creds)
        integration = _integration_name(node_type)
        if integration:
            integrations.add(integration)

        if category == "trigger":
            trigger_nodes.append(name)
        elif category == "decision":
            decision_nodes.append(name)
        elif category == "code":
            code_nodes.append(name)
        elif category == "ai":
            ai_nodes.append(name)

        parameters = raw.get("parameters", {})
        expression_count = _count_expressions(parameters)
        has_error_policy = any(
            key in raw for key in ("onError", "continueOnFail", "retryOnFail", "maxTries", "waitBetweenTries")
        )
        nodes.append(
            N8nNodeSummary(
                name=name,
                node_type=node_type,
                category=category,
                disabled=bool(raw.get("disabled", False)),
                credential_types=creds,
                expression_count=expression_count,
                has_error_policy=has_error_policy,
            )
        )

        if category in {"http", "integration", "ai"} and not has_error_policy and not raw.get("disabled", False):
            risks.append(
                N8nRiskFinding(
                    severity="medium",
                    node=name,
                    finding="External/integration node has no explicit node-level error or retry policy in the export.",
                )
            )
        if category == "code":
            risks.append(
                N8nRiskFinding(
                    severity="low",
                    node=name,
                    finding="Code node contains custom logic that deserves manual review during a deep dive.",
                )
            )

    names = {node.name for node in nodes}
    connected = {edge.source for edge in connections} | {edge.target for edge in connections}
    disconnected = sorted(names - connected)
    sources = {edge.source for edge in connections}
    terminals = sorted(names - sources)

    for name in disconnected:
        risks.append(
            N8nRiskFinding(
                severity="low",
                node=name,
                finding="Node is disconnected from the exported workflow graph.",
            )
        )

    if len(trigger_nodes) == 0:
        risks.append(N8nRiskFinding(severity="medium", finding="No obvious trigger node was detected."))
    if len(trigger_nodes) > 1:
        risks.append(N8nRiskFinding(severity="low", finding="Workflow has multiple detected entry/trigger nodes."))

    return N8nWorkflowReport(
        workflow_name=data.get("name") if isinstance(data.get("name"), str) else None,
        active=data.get("active") if isinstance(data.get("active"), bool) else None,
        node_count=len(nodes),
        connection_count=len(connections),
        trigger_nodes=trigger_nodes,
        decision_nodes=decision_nodes,
        code_nodes=code_nodes,
        ai_nodes=ai_nodes,
        integrations=sorted(integrations),
        credential_types=sorted(credential_types),
        nodes=nodes,
        connections=connections,
        disconnected_nodes=disconnected,
        terminal_nodes=terminals,
        risks=risks,
    )


def n8n_context_for_prompt(report: N8nWorkflowReport) -> str:
    return json.dumps(report.model_dump(), indent=2, ensure_ascii=False)


def format_n8n_report(report: N8nWorkflowReport) -> str:
    lines = [
        "N8N WORKFLOW INTELLIGENCE",
        "=" * 25,
        f"Workflow: {report.workflow_name or 'Unnamed'}",
        f"Active: {report.active if report.active is not None else 'unknown'}",
        f"Nodes: {report.node_count}",
        f"Connections: {report.connection_count}",
        f"Triggers: {', '.join(report.trigger_nodes) or 'none detected'}",
        f"Decision nodes: {', '.join(report.decision_nodes) or 'none detected'}",
        f"Code nodes: {', '.join(report.code_nodes) or 'none'}",
        f"AI nodes: {', '.join(report.ai_nodes) or 'none'}",
        f"Integrations: {', '.join(report.integrations) or 'none detected'}",
        f"Credential types referenced: {', '.join(report.credential_types) or 'none'}",
        f"Disconnected nodes: {', '.join(report.disconnected_nodes) or 'none'}",
        f"Terminal nodes: {', '.join(report.terminal_nodes) or 'none'}",
    ]
    if report.risks:
        lines.extend(["", "RISK / REVIEW SIGNALS", "-" * 21])
        for risk in report.risks:
            where = f" [{risk.node}]" if risk.node else ""
            lines.append(f"{risk.severity.upper()}{where}: {risk.finding}")
    return "\n".join(lines)
