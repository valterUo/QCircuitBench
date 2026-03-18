"""Graph state preparation."""

from __future__ import annotations

import networkx as nx
from qiskit import QuantumCircuit

from qcircuitbench.registry import registry
from qcircuitbench.core import CircuitRecord
from qcircuitbench.utils import circuit_to_record

DESCRIPTION = """\
A graph state |G⟩ is an n-qubit entangled state defined by a graph G=(V,E).
Each vertex is a qubit initialized to |+⟩ (via Hadamard), and a CZ gate is
applied for each edge. Graph states are central to measurement-based quantum
computing, error correction (cluster states, surface codes), and entanglement
theory. Different graphs yield different entanglement structures.
"""

PATTERN = """\
Pattern: H⊗n → CZ(u,v) for each edge (u,v) in G.
Key primitive: CZ-based entanglement matching a graph topology.
"""


def generate_circuit(
    n_qubits: int = 4,
    graph: nx.Graph | None = None,
    **_kwargs,
) -> CircuitRecord:
    """Generate graph state preparation circuit."""
    n = max(n_qubits, 2)
    if graph is None:
        # Default: path graph
        graph = nx.path_graph(n)

    qc = QuantumCircuit(n)
    qc.h(range(n))
    for u, v in graph.edges():
        qc.cz(int(u), int(v))

    return circuit_to_record(
        qc,
        name="graph_state",
        category="state_preparation",
        description=DESCRIPTION,
        parameters={"n_qubits": n, "edges": list(graph.edges())},
        pattern_description=PATTERN,
        difficulty="easy",
    )


registry.register(
    "graph_state",
    generate_circuit,
    category="state_preparation",
    difficulty="easy",
    description="Graph state preparation — CZ-entangled state from a graph",
)
