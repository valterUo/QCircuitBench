"""Quantum Imaginary Time Evolution (QITE)."""

from __future__ import annotations

from qiskit import QuantumCircuit
from qiskit.circuit import Parameter

from qcircuitbench.registry import registry
from qcircuitbench.core import CircuitRecord
from qcircuitbench.utils import circuit_to_record

DESCRIPTION = """\
Quantum Imaginary Time Evolution (QITE) approximates the operator e^{-Hτ}
(imaginary-time evolution) to find the ground state of a Hamiltonian H. Unlike
real-time evolution, imaginary-time suppresses excited states exponentially,
driving any initial state toward the ground state. QITE maps the non-unitary
e^{-Hτ} to a sequence of unitary rotations determined by solving a linear
system at each step.
"""

PATTERN = """\
Pattern: repeat s steps { for each Hamiltonian term h_k:
    apply parameterized unitary exp(-i Σ_j θ_j^(k) P_j · Δτ) }.
θ values are computed classically at each step to approximate imaginary-time flow.
Key primitive: non-unitary evolution approximated by unitary rotations via
McLachlan's variational principle.
"""


def generate_circuit(
    n_qubits: int = 4,
    n_steps: int = 3,
    **_kwargs,
) -> CircuitRecord:
    """Generate QITE circuit for 1D Ising Hamiltonian."""
    n = max(n_qubits, 2)
    qc = QuantumCircuit(n, n)

    # Initial state: |+⟩⊗n
    qc.h(range(n))

    p_idx = 0
    for _step in range(n_steps):
        # ZZ interaction terms: approximate exp(-θ ZZ Δτ) via CNOT-RZ-CNOT
        for i in range(n - 1):
            qc.cx(i, i + 1)
            qc.rz(Parameter(f"θ_zz_{p_idx}"), i + 1)
            p_idx += 1
            qc.cx(i, i + 1)
        # X field terms: approximate via RX
        for i in range(n):
            qc.rx(Parameter(f"θ_x_{p_idx}"), i)
            p_idx += 1

    qc.measure(range(n), range(n))

    return circuit_to_record(
        qc,
        name="qite",
        category="simulation",
        description=DESCRIPTION,
        parameters={"n_qubits": n, "n_steps": n_steps,
                     "n_parameters": p_idx},
        pattern_description=PATTERN,
        difficulty="medium",
    )


registry.register(
    "qite",
    generate_circuit,
    category="simulation",
    difficulty="medium",
    description="QITE — quantum imaginary time evolution for ground states",
)
