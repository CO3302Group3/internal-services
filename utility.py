"""Shared HTTP utilities for selected internal microservices."""

import logging
import os
from typing import Any, Dict, Optional, Union

import httpx

logger = logging.getLogger(__name__)


class ServiceClient:
    """Minimal async HTTP client wrapper."""

    def __init__(self, base_url: str, timeout: float = 30.0):
        if not base_url:
            raise ValueError("base_url is required")
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._client = httpx.AsyncClient(base_url=self.base_url, timeout=timeout)

    @staticmethod
    def _normalise(endpoint: str) -> str:
        return endpoint if endpoint.startswith("/") else f"/{endpoint}"

    async def get(self, endpoint: str, **kwargs) -> httpx.Response:
        path = self._normalise(endpoint)
        logger.info("GET %s%s", self.base_url, path)
        return await self._client.get(path, **kwargs)

    async def post(self, endpoint: str, **kwargs) -> httpx.Response:
        path = self._normalise(endpoint)
        logger.info("POST %s%s", self.base_url, path)
        return await self._client.post(path, **kwargs)

    async def put(self, endpoint: str, **kwargs) -> httpx.Response:
        path = self._normalise(endpoint)
        logger.info("PUT %s%s", self.base_url, path)
        return await self._client.put(path, **kwargs)

    async def delete(self, endpoint: str, **kwargs) -> httpx.Response:
        path = self._normalise(endpoint)
        logger.info("DELETE %s%s", self.base_url, path)
        return await self._client.delete(path, **kwargs)

    async def close(self) -> None:
        await self._client.aclose()


def _normalise_token_payload(token: Union[str, Dict[str, Any]]) -> Dict[str, Any]:
    if isinstance(token, str):
        return {"token": token}
    if isinstance(token, dict):
        if "token" in token:
            return {"token": token["token"]}
        return token
    raise TypeError("token must be a str or dict with token information")


class AdminManagementService:
    """Client helpers for the Admin Management microservice endpoints."""

    def __init__(self, base_url: Optional[str] = None, timeout: float = 30.0):
        service_url = base_url or os.getenv(
            "ADMIN_MANAGEMENT_SERVICE_URL",
            "http://admin-management-service:8000",
        )
        self.client = ServiceClient(service_url, timeout=timeout)

    async def register_admin(self, admin_data: Dict[str, Any]) -> httpx.Response:
        return await self.client.post("/register_admin", json=admin_data)

    async def get_all_non_staff(self, token: Union[str, Dict[str, Any]]) -> httpx.Response:
        payload = _normalise_token_payload(token)
        return await self.client.post("/get_all_non_staff", json=payload)

    async def change_account_status(
        self,
        token: Union[str, Dict[str, Any]],
        user_email: str,
        new_status: str,
    ) -> httpx.Response:
        payload = _normalise_token_payload(token)
        return await self.client.post(
            "/change_account_status",
            params={"user_email": user_email, "new_status": new_status},
            json=payload,
        )

    async def health_check(self) -> httpx.Response:
        return await self.client.get("/health")

    async def close(self) -> None:
        await self.client.close()


class AlertAndEventProcessingService:
    """Client helpers for the Alert and Event Processing microservice."""

    def __init__(self, base_url: Optional[str] = None, timeout: float = 30.0):
        service_url = base_url or os.getenv(
            "ALERT_EVENT_PROCESSING_SERVICE_URL",
            "http://alert-event-processing-service:8000",
        )
        self.client = ServiceClient(service_url, timeout=timeout)

    async def root(self) -> httpx.Response:
        return await self.client.get("/")

    async def health_check(self) -> httpx.Response:
        return await self.client.get("/health")

    async def close(self) -> None:
        await self.client.close()


class DeviceCommandService:
    """Client helpers for the Device Command microservice."""

    def __init__(self, base_url: Optional[str] = None, timeout: float = 30.0):
        service_url = base_url or os.getenv(
            "DEVICE_COMMAND_SERVICE_URL",
            "http://device-command-service:8000",
        )
        self.client = ServiceClient(service_url, timeout=timeout)

    async def health_check(self) -> httpx.Response:
        return await self.client.get("/health")

    async def add_command(self, command_data: Dict[str, Any]) -> httpx.Response:
        return await self.client.post("/add_command", json=command_data)

    async def get_commands(self, device_id: str) -> httpx.Response:
        return await self.client.get(f"/commands/{device_id}")

    async def delete_commands(self, device_id: str) -> httpx.Response:
        return await self.client.delete(f"/commands/delete/{device_id}")

    async def close(self) -> None:
        await self.client.close()


class DeviceOnboardingService:
    """Client helpers for the Device Onboarding microservice."""

    def __init__(self, base_url: Optional[str] = None, timeout: float = 30.0):
        service_url = base_url or os.getenv(
            "DEVICE_ONBOARDING_SERVICE_URL",
            "http://device-onboarding-service:8000",
        )
        self.client = ServiceClient(service_url, timeout=timeout)

    async def health_check(self) -> httpx.Response:
        return await self.client.get("/health")

    async def add_new_device(self, device_data: Dict[str, Any]) -> httpx.Response:
        return await self.client.post("/add_new_device", json=device_data)

    async def get_my_devices(self, user_id: Union[int, str]) -> httpx.Response:
        return await self.client.get(f"/get_my_devices/{user_id}")

    async def get_user_id_by_device_id(self, device_id: str) -> httpx.Response:
        return await self.client.get(f"/get_user_id_by_device_id/{device_id}")

    async def close(self) -> None:
        await self.client.close()


class DeviceTelemetryService:
    """Client helpers for the Device Telemetry microservice."""

    def __init__(self, base_url: Optional[str] = None, timeout: float = 30.0):
        service_url = base_url or os.getenv(
            "DEVICE_TELEMETRY_SERVICE_URL",
            "http://device-telemetry-service:8000",
        )
        self.client = ServiceClient(service_url, timeout=timeout)

    async def health_check(self) -> httpx.Response:
        return await self.client.get("/health")

    async def get_latest(self, device_id: str) -> httpx.Response:
        return await self.client.get(f"/latest/{device_id}")

    async def get_device_status(self, device_id: str) -> httpx.Response:
        return await self.client.get(f"/device/status/{device_id}")

    async def close(self) -> None:
        await self.client.close()


class HealthMonitoringService:
    """Client helpers for the Health Monitoring microservice."""

    def __init__(self, base_url: Optional[str] = None, timeout: float = 30.0):
        service_url = base_url or os.getenv(
            "HEALTH_MONITORING_SERVICE_URL",
            "http://health-monitoring-service:8000",
        )
        self.client = ServiceClient(service_url, timeout=timeout)

    async def health_check(self) -> httpx.Response:
        return await self.client.get("/health")

    async def get_latest_health(self, device_id: str) -> httpx.Response:
        return await self.client.get(f"/{device_id}/latest")

    async def close(self) -> None:
        await self.client.close()


class NotificationMicroserviceService:
    """Client helpers for the Notification microservice."""

    def __init__(self, base_url: Optional[str] = None, timeout: float = 30.0):
        service_url = base_url or os.getenv(
            "NOTIFICATION_SERVICE_URL",
            "http://notification-service:8000",
        )
        self.client = ServiceClient(service_url, timeout=timeout)

    async def root(self) -> httpx.Response:
        return await self.client.get("/")

    async def health_check(self) -> httpx.Response:
        return await self.client.get("/health")

    async def close(self) -> None:
        await self.client.close()


class ParkingSlotService:
    """Client helpers for the Parking Slot microservice."""

    def __init__(self, base_url: Optional[str] = None, timeout: float = 30.0):
        service_url = base_url or os.getenv(
            "PARKING_SLOT_SERVICE_URL",
            "http://parking-slot-service:8000",
        )
        self.client = ServiceClient(service_url, timeout=timeout)

    async def create_parking_slot(
        self,
        slot_data: Dict[str, Any],
        token: Union[str, Dict[str, Any]],
    ) -> httpx.Response:
        payload = _normalise_token_payload(token)
        body = {"payload": slot_data, "authorization": payload}
        return await self.client.post("/parking_slots", json=body)

    async def list_parking_slots(self, status: Optional[str] = None) -> httpx.Response:
        params = {"status": status} if status else None
        return await self.client.get("/parking_slots", params=params)

    async def get_parking_slot(self, slot_id: str) -> httpx.Response:
        return await self.client.get(f"/parking_slots/{slot_id}")

    async def update_parking_slot(
        self,
        slot_id: str,
        updates: Dict[str, Any],
        token: Union[str, Dict[str, Any]],
    ) -> httpx.Response:
        payload = _normalise_token_payload(token)
        body = {"payload": updates, "authorization": payload}
        return await self.client.put(f"/parking_slots/{slot_id}", json=body)

    async def delete_parking_slot(
        self,
        slot_id: str,
        token: Union[str, Dict[str, Any]],
    ) -> httpx.Response:
        payload = _normalise_token_payload(token)
        body = {"authorization": payload}
        return await self.client.delete(f"/parking_slots/{slot_id}", json=body)

    async def assign_parking_slot(
        self,
        slot_id: str,
        assignment: Dict[str, Any],
        token: Union[str, Dict[str, Any]],
    ) -> httpx.Response:
        payload = _normalise_token_payload(token)
        body = {"body": assignment, "authorization": payload}
        return await self.client.post(f"/parking_slots/{slot_id}/assign", json=body)

    async def release_parking_slot(
        self,
        slot_id: str,
        token: Union[str, Dict[str, Any]],
    ) -> httpx.Response:
        payload = _normalise_token_payload(token)
        body = {"authorization": payload}
        return await self.client.post(f"/parking_slots/{slot_id}/release", json=body)

    async def close(self) -> None:
        await self.client.close()


class UserAuthenticationService:
    """Client helpers for the User Authentication microservice."""

    def __init__(self, base_url: Optional[str] = None, timeout: float = 30.0):
        service_url = base_url or os.getenv(
            "USER_AUTH_SERVICE_URL",
            "http://user-auth-service:8000",
        )
        self.client = ServiceClient(service_url, timeout=timeout)

    async def health_check(self) -> httpx.Response:
        return await self.client.get("/health")

    async def register_user(self, user_data: Dict[str, Any]) -> httpx.Response:
        return await self.client.post("/register", json=user_data)

    async def login_user(self, credentials: Union[Dict[str, Any], httpx.Auth, Any]) -> httpx.Response:
        auth_obj: httpx.Auth
        if isinstance(credentials, httpx.Auth):
            auth_obj = credentials
        elif hasattr(credentials, "username") and hasattr(credentials, "password"):
            auth_obj = httpx.BasicAuth(credentials.username, credentials.password)
        elif isinstance(credentials, dict):
            email = credentials.get("email") or credentials.get("username")
            password = credentials.get("password")
            if not email or not password:
                raise ValueError("Credentials must include email/username and password")
            auth_obj = httpx.BasicAuth(email, password)
        else:
            raise TypeError("Unsupported credentials type for login_user")
        return await self.client.post("/login", auth=auth_obj)

    async def validate_token(self, token: Union[str, Dict[str, Any]]) -> httpx.Response:
        payload = _normalise_token_payload(token)
        return await self.client.post("/validate", json=payload)

    async def get_user(self, user_id: Union[int, str]) -> httpx.Response:
        return await self.client.get(f"/user/{user_id}")

    async def make_admin(self, user_id: Union[int, str]) -> httpx.Response:
        return await self.client.post(f"/user/{user_id}/make_admin")

    async def get_all_non_staff(self, token: Union[str, Dict[str, Any]]) -> httpx.Response:
        payload = _normalise_token_payload(token)
        return await self.client.post("/users/non_staff", json=payload)

    async def change_account_status(
        self,
        token: Union[str, Dict[str, Any]],
        target_user_email: str,
        new_status: str,
    ) -> httpx.Response:
        payload = _normalise_token_payload(token)
        return await self.client.post(
            "/change_account_status",
            params={"target_user_email": target_user_email, "new_status": new_status},
            json=payload,
        )

    async def close(self) -> None:
        await self.client.close()





    

