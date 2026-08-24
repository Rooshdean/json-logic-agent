from pathlib import Path
from typing import Callable

from .models import ProjectScanResult


ACTIONS = [
    ("Explain in normal logic", "logic"),
    ("Show as Python", "python"),
    ("Show as JavaScript", "javascript"),
    ("Show as TypeScript", "typescript"),
    ("Draw as Mermaid diagram", "mermaid"),
]


def action_target(label: str) -> str:
    normalized = label.replace("Deep-dive n8n workflow — ", "")
    for action_label, target in ACTIONS:
        if action_label == normalized:
            return target
    raise ValueError(f"Unknown interactive action: {label}")


def selected_file_path(scan: ProjectScanResult, selected_relative_path: str) -> Path:
    root = Path(scan.root)
    return root if root.is_file() else root / selected_relative_path


def run_interactive_scan(scan: ProjectScanResult, explain_callback: Callable[[Path, str], None]) -> None:
    try:
        import questionary
    except ImportError as exc:
        raise RuntimeError("Interactive mode requires questionary. Re-run ./scripts/setup.sh or pip install -e .") from exc

    if not scan.files:
        print("No JSON files found.")
        return

    by_path = {item.path: item for item in scan.files}
    file_choices = [questionary.Choice(title=f"{item.path}  [{item.likely_kind}]", value=item.path) for item in scan.files]

    while True:
        selected = questionary.select("Choose a JSON file:", choices=file_choices + [questionary.Separator(), questionary.Choice("Exit", value="__exit__")], use_arrow_keys=True, use_shortcuts=False).ask()
        if selected in {None, "__exit__"}:
            return

        is_n8n = by_path[selected].likely_kind == "n8n-workflow"
        labels = [f"Deep-dive n8n workflow — {label}" if is_n8n else label for label, _ in ACTIONS]
        action_label = questionary.select(f"What would you like to do with {selected}?", choices=labels + ["Choose another file", "Exit"], use_arrow_keys=True, use_shortcuts=False).ask()
        if action_label in {None, "Exit"}:
            return
        if action_label == "Choose another file":
            continue

        target = action_target(action_label)
        path = selected_file_path(scan, selected)
        print(f"\n--- {action_label}: {selected} ---\n")
        explain_callback(path, target)

        next_action = questionary.select("What next?", choices=["Choose another file", "Use another view for this file", "Exit"], use_arrow_keys=True, use_shortcuts=False).ask()
        if next_action in {None, "Exit"}:
            return
        if next_action == "Choose another file":
            continue

        while next_action == "Use another view for this file":
            action_label = questionary.select(f"Choose another view for {selected}:", choices=labels + ["Choose another file", "Exit"], use_arrow_keys=True, use_shortcuts=False).ask()
            if action_label in {None, "Exit"}:
                return
            if action_label == "Choose another file":
                break
            target = action_target(action_label)
            print(f"\n--- {action_label}: {selected} ---\n")
            explain_callback(path, target)
            next_action = questionary.select("What next?", choices=["Use another view for this file", "Choose another file", "Exit"], use_arrow_keys=True, use_shortcuts=False).ask()
            if next_action in {None, "Exit"}:
                return
