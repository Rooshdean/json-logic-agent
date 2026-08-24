import argparse
import json
from pathlib import Path

from dotenv import load_dotenv

from .agent import JsonLogicAgent


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="jsonlogic",
        description="Translate JSON through a V2 multi-agent pipeline into logic, Python, or JavaScript.",
    )
    parser.add_argument("input", help="Path to a JSON file")
    parser.add_argument(
        "--to",
        choices=["logic", "python", "javascript"],
        default="logic",
        help="Output format",
    )
    parser.add_argument("--out", help="Optional output file")
    parser.add_argument(
        "--show-model",
        action="store_true",
        help="Print the final normalized intermediate LogicModel",
    )
    parser.add_argument(
        "--show-trace",
        action="store_true",
        help="Print all V2 pipeline artifacts: inspector, architect, critic, final model, reviewer",
    )
    parser.add_argument(
        "--trace-out",
        help="Write the full V2 pipeline trace as JSON to this file",
    )
    parser.add_argument("--model", help="Override JSON_LOGIC_MODEL for this run")
    return parser


def main() -> None:
    load_dotenv()
    args = build_parser().parse_args()

    agent = JsonLogicAgent(model=args.model)
    result = agent.translate_file(args.input, target=args.to, include_trace=True)

    if args.show_trace and result.trace:
        print(result.trace.model_dump_json(indent=2))
        print("\n--- RENDERED OUTPUT ---\n")
    elif args.show_model:
        print(result.logic.model_dump_json(indent=2))
        print("\n--- RENDERED OUTPUT ---\n")

    if args.trace_out and result.trace:
        Path(args.trace_out).write_text(
            result.trace.model_dump_json(indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"Wrote V2 trace to {args.trace_out}")

    if args.out:
        Path(args.out).write_text(result.rendered_output + "\n", encoding="utf-8")
        print(f"Wrote {args.to} output to {args.out}")
    else:
        print(result.rendered_output)

    print(f"\nFidelity score: {result.metadata.get('fidelity_score', 'n/a')}/100")

    if result.warnings:
        print("\n--- ASSUMPTIONS / WARNINGS ---")
        print(json.dumps(result.warnings, indent=2))


if __name__ == "__main__":
    main()
