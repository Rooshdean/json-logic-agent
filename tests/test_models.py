from json_logic_agent.models import LogicModel, LogicStep, TranslationResult


def test_logic_model_constructs():
    model = LogicModel(
        summary="Test",
        json_kind="workflow",
        steps=[LogicStep(order=1, title="Start", explanation="Begin")],
    )
    assert model.steps[0].order == 1
    assert model.assumptions == []


def test_mutable_defaults_are_isolated():
    first = LogicModel(summary="One", json_kind="data")
    second = LogicModel(summary="Two", json_kind="data")
    first.actions.append("do_something")
    assert second.actions == []


def test_translation_result_targets():
    logic = LogicModel(summary="Test", json_kind="workflow")
    result = TranslationResult(
        source_name="test.json",
        target="python",
        logic=logic,
        rendered_output="pass",
    )
    assert result.target == "python"
