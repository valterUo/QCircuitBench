"""Smoke tests for qcircuitbench — every algorithm generates without error."""

import pytest
import qcircuitbench


ALGORITHMS = qcircuitbench.list_algorithms()


@pytest.mark.parametrize("name", ALGORITHMS)
def test_generate_default(name):
    """Each algorithm generates a valid CircuitRecord at default qubit count."""
    rec = qcircuitbench.get(name)
    assert rec.name == name
    assert rec.category in qcircuitbench.core.CATEGORIES
    assert rec.width >= 1
    assert rec.depth >= 0
    assert len(rec.qasm) > 0
    assert len(rec.description) > 0


@pytest.mark.parametrize("name", ALGORITHMS)
def test_qasm_header(name):
    """Generated QASM starts with the OpenQASM 3.0 header."""
    rec = qcircuitbench.get(name)
    assert rec.qasm.startswith("OPENQASM 3.0;")


def test_list_algorithms():
    algos = qcircuitbench.list_algorithms()
    assert len(algos) >= 30
    assert "grover" in algos
    assert "shor" in algos
    assert "ghz_state" in algos


def test_list_categories():
    cats = qcircuitbench.list_categories()
    assert "oracular" in cats
    assert "algebraic" in cats
    assert "error_correction" in cats


def test_search():
    assert "shor" in qcircuitbench.search("factor")
    assert "grover" in qcircuitbench.search("search")


def test_get_all_by_category():
    recs = qcircuitbench.get_all(category="state_preparation")
    names = {r.name for r in recs}
    assert "ghz_state" in names
    assert "bell_state" in names


def test_get_all_by_difficulty():
    recs = qcircuitbench.get_all(difficulty="easy")
    assert all(r.difficulty == "easy" for r in recs)
    assert len(recs) > 0


def test_export_jsonl(tmp_path):
    from qcircuitbench.export import to_jsonl
    import json

    path = tmp_path / "test.jsonl"
    n = to_jsonl(path, qubit_range=range(3, 5))
    assert n > 0
    with open(path) as f:
        first = json.loads(f.readline())
    assert "prompt" in first
    assert "completion" in first


def test_export_qasm_dir(tmp_path):
    from qcircuitbench.export import to_qasm_dir

    n = to_qasm_dir(tmp_path / "out", qubit_range=range(3, 4))
    assert n > 0
    assert (tmp_path / "out" / "grover").is_dir()
