"""Central registry for all circuit generators."""

from __future__ import annotations

from typing import Callable, Iterator

from qcircuitbench.core import CircuitRecord, CATEGORIES


# Type for a generator function: (n_qubits, **kwargs) -> CircuitRecord
GeneratorFunc = Callable[..., CircuitRecord]


class CircuitRegistry:
    """Singleton registry mapping algorithm names to their generator functions."""

    def __init__(self) -> None:
        self._generators: dict[str, GeneratorFunc] = {}
        self._meta: dict[str, dict] = {}  # name -> {category, difficulty, ...}

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------
    def register(
        self,
        name: str,
        generator: GeneratorFunc,
        *,
        category: str = "oracular",
        difficulty: str = "medium",
        description: str = "",
    ) -> None:
        """Register a circuit generator under *name*."""
        self._generators[name] = generator
        self._meta[name] = {
            "category": category,
            "difficulty": difficulty,
            "description": description,
        }

    # ------------------------------------------------------------------
    # Querying
    # ------------------------------------------------------------------
    def list_algorithms(self) -> list[str]:
        """Return sorted list of all registered algorithm names."""
        return sorted(self._generators.keys())

    def list_categories(self) -> list[str]:
        """Return the standard category keys."""
        return sorted(CATEGORIES.keys())

    def get(self, name: str, *, n_qubits: int = 4, **kwargs) -> CircuitRecord:
        """Generate a single CircuitRecord for algorithm *name*."""
        if name not in self._generators:
            raise KeyError(
                f"Unknown algorithm '{name}'. "
                f"Available: {', '.join(self.list_algorithms())}"
            )
        return self._generators[name](n_qubits=n_qubits, **kwargs)

    def get_all(
        self,
        *,
        category: str | None = None,
        difficulty: str | None = None,
        n_qubits: int = 4,
        **kwargs,
    ) -> list[CircuitRecord]:
        """Generate CircuitRecords for all matching algorithms."""
        results = []
        for name in self.list_algorithms():
            meta = self._meta[name]
            if category and meta["category"] != category:
                continue
            if difficulty and meta["difficulty"] != difficulty:
                continue
            try:
                results.append(self.get(name, n_qubits=n_qubits, **kwargs))
            except Exception:
                # Skip algorithms that can't be generated with these params
                pass
        return results

    def search(self, query: str) -> list[str]:
        """Search algorithm names and descriptions for *query* (case-insensitive)."""
        q = query.lower()
        hits = []
        for name, meta in self._meta.items():
            if q in name.lower() or q in meta.get("description", "").lower():
                hits.append(name)
        return sorted(hits)

    def iterate(
        self,
        *,
        qubit_range: range = range(2, 9),
        category: str | None = None,
        **kwargs,
    ) -> Iterator[CircuitRecord]:
        """Yield CircuitRecords over a range of qubit counts."""
        for name in self.list_algorithms():
            meta = self._meta[name]
            if category and meta["category"] != category:
                continue
            for n in qubit_range:
                try:
                    yield self.get(name, n_qubits=n, **kwargs)
                except Exception:
                    continue

    def info(self, name: str) -> dict:
        """Return metadata dict for an algorithm."""
        if name not in self._meta:
            raise KeyError(f"Unknown algorithm '{name}'.")
        return dict(self._meta[name])


# Module-level singleton
registry = CircuitRegistry()


# Convenience functions that delegate to the singleton
def list_algorithms() -> list[str]:
    return registry.list_algorithms()


def list_categories() -> list[str]:
    return registry.list_categories()


def get(name: str, *, n_qubits: int = 4, **kwargs) -> CircuitRecord:
    return registry.get(name, n_qubits=n_qubits, **kwargs)


def get_all(
    *,
    category: str | None = None,
    difficulty: str | None = None,
    n_qubits: int = 4,
    **kwargs,
) -> list[CircuitRecord]:
    return registry.get_all(
        category=category, difficulty=difficulty, n_qubits=n_qubits, **kwargs
    )


def search(query: str) -> list[str]:
    return registry.search(query)
