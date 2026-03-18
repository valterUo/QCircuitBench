"""Quantum Signal Processing / QSVT."""

from __future__ import annotations

from qiskit import QuantumCircuit
from qiskit.circuit import Parameter

from qcircuitbench.registry import registry
from qcircuitbench.core import CircuitRecord
from qcircuitbench.utils import circuit_to_record

DESCRIPTION = """\
Quantum Singular Value Transformation (QSVT) is a unifying framework that
subsumes Grover search, QPE, HHL, Hamiltonian simulation, and amplitude
amplification as special cases. Given a block-encoding of a matrix A, QSVT
applies a polynomial transformation to the singular values of A by interleaving
signal rotations (parameterized Z rotations on an ancilla) with signal-processing
unitaries. The choice of phase angles φ_0, …, φ_d determines the polynomial.
"""

PATTERN = """\
Pattern: for k=0..d: RZ(φ_k) on ancilla → controlled-U (block encoding query)
→ (alternating with controlled-U†).
Key primitive: polynomial eigenvalue transformation via interleaved phase rotations.
"""


def generate_circuit(
    n_qubits: int = 4,
    degree: int = 4,
    **_kwargs,
) -> CircuitRecord:
    """Generate a QSVT circuit skeleton with *degree* phase rotations."""
    n = max(n_qubits, 2)
    total = n + 1  # n system qubits + 1 signal qubit (ancilla)
    ancilla = 0
    system = list(range(1, total))

    qc = QuantumCircuit(total, 1)

    # Phase angles (parameterized)
    phases = [Parameter(f"φ_{k}") for k in range(degree + 1)]

    for k in range(degree + 1):
        # Signal rotation on ancilla
        qc.rz(phases[k], ancilla)

        # Block-encoding query (simplified as controlled-H + entangling)
        if k % 2 == 0:
            for s in system:
                qc.ch(ancilla, s)
        else:
            # Conjugate query U†
            for s in reversed(system):
                qc.ch(ancilla, s)

    qc.h(ancilla)
    qc.measure(ancilla, 0)

    return circuit_to_record(
        qc,
        name="qsvt",
        category="algebraic",
        description=DESCRIPTION,
        parameters={"n_qubits": n, "degree": degree,
                     "n_phases": degree + 1},
        pattern_description=PATTERN,
        difficulty="hard",
    )


registry.register(
    "qsvt",
    generate_circuit,
    category="algebraic",
    difficulty="hard",
    description="Quantum Singular Value Transformation — unifying framework",
)
