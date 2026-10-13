# RDK RAFT Controllers

`rdk_raft` provides the RDK-specific controller implementations and a single
`Controller` facade for selecting controllers from test code. The facade keeps
controller construction consistent while returning the underlying controller
instance unchanged.

## Available Controllers

The registered controller names are:

- `boot`
- `firmware_update`
- `deep_sleep`
- `composite_input`
- `hdmi_input`
- `hdmi_output`
- `motion_sensor`
- `thermal_sensor`

## Usage

Import the facade from the installed `rdk_raft` package:

```python
from rdk_raft.controller import Controller

boot_controller = Controller.boot(
	log,
	platform,
	session=session,
	control_port=8080,
)

hdmi_controller = Controller.hdmi_input(log, hdmi_config)
deep_sleep_controller = Controller.deep_sleep(mode, session, port=8080)
```

For dynamic selection, use `create()`:

```python
controller = Controller.create("motion_sensor", platform, session)
```

Use `Controller.available()` to inspect the registered names. The facade
constructors preserve the public constructor arguments of each controller.

## Tests

`test_controller.py` contains unit tests for the facade registry. It verifies
factory registration, duplicate-registration errors, sorted controller names,
argument forwarding, and unknown-controller errors.

Run it from the unified VTS repository with:

```bash
base=/path/to/rdk-halif-aidl-unified-vts/host/tests
cd "$base/rdk_raft"
PYTHONPATH="$base:$base/raft:$base/rdk_raft" \
python3 -m unittest test_controller
```
