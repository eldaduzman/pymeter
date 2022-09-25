"""unittest module"""
from unittest import TestCase, main
from pymeter.api.config import TestPlan, ThreadGroupSimple
from pymeter.api.samplers import HttpSampler
from pymeter.api.timers import UniformRandomTimer


class TestTimer(TestCase):
    """Testing creation of a uniform random timer object"""

    def test_uniform_random_timer(self):
        """when creating the python class, it should wrap around the correct java class"""
        timer = UniformRandomTimer(5000, 7000)
        http_sampler = HttpSampler("Echo", "https://postman-echo.com/get?var=1", timer)
        tg1 = ThreadGroupSimple(1, 1, http_sampler)
        test_plan = TestPlan(tg1)
        stats = test_plan.run()
        self.assertEqual(
            str(type(stats.java_wrapped_element)),
            "<class 'jnius.reflect.us.abstracta.jmeter.javadsl.core.TestPlanStats'>",
        )
        self.assertGreaterEqual(stats.duration, 5000)


if __name__ == "__main__":
    main()
