"""unittest module"""
from unittest import TestCase, main
from pymeter.api import ChildrenAreNotAllowed
from pymeter.api.config import TestPlan, ThreadGroupSimple
from pymeter.api.samplers import HttpSampler
from pymeter.api.timers import UniformRandomTimer, ConstantTimer


class TestTimer(TestCase):
    """Testing creation of a uniform random timer object"""

    def test_timer_children(self):
        with self.assertRaises(ChildrenAreNotAllowed) as exp:
            UniformRandomTimer(2000, 2200).children()
        self.assertEqual(
            str(exp.exception),
            "Cant append children to a timer",
        )
    def test_uniform_random_timer(self):
        """When the minimal time is 5000 milliseconds,
        the total test duration is expected to be at least that."""
        timer = UniformRandomTimer(2000, 2200)
        http_sampler = HttpSampler("Echo", "https://postman-echo.com/get?var=1", timer)
        tg1 = ThreadGroupSimple(1, 1, http_sampler)
        test_plan = TestPlan(tg1)
        stats = test_plan.run()
        self.assertEqual(
            timer.get_java_class_name(),
            "us.abstracta.jmeter.javadsl.core.timers.DslUniformRandomTimer",
        )
        self.assertEqual(
            stats.get_java_class_name(),
            "us.abstracta.jmeter.javadsl.core.TestPlanStats",
        )
        self.assertGreaterEqual(stats.duration_milliseconds, 2000)

    def test_constant_timer(self):
        """When the minimal time is 5000 milliseconds,
        the total test duration is expected to be at least that."""
        timer = ConstantTimer(2000)
        http_sampler = HttpSampler("Echo", "https://postman-echo.com/get?var=1", timer)
        tg1 = ThreadGroupSimple(1, 1, http_sampler)
        test_plan = TestPlan(tg1)
        stats = test_plan.run()
        self.assertEqual(
            timer.get_java_class_name(),
            "us.abstracta.jmeter.javadsl.core.timers.DslConstantTimer",
        )
        self.assertEqual(
            stats.get_java_class_name(),
            "us.abstracta.jmeter.javadsl.core.TestPlanStats",
        )
        self.assertGreaterEqual(stats.duration_milliseconds, 2000)


if __name__ == "__main__":
    main()
