# internal-services

Lightweight async HTTP clients that wrap the internal microservice APIs used across the CO330 platform.  The package keeps each microservice client in a single place so individual services can avoid duplicating boilerplate when they need to talk to each other.

## Installation

```bash
pip install git+https://github.com/CO3302Group3/internal-services.git@v0.1.0
```

For private repositories, provide an access token or use SSH.

## Usage

```python
from internal_services import DeviceOnboardingService

service = DeviceOnboardingService()
response = await service.get_my_devices(user_id="42")
print(response.json())
```

Each client exposes async helpers for the REST endpoints exposed by its microservice.  All clients share the `ServiceClient` wrapper, which handles base URLs, logging, and basic HTTP verbs.

## Development

```bash
pip install -e .
```

Run formatting and type checks before opening a PR.  The project has no additional runtime dependencies beyond `httpx`.
