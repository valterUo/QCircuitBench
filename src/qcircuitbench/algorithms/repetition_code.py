"""Repetition code (bit-flip error correction)."""

from __future__ import annotations

from qiskit import QuantumCircuit

from qcircuitbench.registry import registry
from qcircuitbench.core import CircuitRecord
from qcircuitbench.utils import circuit_to_record

DESCRIPTION = """\
The repetition code is the simplest quantum error-correcting code. It protects
against single bit-flip (X) errors by encoding one logical qubit into n physical
qubits via CNOT fan-out. Syndrome measurements on n-1 ancilla qubits detect
which (if any) data qubit flipped. Majority vote corrects the error.
For a distance-d code, ⌊(d-1)/2⌋ errors can be corrected.
"""

PATTERN = """\
Pattern: CNOT fan-out (data[0] → data[1..n-1]) → syndrome extraction
(CNOT pairs into ancillas) → measure ancillas → conditional X corrections.
Key primitive: redundant encoding + parity-check syndrome measurement.
"""


def generate_circuit(
    n_qubits: int = 3,
    **_kwargs,
) -> CircuitRecord:
    """Generate repetition code circuit (n data qubits, n-1 syndrome qubits)."""
    n = max(n_qubits, 3)
    n_ancilla = n - 1
    total = n + n_ancilla

    qc = QuantumCircuit(total, n_ancilla)

    # Encode: fan-out from qubit 0
    for i in range(1, n):
        qc.cx(0, i)

    qc.barrier()

    # Syndrome extraction
    for i in range(n_ancilla):
        qc.cx(i, n + i)
        qc.cx(i + 1, n + i)

    # Measure syndromes
    qc.measure(range(n, total), range(n_ancilla))

    return circuit_to_record(
        qc,
        name="repetition_code",
        category="error_correction",
        description=DESCRIPTION,
        parameters={"n_qubits": n, "n_ancilla": n_ancilla},
        pattern_description=PATTERN,
        difficulty="easy",
    )


registry.register(
    "repetition_code",
    generate_circuit,
    category="error_correction",
    difficulty="easy",
    description="Repetition code — bit-flip error correction",
)
