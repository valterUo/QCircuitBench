"""Simple Quantum Neural Network (parameterized classifier)."""

from __future__ import annotations

from qiskit import QuantumCircuit
from qiskit.circuit import Parameter

from qcircuitbench.registry import registry
from qcircuitbench.core import CircuitRecord
from qcircuitbench.utils import circuit_to_record

DESCRIPTION = """\
A quantum neural network (QNN) circuit consists of data-encoding layers
interleaved with trainable parameterized layers. This simple classifier uses
angle encoding for inputs and RY/RZ + CNOT layers for trainable weights, forming
a hardware-efficient variational classifier.
"""

PATTERN = """\
Pattern: repeat L layers { RY(x_i) encoding · RY(θ)·RZ(φ) trainable · CNOT entangling }.
Measure readout qubit(s) to obtain class prediction.
Key primitive: interleaved data re-uploading with trainable rotations.
"""


def generate_circuit(
    n_qubits: int = 4,
    n_layers: int = 2,
    **_kwargs,
) -> CircuitRecord:
    """Generate a simple QNN classifier circuit."""
    n = max(n_qubits, 2)
    qc = QuantumCircuit(n, 1)

    p_idx = 0
    for layer in range(n_layers):
        # Data encoding layer (parameterized inputs)
        for qubit in range(n):
            qc.ry(Parameter(f"x_{layer}_{qubit}"), qubit)
        # Trainable layer
        for qubit in range(n):
            qc.ry(Parameter(f"w_{p_idx}"), qubit)
            p_idx += 1
            qc.rz(Parameter(f"w_{p_idx}"), qubit)
            p_idx += 1
        # Entangling layer
        for qubit in range(n - 1):
            qc.cx(qubit, qubit + 1)

    # Measure readout qubit
    qc.measure(0, 0)

    return circuit_to_record(
        qc,
        name="qnn",
        category="machine_learning",
        description=DESCRIPTION,
        parameters={"n_qubits": n, "n_layers": n_layers,
                     "n_trainable_params": p_idx},
        pattern_description=PATTERN,
        difficulty="medium",
    )


registry.register(
    "qnn",
    generate_circuit,
    category="machine_learning",
    difficulty="medium",
    description="Quantum Neural Network — parameterized classifier",
)
