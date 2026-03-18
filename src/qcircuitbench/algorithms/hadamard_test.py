"""Hadamard test — estimating expectation values."""

from __future__ import annotations

from qiskit import QuantumCircuit

from qcircuitbench.registry import registry
from qcircuitbench.core import CircuitRecord
from qcircuitbench.utils import circuit_to_record

DESCRIPTION = """\
The Hadamard test estimates ⟨ψ|U|ψ⟩ (real or imaginary part) for any unitary U
using a single ancilla qubit. The ancilla controls whether U is applied to |ψ⟩.
Measuring the ancilla in the X-basis gives P(0) - P(1) = Re⟨ψ|U|ψ⟩.
Adding an S† gate before measurement gives the imaginary part.
It is a core primitive used in VQE, QSVT, and many variational algorithms.
"""

PATTERN = """\
Pattern: H(ancilla) → [optional S†(ancilla) for Im part] → controlled-U → H(ancilla)
→ Measure ancilla.
Key primitive: interference between |0⟩ and U|ψ⟩ paths extracts overlap.
"""


def generate_circuit(
    n_qubits: int = 4,
    imaginary: bool = False,
    **_kwargs,
) -> CircuitRecord:
    """Generate Hadamard test circuit with a simple controlled-Z unitary."""
    n = max(n_qubits, 1)
    total = n + 1  # n state qubits + 1 ancilla
    ancilla = 0

    qc = QuantumCircuit(total, 1)

    # Prepare state |ψ⟩ in superposition (for demonstration)
    for i in range(1, total):
        qc.h(i)

    # Hadamard test protocol
    qc.h(ancilla)
    if imaginary:
        qc.sdg(ancilla)

    # Controlled-U (example: controlled multi-Z = controlled phase)
    for i in range(1, total):
        qc.cz(ancilla, i)

    qc.h(ancilla)
    qc.measure(ancilla, 0)

    return circuit_to_record(
        qc,
        name="hadamard_test",
        category="quantum_information",
        description=DESCRIPTION,
        parameters={"n_qubits": n, "imaginary": imaginary},
        pattern_description=PATTERN,
        difficulty="easy",
    )


registry.register(
    "hadamard_test",
    generate_circuit,
    category="quantum_information",
    difficulty="easy",
    description="Hadamard test — estimate ⟨ψ|U|ψ⟩ via ancilla interference",
)
