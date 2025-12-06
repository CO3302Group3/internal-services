"""Shared service clients for internal microservices."""

from .utility import (
    AdminManagementService,
    AlertAndEventProcessingService,
    DeviceCommandService,
    DeviceOnboardingService,
    DeviceTelemetryService,
    HealthMonitoringService,
    NotificationMicroserviceService,
    ParkingSlotService,
    ServiceClient,
    UserAuthenticationService,
)

__all__ = [
    "ServiceClient",
    "AdminManagementService",
    "AlertAndEventProcessingService",
    "DeviceCommandService",
    "DeviceOnboardingService",
    "DeviceTelemetryService",
    "HealthMonitoringService",
    "NotificationMicroserviceService",
    "ParkingSlotService",
    "UserAuthenticationService",
]

__version__ = "0.1.1"
