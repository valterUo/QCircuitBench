"""Bell state preparation."""

from __future__ import annotations

from qiskit import QuantumCircuit

from qcircuitbench.registry import registry
from qcircuitbench.core import CircuitRecord
from qcircuitbench.utils import circuit_to_record

DESCRIPTION = """\
Bell states are the four maximally entangled two-qubit states:
|Φ+⟩ = (|00⟩+|11⟩)/√2, |Φ-⟩ = (|00⟩-|11⟩)/√2,
|Ψ+⟩ = (|01⟩+|10⟩)/√2, |Ψ-⟩ = (|01⟩-|10⟩)/√2.
They are the building blocks of quantum teleportation, superdense coding, and
entanglement-based QKD. Preparation requires only one H gate and one CNOT.
"""

PATTERN = """\
Pattern: [optional X gates to select variant] → H(0) → CNOT(0,1).
|Φ+⟩: H·CNOT, |Φ-⟩: Z·H·CNOT, |Ψ+⟩: X·H·CNOT, |Ψ-⟩: X·Z·H·CNOT.
Key primitive: entanglement creation via H + CNOT.
"""

BELL_STATES = ("phi_plus", "phi_minus", "psi_plus", "psi_minus")


def generate_circuit(
    n_qubits: int = 2,
    variant: str = "phi_plus",
    **_kwargs,
) -> CircuitRecord:
    """Generate Bell state preparation circuit."""
    qc = QuantumCircuit(2)

    if variant in ("psi_plus", "psi_minus"):
        qc.x(0)
    if variant in ("phi_minus", "psi_minus"):
        qc.z(0)

    qc.h(0)
    qc.cx(0, 1)

    return circuit_to_record(
        qc,
        name="bell_state",
        category="state_preparation",
        description=DESCRIPTION,
        parameters={"n_qubits": 2, "variant": variant},
        pattern_description=PATTERN,
        difficulty="easy",
    )


registry.register(
    "bell_state",
    generate_circuit,
    category="state_preparation",
    difficulty="easy",
    description="Bell state preparation — maximally entangled qubit pair",
)
