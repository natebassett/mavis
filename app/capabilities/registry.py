"""Capability registration, configuration, lookup, and contract enforcement."""

from __future__ import annotations

from collections.abc import Iterable

from app.capabilities.base import Capability
from app.capabilities.contracts import (
    CapabilityConfiguration,
    CapabilityRequest,
    CapabilityResult,
)
from app.capabilities.errors import (
    CapabilityContractError,
    CapabilityNotFoundError,
    CapabilityRegistrationError,
    InvalidCapabilityRequestError,
)


class CapabilityRegistry:
    """Owns the capability adapters available to one MAVIS runtime.

    The registry has no knowledge of a specific device, model, or transport.
    It only validates the shared contract and prevents accidentally routing an
    action to an absent or disabled capability.
    """

    def __init__(self, capabilities: Iterable[Capability] | None = None):
        self._capabilities: dict[str, Capability] = {}
        self._configurations: dict[str, CapabilityConfiguration] = {}

        if capabilities is not None:
            for capability in capabilities:
                self.register(capability)

    def register(
        self,
        capability: Capability,
        configuration: CapabilityConfiguration | None = None,
        *,
        replace: bool = False,
    ) -> None:
        """Register one capability and its validated configuration.

        Replacing a registration is intentionally explicit so that an adapter
        cannot silently displace another implementation.
        """
        if not isinstance(capability, Capability):
            raise CapabilityRegistrationError(
                "A registered capability must inherit from Capability."
            )

        try:
            name = CapabilityConfiguration(capability=capability.name).capability
        except InvalidCapabilityRequestError as error:
            raise CapabilityRegistrationError(
                "A capability must expose a valid name."
            ) from error

        if name in self._capabilities and not replace:
            raise CapabilityRegistrationError(
                f"Capability '{name}' is already registered."
            )

        configuration = configuration or CapabilityConfiguration(capability=name)

        if configuration.capability != name:
            raise CapabilityRegistrationError(
                "Capability configuration must target the registered capability."
            )

        self._capabilities[name] = capability
        self._configurations[name] = configuration

    def unregister(self, name: str) -> None:
        """Remove a capability and its configuration from this runtime."""
        normalised_name = self._normalise_name(name)
        self.get(normalised_name)
        del self._capabilities[normalised_name]
        del self._configurations[normalised_name]

    def get(self, name: str) -> Capability:
        """Return a named capability or raise a domain-specific lookup error."""
        normalised_name = self._normalise_name(name)

        try:
            return self._capabilities[normalised_name]
        except KeyError as error:
            raise CapabilityNotFoundError(
                f"Capability '{normalised_name}' is not registered."
            ) from error

    def _normalise_name(self, name: str) -> str:
        """Normalise a public registry lookup name to its canonical identifier."""
        try:
            return CapabilityConfiguration(capability=name).capability
        except InvalidCapabilityRequestError as error:
            raise CapabilityNotFoundError(
                "A valid capability name is required for lookup."
            ) from error

    def configuration_for(self, name: str) -> CapabilityConfiguration:
        """Return the immutable configuration for a registered capability."""
        normalised_name = self._normalise_name(name)
        self.get(normalised_name)
        return self._configurations[normalised_name]

    def configure(self, configuration: CapabilityConfiguration) -> None:
        """Replace configuration for an existing registered capability."""
        self.get(configuration.capability)
        self._configurations[configuration.capability] = configuration

    def names(self) -> tuple[str, ...]:
        """Return stable capability names in deterministic order."""
        return tuple(sorted(self._capabilities))

    def execute(self, request: CapabilityRequest) -> CapabilityResult:
        """Execute a request through its enabled capability and validate output."""
        if not isinstance(request, CapabilityRequest):
            raise CapabilityContractError(
                "Registry execution requires a CapabilityRequest."
            )

        capability = self.get(request.capability)
        configuration = self.configuration_for(request.capability)

        if not configuration.enabled:
            return CapabilityResult.rejected(
                request,
                f"Capability '{request.capability}' is disabled.",
                error_code="capability_disabled",
            )

        result = capability.execute(request)

        if not isinstance(result, CapabilityResult):
            raise CapabilityContractError(
                f"Capability '{request.capability}' returned an invalid result."
            )

        if (
            result.request_id != request.request_id
            or result.capability != request.capability
            or result.action != request.action
        ):
            raise CapabilityContractError(
                f"Capability '{request.capability}' returned a result for a "
                "different request."
            )

        return result
