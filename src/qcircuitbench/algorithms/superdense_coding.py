"""Superdense coding."""

from __future__ import annotations

from qiskit import QuantumCircuit

from qcircuitbench.registry import registry
from qcircuitbench.core import CircuitRecord
from qcircuitbench.utils import circuit_to_record

DESCRIPTION = """\
Superdense coding transmits two classical bits using one qubit, given a
pre-shared Bell pair. Alice encodes her 2-bit message by applying I, X, Z,
or XZ (= iY) to her half of the Bell pair, then sends it to Bob. Bob performs
a Bell measurement to recover both bits. This demonstrates that entanglement
doubles the classical capacity of a quantum channel.
"""

PATTERN = """\
Pattern: Bell pair (H·CNOT) → Alice applies {I, X, Z, XZ} on qubit 0
→ Bob: CNOT(0,1)·H(0)·Measure.
Key primitive: encoding 2 classical bits into 4 Bell states.
"""

MESSAGES = {"00": "I", "01": "X", "10": "Z", "11": "XZ"}


def generate_circuit(
    n_qubits: int = 2,
    message: str = "01",
    **_kwargs,
) -> CircuitRecord:
    """Generate superdense coding circuit."""
    qc = QuantumCircuit(2, 2)

    # Create Bell pair
    qc.h(0)
    qc.cx(0, 1)

    # Alice encodes message
    if message[1] == "1":
        qc.x(0)
    if message[0] == "1":
        qc.z(0)

    # Bob decodes
    qc.cx(0, 1)
    qc.h(0)
    qc.measure([0, 1], [0, 1])

    return circuit_to_record(
        qc,
        name="superdense_coding",
        category="quantum_information",
        description=DESCRIPTION,
        parameters={"n_qubits": 2, "message": message},
        pattern_description=PATTERN,
        difficulty="easy",
    )


registry.register(
    "superdense_coding",
    generate_circuit,
    category="quantum_information",
    difficulty="easy",
    description="Superdense coding — 2 classical bits via 1 qubit",
)
