"""Core data types for qcircuitbench."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class CircuitRecord:
    """A single quantum circuit with its full metadata.

    Attributes:
        name: Algorithm identifier (e.g. 'grover', 'qft').
        category: One of the standard categories (see CATEGORIES).
        qasm: OpenQASM 3.0 string representation of the circuit.
        description: Natural-language description of the algorithm/circuit.
        parameters: Dict of generation parameters (n_qubits, etc.).
        pattern_description: Description of the circuit-level patterns
            (e.g. "oracle–diffusion iteration", "QFT butterfly").
        difficulty: 'easy', 'medium', or 'hard'.
        gate_list: Ordered list of gate names used in the circuit.
        depth: Circuit depth.
        width: Number of qubits.
        metadata: Any extra key-value metadata.
    """

    name: str
    category: str
    qasm: str
    description: str
    parameters: dict[str, Any] = field(default_factory=dict)
    pattern_description: str = ""
    difficulty: str = "medium"
    gate_list: list[str] = field(default_factory=list)
    depth: int = 0
    width: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)


# Standard algorithm categories
CATEGORIES = {
    "algebraic": "Algebraic & Number-Theoretic algorithms (Shor, QPE, QFT …)",
    "oracular": "Oracular / query-based algorithms (Grover, BV, DJ, Simon …)",
    "variational": "Variational / parameterized circuits (QAOA, VQE, QAE …)",
    "state_preparation": "State preparation protocols (GHZ, W, Bell, Graph State …)",
    "quantum_information": "Quantum information protocols (Teleportation, Superdense, QKD, Swap Test …)",
    "error_correction": "Quantum error correction codes (Steane, Shor-9, Repetition …)",
    "arithmetic": "Quantum arithmetic circuits (Adder, Multiplier …)",
    "simulation": "Hamiltonian simulation circuits (Trotter, Quantum Walk …)",
    "machine_learning": "Quantum ML circuits (QNN, classifiers …)",
    "random": "Random circuit families (Clifford, Universal gate set …)",
}

DIFFICULTIES = ("easy", "medium", "hard")
