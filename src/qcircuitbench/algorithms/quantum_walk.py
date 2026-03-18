"""Discrete-time quantum walk on a cycle."""

from __future__ import annotations

from qiskit import QuantumCircuit

from qcircuitbench.registry import registry
from qcircuitbench.core import CircuitRecord
from qcircuitbench.utils import circuit_to_record

DESCRIPTION = """\
A discrete-time quantum walk (DTQW) on a cycle graph is the quantum analogue
of a classical random walk. It uses a coin qubit to determine direction and
shift operations (conditional increments/decrements of position) on a position
register. After t steps, the quantum walker spreads ballistically (∝t) vs
classically (∝√t), providing quadratic speedup for spatial search.
"""

PATTERN = """\
Pattern: repeat t steps { Coin(H on coin qubit) → Shift(conditional increment/
decrement of position register) }.
Shift uses CNOT cascades conditioned on coin qubit.
Key primitive: coin-flip + conditional shift = quantum walk step.
"""


def _increment(qc: QuantumCircuit, pos_qubits: list[int], control: int) -> None:
    """Controlled increment of position register."""
    n = len(pos_qubits)
    for i in range(n - 1, 0, -1):
        controls = [control] + pos_qubits[:i]
        qc.mcx(controls, pos_qubits[i])
    qc.cx(control, pos_qubits[0])


def _decrement(qc: QuantumCircuit, pos_qubits: list[int], control: int) -> None:
    """Controlled decrement = X on control, controlled increment, X on control."""
    qc.x(control)
    _increment(qc, pos_qubits, control)
    qc.x(control)


def generate_circuit(
    n_qubits: int = 4,
    n_steps: int = 3,
    **_kwargs,
) -> CircuitRecord:
    """Generate DTQW on a cycle with n_qubits position qubits + 1 coin qubit."""
    n_pos = max(n_qubits, 2)
    total = n_pos + 1  # position + coin
    coin = 0
    pos = list(range(1, total))

    qc = QuantumCircuit(total, n_pos)

    for _ in range(n_steps):
        # Coin flip
        qc.h(coin)
        # Conditional shift
        _increment(qc, pos, coin)
        # Decrement for opposite direction
        _decrement(qc, pos, coin)

    qc.measure(pos, range(n_pos))

    return circuit_to_record(
        qc,
        name="quantum_walk",
        category="simulation",
        description=DESCRIPTION,
        parameters={"n_qubits": n_pos, "n_steps": n_steps,
                     "total_qubits": total},
        pattern_description=PATTERN,
        difficulty="medium",
    )


registry.register(
    "quantum_walk",
    generate_circuit,
    category="simulation",
    difficulty="medium",
    description="Discrete-time quantum walk on a cycle",
)
