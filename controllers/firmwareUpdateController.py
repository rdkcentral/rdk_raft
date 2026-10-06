"""Public firmware-update controller."""

from .firmwareUpdateModules.virtualFirmwareUpdate import virtualFirmwareUpdate


class FirmwareUpdateController(virtualFirmwareUpdate):
    """Expose the existing virtual firmware-update implementation."""
