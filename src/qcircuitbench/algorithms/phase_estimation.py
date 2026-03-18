"""Quantum Phase Estimation (QPE)."""

from __future__ import annotations

from math import pi
from qiskit import QuantumCircuit

from qcircuitbench.registry import registry
from qcircuitbench.core import CircuitRecord
from qcircuitbench.utils import circuit_to_record

DESCRIPTION = """\
Quantum Phase Estimation estimates the eigenvalue phase θ of a unitary U
such that U|ψ⟩ = e^{2πiθ}|ψ⟩. It uses t counting qubits for t bits of
precision and one eigenstate register. Controlled-U^(2^k) gates transfer phase
information to the counting register, and an inverse QFT extracts the binary
representation of θ.
"""

PATTERN = """\
Pattern: H⊗t (counting) → controlled-U^{2^k} for k=0..t-1 → inverse QFT → Measure.
Key primitive: controlled powers of U accumulate phase into counting qubits;
inverse QFT converts phase to a computational-basis readout.
"""


def _inverse_qft(qc: QuantumCircuit, qubits: list[int]) -> None:
    """Append inverse QFT on the given qubits."""
    n = len(qubits)
    for i in range(n // 2):
        qc.swap(qubits[i], qubits[n - 1 - i])
    for target in range(n):
        qc.h(qubits[target])
        for control in range(target):
            angle = -pi / (2 ** (target - control))
            qc.cp(angle, qubits[control], qubits[target])


def generate_circuit(
    n_qubits: int = 4,
    phase: float = 1 / 3,
    **_kwargs,
) -> CircuitRecord:
    """Generate QPE circuit estimating a phase with *n_qubits* precision bits."""
    t = max(n_qubits, 2)  # counting qubits
    total = t + 1  # +1 for eigenstate qubit

    qc = QuantumCircuit(total, t)

    # Prepare eigenstate |1⟩
    qc.x(t)

    # Hadamard on counting qubits
    qc.h(range(t))

    # Controlled-U^(2^k): U = P(2πθ)
    for k in range(t):
        angle = 2 * pi * phase * (2**k)
        qc.cp(angle, k, t)

    # Inverse QFT on counting qubits
    _inverse_qft(qc, list(range(t)))

    qc.measure(range(t), range(t))

    return circuit_to_record(
        qc,
        name="phase_estimation",
        category="algebraic",
        description=DESCRIPTION,
        parameters={"n_qubits": t, "phase": phase},
        pattern_description=PATTERN,
        difficulty="medium",
    )


registry.register(
    "phase_estimation",
    generate_circuit,
    category="algebraic",
    difficulty="medium",
    description="Quantum Phase Estimation — eigenvalue extraction",
)
