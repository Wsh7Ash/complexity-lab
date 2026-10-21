"""Counter helpers for instrumented algorithms.

Every instrumented algorithm returns a :class:`Counts` instance alongside its
result.  The fields are intentionally broad so a single data structure can
capture comparisons, swaps, probes and generic accesses across sorting,
searching and hashing code.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass
class Counts:
    """Operation counters accumulated while running an algorithm."""

    comparisons: int = 0
    swaps: int = 0
    probes: int = 0
    accesses: int = 0

    def add(self, other: "Counts") -> None:
        """Add another Counts instance into this one, in place."""
        self.comparisons += other.comparisons
        self.swaps += other.swaps
        self.probes += other.probes
        self.accesses += other.accesses

    def to_dict(self) -> Dict[str, int]:
        """Serialise the counters to a plain dictionary."""
        return {
            "comparisons": self.comparisons,
            "swaps": self.swaps,
            "probes": self.probes,
            "accesses": self.accesses,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, int]) -> "Counts":
        """Rebuild a Counts instance from a plain dictionary."""
        return cls(
            comparisons=int(d.get("comparisons", 0)),
            swaps=int(d.get("swaps", 0)),
            probes=int(d.get("probes", 0)),
            accesses=int(d.get("accesses", 0)),
        )

    def primary(self, algo: str = "") -> int:
        """Return the dominant operation count for growth fitting.

        Search algorithms are characterised by probes; sorting algorithms by
        comparisons (falling back to swaps when an algorithm does not compare
        in the usual sense).
        """
        search_suffixes = ("search", "lookup")
        if any(algo.endswith(s) for s in search_suffixes):
            return self.probes or self.comparisons
        return self.comparisons or self.swaps