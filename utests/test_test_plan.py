"""unittest module"""
from unittest import TestCase, main
from pymeter.api.config import TestPlan


class TestTestPlanClass(TestCase):
    """"""

    def test_creation_of_empty_test_plan(self):
        """when creating the python class, it should wrap around the correct java class"""
        python_test_plan_object = TestPlan()
        java_test_plan_object = python_test_plan_object.java_wrapped_element
        self.assertEqual(
            str(type(java_test_plan_object)),
            "<class 'jnius.reflect.us.abstracta.jmeter.javadsl.core.DslTestPlan'>",
        )


if __name__ == "__main__":
    main()
