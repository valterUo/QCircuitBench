"""Quantum Monte Carlo Integration."""

from __future__ import annotations

from math import pi
from qiskit import QuantumCircuit

from qcircuitbench.registry import registry
from qcircuitbench.core import CircuitRecord
from qcircuitbench.utils import circuit_to_record

DESCRIPTION = """\
Quantum Monte Carlo (QMC) Integration uses amplitude estimation to compute
integrals and expectations with quadratic speedup: O(1/ε) quantum queries vs
O(1/ε²) classical samples. The function to integrate is loaded into quantum
amplitudes via a state-preparation oracle, and amplitude estimation extracts
the expected value. Applications include option pricing and risk analysis.
"""

PATTERN = """\
Pattern: State preparation P (load distribution) → function evaluation R
(rotate ancilla proportionally to f(x)) → Amplitude Estimation (QPE on
Q = Grover iterate of P·R).
Key primitive: function loading into amplitudes + amplitude estimation.
"""


def _inverse_qft(qc: QuantumCircuit, qubits: list[int]) -> None:
    n = len(qubits)
    for i in range(n // 2):
        qc.swap(qubits[i], qubits[n - 1 - i])
    for j in range(n):
        qc.h(qubits[j])
        for k in range(j):
            qc.cp(-pi / (2 ** (j - k)), qubits[k], qubits[j])


def generate_circuit(
    n_qubits: int = 4,
    n_eval: int | None = None,
    **_kwargs,
) -> CircuitRecord:
    """Generate QMC integration circuit."""
    n_state = max(n_qubits, 2)
    m = n_eval or n_state
    ancilla_count = 1
    total = m + n_state + ancilla_count

    count_qubits = list(range(m))
    state_qubits = list(range(m, m + n_state))
    anc = m + n_state

    qc = QuantumCircuit(total, m)

    # State preparation: uniform superposition (uniform distribution)
    qc.h(state_qubits)

    # Function evaluation: controlled RY on ancilla (f(x) ~ x/2^n)
    for i, sq in enumerate(state_qubits):
        angle = pi / (2 ** (n_state - i))
        qc.cry(angle, sq, anc)

    # Amplitude estimation via QPE on Grover iterate
    qc.h(count_qubits)

    # Simplified Grover iterate as a gate
    grover_step = QuantumCircuit(n_state + ancilla_count, name="Q")
    grover_step.z(n_state)  # mark
    grover_step.h(range(n_state))
    grover_step.x(range(n_state))
    grover_step.h(n_state - 1)
    if n_state > 1:
        grover_step.mcx(list(range(n_state - 1)), n_state - 1)
    grover_step.h(n_state - 1)
    grover_step.x(range(n_state))
    grover_step.h(range(n_state))
    grover_gate = grover_step.to_gate().control(1)

    for k in range(m):
        for _ in range(2**k):
            qc.append(grover_gate, [count_qubits[k]] + state_qubits + [anc])

    _inverse_qft(qc, count_qubits)
    qc.measure(count_qubits, list(range(m)))

    return circuit_to_record(
        qc,
        name="qmc_integration",
        category="variational",
        description=DESCRIPTION,
        parameters={"n_qubits": n_state, "n_eval": m,
                     "total_qubits": total},
        pattern_description=PATTERN,
        difficulty="medium",
    )


registry.register(
    "qmc_integration",
    generate_circuit,
    category="variational",
    difficulty="medium",
    description="Quantum Monte Carlo Integration — quadratic speedup for integrals",
)
