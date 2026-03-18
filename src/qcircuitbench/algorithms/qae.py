"""Quantum Amplitude Estimation (QAE)."""

from __future__ import annotations

from math import pi
from qiskit import QuantumCircuit

from qcircuitbench.registry import registry
from qcircuitbench.core import CircuitRecord
from qcircuitbench.utils import circuit_to_record

DESCRIPTION = """\
Quantum Amplitude Estimation (QAE) estimates the probability a of a quantum
state preparation oracle marking a 'good' state. It combines Grover-like
amplitude amplification with phase estimation to extract a = sin²(θ) with
quadratic speedup over classical sampling.
"""

PATTERN = """\
Pattern: H⊗m (counting) → controlled-Q^{2^k} on state register → inverse QFT → Measure.
Q is the Grover iterate (oracle + diffusion). Like QPE but applied to the
Grover operator to read off the angle θ.
"""


def _grover_iterate(n: int) -> QuantumCircuit:
    """Simple Grover iterate: oracle marks |0⟩, then diffusion."""
    qc = QuantumCircuit(n, name="Q")
    # Oracle: phase-flip |0...0⟩
    qc.x(range(n))
    qc.h(n - 1)
    qc.mcx(list(range(n - 1)), n - 1)
    qc.h(n - 1)
    qc.x(range(n))
    # Diffusion
    qc.h(range(n))
    qc.x(range(n))
    qc.h(n - 1)
    qc.mcx(list(range(n - 1)), n - 1)
    qc.h(n - 1)
    qc.x(range(n))
    qc.h(range(n))
    return qc


def _inverse_qft(qc: QuantumCircuit, qubits: list[int]) -> None:
    n = len(qubits)
    for i in range(n // 2):
        qc.swap(qubits[i], qubits[n - 1 - i])
    for target in range(n):
        qc.h(qubits[target])
        for control in range(target):
            qc.cp(-pi / (2 ** (target - control)), qubits[control], qubits[target])


def generate_circuit(
    n_qubits: int = 4,
    n_counting: int | None = None,
    **_kwargs,
) -> CircuitRecord:
    """Generate QAE circuit."""
    n_state = max(n_qubits, 2)
    m = n_counting or n_state
    total = m + n_state

    qc = QuantumCircuit(total, m)

    # Initialize state register in superposition
    qc.h(range(m, total))

    # Hadamard on counting register
    qc.h(range(m))

    # Controlled Grover iterates
    grover_qc = _grover_iterate(n_state)
    grover_gate = grover_qc.to_gate().control(1)
    for k in range(m):
        for _ in range(2**k):
            qc.append(grover_gate, [k] + list(range(m, total)))

    # Inverse QFT on counting register
    _inverse_qft(qc, list(range(m)))

    qc.measure(range(m), range(m))

    return circuit_to_record(
        qc,
        name="qae",
        category="variational",
        description=DESCRIPTION,
        parameters={"n_qubits": n_state, "n_counting": m},
        pattern_description=PATTERN,
        difficulty="easy",
    )


registry.register(
    "qae",
    generate_circuit,
    category="variational",
    difficulty="easy",
    description="Quantum Amplitude Estimation",
)
