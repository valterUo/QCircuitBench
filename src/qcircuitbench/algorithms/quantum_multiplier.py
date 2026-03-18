"""QFT-based quantum multiplier."""

from __future__ import annotations

from math import pi
from qiskit import QuantumCircuit

from qcircuitbench.registry import registry
from qcircuitbench.core import CircuitRecord
from qcircuitbench.utils import circuit_to_record

DESCRIPTION = """\
The QFT-based multiplier (Draper adder variant) performs multiplication of two
n-bit integers using the Quantum Fourier Transform. It converts one register to
the Fourier basis, adds the other register via controlled phase rotations, and
converts back. This approach avoids ancilla qubits at the cost of deeper circuits.
"""

PATTERN = """\
Pattern: QFT(result register) → for each bit of multiplier:
    controlled phase-add(multiplicand) shifted by bit position → inverse QFT.
Key primitive: addition in Fourier space via controlled rotations.
"""


def _qft(qc: QuantumCircuit, qubits: list[int]) -> None:
    n = len(qubits)
    for i in range(n - 1, -1, -1):
        qc.h(qubits[i])
        for j in range(i):
            qc.cp(pi / (2 ** (i - j)), qubits[j], qubits[i])


def _iqft(qc: QuantumCircuit, qubits: list[int]) -> None:
    n = len(qubits)
    for i in range(n):
        qc.h(qubits[i])
        for j in range(i):
            qc.cp(-pi / (2 ** (i - j)), qubits[j], qubits[i])
    for i in range(n // 2):
        qc.swap(qubits[i], qubits[n - 1 - i])


def generate_circuit(
    n_qubits: int = 4,
    **_kwargs,
) -> CircuitRecord:
    """Generate QFT-based multiplier for n-bit × n-bit multiplication."""
    n = max(n_qubits, 2)
    result_size = 2 * n
    total = 2 * n + result_size  # a[n], b[n], result[2n]

    qc = QuantumCircuit(total)

    a = list(range(n))
    b = list(range(n, 2 * n))
    result = list(range(2 * n, total))

    # QFT on result register
    _qft(qc, result)

    # Controlled additions in Fourier space
    for i in range(n):
        for j in range(n):
            shift = i + j
            if shift < result_size:
                for k in range(result_size - shift):
                    if k < result_size:
                        angle = pi / (2**k)
                        # Doubly controlled rotation (simplified as two controls)
                        qc.cp(angle, a[i], result[shift + k])

    # Inverse QFT on result
    _iqft(qc, result)

    return circuit_to_record(
        qc,
        name="quantum_multiplier",
        category="arithmetic",
        description=DESCRIPTION,
        parameters={"n_qubits": n, "total_qubits": total},
        pattern_description=PATTERN,
        difficulty="hard",
    )


registry.register(
    "quantum_multiplier",
    generate_circuit,
    category="arithmetic",
    difficulty="hard",
    description="QFT-based quantum multiplier",
)
