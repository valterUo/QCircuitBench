"""Grover's search algorithm."""

from __future__ import annotations

import math
from qiskit import QuantumCircuit

from qcircuitbench.registry import registry
from qcircuitbench.core import CircuitRecord
from qcircuitbench.utils import circuit_to_record

DESCRIPTION = """\
Grover's algorithm performs unstructured search over N=2^n items in O(√N) queries.
Given an oracle that marks a target state with a phase flip, the algorithm
repeatedly applies the oracle followed by a diffusion operator to amplify the
amplitude of the marked state. After ~π/4·√N iterations the target is measured
with high probability.
"""

PATTERN = """\
Pattern: [H⊗n] → repeat ⌊π/4·√N⌋ times { Oracle · Diffusion } → Measure.
The diffusion operator is H⊗n · X⊗n · MCZ · X⊗n · H⊗n.
Key primitive: amplitude amplification via oracle + reflection about mean.
"""


def _diffusion_operator(n: int) -> QuantumCircuit:
    """Diffusion (inversion about the mean) on *n* qubits."""
    qc = QuantumCircuit(n, name="Diffuser")
    qc.h(range(n))
    qc.x(range(n))
    qc.h(n - 1)
    qc.mcx(list(range(n - 1)), n - 1)
    qc.h(n - 1)
    qc.x(range(n))
    qc.h(range(n))
    return qc


def _default_oracle(n: int, marked: int = 0) -> QuantumCircuit:
    """Phase-flip oracle marking state |marked⟩ on *n* qubits."""
    qc = QuantumCircuit(n, name="Oracle")
    # Flip bits so that |marked⟩ maps to |11…1⟩
    for i in range(n):
        if not (marked >> i & 1):
            qc.x(i)
    qc.h(n - 1)
    qc.mcx(list(range(n - 1)), n - 1)
    qc.h(n - 1)
    for i in range(n):
        if not (marked >> i & 1):
            qc.x(i)
    return qc


def generate_circuit(
    n_qubits: int = 4,
    marked_state: int = 0,
    **_kwargs,
) -> CircuitRecord:
    """Generate a Grover circuit searching for *marked_state*."""
    n = max(n_qubits, 2)
    num_iterations = max(1, math.floor(math.pi / 4 * math.sqrt(2**n)))

    oracle = _default_oracle(n, marked_state)
    diffuser = _diffusion_operator(n)

    qc = QuantumCircuit(n, n)
    qc.h(range(n))
    for _ in range(num_iterations):
        qc.compose(oracle, inplace=True)
        qc.compose(diffuser, inplace=True)
    qc.measure(range(n), range(n))

    return circuit_to_record(
        qc,
        name="grover",
        category="oracular",
        description=DESCRIPTION,
        parameters={"n_qubits": n, "marked_state": marked_state,
                     "iterations": num_iterations},
        pattern_description=PATTERN,
        difficulty="medium",
    )


registry.register(
    "grover",
    generate_circuit,
    category="oracular",
    difficulty="medium",
    description="Grover's unstructured search algorithm",
)
