"""unittest module"""
import os
import uuid
from unittest import TestCase, main

from pymeter.api.config import (
    SetupThreadGroup,
    TeardownThreadGroup,
    TestPlan,
    ThreadGroupSimple,
    ThreadGroupWithRampUpAndHold,
)
from pymeter.api.reporters import HtmlReporter
from pymeter.api.samplers import DummySampler, HttpSampler


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

    def test_creation_of_test_plan_with_valid_children_out_of_constructor(self):
        """When children are passed through,
        result should still be a dsl test plan class"""
        tg1 = ThreadGroupWithRampUpAndHold(10, 10, 10)
        tg2 = ThreadGroupWithRampUpAndHold(10, 10, 10)
        test_plan = TestPlan()
        test_plan.children(tg1, tg2)

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

    def test_creation_of_test_plan_with_invalid_children_out_of_constructor(self):
        """Children must be of type TestPlanChildElement,
        in any other case, should through `TypeError`"""
        with self.assertRaises(TypeError) as exp:
            test_plan = TestPlan()
            test_plan.children(1,2,"aa")
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
        tg1 = ThreadGroupWithRampUpAndHold(10, 1, 5, http_sampler)
        test_plan = TestPlan(tg1)
        stats = test_plan.run()
        self.assertEqual(
            test_plan.get_java_class_name(),
            "us.abstracta.jmeter.javadsl.core.DslTestPlan",
        )
        self.assertGreaterEqual(stats.duration_milliseconds, 5000)
        self.assertLessEqual(
            stats.sample_time_mean_milliseconds, stats.sample_time_max_milliseconds
        )
        self.assertLessEqual(
            stats.sample_time_min_milliseconds, stats.sample_time_median_milliseconds
        )
        self.assertLessEqual(
            stats.sample_time_median_milliseconds,
            stats.sample_time_90_percentile_milliseconds,
        )
        # self.assertLessEqual(
        #     stats.sample_time_90_percentile_milliseconds,
        #     stats.sample_time_95_percentile_milliseconds,
        # )
        # self.assertLessEqual(
        #     stats.sample_time_95_percentile_milliseconds,
        #     stats.sample_time_99_percentile_milliseconds,
        # )
        self.assertLessEqual(
            stats.sample_time_99_percentile_milliseconds,
            stats.sample_time_max_milliseconds,
        )

    def test_run_empty_flow(self):
        """should run test flow with no exceptions"""
        tg1 = ThreadGroupWithRampUpAndHold(1, 1, 1)
        test_plan = TestPlan(tg1)
        test_plan.run()

    def test_run_validate_order(self):
        """should run test flow with no exceptions"""

        dummy_sampler_for_setup = DummySampler("dummy_setup", "hi dummy")
        dummy_sampler_for_main = DummySampler("dummy_main", "hi dummy")
        dummy_sampler_for_teardown = DummySampler("dummy_teardown", "hi dummy")
        tg_setup = SetupThreadGroup(dummy_sampler_for_setup)
        tg_main = ThreadGroupSimple(1, 1, dummy_sampler_for_main)
        tg_teardown = TeardownThreadGroup(dummy_sampler_for_teardown)
        output_dir = os.path.join("output", str(uuid.uuid4()))
        html_reporter = HtmlReporter(output_dir)
        test_plan = TestPlan(tg_setup, tg_main, tg_teardown, html_reporter)
        test_plan.run()

        path_to_jtl = os.path.join(output_dir, "report.jtl")
        with open(path_to_jtl, "r", encoding="utf-8") as jtl_file:
            next(jtl_file)
            lst = [line.split(",")[2] for line in jtl_file]
            self.assertListEqual(["dummy_setup", "dummy_main", "dummy_teardown"], lst)


if __name__ == "__main__":
    main()
