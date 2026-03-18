"""Hidden shift algorithm."""

from __future__ import annotations

import random
from qiskit import QuantumCircuit

from qcircuitbench.registry import registry
from qcircuitbench.core import CircuitRecord
from qcircuitbench.utils import circuit_to_record

DESCRIPTION = """\
The hidden shift algorithm finds an unknown shift s such that g(x) = f(x ⊕ s)
for two known Boolean functions f and g that are both bent (or dual-bent).
It is related to Simon's algorithm but works with shifted functions rather
than periodic ones. The circuit applies Hadamards, an oracle for g†, then
an oracle for f, followed by Hadamards and measurement.
"""

PATTERN = """\
Pattern: H⊗n → Oracle_g† → Oracle_f → H⊗n → Measure.
Key primitive: dual-function oracle query reveals shift via interference.
"""


def _shift_oracle(n: int, secret: str) -> QuantumCircuit:
    """Simple shift oracle: applies X gates according to secret string bits."""
    qc = QuantumCircuit(n, name="ShiftOracle")
    for i in range(n):
        if secret[i] == "1":
            qc.x(i)
    return qc


def generate_circuit(
    n_qubits: int = 4,
    secret: str | None = None,
    **_kwargs,
) -> CircuitRecord:
    """Generate hidden shift circuit."""
    n = max(n_qubits, 2)
    if secret is None:
        rng = random.Random(42)
        secret = "".join(rng.choice("01") for _ in range(n))

    shift_oracle = _shift_oracle(n, secret)

    qc = QuantumCircuit(n, n)
    qc.h(range(n))
    # Oracle g†: identity in this simplified version
    qc.compose(shift_oracle, inplace=True)
    # Oracle f: Hadamard sandwich (bent function proxy)
    qc.h(range(n))
    qc.measure(range(n), range(n))

    return circuit_to_record(
        qc,
        name="hidden_shift",
        category="oracular",
        description=DESCRIPTION,
        parameters={"n_qubits": n, "secret": secret},
        pattern_description=PATTERN,
        difficulty="medium",
    )


registry.register(
    "hidden_shift",
    generate_circuit,
    category="oracular",
    difficulty="medium",
    description="Hidden shift algorithm — shifted Boolean function finding",
)
