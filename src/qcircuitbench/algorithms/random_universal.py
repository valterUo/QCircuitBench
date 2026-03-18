"""Random universal gate set circuits."""

from __future__ import annotations

import random
from qiskit import QuantumCircuit

from qcircuitbench.registry import registry
from qcircuitbench.core import CircuitRecord
from qcircuitbench.utils import circuit_to_record

DESCRIPTION = """\
A random universal circuit is composed of gates from the universal gate set
{H, S, T, CNOT}. Unlike Clifford circuits, adding the T gate makes the set
computationally universal — capable of approximating any unitary to arbitrary
precision (Solovay-Kitaev theorem). These circuits cannot be efficiently
classically simulated in general.
"""

PATTERN = """\
Pattern: random sequence of l gates from {H, S, T, CNOT} on random qubit(s).
Key primitive: T gate breaks Clifford-group closure and enables universality.
"""


def generate_circuit(
    n_qubits: int = 4,
    n_gates: int = 20,
    seed: int = 42,
    **_kwargs,
) -> CircuitRecord:
    """Generate random universal circuit."""
    n = max(n_qubits, 2)
    rng = random.Random(seed)

    qc = QuantumCircuit(n, n)
    for _ in range(n_gates):
        gate = rng.choice(["h", "s", "t", "cx"])
        if gate in ("h", "s", "t"):
            q = rng.randrange(n)
            getattr(qc, gate)(q)
        else:
            q1, q2 = rng.sample(range(n), 2)
            qc.cx(q1, q2)

    qc.measure(range(n), range(n))

    return circuit_to_record(
        qc,
        name="random_universal",
        category="random",
        description=DESCRIPTION,
        parameters={"n_qubits": n, "n_gates": n_gates, "seed": seed},
        pattern_description=PATTERN,
        difficulty="hard",
    )


registry.register(
    "random_universal",
    generate_circuit,
    category="random",
    difficulty="hard",
    description="Random universal circuit — {H, S, T, CNOT} gate set",
)
