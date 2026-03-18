"""Export utilities — convert registry contents to training-data formats."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Iterator

from qcircuitbench.core import CircuitRecord
from qcircuitbench.registry import registry


def _record_to_dict(record: CircuitRecord) -> dict:
    """Serialise a CircuitRecord to a plain dict."""
    return {
        "name": record.name,
        "category": record.category,
        "qasm": record.qasm,
        "description": record.description,
        "parameters": record.parameters,
        "pattern_description": record.pattern_description,
        "difficulty": record.difficulty,
        "gate_list": record.gate_list,
        "depth": record.depth,
        "width": record.width,
        "metadata": record.metadata,
    }


def _training_pair(record: CircuitRecord) -> dict:
    """Create a prompt/completion pair suitable for LLM fine-tuning."""
    prompt = (
        f"Generate an OpenQASM 3.0 circuit for the following task.\n\n"
        f"Algorithm: {record.name}\n"
        f"Category: {record.category}\n"
        f"Description: {record.description.strip()}\n"
        f"Parameters: {json.dumps(record.parameters)}\n\n"
        f"Respond with the complete QASM code."
    )
    return {
        "prompt": prompt,
        "completion": record.qasm,
        "metadata": {
            "name": record.name,
            "category": record.category,
            "difficulty": record.difficulty,
            "pattern_description": record.pattern_description,
            "gate_list": record.gate_list,
            "depth": record.depth,
            "width": record.width,
        },
    }


# ------------------------------------------------------------------
# Public API
# ------------------------------------------------------------------

def iterate_records(
    *,
    qubit_range: range = range(2, 9),
    category: str | None = None,
    difficulty: str | None = None,
) -> Iterator[CircuitRecord]:
    """Yield CircuitRecords across all algorithms and qubit counts."""
    for name in registry.list_algorithms():
        meta = registry.info(name)
        if category and meta["category"] != category:
            continue
        if difficulty and meta["difficulty"] != difficulty:
            continue
        for n in qubit_range:
            try:
                yield registry.get(name, n_qubits=n)
            except Exception:
                continue


def to_jsonl(
    path: str | Path,
    *,
    qubit_range: range = range(2, 9),
    category: str | None = None,
    difficulty: str | None = None,
    mode: str = "training",
) -> int:
    """Export records to a JSONL file. Returns the number of records written.

    *mode*:
      - ``"training"`` — prompt/completion pairs for LLM fine-tuning
      - ``"raw"``      — full CircuitRecord dicts
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with open(path, "w") as f:
        for rec in iterate_records(
            qubit_range=qubit_range, category=category, difficulty=difficulty
        ):
            if mode == "training":
                obj = _training_pair(rec)
            else:
                obj = _record_to_dict(rec)
            f.write(json.dumps(obj) + "\n")
            count += 1
    return count


def to_qasm_dir(
    directory: str | Path,
    *,
    qubit_range: range = range(2, 9),
    category: str | None = None,
) -> int:
    """Export QASM files + metadata JSONs into a directory tree.

    Structure:
        directory/<algorithm>/<algorithm>_n<qubits>.qasm
        directory/<algorithm>/<algorithm>_n<qubits>.json
    """
    directory = Path(directory)
    count = 0
    for rec in iterate_records(qubit_range=qubit_range, category=category):
        algo_dir = directory / rec.name
        algo_dir.mkdir(parents=True, exist_ok=True)
        n = rec.parameters.get("n_qubits", rec.width)
        base = f"{rec.name}_n{n}"
        (algo_dir / f"{base}.qasm").write_text(rec.qasm)
        (algo_dir / f"{base}.json").write_text(
            json.dumps(_record_to_dict(rec), indent=2)
        )
        count += 1
    return count


def to_hf_dataset(
    *,
    qubit_range: range = range(2, 9),
    category: str | None = None,
):
    """Export as a HuggingFace ``datasets.Dataset`` (requires ``datasets`` extra).

    Returns:
        datasets.Dataset with columns: prompt, completion, name, category, ...
    """
    try:
        from datasets import Dataset
    except ImportError:
        raise ImportError(
            "Install the 'datasets' package: pip install qcircuitbench[export]"
        )

    rows = []
    for rec in iterate_records(qubit_range=qubit_range, category=category):
        pair = _training_pair(rec)
        flat = {
            "prompt": pair["prompt"],
            "completion": pair["completion"],
            **pair["metadata"],
            "gate_list": json.dumps(pair["metadata"]["gate_list"]),
        }
        rows.append(flat)
    return Dataset.from_list(rows)
