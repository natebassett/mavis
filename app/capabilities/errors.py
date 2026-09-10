"""Domain errors raised by the capability framework."""


class CapabilityError(Exception):
    """Base class for errors associated with a MAVIS capability."""


class InvalidCapabilityRequestError(CapabilityError, ValueError):
    """Raised when a capability request or configuration is malformed."""


class CapabilityRegistrationError(CapabilityError):
    """Raised when a capability cannot be registered safely."""


class CapabilityNotFoundError(CapabilityError, LookupError):
    """Raised when an action targets an unregistered capability."""


class CapabilityExecutionError(CapabilityError):
    """Raised when a capability cannot execute the requested action."""


class CapabilityContractError(CapabilityError):
    """Raised when a capability returns a result that breaks the contract."""
