"""Swap test circuit."""

from __future__ import annotations

from qiskit import QuantumCircuit

from qcircuitbench.registry import registry
from qcircuitbench.core import CircuitRecord
from qcircuitbench.utils import circuit_to_record

DESCRIPTION = """\
The swap test measures the overlap |⟨ψ|φ⟩|² between two quantum states without
directly computing the inner product. It uses an ancilla qubit and controlled-SWAP
gates. If the ancilla is measured as |0⟩, the probability relates to the overlap:
P(0) = (1 + |⟨ψ|φ⟩|²)/2. The swap test is used in quantum fingerprinting, state
comparison, and kernel-based quantum ML.
"""

PATTERN = """\
Pattern: H(ancilla) → CSWAP(ancilla, ψ_i, φ_i) for i=0..n-1 → H(ancilla) → Measure.
Key primitive: Fredkin (CSWAP) gates controlled by ancilla qubit.
"""


def generate_circuit(
    n_qubits: int = 4,
    **_kwargs,
) -> CircuitRecord:
    """Generate swap test circuit comparing two n-qubit states."""
    n = max(n_qubits, 2)
    total = 2 * n + 1  # n + n + 1 ancilla
    ancilla = 2 * n

    qc = QuantumCircuit(total, 1)

    # Prepare test states: |ψ⟩ = H|0⟩⊗n and |φ⟩ = |0⟩⊗n (for demonstration)
    for i in range(n):
        qc.h(i)

    # Swap test
    qc.h(ancilla)
    for i in range(n):
        qc.cswap(ancilla, i, i + n)
    qc.h(ancilla)
    qc.measure(ancilla, 0)

    return circuit_to_record(
        qc,
        name="swap_test",
        category="quantum_information",
        description=DESCRIPTION,
        parameters={"n_qubits": n, "total_qubits": total},
        pattern_description=PATTERN,
        difficulty="easy",
    )


registry.register(
    "swap_test",
    generate_circuit,
    category="quantum_information",
    difficulty="easy",
    description="Swap test — state overlap estimation",
)
