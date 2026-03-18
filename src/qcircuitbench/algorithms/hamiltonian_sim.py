"""Trotterized Hamiltonian simulation (1D Ising model)."""

from __future__ import annotations

from math import pi
from qiskit import QuantumCircuit

from qcircuitbench.registry import registry
from qcircuitbench.core import CircuitRecord
from qcircuitbench.utils import circuit_to_record

DESCRIPTION = """\
Hamiltonian simulation approximates the time evolution e^{-iHt} of a quantum
system. For the 1D transverse-field Ising model H = -J Σ Z_i Z_{i+1} - h Σ X_i,
Trotterization decomposes the evolution into small steps, each applying ZZ
interactions (via CNOT-RZ-CNOT) and single-qubit X rotations. Higher Trotter
order reduces approximation error.
"""

PATTERN = """\
Pattern: repeat r Trotter steps {
    for each pair (i,i+1): CNOT(i,i+1) · RZ(2Jt/r) · CNOT(i,i+1)    [ZZ term]
    for each qubit i: RX(2ht/r)                                        [X term]
}
Key primitive: Suzuki-Trotter product formula for operator splitting.
"""


def generate_circuit(
    n_qubits: int = 4,
    n_steps: int = 3,
    time: float = 1.0,
    j_coupling: float = 1.0,
    h_field: float = 0.5,
    **_kwargs,
) -> CircuitRecord:
    """Generate Trotterized 1D Ising Hamiltonian simulation."""
    n = max(n_qubits, 2)
    dt = time / n_steps

    qc = QuantumCircuit(n)

    for _step in range(n_steps):
        # ZZ interaction terms
        for i in range(n - 1):
            qc.cx(i, i + 1)
            qc.rz(2 * j_coupling * dt, i + 1)
            qc.cx(i, i + 1)
        # Transverse field terms
        for i in range(n):
            qc.rx(2 * h_field * dt, i)

    return circuit_to_record(
        qc,
        name="hamiltonian_sim",
        category="simulation",
        description=DESCRIPTION,
        parameters={"n_qubits": n, "n_steps": n_steps, "time": time,
                     "j_coupling": j_coupling, "h_field": h_field},
        pattern_description=PATTERN,
        difficulty="medium",
    )


registry.register(
    "hamiltonian_sim",
    generate_circuit,
    category="simulation",
    difficulty="medium",
    description="Trotterized Hamiltonian simulation — 1D Ising model",
)
