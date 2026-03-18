"""Quantum Autoencoder for data compression."""

from __future__ import annotations

from math import pi
import numpy as np
from qiskit import QuantumCircuit

from qcircuitbench.registry import registry
from qcircuitbench.core import CircuitRecord
from qcircuitbench.utils import circuit_to_record

DESCRIPTION = """\
A Quantum Autoencoder compresses an n-qubit quantum state into fewer qubits
by training a parameterised encoder U(θ) to map information into a latent
register while pushing the "trash" qubits to |0⟩. After training, measuring
the trash qubits in |0⟩ confirms successful compression. The decoder is
U†(θ). This enables efficient quantum data compression and denoising.
"""

PATTERN = """\
Pattern: Input state on n qubits → parameterised encoder U(θ) acting on all
qubits → measure trash qubits (should yield |0⟩) → latent qubits hold
compressed representation. Cost = 1 − Pr(trash = 0^k).
"""


def generate_circuit(
    n_qubits: int = 4,
    n_latent: int | None = None,
    depth: int = 2,
    **_kwargs,
) -> CircuitRecord:
    """Generate quantum autoencoder circuit."""
    n = max(n_qubits, 3)
    if n_latent is None:
        n_latent = max(1, n // 2)
    n_trash = n - n_latent

    qc = QuantumCircuit(n, n_trash)

    latent = list(range(n_latent))
    trash = list(range(n_latent, n))

    # Prepare an example input state (entangled GHZ-like)
    qc.h(0)
    for i in range(1, n):
        qc.cx(0, i)
    qc.barrier()

    # Parameterised encoder
    rng = np.random.default_rng(42)
    for d in range(depth):
        for q in range(n):
            theta = float(rng.uniform(0, 2 * pi))
            qc.ry(theta, q)
        for q in range(n - 1):
            qc.cx(q, q + 1)
        # Also entangle last → first for ring topology
        if n > 2:
            qc.cx(n - 1, 0)

    qc.barrier()

    # Measure trash qubits (should be |0⟩ after successful training)
    qc.measure(trash, list(range(n_trash)))

    return circuit_to_record(
        qc,
        name="quantum_autoencoder",
        category="machine_learning",
        description=DESCRIPTION,
        parameters={"n_qubits": n, "n_latent": n_latent,
                     "n_trash": n_trash, "depth": depth},
        pattern_description=PATTERN,
        difficulty="medium",
    )


registry.register(
    "quantum_autoencoder",
    generate_circuit,
    category="machine_learning",
    difficulty="medium",
    description="Quantum Autoencoder — parameterised data compression",
)
