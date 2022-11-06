"""unittest module"""
import os
import uuid
from unittest import TestCase, main
from collections import Counter
from pymeter.api import ChildrenAreNotAllowed
from pymeter.api.config import (
    TestPlan,
    ThreadGroupSimple,
    Vars,
)
from pymeter.api.reporters import HtmlReporter
from pymeter.api.samplers import HttpSampler


class TestVars(TestCase):
    """Testing vars"""

    def test_vars_children(self):
        with self.assertRaises(ChildrenAreNotAllowed) as exp:
            Vars().children()
        self.assertEqual(
            str(exp.exception),
            "Cant append children to vars",
        )

    def test_vars_set_from_constructor(self):

        output_dir = os.path.join("output", str(uuid.uuid4()))
        html_reporter = HtmlReporter(output_dir)
        variables = Vars(my_id="value1")
        http_sampler1 = HttpSampler(
            "Echo_${my_id}", "https://postman-echo.com/get?var=${my_id}"
        )
        thread_group = ThreadGroupSimple(2, 1)
        thread_group.children(http_sampler1)

        test_plan = TestPlan(thread_group, html_reporter, variables)
        test_plan.run()

        self.assertTrue(os.path.exists(output_dir))
        path_to_jtl = os.path.join(output_dir, "report.jtl")
        with open(path_to_jtl, "r", encoding="utf-8") as jtl_file:
            next(jtl_file)
            all_samplers = [line.split(",")[2] for line in jtl_file]
            cntr = Counter(all_samplers)
            self.assertDictEqual({"Echo_value1": 2}, cntr)

    def test_vars_set_from_set_method(self):

        output_dir = os.path.join("output", str(uuid.uuid4()))
        html_reporter = HtmlReporter(output_dir)
        variables = Vars()
        variables.set("my_id", "value1")
        http_sampler1 = HttpSampler(
            "Echo_${my_id}", "https://postman-echo.com/get?var=${my_id}"
        )
        thread_group = ThreadGroupSimple(2, 1)
        thread_group.children(http_sampler1)

        test_plan = TestPlan(thread_group, html_reporter, variables)
        test_plan.run()

        self.assertTrue(os.path.exists(output_dir))
        path_to_jtl = os.path.join(output_dir, "report.jtl")
        with open(path_to_jtl, "r", encoding="utf-8") as jtl_file:
            next(jtl_file)
            all_samplers = [line.split(",")[2] for line in jtl_file]
            cntr = Counter(all_samplers)
            self.assertDictEqual({"Echo_value1": 2}, cntr)

    def test_vars_value_is_int(self):

        output_dir = os.path.join("output", str(uuid.uuid4()))
        html_reporter = HtmlReporter(output_dir)
        variables = Vars()
        variables.set("my_id", 1)
        http_sampler1 = HttpSampler(
            "Echo_${my_id}", "https://postman-echo.com/get?var=${my_id}"
        )
        thread_group = ThreadGroupSimple(2, 1)
        thread_group.children(http_sampler1)

        test_plan = TestPlan(thread_group, html_reporter, variables)
        test_plan.run()

        self.assertTrue(os.path.exists(output_dir))
        path_to_jtl = os.path.join(output_dir, "report.jtl")
        with open(path_to_jtl, "r", encoding="utf-8") as jtl_file:
            next(jtl_file)
            all_samplers = [line.split(",")[2] for line in jtl_file]
            cntr = Counter(all_samplers)
            self.assertDictEqual({"Echo_1": 2}, cntr)

    def test_vars_value_is_stringable_class(self):
        class C:
            def __repr__(self) -> str:
                return "hello"

        output_dir = os.path.join("output", str(uuid.uuid4()))
        html_reporter = HtmlReporter(output_dir)
        variables = Vars()
        variables.set("my_id", C())
        http_sampler1 = HttpSampler(
            "Echo_${my_id}", "https://postman-echo.com/get?var=${my_id}"
        )
        thread_group = ThreadGroupSimple(2, 1)
        thread_group.children(http_sampler1)

        test_plan = TestPlan(thread_group, html_reporter, variables)
        test_plan.run()

        self.assertTrue(os.path.exists(output_dir))
        path_to_jtl = os.path.join(output_dir, "report.jtl")
        with open(path_to_jtl, "r", encoding="utf-8") as jtl_file:
            next(jtl_file)
            all_samplers = [line.split(",")[2] for line in jtl_file]
            cntr = Counter(all_samplers)
            self.assertDictEqual({"Echo_hello": 2}, cntr)

    def test_vars_illegal_key_type(self):

        with self.assertRaises(TypeError) as exp:
            variables = Vars()
            variables.set(1, "value1")

        self.assertEqual(str(exp.exception), "Keys must be strings")


if __name__ == "__main__":
    main()
