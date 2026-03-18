"""
qcircuitbench — A comprehensive quantum circuit generation platform.

Usage:
    import qcircuitbench
    
    # List all available algorithms
    qcircuitbench.list_algorithms()
    
    # Get a circuit
    record = qcircuitbench.get("grover", n_qubits=4)
    print(record.qasm)
    print(record.description)
    
    # Import from specific modules
    from qcircuitbench.algorithms import grover
    circuit = grover.generate_circuit(n_qubits=4)
"""

from qcircuitbench.core import CircuitRecord
from qcircuitbench.registry import (
    registry,
    list_algorithms,
    list_categories,
    get,
    get_all,
    search,
)

# Force registration of all algorithm modules
import qcircuitbench.algorithms  # noqa: F401

__version__ = "0.1.0"

__all__ = [
    "CircuitRecord",
    "registry",
    "list_algorithms",
    "list_categories",
    "get",
    "get_all",
    "search",
]
