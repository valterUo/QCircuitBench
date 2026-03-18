"""W state preparation."""

from __future__ import annotations

import math
from qiskit import QuantumCircuit

from qcircuitbench.registry import registry
from qcircuitbench.core import CircuitRecord
from qcircuitbench.utils import circuit_to_record

DESCRIPTION = """\
The W state is an entangled n-qubit state with exactly one excitation spread
equally: (|100…0⟩ + |010…0⟩ + … + |000…1⟩)/√n. Unlike GHZ states, W states
retain bipartite entanglement when any qubit is traced out. Preparation uses
a cascade of controlled rotations to distribute a single excitation.
"""

PATTERN = """\
Pattern: X(0) → for k=0..n-2: RY(θ_k) controlled rotation to split amplitude
from qubit k to qubit k+1, where θ_k = 2·arccos(√(1/(n-k))).
Key primitive: amplitude redistribution via controlled rotations.
"""


def generate_circuit(
    n_qubits: int = 4,
    **_kwargs,
) -> CircuitRecord:
    """Generate W state preparation circuit."""
    n = max(n_qubits, 2)
    qc = QuantumCircuit(n)

    # Start with |100...0⟩
    qc.x(0)

    # Distribute the excitation
    for i in range(n - 1):
        # Rotation angle to split amplitude equally among remaining qubits
        theta = 2 * math.acos(math.sqrt(1 / (n - i)))
        qc.cry(theta, i, i + 1)
        qc.cx(i + 1, i)

    return circuit_to_record(
        qc,
        name="w_state",
        category="state_preparation",
        description=DESCRIPTION,
        parameters={"n_qubits": n},
        pattern_description=PATTERN,
        difficulty="medium",
    )


registry.register(
    "w_state",
    generate_circuit,
    category="state_preparation",
    difficulty="medium",
    description="W state preparation — single-excitation entangled state",
)
