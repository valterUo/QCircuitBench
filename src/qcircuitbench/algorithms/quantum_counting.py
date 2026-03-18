"""Quantum Counting (Grover + QPE)."""

from __future__ import annotations

from math import pi
from qiskit import QuantumCircuit

from qcircuitbench.registry import registry
from qcircuitbench.core import CircuitRecord
from qcircuitbench.utils import circuit_to_record

DESCRIPTION = """\
Quantum Counting combines Grover's search operator with Quantum Phase Estimation
to *count* the number of solutions M to a search problem among N = 2^n items,
without needing to find them. QPE applied to the Grover iterate G extracts the
angle θ where sin²(θ) = M/N, yielding M with precision dependent on the number
of counting qubits t. Complexity: O(√N) vs O(N) classically.
"""

PATTERN = """\
Pattern: H⊗t (counting) · H⊗n (search) → controlled-G^{2^k} for k=0..t-1
→ inverse QFT on counting → Measure.
G = Oracle · Diffusion is the standard Grover iterate.
Key primitive: QPE applied to the Grover operator to read off the solution count.
"""


def _grover_iterate(n: int) -> QuantumCircuit:
    """Grover iterate: oracle (marks |0⟩) + diffusion."""
    qc = QuantumCircuit(n, name="G")
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
    for j in range(n):
        qc.h(qubits[j])
        for k in range(j):
            qc.cp(-pi / (2 ** (j - k)), qubits[k], qubits[j])


def generate_circuit(
    n_qubits: int = 4,
    n_counting: int | None = None,
    **_kwargs,
) -> CircuitRecord:
    """Generate Quantum Counting circuit."""
    n = max(n_qubits, 2)
    t = n_counting or n
    total = t + n

    qc = QuantumCircuit(total, t)

    # Superposition on search register
    qc.h(range(t, total))
    # Hadamard on counting register
    qc.h(range(t))

    # Controlled Grover iterates
    grover_gate = _grover_iterate(n).to_gate().control(1)
    for k in range(t):
        for _ in range(2**k):
            qc.append(grover_gate, [k] + list(range(t, total)))

    # Inverse QFT on counting register
    _inverse_qft(qc, list(range(t)))

    qc.measure(range(t), range(t))

    return circuit_to_record(
        qc,
        name="quantum_counting",
        category="oracular",
        description=DESCRIPTION,
        parameters={"n_qubits": n, "n_counting": t},
        pattern_description=PATTERN,
        difficulty="medium",
    )


registry.register(
    "quantum_counting",
    generate_circuit,
    category="oracular",
    difficulty="medium",
    description="Quantum Counting — estimate number of search solutions",
)
