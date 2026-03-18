"""QAOA for Max-Cut."""

from __future__ import annotations

import networkx as nx
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter

from qcircuitbench.registry import registry
from qcircuitbench.core import CircuitRecord
from qcircuitbench.utils import circuit_to_record

DESCRIPTION = """\
The Quantum Approximate Optimization Algorithm (QAOA) finds approximate
solutions to combinatorial optimization problems. For Max-Cut on a graph G,
the circuit alternates between a problem unitary (ZZ interactions on each edge)
and a mixer unitary (X rotations on each qubit) for p layers. The parameters
γ and β are classically optimized.
"""

PATTERN = """\
Pattern: H⊗n → repeat p times { exp(-iγC) · exp(-iβB) } → Measure.
C = cost Hamiltonian (RZZ on edges), B = mixer (RX on each qubit).
Key primitive: alternating cost/mixer layers approximate adiabatic evolution.
"""


def generate_circuit(
    n_qubits: int = 4,
    n_layers: int = 1,
    graph: nx.Graph | None = None,
    **_kwargs,
) -> CircuitRecord:
    """Generate QAOA Max-Cut circuit."""
    n = max(n_qubits, 2)
    if graph is None:
        # Default: random regular graph
        graph = nx.random_regular_graph(d=min(3, n - 1), n=n, seed=42)

    beta = [Parameter(f"β_{i}") for i in range(n_layers)]
    gamma = [Parameter(f"γ_{i}") for i in range(n_layers)]

    qc = QuantumCircuit(n, n)
    qc.h(range(n))

    for layer in range(n_layers):
        # Cost layer
        for u, v in graph.edges():
            qc.rzz(2 * gamma[layer], int(u), int(v))
        # Mixer layer
        for qubit in range(n):
            qc.rx(2 * beta[layer], qubit)

    qc.measure(range(n), range(n))

    return circuit_to_record(
        qc,
        name="qaoa",
        category="variational",
        description=DESCRIPTION,
        parameters={"n_qubits": n, "n_layers": n_layers,
                     "edges": list(graph.edges())},
        pattern_description=PATTERN,
        difficulty="hard",
    )


registry.register(
    "qaoa",
    generate_circuit,
    category="variational",
    difficulty="hard",
    description="QAOA for Max-Cut — variational combinatorial optimization",
)
