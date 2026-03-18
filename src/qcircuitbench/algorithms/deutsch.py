"""Deutsch's algorithm (single-qubit oracle)."""

from __future__ import annotations

from qiskit import QuantumCircuit

from qcircuitbench.registry import registry
from qcircuitbench.core import CircuitRecord
from qcircuitbench.utils import circuit_to_record

DESCRIPTION = """\
Deutsch's algorithm is the simplest quantum algorithm: it determines whether a
single-bit Boolean function f:{0,1}→{0,1} is constant or balanced using one
query. It operates on 2 qubits (input + ancilla) and is the precursor to the
Deutsch-Jozsa algorithm.
"""

PATTERN = """\
Pattern: H⊗2 with ancilla in |−⟩ → Oracle → H on input → Measure.
If measurement is 0, f is constant; if 1, f is balanced.
"""


def generate_circuit(
    n_qubits: int = 2,
    oracle_type: str = "balanced",
    **_kwargs,
) -> CircuitRecord:
    """Generate Deutsch's 2-qubit algorithm circuit."""
    qc = QuantumCircuit(2, 1)
    # Prepare ancilla in |−⟩
    qc.x(1)
    qc.h([0, 1])
    # Oracle
    if oracle_type == "balanced":
        qc.cx(0, 1)
    elif oracle_type == "constant_1":
        qc.x(1)
    # constant_0 → identity (do nothing)
    qc.h(0)
    qc.measure(0, 0)

    return circuit_to_record(
        qc,
        name="deutsch",
        category="oracular",
        description=DESCRIPTION,
        parameters={"n_qubits": 2, "oracle_type": oracle_type},
        pattern_description=PATTERN,
        difficulty="easy",
    )


registry.register(
    "deutsch",
    generate_circuit,
    category="oracular",
    difficulty="easy",
    description="Deutsch's algorithm — simplest quantum oracle problem",
)
