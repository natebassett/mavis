"""Immutable data contracts shared by every MAVIS capability."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from types import MappingProxyType
from typing import Any, Mapping
from uuid import uuid4

from app.capabilities.errors import InvalidCapabilityRequestError


_EMPTY_MAPPING: Mapping[str, Any] = MappingProxyType({})


def _normalise_identifier(value: str, field_name: str) -> str:
    """Return a canonical capability/action identifier or raise a clear error."""
    if not isinstance(value, str):
        raise InvalidCapabilityRequestError(
            f"{field_name} must be a string, not {type(value).__name__}."
        )

    normalised = value.strip().lower()

    if not normalised:
        raise InvalidCapabilityRequestError(f"{field_name} must not be empty.")

    if not normalised[0].isalpha() or not all(
        character.isalnum() or character in {"_", "-"}
        for character in normalised
    ):
        raise InvalidCapabilityRequestError(
            f"{field_name} must start with a letter and contain only letters, "
            "numbers, underscores, or hyphens."
        )

    return normalised


def _freeze_mapping(value: Mapping[str, Any], field_name: str) -> Mapping[str, Any]:
    """Make a shallow immutable copy of a mapping supplied to a contract."""
    if not isinstance(value, Mapping):
        raise InvalidCapabilityRequestError(f"{field_name} must be a mapping.")

    if not value:
        return _EMPTY_MAPPING

    return MappingProxyType(dict(value))


def _normalise_timestamp(value: datetime, field_name: str) -> datetime:
    """Require timezone-aware timestamps and store them in UTC."""
    if not isinstance(value, datetime):
        raise InvalidCapabilityRequestError(f"{field_name} must be a datetime.")

    if value.tzinfo is None or value.utcoffset() is None:
        raise InvalidCapabilityRequestError(
            f"{field_name} must be timezone-aware."
        )

    return value.astimezone(timezone.utc)


class CapabilityStatus(str, Enum):
    """The terminal status of one capability action."""

    SUCCEEDED = "succeeded"
    REJECTED = "rejected"
    FAILED = "failed"
    UNSUPPORTED = "unsupported"


@dataclass(frozen=True, slots=True)
class CapabilityConfiguration:
    """Validated, immutable configuration for one registered capability."""

    capability: str
    enabled: bool = True
    settings: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "capability",
            _normalise_identifier(self.capability, "capability"),
        )

        if not isinstance(self.enabled, bool):
            raise InvalidCapabilityRequestError("enabled must be a boolean.")

        object.__setattr__(
            self,
            "settings",
            _freeze_mapping(self.settings, "settings"),
        )


@dataclass(frozen=True, slots=True)
class CapabilityRequest:
    """A single request to perform a named action through a capability."""

    capability: str
    action: str
    parameters: Mapping[str, Any] = field(default_factory=dict)
    context: Mapping[str, Any] = field(default_factory=dict)
    request_id: str = field(default_factory=lambda: str(uuid4()))
    requested_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "capability",
            _normalise_identifier(self.capability, "capability"),
        )
        object.__setattr__(
            self,
            "action",
            _normalise_identifier(self.action, "action"),
        )
        object.__setattr__(
            self,
            "parameters",
            _freeze_mapping(self.parameters, "parameters"),
        )
        object.__setattr__(
            self,
            "context",
            _freeze_mapping(self.context, "context"),
        )

        if not isinstance(self.request_id, str) or not self.request_id.strip():
            raise InvalidCapabilityRequestError(
                "request_id must be a non-empty string."
            )

        object.__setattr__(
            self,
            "request_id",
            self.request_id.strip(),
        )
        object.__setattr__(
            self,
            "requested_at",
            _normalise_timestamp(self.requested_at, "requested_at"),
        )


@dataclass(frozen=True, slots=True)
class CapabilityResult:
    """The validated, terminal outcome of a capability action."""

    request_id: str
    capability: str
    action: str
    status: CapabilityStatus
    message: str
    data: Mapping[str, Any] = field(default_factory=dict)
    error_code: str | None = None
    completed_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    def __post_init__(self) -> None:
        if not isinstance(self.request_id, str) or not self.request_id.strip():
            raise InvalidCapabilityRequestError(
                "request_id must be a non-empty string."
            )

        object.__setattr__(self, "request_id", self.request_id.strip())
        object.__setattr__(
            self,
            "capability",
            _normalise_identifier(self.capability, "capability"),
        )
        object.__setattr__(
            self,
            "action",
            _normalise_identifier(self.action, "action"),
        )

        try:
            status = CapabilityStatus(self.status)
        except ValueError as error:
            raise InvalidCapabilityRequestError(
                f"status must be a CapabilityStatus, not {self.status!r}."
            ) from error

        object.__setattr__(self, "status", status)

        if not isinstance(self.message, str) or not self.message.strip():
            raise InvalidCapabilityRequestError("message must be a non-empty string.")

        object.__setattr__(self, "message", self.message.strip())
        object.__setattr__(self, "data", _freeze_mapping(self.data, "data"))
        object.__setattr__(
            self,
            "completed_at",
            _normalise_timestamp(self.completed_at, "completed_at"),
        )

        if self.error_code is not None:
            object.__setattr__(
                self,
                "error_code",
                _normalise_identifier(self.error_code, "error_code"),
            )

        if self.status is CapabilityStatus.SUCCEEDED and self.error_code:
            raise InvalidCapabilityRequestError(
                "A successful result must not include an error_code."
            )

    @property
    def was_successful(self) -> bool:
        """Whether the action completed successfully."""
        return self.status is CapabilityStatus.SUCCEEDED

    @classmethod
    def succeeded(
        cls,
        request: CapabilityRequest,
        message: str,
        data: Mapping[str, Any] | None = None,
    ) -> "CapabilityResult":
        """Create a successful result linked to a request."""
        return cls(
            request_id=request.request_id,
            capability=request.capability,
            action=request.action,
            status=CapabilityStatus.SUCCEEDED,
            message=message,
            data={} if data is None else data,
        )

    @classmethod
    def rejected(
        cls,
        request: CapabilityRequest,
        message: str,
        error_code: str = "action_rejected",
    ) -> "CapabilityResult":
        """Create a result for an action rejected by policy or configuration."""
        return cls(
            request_id=request.request_id,
            capability=request.capability,
            action=request.action,
            status=CapabilityStatus.REJECTED,
            message=message,
            error_code=error_code,
        )

    @classmethod
    def failed(
        cls,
        request: CapabilityRequest,
        message: str,
        error_code: str = "execution_failed",
    ) -> "CapabilityResult":
        """Create a result for an attempted action that did not complete."""
        return cls(
            request_id=request.request_id,
            capability=request.capability,
            action=request.action,
            status=CapabilityStatus.FAILED,
            message=message,
            error_code=error_code,
        )

    @classmethod
    def unsupported(
        cls,
        request: CapabilityRequest,
        message: str,
        error_code: str = "action_unsupported",
    ) -> "CapabilityResult":
        """Create a result for an action the selected capability does not support."""
        return cls(
            request_id=request.request_id,
            capability=request.capability,
            action=request.action,
            status=CapabilityStatus.UNSUPPORTED,
            message=message,
            error_code=error_code,
        )
