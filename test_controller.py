import unittest

from controller import Controller


class ControllerFacadeTests(unittest.TestCase):
    def setUp(self):
        self.previous_factories = Controller._factories.copy()
        Controller._factories.clear()

    def tearDown(self):
        Controller._factories.clear()
        Controller._factories.update(self.previous_factories)

    def test_named_constructor_preserves_factory_arguments(self):
        calls = []

        def factory(*args, **kwargs):
            calls.append((args, kwargs))
            return "controller"

        Controller.register("hdmi_input", factory)

        result = Controller.hdmi_input("log", {"type": "virtual"})

        self.assertEqual(result, "controller")
        self.assertEqual(calls, [(('log', {"type": "virtual"}), {})])

    def test_available_is_sorted(self):
        Controller.register("thermal_sensor", object)
        Controller.register("boot", object)

        self.assertEqual(Controller.available(), ("boot", "thermal_sensor"))

    def test_unknown_controller_reports_available_names(self):
        Controller.register("boot", object)

        with self.assertRaisesRegex(
            ValueError, r"Unknown controller: missing\. Available controllers: boot"
        ):
            Controller.create("missing")

    def test_duplicate_registration_is_rejected(self):
        Controller.register("boot", object)

        with self.assertRaisesRegex(ValueError, "Controller already registered: boot"):
            Controller.register("boot", object)


if __name__ == "__main__":
    unittest.main()