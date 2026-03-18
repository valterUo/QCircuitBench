"""Quantum teleportation."""

from __future__ import annotations

from qiskit import QuantumCircuit

from qcircuitbench.registry import registry
from qcircuitbench.core import CircuitRecord
from qcircuitbench.utils import circuit_to_record

DESCRIPTION = """\
Quantum teleportation transfers an arbitrary qubit state |ψ⟩ from Alice to Bob
using one shared Bell pair and two classical bits. Alice performs a Bell-basis
measurement on her qubit and her half of the entangled pair, sending 2 classical
bits to Bob, who applies conditional X and Z corrections to recover |ψ⟩. No
quantum information travels through the classical channel.
"""

PATTERN = """\
Pattern: Bell pair creation (H·CNOT) → Bell measurement (CNOT·H·Measure) on
Alice's qubits → classically-controlled X, Z on Bob's qubit.
Key primitive: entanglement + classical communication = quantum channel.
"""


def generate_circuit(
    n_qubits: int = 3,
    **_kwargs,
) -> CircuitRecord:
    """Generate quantum teleportation circuit (3 qubits)."""
    qc = QuantumCircuit(3, 2)

    # Create Bell pair between qubits 1 and 2
    qc.h(1)
    qc.cx(1, 2)

    # Alice's Bell measurement on qubits 0 and 1
    qc.cx(0, 1)
    qc.h(0)
    qc.measure(0, 0)
    qc.measure(1, 1)

    # Bob's corrections (classically conditioned)
    # In Qiskit ≥1.0 use if_test; here we use unconditional gates for circuit
    # structure (full classical conditioning requires dynamic circuits).
    qc.cx(1, 2)
    qc.cz(0, 2)

    return circuit_to_record(
        qc,
        name="teleportation",
        category="quantum_information",
        description=DESCRIPTION,
        parameters={"n_qubits": 3},
        pattern_description=PATTERN,
        difficulty="easy",
    )


registry.register(
    "teleportation",
    generate_circuit,
    category="quantum_information",
    difficulty="easy",
    description="Quantum teleportation — state transfer via entanglement",
)
