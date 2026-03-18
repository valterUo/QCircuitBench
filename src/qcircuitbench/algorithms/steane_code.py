"""Steane 7-qubit error-correcting code."""

from __future__ import annotations

from qiskit import QuantumCircuit

from qcircuitbench.registry import registry
from qcircuitbench.core import CircuitRecord
from qcircuitbench.utils import circuit_to_record

DESCRIPTION = """\
The Steane code is a [[7,1,3]] CSS code that encodes 1 logical qubit into 7
physical qubits and corrects any single-qubit error. It is based on the
classical [7,4,3] Hamming code. Being a CSS code, X and Z errors are corrected
independently. The encoding circuit uses Hadamard and CNOT gates following
the Hamming parity-check matrix structure.
"""

PATTERN = """\
Pattern: Prepare |0⟩_L via CNOT network from Hamming code generators:
CNOT from qubit 0 → {3,4,5,6}, plus CNOT from qubit 1 → {1,2,5,6},
plus CNOT from qubit 2 → {0,2,4,6}, then Hadamards for X-type stabilizers.
Key primitive: CSS code encoding from classical linear code.
"""


def generate_circuit(
    n_qubits: int = 7,
    **_kwargs,
) -> CircuitRecord:
    """Generate Steane 7-qubit code encoding circuit."""
    qc = QuantumCircuit(7)

    # Encode |0⟩_L using Hamming code structure
    # Generator rows: g1=[1,1,1,1,0,0,0], g2=[0,1,1,0,1,1,0], g3=[0,0,1,0,0,1,1]
    # Start with data on qubit 0, spread via CNOTs

    # Prepare superposition for CSS
    qc.h(0)
    qc.h(1)
    qc.h(2)

    # Hamming code CNOT pattern
    qc.cx(0, 3)
    qc.cx(0, 4)
    qc.cx(0, 5)
    qc.cx(1, 3)
    qc.cx(1, 5)
    qc.cx(1, 6)
    qc.cx(2, 4)
    qc.cx(2, 5)
    qc.cx(2, 6)

    return circuit_to_record(
        qc,
        name="steane_code",
        category="error_correction",
        description=DESCRIPTION,
        parameters={"n_qubits": 7},
        pattern_description=PATTERN,
        difficulty="medium",
    )


registry.register(
    "steane_code",
    generate_circuit,
    category="error_correction",
    difficulty="medium",
    description="Steane 7-qubit code — [[7,1,3]] CSS code",
)
