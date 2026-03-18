"""BB84 Quantum Key Distribution."""

from __future__ import annotations

import random
from qiskit import QuantumCircuit

from qcircuitbench.registry import registry
from qcircuitbench.core import CircuitRecord
from qcircuitbench.utils import circuit_to_record

DESCRIPTION = """\
BB84 is the first quantum key distribution protocol (Bennett & Brassard 1984).
Alice randomly encodes bits in either the Z-basis ({|0⟩,|1⟩}) or X-basis
({|+⟩,|−⟩}). Bob randomly measures in Z or X basis. They publicly compare
bases (not values) and keep only matching-basis bits as the secret key.
Eavesdropping introduces detectable errors due to the no-cloning theorem.
"""

PATTERN = """\
Pattern: For each bit: Alice prepares (X if bit=1, H if X-basis) → Bob measures
(H if X-basis, then measure). Sifting: discard mismatched-basis bits.
Key primitive: conjugate coding — information is secure when basis is unknown.
"""


def generate_circuit(
    n_qubits: int = 4,
    seed: int = 42,
    **_kwargs,
) -> CircuitRecord:
    """Generate BB84 QKD circuit for n_qubits key bits."""
    n = max(n_qubits, 2)
    rng = random.Random(seed)

    alice_bits = [rng.randint(0, 1) for _ in range(n)]
    alice_bases = [rng.randint(0, 1) for _ in range(n)]  # 0=Z, 1=X
    bob_bases = [rng.randint(0, 1) for _ in range(n)]

    qc = QuantumCircuit(n, n)

    # Alice prepares
    for i in range(n):
        if alice_bits[i] == 1:
            qc.x(i)
        if alice_bases[i] == 1:
            qc.h(i)

    qc.barrier()

    # Bob measures
    for i in range(n):
        if bob_bases[i] == 1:
            qc.h(i)

    qc.measure(range(n), range(n))

    return circuit_to_record(
        qc,
        name="qkd_bb84",
        category="quantum_information",
        description=DESCRIPTION,
        parameters={"n_qubits": n, "alice_bits": alice_bits,
                     "alice_bases": alice_bases, "bob_bases": bob_bases},
        pattern_description=PATTERN,
        difficulty="easy",
    )


registry.register(
    "qkd_bb84",
    generate_circuit,
    category="quantum_information",
    difficulty="easy",
    description="BB84 quantum key distribution protocol",
)
