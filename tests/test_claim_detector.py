import importlib.util
from pathlib import Path

module_path = Path(__file__).resolve().parents[1] / "src/pipeline/claim_detector.py"
spec = importlib.util.spec_from_file_location("claim_detector", module_path)
claim_detector_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(claim_detector_module)
ClaimDetector = claim_detector_module.ClaimDetector


def test_claim_detector_init():
    detector = ClaimDetector(api_key="test")
    assert isinstance(detector, ClaimDetector)
