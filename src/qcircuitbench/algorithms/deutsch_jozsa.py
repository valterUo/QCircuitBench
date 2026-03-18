"""Deutsch-Jozsa algorithm."""

from __future__ import annotations

import random
from qiskit import QuantumCircuit

from qcircuitbench.registry import registry
from qcircuitbench.core import CircuitRecord
from qcircuitbench.utils import circuit_to_record

DESCRIPTION = """\
The Deutsch-Jozsa algorithm determines whether a Boolean function f:{0,1}^n→{0,1}
is constant or balanced using a single query. Classically, 2^(n-1)+1 queries are
needed in the worst case. After Hadamard transforms, the oracle is queried, and
a final round of Hadamards collapses all qubits to |0⟩ if f is constant.
"""

PATTERN = """\
Pattern: H⊗n ⊗ X·H(ancilla) → Oracle → H⊗n → Measure.
If all measurement results are 0, f is constant; otherwise balanced.
Key primitive: phase kickback distinguishes global vs local function properties.
"""


def _balanced_oracle(n: int, seed: int = 42) -> QuantumCircuit:
    """A balanced oracle that flips the ancilla for exactly half the inputs."""
    rng = random.Random(seed)
    qc = QuantumCircuit(n + 1, name="Oracle")
    # Pick a random balanced pattern: CNOT from a random qubit
    control = rng.randrange(n)
    qc.cx(control, n)
    return qc


def _constant_oracle(n: int, value: int = 0) -> QuantumCircuit:
    """A constant oracle (f=0 or f=1)."""
    qc = QuantumCircuit(n + 1, name="Oracle")
    if value == 1:
        qc.x(n)
    return qc


def generate_circuit(
    n_qubits: int = 4,
    oracle_type: str = "balanced",
    **_kwargs,
) -> CircuitRecord:
    """Generate Deutsch-Jozsa circuit."""
    n = max(n_qubits, 2)
    if oracle_type == "balanced":
        oracle = _balanced_oracle(n)
    else:
        oracle = _constant_oracle(n)

    qc = QuantumCircuit(n + 1, n)
    qc.h(range(n))
    qc.x(n)
    qc.h(n)
    qc.compose(oracle, inplace=True)
    qc.h(range(n))
    qc.measure(range(n), range(n))

    return circuit_to_record(
        qc,
        name="deutsch_jozsa",
        category="oracular",
        description=DESCRIPTION,
        parameters={"n_qubits": n, "oracle_type": oracle_type},
        pattern_description=PATTERN,
        difficulty="easy",
    )


registry.register(
    "deutsch_jozsa",
    generate_circuit,
    category="oracular",
    difficulty="easy",
    description="Deutsch-Jozsa algorithm — constant vs balanced oracle",
)
