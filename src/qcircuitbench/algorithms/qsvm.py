"""Quantum Support Vector Machine — kernel evaluation."""

from __future__ import annotations

from math import pi
from qiskit import QuantumCircuit

from qcircuitbench.registry import registry
from qcircuitbench.core import CircuitRecord
from qcircuitbench.utils import circuit_to_record

DESCRIPTION = """\
Quantum SVM (QSVM) maps classical data into a high-dimensional Hilbert space
via a quantum feature map and evaluates the kernel K(x, x') = |⟨φ(x')|φ(x)⟩|²
using the compute-uncompute (swap-test-free) method. The ZZ feature map encodes
feature vectors with entangling ZZ rotations, enabling kernel-based
classification potentially intractable classically.
"""

PATTERN = """\
Pattern: Feature map U(x) → adjoint U†(x') → measurement in computational basis.
P(0^n) = |⟨φ(x')|φ(x)⟩|² gives the kernel value.
Variant: ZZ feature map with depth=2 data re-uploading.
"""


def _zz_feature_map(qc: QuantumCircuit, qubits: list[int],
                    features: list[float], reps: int = 2) -> None:
    """Apply ZZ feature map."""
    n = len(qubits)
    for _ in range(reps):
        for i, q in enumerate(qubits):
            qc.h(q)
            qc.rz(2.0 * features[i % len(features)], q)
        for i in range(n - 1):
            qc.cx(qubits[i], qubits[i + 1])
            val = 2.0 * (pi - features[i % len(features)]) * \
                        (pi - features[(i + 1) % len(features)])
            qc.rz(val, qubits[i + 1])
            qc.cx(qubits[i], qubits[i + 1])


def _zz_feature_map_inverse(qc: QuantumCircuit, qubits: list[int],
                             features: list[float], reps: int = 2) -> None:
    """Apply adjoint (inverse) of ZZ feature map."""
    n = len(qubits)
    for _ in range(reps):
        for i in range(n - 2, -1, -1):
            val = 2.0 * (pi - features[i % len(features)]) * \
                        (pi - features[(i + 1) % len(features)])
            qc.cx(qubits[i], qubits[i + 1])
            qc.rz(-val, qubits[i + 1])
            qc.cx(qubits[i], qubits[i + 1])
        for i in range(n - 1, -1, -1):
            q = qubits[i]
            qc.rz(-2.0 * features[i % len(features)], q)
            qc.h(q)


def generate_circuit(
    n_qubits: int = 4,
    features_x: list[float] | None = None,
    features_xp: list[float] | None = None,
    reps: int = 2,
    **_kwargs,
) -> CircuitRecord:
    """Generate QSVM kernel evaluation circuit."""
    n = max(n_qubits, 2)
    if features_x is None:
        features_x = [0.3 * (i + 1) for i in range(n)]
    if features_xp is None:
        features_xp = [0.5 * (i + 1) for i in range(n)]

    qc = QuantumCircuit(n, n)
    qubits = list(range(n))

    # Encode x
    _zz_feature_map(qc, qubits, features_x, reps=reps)

    qc.barrier()

    # Adjoint encode x'  (inverse of feature map for x')
    _zz_feature_map_inverse(qc, qubits, features_xp, reps=reps)

    qc.measure(qubits, list(range(n)))

    return circuit_to_record(
        qc,
        name="qsvm_kernel",
        category="machine_learning",
        description=DESCRIPTION,
        parameters={"n_qubits": n, "reps": reps,
                     "features_x": features_x, "features_xp": features_xp},
        pattern_description=PATTERN,
        difficulty="medium",
    )


registry.register(
    "qsvm_kernel",
    generate_circuit,
    category="machine_learning",
    difficulty="medium",
    description="Quantum SVM kernel evaluation via ZZ feature map",
)
