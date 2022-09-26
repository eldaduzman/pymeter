"""unittest module"""
from unittest import TestCase, main
from pymeter.api.config import ThreadGroupWithRampUpAndHold
from pymeter.api.samplers import HttpSampler


class TestThreadGroupClass(TestCase):
    """Testing creation of a thread group object"""

    def test_creation_of_empty_thread_group(self):
        """when creating the python class, it should wrap around the correct java class"""
        python_thread_group_object = ThreadGroupWithRampUpAndHold(1, 1, 1)
        self.assertEqual(
            python_thread_group_object.get_java_class_name(),
            "us.abstracta.jmeter.javadsl.core.threadgroups.DslDefaultThreadGroup",
        )

    def test_creation_of_thread_group_with_valid_children(self):
        """When children are passed through,
        result should still be a dsl test plan class"""
        http_sampler = HttpSampler("sampler", "")
        python_thread_group_object = ThreadGroupWithRampUpAndHold(1, 1, 1, http_sampler)
        self.assertEqual(
            python_thread_group_object.get_java_class_name(),
            "us.abstracta.jmeter.javadsl.core.threadgroups.DslDefaultThreadGroup",
        )

    def test_creation_of_thread_group_with_invalid_children(self):
        """Children must be of type ThreadGroupChildElement,
        in any other case, should through `TypeError`"""
        with self.assertRaises(TypeError) as exp:
            python_thread_group_object = ThreadGroupWithRampUpAndHold(
                1, 1, 1, "http_sampler"
            )
            self.assertEqual(
                python_thread_group_object.get_java_class_name(),
                "us.abstracta.jmeter.javadsl.core.threadgroups.DslDefaultThreadGroup",
            )
        self.assertEqual(
            str(exp.exception),
            "only takes children of type `ThreadGroupChildElement`",
        )


if __name__ == "__main__":
    main()
