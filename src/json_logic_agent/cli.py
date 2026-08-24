import argparse
import json
import sys
from pathlib import Path

from dotenv import load_dotenv

from .agent import JsonLogicAgent
from .exporter import export_report
from .interactive import run_interactive_scan
from .n8n import analyze_n8n_workflow, format_n8n_report, is_n8n_workflow
from .scanner import scan_project

TARGETS = ["logic", "python", "javascript", "typescript", "mermaid"]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="jsonlogic", description="Understand JSON and n8n workflows as normal logic, code, diagrams, or exportable reports.")
    sub = parser.add_subparsers(dest="command")

    explain = sub.add_parser("explain", help="Explain or translate one JSON/n8n workflow file")
    explain.add_argument("input")
    explain.add_argument("--to", choices=TARGETS, default="logic")
    explain.add_argument("--out", help="Save only the rendered target output")
    explain.add_argument("--export", help="Save the complete analysis report as .md or .pdf")
    explain.add_argument("--show-model", action="store_true")
    explain.add_argument("--show-trace", action="store_true")
    explain.add_argument("--trace-out")
    explain.add_argument("--n8n-report", action="store_true", help="Print deterministic n8n workflow intelligence before semantic output")
    explain.add_argument("--model")

    n8n = sub.add_parser("n8n", help="Deep-dive an exported n8n workflow")
    n8n.add_argument("input")
    n8n.add_argument("--to", choices=TARGETS, default="logic")
    n8n.add_argument("--report-only", action="store_true", help="Run only local deterministic n8n analysis; no model/API call")
    n8n.add_argument("--report-json", action="store_true", help="Print deterministic n8n report as JSON")
    n8n.add_argument("--out", help="Save only the rendered target output")
    n8n.add_argument("--export", help="Save the complete analysis report as .md or .pdf")
    n8n.add_argument("--show-trace", action="store_true")
    n8n.add_argument("--model")

    scan = sub.add_parser("scan", help="Discover JSON/n8n files and interactively choose how to view them")
    scan.add_argument("path", nargs="?", default=".")
    scan.add_argument("--json", action="store_true")
    scan.add_argument("--no-interactive", action="store_true")
    scan.add_argument("--max-bytes", type=int, default=1_000_000)
    scan.add_argument("--model")

    parser.add_argument("legacy_input", nargs="?", help=argparse.SUPPRESS)
    parser.add_argument("--to", dest="legacy_to", choices=TARGETS, help=argparse.SUPPRESS)
    parser.add_argument("--out", dest="legacy_out", help=argparse.SUPPRESS)
    parser.add_argument("--export", dest="legacy_export", help=argparse.SUPPRESS)
    parser.add_argument("--show-model", dest="legacy_show_model", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--show-trace", dest="legacy_show_trace", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--trace-out", dest="legacy_trace_out", help=argparse.SUPPRESS)
    parser.add_argument("--model", dest="legacy_model", help=argparse.SUPPRESS)
    return parser


def _load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _print_scan_result(result) -> None:
    print(f"JSON Logic Agent V5.2 — project scan\nRoot: {result.root}\n")
    if not result.files:
        print("No JSON files found.")
    for item in result.files:
        badge = " [n8n deep-dive]" if item.likely_kind == "n8n-workflow" else ""
        print(f"{item.path}{badge}\n  → {item.likely_kind}: {item.note}")
        if item.top_level_keys:
            print(f"  keys: {', '.join(item.top_level_keys[:8])}")
    if result.skipped_large_files:
        print(f"\nSkipped large files: {len(result.skipped_large_files)}")
    if result.skipped_invalid_json:
        print(f"Skipped invalid JSON files: {len(result.skipped_invalid_json)}")


def _run_scan(args) -> None:
    result = scan_project(args.path, max_bytes=args.max_bytes)
    if args.json:
        print(result.model_dump_json(indent=2))
        return
    if not args.no_interactive and sys.stdin.isatty() and sys.stdout.isatty():
        print(f"JSON Logic Agent V5.2\nFound {len(result.files)} JSON file(s) in {result.root}. n8n exports are detected automatically.\n")
        run_interactive_scan(result, lambda path, target: _run_explain(path, target, None, None, False, False, None, args.model, True))
        return
    _print_scan_result(result)


def _run_explain(input_path, target, out, export, show_model, show_trace, trace_out, model, show_n8n_report=False) -> None:
    agent = JsonLogicAgent(model=model)
    result = agent.translate_file(input_path, target=target, include_trace=True)

    if show_n8n_report and result.n8n_report:
        print(format_n8n_report(result.n8n_report))
        print("\n--- SEMANTIC DEEP DIVE ---\n")
    if show_trace and result.trace:
        print(result.trace.model_dump_json(indent=2))
        print("\n--- RENDERED OUTPUT ---\n")
    elif show_model:
        print(result.logic.model_dump_json(indent=2))
        print("\n--- RENDERED OUTPUT ---\n")
    if trace_out and result.trace:
        Path(trace_out).write_text(result.trace.model_dump_json(indent=2) + "\n", encoding="utf-8")
        print(f"Wrote V5.2 trace to {trace_out}")
    if out:
        Path(out).write_text(result.rendered_output + "\n", encoding="utf-8")
        print(f"Wrote {target} output to {out}")
    else:
        print(result.rendered_output)
    print(f"\nSource format: {result.metadata.get('source_format')} | Fidelity score: {result.metadata.get('fidelity_score', 'n/a')}/100")
    if result.warnings:
        print("\n--- ASSUMPTIONS / WARNINGS ---")
        print(json.dumps(result.warnings, indent=2))
    if export:
        exported = export_report(result, export)
        print(f"\nExported complete report to {exported}")


def _run_n8n(args) -> None:
    data = _load_json(args.input)
    if not is_n8n_workflow(data):
        raise SystemExit("This file was not detected as an exported n8n workflow. Use `jsonlogic explain` for generic JSON.")
    report = analyze_n8n_workflow(data)
    if args.report_json:
        print(report.model_dump_json(indent=2))
        if args.report_only:
            return
    elif args.report_only:
        print(format_n8n_report(report))
        return
    _run_explain(args.input, args.to, args.out, args.export, False, args.show_trace, None, args.model, True)


def main() -> None:
    load_dotenv()
    args = build_parser().parse_args()
    if args.command == "scan":
        _run_scan(args); return
    if args.command == "n8n":
        _run_n8n(args); return
    if args.command == "explain":
        _run_explain(args.input, args.to, args.out, args.export, args.show_model, args.show_trace, args.trace_out, args.model, args.n8n_report); return
    if args.legacy_input:
        _run_explain(args.legacy_input, args.legacy_to or "logic", args.legacy_out, args.legacy_export, args.legacy_show_model, args.legacy_show_trace, args.legacy_trace_out, args.legacy_model); return
    build_parser().print_help()


if __name__ == "__main__":
    main()
