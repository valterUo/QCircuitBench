"""HHL algorithm for linear systems."""

from __future__ import annotations

from math import pi
from qiskit import QuantumCircuit

from qcircuitbench.registry import registry
from qcircuitbench.core import CircuitRecord
from qcircuitbench.utils import circuit_to_record

DESCRIPTION = """\
The Harrow-Hassidim-Lloyd (HHL) algorithm solves the linear system Ax = b for
a sparse Hermitian matrix A in time poly(log N, κ), where N is the matrix
dimension and κ the condition number — exponentially faster than classical
methods. It uses QPE to extract eigenvalues of A, controlled rotations to encode
the inverse eigenvalues into an ancilla, and inverse QPE to uncompute.
"""

PATTERN = """\
Pattern: Encode |b⟩ → QPE(e^{iAt}) on clock register → controlled RY(arcsin(C/λ_j))
on ancilla → inverse QPE → measure ancilla and post-select on |1⟩.
Key primitive: eigenvalue inversion via controlled rotation conditioned on QPE output.
"""


def _qft(qc: QuantumCircuit, qubits: list[int]) -> None:
    n = len(qubits)
    for i in range(n - 1, -1, -1):
        qc.h(qubits[i])
        for j in range(i):
            qc.cp(pi / (2 ** (i - j)), qubits[j], qubits[i])


def _iqft(qc: QuantumCircuit, qubits: list[int]) -> None:
    n = len(qubits)
    for i in range(n // 2):
        qc.swap(qubits[i], qubits[n - 1 - i])
    for j in range(n):
        qc.h(qubits[j])
        for k in range(j):
            qc.cp(-pi / (2 ** (j - k)), qubits[k], qubits[j])


def generate_circuit(
    n_qubits: int = 4,
    **_kwargs,
) -> CircuitRecord:
    """Generate simplified HHL circuit (2x2 system demonstration)."""
    n_clock = max(n_qubits, 2)
    n_b = 1       # single qubit for |b⟩
    n_anc = 1     # ancilla for eigenvalue inversion
    total = n_clock + n_b + n_anc

    clock = list(range(n_clock))
    b_qubit = n_clock
    ancilla = n_clock + 1

    qc = QuantumCircuit(total, 1)

    # Prepare |b⟩ (simple example: |1⟩)
    qc.x(b_qubit)

    # QPE: Hadamard on clock
    qc.h(clock)

    # Controlled e^{iAt} rotations (simplified: controlled phase)
    for k in range(n_clock):
        angle = 2 * pi / (2 ** (n_clock - k))
        qc.cp(angle, clock[k], b_qubit)

    # Inverse QFT on clock
    _iqft(qc, clock)

    # Eigenvalue inversion: controlled rotations on ancilla
    for k in range(n_clock):
        angle = pi / (2 ** (k + 1))
        qc.cry(angle, clock[k], ancilla)

    # Uncompute QPE: QFT then undo controlled phases
    _qft(qc, clock)
    for k in range(n_clock - 1, -1, -1):
        angle = -2 * pi / (2 ** (n_clock - k))
        qc.cp(angle, clock[k], b_qubit)
    qc.h(clock)

    # Measure ancilla (post-select on |1⟩)
    qc.measure(ancilla, 0)

    return circuit_to_record(
        qc,
        name="hhl",
        category="algebraic",
        description=DESCRIPTION,
        parameters={"n_qubits": n_clock, "n_clock": n_clock,
                     "total_qubits": total},
        pattern_description=PATTERN,
        difficulty="hard",
    )


registry.register(
    "hhl",
    generate_circuit,
    category="algebraic",
    difficulty="hard",
    description="HHL algorithm — quantum linear systems solver",
)
