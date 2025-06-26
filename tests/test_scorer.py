import importlib.util
from pathlib import Path

module_path = Path(__file__).resolve().parents[1] / "src/pipeline/scorer.py"
spec = importlib.util.spec_from_file_location("scorer", module_path)
scorer_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scorer_module)
FactCheckScorer = scorer_module.FactCheckScorer


def test_scorer_init():
    scorer = FactCheckScorer(api_key="test")
    assert isinstance(scorer, FactCheckScorer)
