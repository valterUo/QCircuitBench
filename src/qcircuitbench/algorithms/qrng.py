"""Quantum Random Number Generator."""

from __future__ import annotations

from qiskit import QuantumCircuit

from qcircuitbench.registry import registry
from qcircuitbench.core import CircuitRecord
from qcircuitbench.utils import circuit_to_record

DESCRIPTION = """\
A quantum random number generator (QRNG) produces true random bits by exploiting
quantum superposition. Each qubit is placed in an equal superposition via Hadamard
and measured, yielding 0 or 1 with exactly 50% probability each. Unlike
pseudorandom number generators, the output is guaranteed random by quantum
mechanics (Born rule).
"""

PATTERN = """\
Pattern: H⊗n → Measure all.
Simplest possible quantum circuit — each qubit independently produces one random bit.
"""


def generate_circuit(
    n_qubits: int = 4,
    **_kwargs,
) -> CircuitRecord:
    """Generate QRNG circuit producing n random bits."""
    n = max(n_qubits, 1)
    qc = QuantumCircuit(n, n)
    qc.h(range(n))
    qc.measure(range(n), range(n))

    return circuit_to_record(
        qc,
        name="qrng",
        category="quantum_information",
        description=DESCRIPTION,
        parameters={"n_qubits": n},
        pattern_description=PATTERN,
        difficulty="easy",
    )


registry.register(
    "qrng",
    generate_circuit,
    category="quantum_information",
    difficulty="easy",
    description="Quantum random number generator",
)
