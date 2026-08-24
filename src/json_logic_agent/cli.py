import argparse
import json
from pathlib import Path

from dotenv import load_dotenv

from .agent import JsonLogicAgent
from .scanner import scan_project

TARGETS = ["logic", "python", "javascript", "typescript", "mermaid"]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="jsonlogic",
        description="Understand JSON as normal logic, code, or diagrams.",
    )
    sub = parser.add_subparsers(dest="command")

    explain = sub.add_parser("explain", help="Explain or translate one JSON file")
    explain.add_argument("input", help="Path to a JSON file")
    explain.add_argument("--to", choices=TARGETS, default="logic")
    explain.add_argument("--out", help="Optional output file")
    explain.add_argument("--show-model", action="store_true")
    explain.add_argument("--show-trace", action="store_true")
    explain.add_argument("--trace-out", help="Write full pipeline trace as JSON")
    explain.add_argument("--model", help="Override JSON_LOGIC_MODEL")

    scan = sub.add_parser("scan", help="Discover and classify JSON files in a project")
    scan.add_argument("path", nargs="?", default=".", help="Project directory; defaults to current directory")
    scan.add_argument("--json", action="store_true", help="Print machine-readable scan result")
    scan.add_argument("--max-bytes", type=int, default=1_000_000, help="Skip JSON files larger than this")

    # Backward-compatible V1/V2 form: jsonlogic file.json --to python
    parser.add_argument("legacy_input", nargs="?", help=argparse.SUPPRESS)
    parser.add_argument("--to", dest="legacy_to", choices=TARGETS, help=argparse.SUPPRESS)
    parser.add_argument("--out", dest="legacy_out", help=argparse.SUPPRESS)
    parser.add_argument("--show-model", dest="legacy_show_model", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--show-trace", dest="legacy_show_trace", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--trace-out", dest="legacy_trace_out", help=argparse.SUPPRESS)
    parser.add_argument("--model", dest="legacy_model", help=argparse.SUPPRESS)
    return parser


def _print_scan(args) -> None:
    result = scan_project(args.path, max_bytes=args.max_bytes)
    if args.json:
        print(result.model_dump_json(indent=2))
        return

    print(f"JSON Logic Agent V3 — project scan\nRoot: {result.root}\n")
    if not result.files:
        print("No JSON files found.")
    for item in result.files:
        print(f"{item.path}")
        print(f"  → {item.likely_kind}: {item.note}")
        if item.top_level_keys:
            print(f"  keys: {', '.join(item.top_level_keys[:8])}")
    if result.skipped_large_files:
        print(f"\nSkipped large files: {len(result.skipped_large_files)}")
    if result.skipped_invalid_json:
        print(f"Skipped invalid JSON files: {len(result.skipped_invalid_json)}")


def _run_explain(input_path, target, out, show_model, show_trace, trace_out, model) -> None:
    agent = JsonLogicAgent(model=model)
    result = agent.translate_file(input_path, target=target, include_trace=True)

    if show_trace and result.trace:
        print(result.trace.model_dump_json(indent=2))
        print("\n--- RENDERED OUTPUT ---\n")
    elif show_model:
        print(result.logic.model_dump_json(indent=2))
        print("\n--- RENDERED OUTPUT ---\n")

    if trace_out and result.trace:
        Path(trace_out).write_text(result.trace.model_dump_json(indent=2) + "\n", encoding="utf-8")
        print(f"Wrote V3 trace to {trace_out}")

    if out:
        Path(out).write_text(result.rendered_output + "\n", encoding="utf-8")
        print(f"Wrote {target} output to {out}")
    else:
        print(result.rendered_output)

    print(f"\nFidelity score: {result.metadata.get('fidelity_score', 'n/a')}/100")
    if result.warnings:
        print("\n--- ASSUMPTIONS / WARNINGS ---")
        print(json.dumps(result.warnings, indent=2))


def main() -> None:
    load_dotenv()
    args = build_parser().parse_args()

    if args.command == "scan":
        _print_scan(args)
        return

    if args.command == "explain":
        _run_explain(args.input, args.to, args.out, args.show_model, args.show_trace, args.trace_out, args.model)
        return

    if args.legacy_input:
        _run_explain(
            args.legacy_input,
            args.legacy_to or "logic",
            args.legacy_out,
            args.legacy_show_model,
            args.legacy_show_trace,
            args.legacy_trace_out,
            args.legacy_model,
        )
        return

    build_parser().print_help()


if __name__ == "__main__":
    main()
