"""Shor's factoring algorithm (simplified QPE-based circuit)."""

from __future__ import annotations

import math
from math import pi
from qiskit import QuantumCircuit

from qcircuitbench.registry import registry
from qcircuitbench.core import CircuitRecord
from qcircuitbench.utils import circuit_to_record

DESCRIPTION = """\
Shor's algorithm factors an integer N in polynomial time using quantum period
finding. It picks a random base a, constructs a unitary U|y⟩ = |ay mod N⟩, and
uses QPE to find the period r of a^r ≡ 1 (mod N). The GCD of a^(r/2)±1 and N
then yields factors. This implementation builds the modular exponentiation as
controlled swap gates for small instances.
"""

PATTERN = """\
Pattern: H⊗(2n) (counting) → init |1⟩ (work) → controlled modular multiplications
→ inverse QFT → Measure counting register.
Key primitives: modular exponentiation via repeated squaring, QPE, inverse QFT.
"""


def _controlled_modmul(qc: QuantumCircuit, control: int, a: int, N: int,
                        work_qubits: list[int]) -> None:
    """Simplified controlled modular multiplication for small N."""
    n = len(work_qubits)
    # For demonstration: apply controlled swaps that permute the work register
    # This is a simplified version; full Shor uses Beauregard's circuit
    if a % N == 1:
        return
    for i in range(n - 1):
        qc.cswap(control, work_qubits[i], work_qubits[(i + 1) % n])


def _inverse_qft(qc: QuantumCircuit, qubits: list[int]) -> None:
    n = len(qubits)
    for i in range(n // 2):
        qc.swap(qubits[i], qubits[n - 1 - i])
    for target in range(n):
        qc.h(qubits[target])
        for control in range(target):
            qc.cp(-pi / (2 ** (target - control)), qubits[control], qubits[target])


def generate_circuit(
    n_qubits: int = 4,
    N: int = 15,
    a: int = 7,
    **_kwargs,
) -> CircuitRecord:
    """Generate simplified Shor circuit for factoring N with base a."""
    n = max(math.ceil(math.log2(N + 1)), 2)
    counting = max(n_qubits, 2 * n)
    total = counting + n

    qc = QuantumCircuit(total, counting)

    # Work register: initialize to |1⟩
    work = list(range(counting, total))
    qc.x(work[0])

    # Hadamard on counting register
    qc.h(range(counting))

    # Controlled modular exponentiation
    for k in range(counting):
        power = pow(a, 2**k, N)
        _controlled_modmul(qc, k, power, N, work)

    # Inverse QFT on counting register
    _inverse_qft(qc, list(range(counting)))

    qc.measure(range(counting), range(counting))

    return circuit_to_record(
        qc,
        name="shor",
        category="algebraic",
        description=DESCRIPTION,
        parameters={"n_qubits": counting, "N": N, "a": a,
                     "work_qubits": n},
        pattern_description=PATTERN,
        difficulty="hard",
    )


registry.register(
    "shor",
    generate_circuit,
    category="algebraic",
    difficulty="hard",
    description="Shor's factoring algorithm — period finding via QPE",
)
