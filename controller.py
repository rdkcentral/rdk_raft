"""Registry-based entry point for migrated host controllers."""

from collections.abc import Callable
from typing import Any, ClassVar


ControllerFactory = Callable[..., object]


class Controller:
    """Create migrated controllers without wrapping their public APIs."""

    _factories: ClassVar[dict[str, ControllerFactory]] = {}

    @classmethod
    def register(cls, name: str, factory: ControllerFactory) -> None:
        if name in cls._factories:
            raise ValueError(f"Controller already registered: {name}")
        cls._factories[name] = factory

    @classmethod
    def create(cls, name: str, /, *args: Any, **kwargs: Any) -> object:
        try:
            factory = cls._factories[name]
        except KeyError as error:
            available = ", ".join(sorted(cls._factories))
            raise ValueError(
                f"Unknown controller: {name}. Available controllers: {available}"
            ) from error
        return factory(*args, **kwargs)

    @classmethod
    def available(cls) -> tuple[str, ...]:
        return tuple(sorted(cls._factories))

    @classmethod
    def boot(
        cls, log: Any, platform: str, session: Any = None, control_port: int = 8080
    ) -> object:
        return cls.create("boot", log, platform, session, control_port)

    @classmethod
    def firmware_update(
        cls, session: Any, prompt: str = "~#", port: int = 8087
    ) -> object:
        return cls.create("firmware_update", session, prompt, port)

    @classmethod
    def deep_sleep(
        cls,
        mode: str,
        session: Any,
        process_name: str = "",
        bin_path: str = "",
        prompt: str = "~#",
        port: int = 8080,
    ) -> object:
        return cls.create(
            "deep_sleep", mode, session, process_name, bin_path, prompt, port
        )

    @classmethod
    def composite_input(cls, log: Any, config: dict[str, Any]) -> object:
        return cls.create("composite_input", log, config)

    @classmethod
    def hdmi_input(cls, log: Any, config: dict[str, Any]) -> object:
        return cls.create("hdmi_input", log, config)

    @classmethod
    def hdmi_output(cls, log: Any, config: dict[str, Any]) -> object:
        return cls.create("hdmi_output", log, config)

    @classmethod
    def motion_sensor(
        cls, platform: str, session: Any, prompt: str = "~#", port: int = 8080
    ) -> object:
        return cls.create("motion_sensor", platform, session, prompt, port)

    @classmethod
    def thermal_sensor(
        cls, platform: str, session: Any, prompt: str = "~#", port: int = 8080
    ) -> object:
        return cls.create("thermal_sensor", platform, session, prompt, port)