"""Shared helpers for circuit generators."""

from __future__ import annotations

from qiskit import QuantumCircuit
from qiskit.qasm3 import dumps as qasm3_dumps

from qcircuitbench.core import CircuitRecord


def circuit_to_record(
    circuit: QuantumCircuit,
    *,
    name: str,
    category: str,
    description: str,
    parameters: dict,
    pattern_description: str = "",
    difficulty: str = "medium",
    metadata: dict | None = None,
) -> CircuitRecord:
    """Convert a Qiskit QuantumCircuit into a CircuitRecord."""
    # Extract gate list
    gate_list = [inst.operation.name for inst in circuit.data]

    # Generate QASM 3 string
    try:
        qasm = qasm3_dumps(circuit)
    except Exception:
        qasm = ""

    return CircuitRecord(
        name=name,
        category=category,
        qasm=qasm,
        description=description,
        parameters=parameters,
        pattern_description=pattern_description,
        difficulty=difficulty,
        gate_list=gate_list,
        depth=circuit.depth(),
        width=circuit.num_qubits,
        metadata=metadata or {},
    )
