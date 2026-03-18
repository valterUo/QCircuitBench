"""Variational Quantum Linear Solver (VQLS)."""

from __future__ import annotations

from math import pi
import numpy as np
from qiskit import QuantumCircuit

from qcircuitbench.registry import registry
from qcircuitbench.core import CircuitRecord
from qcircuitbench.utils import circuit_to_record

DESCRIPTION = """\
The Variational Quantum Linear Solver (VQLS) solves Ax = b using a
parameterised ansatz |x(θ)⟩ and a cost function that measures the
projection of A|x(θ)⟩ onto the subspace orthogonal to |b⟩. The cost
is evaluated with Hadamard-test sub-circuits and optimised classically.
Unlike HHL, VQLS is near-term-friendly with shallow circuits.
"""

PATTERN = """\
Pattern: Prepare |b⟩ on system register → apply parameterised ansatz V(θ) →
use Hadamard test with controlled-A_l unitaries on an ancilla to evaluate
cost C = 1 - |⟨b|A|x(θ)⟩|² / ⟨x(θ)|A†A|x(θ)⟩. Classical loop minimises C.
"""


def generate_circuit(
    n_qubits: int = 3,
    depth: int = 2,
    **_kwargs,
) -> CircuitRecord:
    """Generate a single cost-evaluation circuit of VQLS."""
    n_sys = max(n_qubits, 2)

    # 1 ancilla for Hadamard test + n_sys system qubits
    total = 1 + n_sys
    anc = 0
    sys_qubits = list(range(1, 1 + n_sys))

    qc = QuantumCircuit(total, 1)

    # Hadamard test ancilla
    qc.h(anc)

    # Prepare |b⟩  (simple: uniform superposition)
    qc.h(sys_qubits)

    # Parameterised ansatz V(θ) on system
    rng = np.random.default_rng(42)
    for d in range(depth):
        for q in sys_qubits:
            theta = float(rng.uniform(0, 2 * pi))
            qc.ry(theta, q)
        for i in range(len(sys_qubits) - 1):
            qc.cx(sys_qubits[i], sys_qubits[i + 1])

    # Controlled-A_l (simplified: A = sum of Pauli terms)
    # Term 1: controlled-Z on first qubit
    qc.cz(anc, sys_qubits[0])
    # Term 2: controlled-X on second qubit
    qc.cx(anc, sys_qubits[1])

    # Hadamard + measure ancilla
    qc.h(anc)
    qc.measure(anc, 0)

    return circuit_to_record(
        qc,
        name="vqls",
        category="variational",
        description=DESCRIPTION,
        parameters={"n_qubits": n_sys, "depth": depth,
                     "total_qubits": total},
        pattern_description=PATTERN,
        difficulty="medium",
    )


registry.register(
    "vqls",
    generate_circuit,
    category="variational",
    difficulty="medium",
    description="Variational Quantum Linear Solver — near-term Ax=b",
)
