"""Quantum Fourier Transform."""

from __future__ import annotations

from math import pi
from qiskit import QuantumCircuit

from qcircuitbench.registry import registry
from qcircuitbench.core import CircuitRecord
from qcircuitbench.utils import circuit_to_record

DESCRIPTION = """\
The Quantum Fourier Transform (QFT) maps computational basis states to their
Fourier-transformed amplitudes. It is the quantum analogue of the discrete
Fourier transform and is a key subroutine in Shor's algorithm, phase estimation,
and many other quantum algorithms. The QFT on n qubits uses O(n²) gates.
"""

PATTERN = """\
Pattern: For each qubit j (high to low): H(j), then controlled-R_k rotations
from all lower qubits, followed by qubit reversal swaps.
Key primitive: butterfly-like controlled phase rotations build up Fourier
coefficients qubit by qubit.
"""


def _qft_rotations(qc: QuantumCircuit, n: int) -> None:
    """Apply the QFT rotation layer."""
    for target in range(n - 1, -1, -1):
        qc.h(target)
        for control in range(target):
            angle = pi / (2 ** (target - control))
            qc.cp(angle, control, target)


def generate_circuit(
    n_qubits: int = 4,
    **_kwargs,
) -> CircuitRecord:
    """Generate a QFT circuit on *n_qubits* qubits."""
    n = max(n_qubits, 2)
    qc = QuantumCircuit(n)

    _qft_rotations(qc, n)

    # Swap qubits for correct output ordering
    for i in range(n // 2):
        qc.swap(i, n - i - 1)

    return circuit_to_record(
        qc,
        name="qft",
        category="algebraic",
        description=DESCRIPTION,
        parameters={"n_qubits": n},
        pattern_description=PATTERN,
        difficulty="medium",
    )


registry.register(
    "qft",
    generate_circuit,
    category="algebraic",
    difficulty="medium",
    description="Quantum Fourier Transform",
)
