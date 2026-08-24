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
    """Return the render target associated with a menu label."""
    for action_label, target in ACTIONS:
        if action_label == label:
            return target
    raise ValueError(f"Unknown interactive action: {label}")


def selected_file_path(scan: ProjectScanResult, selected_relative_path: str) -> Path:
    root = Path(scan.root)
    if root.is_file():
        return root
    return root / selected_relative_path


def run_interactive_scan(
    scan: ProjectScanResult,
    explain_callback: Callable[[Path, str], None],
) -> None:
    """Launch the V4 arrow-key terminal flow for a completed project scan."""
    try:
        import questionary
    except ImportError as exc:  # pragma: no cover - protected by package dependency
        raise RuntimeError(
            "Interactive mode requires questionary. Re-run ./scripts/setup.sh or pip install -e ."
        ) from exc

    if not scan.files:
        print("No JSON files found.")
        return

    file_choices = [
        questionary.Choice(
            title=f"{item.path}  [{item.likely_kind}]",
            value=item.path,
        )
        for item in scan.files
    ]

    while True:
        selected = questionary.select(
            "Choose a JSON file:",
            choices=file_choices + [questionary.Separator(), questionary.Choice("Exit", value="__exit__")],
            use_arrow_keys=True,
            use_shortcuts=False,
        ).ask()

        if selected in {None, "__exit__"}:
            return

        action_label = questionary.select(
            f"What would you like to do with {selected}?",
            choices=[label for label, _ in ACTIONS] + ["Choose another file", "Exit"],
            use_arrow_keys=True,
            use_shortcuts=False,
        ).ask()

        if action_label in {None, "Exit"}:
            return
        if action_label == "Choose another file":
            continue

        target = action_target(action_label)
        path = selected_file_path(scan, selected)
        print(f"\n--- {action_label}: {selected} ---\n")
        explain_callback(path, target)

        next_action = questionary.select(
            "What next?",
            choices=["Choose another file", "Use another view for this file", "Exit"],
            use_arrow_keys=True,
            use_shortcuts=False,
        ).ask()

        if next_action in {None, "Exit"}:
            return
        if next_action == "Choose another file":
            continue

        # Keep the same file and ask only for another representation.
        while next_action == "Use another view for this file":
            action_label = questionary.select(
                f"Choose another view for {selected}:",
                choices=[label for label, _ in ACTIONS] + ["Choose another file", "Exit"],
                use_arrow_keys=True,
                use_shortcuts=False,
            ).ask()
            if action_label in {None, "Exit"}:
                return
            if action_label == "Choose another file":
                break

            target = action_target(action_label)
            print(f"\n--- {action_label}: {selected} ---\n")
            explain_callback(path, target)

            next_action = questionary.select(
                "What next?",
                choices=["Use another view for this file", "Choose another file", "Exit"],
                use_arrow_keys=True,
                use_shortcuts=False,
            ).ask()
            if next_action in {None, "Exit"}:
                return

        # Any break from the inner loop returns to file selection.
