"""Quantum ripple-carry adder."""

from __future__ import annotations

from qiskit import QuantumCircuit

from qcircuitbench.registry import registry
from qcircuitbench.core import CircuitRecord
from qcircuitbench.utils import circuit_to_record

DESCRIPTION = """\
The quantum ripple-carry adder (CDKM adder, Cuccaro et al. 2004) adds two
n-bit integers stored in quantum registers, using one ancilla qubit for carry
propagation. It uses O(n) Toffoli and CNOT gates. The circuit computes
|a⟩|b⟩ → |a⟩|a+b⟩ in-place, which is a key subroutine in Shor's algorithm
and other quantum arithmetic.
"""

PATTERN = """\
Pattern: Carry propagation (Toffoli + CNOT cascade forward) → sum computation
(CNOT at MSB) → uncarry propagation (reverse cascade).
Key primitive: reversible carry-ripple with Toffoli gates.
"""


def _majority(qc: QuantumCircuit, a: int, b: int, c: int) -> None:
    """MAJ gate: majority of three bits."""
    qc.cx(c, b)
    qc.cx(c, a)
    qc.ccx(a, b, c)


def _unmajority_add(qc: QuantumCircuit, a: int, b: int, c: int) -> None:
    """UMA gate: unmajority and add."""
    qc.ccx(a, b, c)
    qc.cx(c, a)
    qc.cx(a, b)


def generate_circuit(
    n_qubits: int = 4,
    **_kwargs,
) -> CircuitRecord:
    """Generate ripple-carry adder for n-bit addition."""
    n = max(n_qubits, 2)
    # Register layout: a[0..n-1], b[0..n-1], carry_in, carry_out = 2n+1 qubits
    # Simplified: a[0..n-1], b[0..n], with b[n] as overflow
    total = 2 * n + 1
    qc = QuantumCircuit(total)

    # a qubits: 0..n-1, b qubits: n..2n, carry: 2n
    carry = 2 * n
    a = list(range(n))
    b = list(range(n, 2 * n + 1))

    # Forward carry propagation
    for i in range(n):
        _majority(qc, carry if i == 0 else b[i - 1], a[i], b[i])

    # MSB carry out
    qc.cx(b[n - 1], b[n])

    # Reverse: unmajority and add
    for i in range(n - 1, -1, -1):
        _unmajority_add(qc, carry if i == 0 else b[i - 1], a[i], b[i])

    return circuit_to_record(
        qc,
        name="quantum_adder",
        category="arithmetic",
        description=DESCRIPTION,
        parameters={"n_qubits": n, "total_qubits": total},
        pattern_description=PATTERN,
        difficulty="medium",
    )


registry.register(
    "quantum_adder",
    generate_circuit,
    category="arithmetic",
    difficulty="medium",
    description="Quantum ripple-carry adder — reversible n-bit addition",
)
