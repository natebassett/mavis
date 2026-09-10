"""Unit tests for the Phase 2 capability framework contracts."""

from __future__ import annotations

from datetime import datetime
from types import MappingProxyType
import unittest

from app.capabilities import (
    Capability,
    CapabilityConfiguration,
    CapabilityContractError,
    CapabilityNotFoundError,
    CapabilityRegistrationError,
    CapabilityRegistry,
    CapabilityRequest,
    CapabilityResult,
    CapabilityStatus,
    InvalidCapabilityRequestError,
)


class EchoCapability(Capability):
    """Small test-only capability that echoes a requested value."""

    @property
    def name(self) -> str:
        return "echo"

    def execute(self, request: CapabilityRequest) -> CapabilityResult:
        return CapabilityResult.succeeded(
            request,
            "Echo completed.",
            data={"value": request.parameters.get("value")},
        )


class IncorrectResultCapability(Capability):
    """Test double that intentionally violates the result correlation contract."""

    @property
    def name(self) -> str:
        return "incorrect-result"

    def execute(self, request: CapabilityRequest) -> CapabilityResult:
        return CapabilityResult(
            request_id="different-request",
            capability=request.capability,
            action=request.action,
            status=CapabilityStatus.SUCCEEDED,
            message="Incorrect result.",
        )


class CapabilityFrameworkTests(unittest.TestCase):
    def test_request_normalises_identifiers_and_freezes_mappings(self) -> None:
        request = CapabilityRequest(
            capability="  Echo ",
            action="  Say-Value ",
            parameters={"value": "MAVIS"},
            context={"user": "Nathaniel"},
        )

        self.assertEqual("echo", request.capability)
        self.assertEqual("say-value", request.action)
        self.assertIsInstance(request.parameters, MappingProxyType)
        self.assertEqual("MAVIS", request.parameters["value"])

        with self.assertRaises(TypeError):
            request.parameters["value"] = "changed"  # type: ignore[index]

    def test_request_rejects_invalid_identifiers_and_naive_timestamps(self) -> None:
        with self.assertRaises(InvalidCapabilityRequestError):
            CapabilityRequest(capability="invalid name", action="run")

        with self.assertRaises(InvalidCapabilityRequestError):
            CapabilityRequest(
                capability="echo",
                action="run",
                requested_at=datetime.now(),
            )

    def test_result_factories_preserve_request_correlation(self) -> None:
        request = CapabilityRequest(capability="echo", action="say")
        result = CapabilityResult.succeeded(request, "Completed.")

        self.assertTrue(result.was_successful)
        self.assertEqual(CapabilityStatus.SUCCEEDED, result.status)
        self.assertEqual(request.request_id, result.request_id)
        self.assertEqual(request.capability, result.capability)
        self.assertEqual(request.action, result.action)

    def test_success_result_cannot_include_an_error_code(self) -> None:
        request = CapabilityRequest(capability="echo", action="say")

        with self.assertRaises(InvalidCapabilityRequestError):
            CapabilityResult(
                request_id=request.request_id,
                capability=request.capability,
                action=request.action,
                status=CapabilityStatus.SUCCEEDED,
                message="Completed.",
                error_code="should_not_exist",
            )

    def test_registry_registers_and_executes_a_capability(self) -> None:
        registry = CapabilityRegistry()
        registry.register(EchoCapability())
        request = CapabilityRequest(
            capability="echo",
            action="say",
            parameters={"value": "hello"},
        )

        result = registry.execute(request)

        self.assertEqual(("echo",), registry.names())
        self.assertEqual(CapabilityStatus.SUCCEEDED, result.status)
        self.assertEqual("hello", result.data["value"])

    def test_registry_rejects_duplicate_or_missing_capabilities(self) -> None:
        registry = CapabilityRegistry([EchoCapability()])

        with self.assertRaises(CapabilityRegistrationError):
            registry.register(EchoCapability())

        with self.assertRaises(CapabilityNotFoundError):
            registry.get("missing")

    def test_registry_uses_canonical_names_for_lookup_and_removal(self) -> None:
        registry = CapabilityRegistry([EchoCapability()])

        self.assertIsInstance(registry.get(" ECHO "), EchoCapability)
        registry.unregister(" ECHO ")

        self.assertEqual((), registry.names())

    def test_disabled_capability_returns_a_rejected_result(self) -> None:
        registry = CapabilityRegistry()
        registry.register(
            EchoCapability(),
            CapabilityConfiguration(capability="echo", enabled=False),
        )

        result = registry.execute(CapabilityRequest("echo", "say"))

        self.assertEqual(CapabilityStatus.REJECTED, result.status)
        self.assertEqual("capability_disabled", result.error_code)

    def test_registry_rejects_result_for_a_different_request(self) -> None:
        registry = CapabilityRegistry([IncorrectResultCapability()])

        with self.assertRaises(CapabilityContractError):
            registry.execute(
                CapabilityRequest(capability="incorrect-result", action="run")
            )


if __name__ == "__main__":
    unittest.main()
