"""Algorithm registry — imports all submodules to trigger registration."""

# Oracular algorithms
from qcircuitbench.algorithms import grover  # noqa: F401
from qcircuitbench.algorithms import bernstein_vazirani  # noqa: F401
from qcircuitbench.algorithms import deutsch_jozsa  # noqa: F401
from qcircuitbench.algorithms import deutsch  # noqa: F401
from qcircuitbench.algorithms import simon  # noqa: F401
from qcircuitbench.algorithms import hidden_shift  # noqa: F401
from qcircuitbench.algorithms import quantum_counting  # noqa: F401

# Algebraic / number-theoretic
from qcircuitbench.algorithms import qft  # noqa: F401
from qcircuitbench.algorithms import phase_estimation  # noqa: F401
from qcircuitbench.algorithms import shor  # noqa: F401
from qcircuitbench.algorithms import hhl  # noqa: F401
from qcircuitbench.algorithms import discrete_log  # noqa: F401
from qcircuitbench.algorithms import qsvt  # noqa: F401

# Variational
from qcircuitbench.algorithms import qaoa  # noqa: F401
from qcircuitbench.algorithms import vqe  # noqa: F401
from qcircuitbench.algorithms import qae  # noqa: F401
from qcircuitbench.algorithms import data_encoding  # noqa: F401
from qcircuitbench.algorithms import qnn  # noqa: F401
from qcircuitbench.algorithms import qmc  # noqa: F401
from qcircuitbench.algorithms import vqls  # noqa: F401

# State preparation
from qcircuitbench.algorithms import ghz_state  # noqa: F401
from qcircuitbench.algorithms import w_state  # noqa: F401
from qcircuitbench.algorithms import bell_state  # noqa: F401
from qcircuitbench.algorithms import graph_state  # noqa: F401

# Quantum information protocols
from qcircuitbench.algorithms import teleportation  # noqa: F401
from qcircuitbench.algorithms import superdense_coding  # noqa: F401
from qcircuitbench.algorithms import swap_test  # noqa: F401
from qcircuitbench.algorithms import qkd_bb84  # noqa: F401
from qcircuitbench.algorithms import qrng  # noqa: F401
from qcircuitbench.algorithms import hadamard_test  # noqa: F401

# Error correction
from qcircuitbench.algorithms import repetition_code  # noqa: F401
from qcircuitbench.algorithms import shor_code  # noqa: F401
from qcircuitbench.algorithms import steane_code  # noqa: F401

# Arithmetic
from qcircuitbench.algorithms import quantum_adder  # noqa: F401
from qcircuitbench.algorithms import quantum_multiplier  # noqa: F401

# Simulation
from qcircuitbench.algorithms import hamiltonian_sim  # noqa: F401
from qcircuitbench.algorithms import quantum_walk  # noqa: F401
from qcircuitbench.algorithms import qite  # noqa: F401

# Machine learning
from qcircuitbench.algorithms import qsvm  # noqa: F401
from qcircuitbench.algorithms import quantum_autoencoder  # noqa: F401

# Random circuit families
from qcircuitbench.algorithms import random_clifford  # noqa: F401
from qcircuitbench.algorithms import random_universal  # noqa: F401
