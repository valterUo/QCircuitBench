"""Shor's 9-qubit error-correcting code."""

from __future__ import annotations

from qiskit import QuantumCircuit

from qcircuitbench.registry import registry
from qcircuitbench.core import CircuitRecord
from qcircuitbench.utils import circuit_to_record

DESCRIPTION = """\
Shor's 9-qubit code is the first quantum error-correcting code, capable of
correcting arbitrary single-qubit errors (bit-flip, phase-flip, or both).
It encodes 1 logical qubit into 9 physical qubits by concatenating a 3-qubit
phase-flip code with a 3-qubit bit-flip code. The encoding uses CNOT and
Hadamard gates to create the protected logical state.
"""

PATTERN = """\
Pattern: Phase-flip encoding: CNOT(0→3), CNOT(0→6), H on {0,3,6}.
Bit-flip encoding: CNOT(0→1), CNOT(0→2), CNOT(3→4), CNOT(3→5), CNOT(6→7), CNOT(6→8).
Key primitive: concatenated code — outer phase-flip ∘ inner bit-flip.
"""


def generate_circuit(
    n_qubits: int = 9,
    **_kwargs,
) -> CircuitRecord:
    """Generate Shor 9-qubit code encoding circuit."""
    qc = QuantumCircuit(9)

    # Phase-flip code layer
    qc.cx(0, 3)
    qc.cx(0, 6)
    qc.h(0)
    qc.h(3)
    qc.h(6)

    # Bit-flip code layer
    qc.cx(0, 1)
    qc.cx(0, 2)
    qc.cx(3, 4)
    qc.cx(3, 5)
    qc.cx(6, 7)
    qc.cx(6, 8)

    return circuit_to_record(
        qc,
        name="shor_code",
        category="error_correction",
        description=DESCRIPTION,
        parameters={"n_qubits": 9},
        pattern_description=PATTERN,
        difficulty="medium",
    )


registry.register(
    "shor_code",
    generate_circuit,
    category="error_correction",
    difficulty="medium",
    description="Shor's 9-qubit code — first QEC code",
)
