"""unittest module"""
from unittest import TestCase, main
from pymeter.api.config import TestPlan, ThreadGroupWithRampUpAndHold
from pymeter.api.samplers import HttpSampler


class TestTestPlanClass(TestCase):
    """Testing creation of a test plan object"""

    def test_creation_of_empty_test_plan(self):
        """when creating the python class, it should wrap around the correct java class"""
        python_test_plan_object = TestPlan()
        self.assertEqual(
            python_test_plan_object.get_java_class_name(),
            "us.abstracta.jmeter.javadsl.core.DslTestPlan",
        )

    def test_creation_of_test_plan_with_valid_children(self):
        """When children are passed through,
        result should still be a dsl test plan class"""
        tg1 = ThreadGroupWithRampUpAndHold(10, 10, 10)
        tg2 = ThreadGroupWithRampUpAndHold(10, 10, 10)
        test_plan = TestPlan(tg1, tg2)
        self.assertEqual(
            test_plan.get_java_class_name(),
            "us.abstracta.jmeter.javadsl.core.DslTestPlan",
        )

    def test_creation_of_test_plan_with_invalid_children(self):
        """Children must be of type TestPlanChildElement,
        in any other case, should through `TypeError`"""
        with self.assertRaises(TypeError) as exp:
            test_plan = TestPlan(1, "aaa")
            self.assertEqual(
                test_plan.get_java_class_name(),
                "us.abstracta.jmeter.javadsl.core.DslTestPlan",
            )
        self.assertEqual(
            str(exp.exception),
            "only takes children of type `TestPlanChildElement`",
        )

    def test_run_positive_flow(self):
        """should run test flow with no exceptions"""
        http_sampler = HttpSampler("Echo", "https://postman-echo.com/get?var=1")
        tg1 = ThreadGroupWithRampUpAndHold(10, 1, 3, http_sampler)
        test_plan = TestPlan(tg1)
        stats = test_plan.run()
        self.assertEqual(
            test_plan.get_java_class_name(),
            "us.abstracta.jmeter.javadsl.core.DslTestPlan",
        )
        self.assertGreaterEqual(stats.duration_milliseconds, 3000)
        self.assertLessEqual(stats.sample_time_mean_milliseconds, stats.sample_time_max_milliseconds)
        self.assertLessEqual(
            stats.sample_time_min_milliseconds, stats.sample_time_median_milliseconds
        )
        self.assertLessEqual(
            stats.sample_time_median_milliseconds,
            stats.sample_time_90_percentile_milliseconds,
        )
        self.assertLessEqual(
            stats.sample_time_90_percentile_milliseconds,
            stats.sample_time_95_percentile_milliseconds,
        )
        self.assertLessEqual(
            stats.sample_time_95_percentile_milliseconds,
            stats.sample_time_99_percentile_milliseconds,
        )
        self.assertLessEqual(
            stats.sample_time_95_percentile_milliseconds,
            stats.sample_time_max_milliseconds,
        )


if __name__ == "__main__":
    main()
