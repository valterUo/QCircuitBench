"""VQE with EfficientSU2 ansatz."""

from __future__ import annotations

from qiskit import QuantumCircuit
from qiskit.circuit import Parameter

from qcircuitbench.registry import registry
from qcircuitbench.core import CircuitRecord
from qcircuitbench.utils import circuit_to_record

DESCRIPTION = """\
The Variational Quantum Eigensolver (VQE) estimates the ground-state energy of
a Hamiltonian using a parameterized ansatz circuit. The EfficientSU2 ansatz
consists of layers of single-qubit RY and RZ rotations followed by a CNOT
entangling ladder. Parameters are optimized classically to minimize ⟨H⟩.
"""

PATTERN = """\
Pattern: repeat d layers { RY(θ)⊗n · RZ(φ)⊗n · CNOT-ladder } → Measure.
Key primitive: hardware-efficient ansatz with alternating rotation/entangling layers.
"""


def generate_circuit(
    n_qubits: int = 4,
    n_layers: int = 2,
    **_kwargs,
) -> CircuitRecord:
    """Generate VQE EfficientSU2 ansatz."""
    n = max(n_qubits, 2)
    qc = QuantumCircuit(n, n)

    param_idx = 0
    for layer in range(n_layers):
        # Rotation layer
        for qubit in range(n):
            qc.ry(Parameter(f"θ_{param_idx}"), qubit)
            param_idx += 1
            qc.rz(Parameter(f"θ_{param_idx}"), qubit)
            param_idx += 1
        # Entangling layer (linear connectivity)
        for qubit in range(n - 1):
            qc.cx(qubit, qubit + 1)

    # Final rotation layer
    for qubit in range(n):
        qc.ry(Parameter(f"θ_{param_idx}"), qubit)
        param_idx += 1
        qc.rz(Parameter(f"θ_{param_idx}"), qubit)
        param_idx += 1

    qc.measure(range(n), range(n))

    return circuit_to_record(
        qc,
        name="vqe",
        category="variational",
        description=DESCRIPTION,
        parameters={"n_qubits": n, "n_layers": n_layers,
                     "n_parameters": param_idx},
        pattern_description=PATTERN,
        difficulty="hard",
    )


registry.register(
    "vqe",
    generate_circuit,
    category="variational",
    difficulty="hard",
    description="VQE with EfficientSU2 ansatz — variational eigensolver",
)
