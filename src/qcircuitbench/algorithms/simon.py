"""Simon's algorithm."""

from __future__ import annotations

import random
from qiskit import QuantumCircuit

from qcircuitbench.registry import registry
from qcircuitbench.core import CircuitRecord
from qcircuitbench.utils import circuit_to_record

DESCRIPTION = """\
Simon's algorithm finds a hidden period string s such that f(x) = f(y) iff
x ⊕ y ∈ {0, s}. It uses O(n) quantum queries compared to O(2^(n/2))
classically. The circuit applies Hadamards, queries the oracle on n input
and n output qubits, then applies Hadamards again and measures the input
register. Repeating O(n) times and solving a linear system reveals s.
"""

PATTERN = """\
Pattern: H⊗n (input) → Oracle(input, output) → H⊗n (input) → Measure input.
Key primitive: oracle entangles input and output registers; Hadamard on input
produces a random vector orthogonal to s.
"""


def _simon_oracle(n: int, secret: str) -> QuantumCircuit:
    """Two-to-one oracle for Simon's problem with hidden string *secret*."""
    qc = QuantumCircuit(2 * n, name="Oracle")
    # Copy input to output
    for i in range(n):
        qc.cx(i, i + n)
    # XOR secret into output for inputs with leading bit = 1
    if secret != "0" * n:
        # Find first 1-bit in secret
        j = secret.index("1")
        for i in range(n):
            if secret[i] == "1":
                qc.cx(j, i + n)
    return qc


def generate_circuit(
    n_qubits: int = 4,
    secret: str | None = None,
    **_kwargs,
) -> CircuitRecord:
    """Generate Simon's algorithm circuit."""
    n = max(n_qubits, 2)
    if secret is None:
        # Random non-trivial secret
        rng = random.Random(42)
        secret = "".join(rng.choice("01") for _ in range(n))
        if secret == "0" * n:
            secret = "1" + "0" * (n - 1)

    oracle = _simon_oracle(n, secret)

    qc = QuantumCircuit(2 * n, n)
    qc.h(range(n))
    qc.compose(oracle, inplace=True)
    qc.h(range(n))
    qc.measure(range(n), range(n))

    return circuit_to_record(
        qc,
        name="simon",
        category="oracular",
        description=DESCRIPTION,
        parameters={"n_qubits": n, "secret": secret},
        pattern_description=PATTERN,
        difficulty="medium",
    )


registry.register(
    "simon",
    generate_circuit,
    category="oracular",
    difficulty="medium",
    description="Simon's algorithm — hidden period finding",
)
