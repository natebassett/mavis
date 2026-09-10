"""Public contracts for MAVIS capabilities.

A capability is a replaceable adapter that performs one bounded kind of
action. The Phase 2 framework deliberately contains no real-world adapters;
simulated and hardware-backed implementations will use these same contracts.
"""

from app.capabilities.base import Capability
from app.capabilities.contracts import (
    CapabilityConfiguration,
    CapabilityRequest,
    CapabilityResult,
    CapabilityStatus,
)
from app.capabilities.errors import (
    CapabilityContractError,
    CapabilityError,
    CapabilityExecutionError,
    CapabilityNotFoundError,
    CapabilityRegistrationError,
    InvalidCapabilityRequestError,
)
from app.capabilities.registry import CapabilityRegistry

__all__ = [
    "Capability",
    "CapabilityConfiguration",
    "CapabilityContractError",
    "CapabilityError",
    "CapabilityExecutionError",
    "CapabilityNotFoundError",
    "CapabilityRegistrationError",
    "CapabilityRegistry",
    "CapabilityRequest",
    "CapabilityResult",
    "CapabilityStatus",
    "InvalidCapabilityRequestError",
]
