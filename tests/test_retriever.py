import importlib.util
from pathlib import Path

module_path = Path(__file__).resolve().parents[1] / "src/pipeline/retriever.py"
spec = importlib.util.spec_from_file_location("retriever", module_path)
retriever_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(retriever_module)
search = retriever_module.search


def test_search_signature():
    assert callable(search)
