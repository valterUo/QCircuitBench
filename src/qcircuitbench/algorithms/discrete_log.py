"""Discrete logarithm algorithm."""

from __future__ import annotations

from math import pi
from qiskit import QuantumCircuit

from qcircuitbench.registry import registry
from qcircuitbench.core import CircuitRecord
from qcircuitbench.utils import circuit_to_record

DESCRIPTION = """\
The quantum discrete logarithm algorithm finds s such that b = a^s mod N in
polynomial time, generalizing Shor's period-finding approach. It uses two
QPE registers: one to extract the order r of a, and one to extract the
discrete log s. The circuit applies controlled modular exponentiations for
both a and b, followed by inverse QFTs on both registers.
"""

PATTERN = """\
Pattern: H⊗t (register 1) · H⊗t (register 2) → controlled-a^{2^k}(reg 1)
→ controlled-b^{2^k}(reg 2) → inverse QFT(reg 1) · inverse QFT(reg 2)
→ Measure both.
Key primitive: double-register QPE extracts both order and discrete log.
"""


def _iqft(qc: QuantumCircuit, qubits: list[int]) -> None:
    n = len(qubits)
    for i in range(n // 2):
        qc.swap(qubits[i], qubits[n - 1 - i])
    for j in range(n):
        qc.h(qubits[j])
        for k in range(j):
            qc.cp(-pi / (2 ** (j - k)), qubits[k], qubits[j])


def generate_circuit(
    n_qubits: int = 4,
    **_kwargs,
) -> CircuitRecord:
    """Generate discrete-log circuit (simplified demonstration)."""
    t = max(n_qubits, 2)  # bits per QPE register
    n_work = max(t // 2, 2)  # work register
    total = 2 * t + n_work

    reg1 = list(range(t))
    reg2 = list(range(t, 2 * t))
    work = list(range(2 * t, total))

    qc = QuantumCircuit(total, 2 * t)

    # Initialize work register
    qc.x(work[0])

    # Hadamard on both QPE registers
    qc.h(reg1)
    qc.h(reg2)

    # Controlled modular exponentiations (simplified as controlled phases)
    for k in range(t):
        angle_a = 2 * pi * (2**k) / (2**t)
        qc.cp(angle_a, reg1[k], work[0])
    for k in range(t):
        angle_b = 2 * pi * (2**k) / (2**t)
        qc.cp(angle_b, reg2[k], work[0])

    # Inverse QFT on both registers
    _iqft(qc, reg1)
    _iqft(qc, reg2)

    qc.measure(reg1 + reg2, list(range(2 * t)))

    return circuit_to_record(
        qc,
        name="discrete_log",
        category="algebraic",
        description=DESCRIPTION,
        parameters={"n_qubits": t, "total_qubits": total},
        pattern_description=PATTERN,
        difficulty="hard",
    )


registry.register(
    "discrete_log",
    generate_circuit,
    category="algebraic",
    difficulty="hard",
    description="Discrete logarithm — quantum algorithm for b = a^s mod N",
)
