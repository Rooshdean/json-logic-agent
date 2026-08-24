from json_logic_agent.models import (
    CritiqueReport,
    InspectionReport,
    LogicModel,
    LogicStep,
    PipelineTrace,
    ReviewReport,
    TranslationResult,
)


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
    for target in ["logic", "python", "javascript", "typescript", "mermaid"]:
        result = TranslationResult(
            source_name="test.json",
            target=target,
            logic=logic,
            rendered_output="pass",
        )
        assert result.target == target


def test_pipeline_trace_constructs():
    inspection = InspectionReport(
        json_kind="workflow",
        structural_summary="A simple workflow",
        confidence=0.9,
    )
    draft = LogicModel(summary="Draft", json_kind="workflow")
    critique = CritiqueReport(verdict="accept")
    final = LogicModel(summary="Final", json_kind="workflow")
    review = ReviewReport(verdict="pass", fidelity_score=97)

    trace = PipelineTrace(
        inspection=inspection,
        draft_logic=draft,
        critique=critique,
        final_logic=final,
        review=review,
    )

    assert trace.review is not None
    assert trace.review.fidelity_score == 97


def test_review_score_bounds():
    review = ReviewReport(verdict="pass", fidelity_score=100)
    assert review.fidelity_score == 100
