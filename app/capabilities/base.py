"""Abstract interface implemented by all MAVIS capability adapters."""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.capabilities.contracts import CapabilityRequest, CapabilityResult


class Capability(ABC):
    """A named adapter that executes a bounded family of actions.

    Capability implementations must not perform policy decisions. They receive
    a validated request and return a terminal result. The action lifecycle and
    safety policy layers are introduced separately in Phase 2.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the stable, lower-case identifier for this capability."""

    @abstractmethod
    def execute(self, request: CapabilityRequest) -> CapabilityResult:
        """Execute one request and return a result linked to that request."""
