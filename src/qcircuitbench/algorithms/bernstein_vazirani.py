"""Bernstein-Vazirani algorithm."""

from __future__ import annotations

from qiskit import QuantumCircuit

from qcircuitbench.registry import registry
from qcircuitbench.core import CircuitRecord
from qcircuitbench.utils import circuit_to_record

DESCRIPTION = """\
The Bernstein-Vazirani algorithm determines a secret n-bit string s in a single
query to an oracle f(x) = s·x (mod 2). Classically this requires n queries.
The circuit applies Hadamard gates to all qubits, queries the oracle with an
ancilla prepared in |−⟩, then applies Hadamards again. Measuring the first n
qubits directly reveals s.
"""

PATTERN = """\
Pattern: H⊗n ⊗ X·H(ancilla) → Oracle → H⊗n → Measure.
Key primitive: phase kickback from the ancilla turns bit-wise inner product
into phase information that Hadamard transforms reveal.
"""


def _oracle(n: int, secret: str) -> QuantumCircuit:
    """Oracle implementing f(x) = s·x mod 2."""
    qc = QuantumCircuit(n + 1, name="Oracle")
    s = secret[::-1]  # reverse for qiskit ordering
    for i in range(n):
        if s[i] == "1":
            qc.cx(i, n)
    return qc


def generate_circuit(
    n_qubits: int = 4,
    secret: str | None = None,
    **_kwargs,
) -> CircuitRecord:
    """Generate Bernstein-Vazirani circuit for a given secret string."""
    n = max(n_qubits, 2)
    if secret is None:
        # Default: alternating bits
        secret = ("10" * n)[:n]
    assert len(secret) == n

    oracle = _oracle(n, secret)

    qc = QuantumCircuit(n + 1, n)
    qc.h(range(n))
    qc.x(n)
    qc.h(n)
    qc.compose(oracle, inplace=True)
    qc.h(range(n))
    qc.measure(range(n), range(n))

    return circuit_to_record(
        qc,
        name="bernstein_vazirani",
        category="oracular",
        description=DESCRIPTION,
        parameters={"n_qubits": n, "secret": secret},
        pattern_description=PATTERN,
        difficulty="easy",
    )


registry.register(
    "bernstein_vazirani",
    generate_circuit,
    category="oracular",
    difficulty="easy",
    description="Bernstein-Vazirani algorithm — single-query hidden string",
)
