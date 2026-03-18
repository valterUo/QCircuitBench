"""GHZ state preparation."""

from __future__ import annotations

from qiskit import QuantumCircuit

from qcircuitbench.registry import registry
from qcircuitbench.core import CircuitRecord
from qcircuitbench.utils import circuit_to_record

DESCRIPTION = """\
The GHZ (Greenberger-Horne-Zeilinger) state is a maximally entangled n-qubit
state: (|00…0⟩ + |11…1⟩)/√2. It is prepared by applying a Hadamard gate to the
first qubit followed by a cascade of CNOT gates. GHZ states are fundamental
in quantum information, used in entanglement witnesses, quantum secret sharing,
and tests of quantum nonlocality.
"""

PATTERN = """\
Pattern: H(0) → CNOT(0,1) → CNOT(0,2) → … → CNOT(0,n-1).
Key primitive: fan-out entanglement from a single Hadamard.
"""


def generate_circuit(
    n_qubits: int = 4,
    **_kwargs,
) -> CircuitRecord:
    """Generate GHZ state preparation circuit."""
    n = max(n_qubits, 2)
    qc = QuantumCircuit(n)
    qc.h(0)
    for i in range(1, n):
        qc.cx(0, i)

    return circuit_to_record(
        qc,
        name="ghz_state",
        category="state_preparation",
        description=DESCRIPTION,
        parameters={"n_qubits": n},
        pattern_description=PATTERN,
        difficulty="easy",
    )


registry.register(
    "ghz_state",
    generate_circuit,
    category="state_preparation",
    difficulty="easy",
    description="GHZ state preparation — maximally entangled state",
)
