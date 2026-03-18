"""Random Clifford circuits."""

from __future__ import annotations

import random
from qiskit import QuantumCircuit

from qcircuitbench.registry import registry
from qcircuitbench.core import CircuitRecord
from qcircuitbench.utils import circuit_to_record

DESCRIPTION = """\
A random Clifford circuit is composed of gates from the Clifford group {H, S, CNOT}.
Clifford circuits are efficiently simulable classically (Gottesman-Knill theorem)
but form the backbone of error correction, randomized benchmarking, and
stabilizer-based protocols. Random instances serve as baselines for circuit
synthesis benchmarks.
"""

PATTERN = """\
Pattern: random sequence of l gates, each uniformly chosen from {H, S, CNOT}
on random qubit(s).
Key primitive: Clifford group closure — all compositions remain in the Clifford group.
"""


def generate_circuit(
    n_qubits: int = 4,
    n_gates: int = 20,
    seed: int = 42,
    **_kwargs,
) -> CircuitRecord:
    """Generate random Clifford circuit."""
    n = max(n_qubits, 2)
    rng = random.Random(seed)

    qc = QuantumCircuit(n, n)
    for _ in range(n_gates):
        gate = rng.choice(["h", "s", "cx"])
        if gate in ("h", "s"):
            q = rng.randrange(n)
            getattr(qc, gate)(q)
        else:
            q1, q2 = rng.sample(range(n), 2)
            qc.cx(q1, q2)

    qc.measure(range(n), range(n))

    return circuit_to_record(
        qc,
        name="random_clifford",
        category="random",
        description=DESCRIPTION,
        parameters={"n_qubits": n, "n_gates": n_gates, "seed": seed},
        pattern_description=PATTERN,
        difficulty="hard",
    )


registry.register(
    "random_clifford",
    generate_circuit,
    category="random",
    difficulty="hard",
    description="Random Clifford circuit — {H, S, CNOT} gate set",
)
