"""Data encoding circuits (angle, amplitude, basis)."""

from __future__ import annotations

import math
from qiskit import QuantumCircuit

from qcircuitbench.registry import registry
from qcircuitbench.core import CircuitRecord
from qcircuitbench.utils import circuit_to_record

DESCRIPTION = """\
Data encoding circuits embed classical data into quantum states. Three common
strategies:
- Angle encoding: each feature → RY rotation angle on one qubit.
- Basis encoding: binary string → computational basis state via X gates.
- Amplitude encoding: data vector → amplitudes of a quantum state.
These are building blocks for quantum machine learning.
"""

PATTERN = """\
Angle encoding: RY(x_i) on qubit i.
Basis encoding: X on qubits where the bit is 1.
Key primitive: classical-to-quantum data loading.
"""


def generate_circuit(
    n_qubits: int = 4,
    encoding: str = "angle",
    data: list[float] | None = None,
    **_kwargs,
) -> CircuitRecord:
    """Generate a data encoding circuit."""
    n = max(n_qubits, 2)

    if data is None:
        # Default data: evenly-spaced angles
        data = [i * math.pi / n for i in range(n)]

    qc = QuantumCircuit(n)

    if encoding == "angle":
        for i in range(min(n, len(data))):
            qc.ry(data[i], i)
    elif encoding == "basis":
        # Interpret data as binary bits
        for i in range(min(n, len(data))):
            if data[i] > 0.5:
                qc.x(i)
    else:
        raise ValueError(f"Unknown encoding: {encoding}")

    return circuit_to_record(
        qc,
        name="data_encoding",
        category="variational",
        description=DESCRIPTION,
        parameters={"n_qubits": n, "encoding": encoding, "data": data[:n]},
        pattern_description=PATTERN,
        difficulty="easy",
    )


registry.register(
    "data_encoding",
    generate_circuit,
    category="variational",
    difficulty="easy",
    description="Data encoding circuits — angle, basis, amplitude",
)
