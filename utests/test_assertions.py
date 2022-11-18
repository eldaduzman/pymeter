"""unittest module"""
import json
import os
from unittest import TestCase, main
import uuid
from pymeter.api import ChildrenAreNotAllowed
from pymeter.api.config import TestPlan, ThreadGroupSimple
from pymeter.api.postprocessors import JsonExtractor
from pymeter.api.reporters import HtmlReporter
from pymeter.api.samplers import DummySampler, HttpSampler
from pymeter.api.assertions import ResponseAssertion


class TestAssertions(TestCase):
    def test_assertion_object_creation(self):
        response_assertion = ResponseAssertion()
        self.assertEqual(
            response_assertion.get_java_class_name(),
            "us.abstracta.jmeter.javadsl.core.assertions.DslResponseAssertion",
        )

    def test_assertion_children(self):
        with self.assertRaises(ChildrenAreNotAllowed) as exp:
            ResponseAssertion().children()
        self.assertEqual(
            str(exp.exception),
            "Cant append children to assertion",
        )

    def test_assertion_object_creation_with_contains_substrings(self):
        response_assertion = ResponseAssertion().contains_substrings("var", "args")
        self.assertEqual(
            response_assertion.get_java_class_name(),
            "us.abstracta.jmeter.javadsl.core.assertions.DslResponseAssertion",
        )

    def test_assertion_object_should_pass(self):
        response_assertion = ResponseAssertion().contains_substrings("var", "args")
        output_dir = os.path.join("output", str(uuid.uuid4()))
        html_reporter = HtmlReporter(output_dir)
        http_sampler = HttpSampler(
            "Echo", "https://postman-echo.com/get?var=1", response_assertion
        )
        thread_group = ThreadGroupSimple(1, 1)
        thread_group.children(http_sampler)
        test_plan = TestPlan(thread_group, html_reporter)
        test_plan.run()
        path_to_stats = os.path.join(output_dir, "statistics.json")
        with open(path_to_stats, "r", encoding="utf-8") as stats_file:
            self.assertEqual(0, json.loads(stats_file.read())["Total"]["errorCount"])

    def test_assertion_object_should_fail(self):
        response_assertion = ResponseAssertion().contains_substrings("notfound")
        output_dir = os.path.join("output", str(uuid.uuid4()))
        html_reporter = HtmlReporter(output_dir)
        http_sampler = HttpSampler(
            "Echo", "https://postman-echo.com/get?var=1", response_assertion
        )
        thread_group = ThreadGroupSimple(1, 3)
        thread_group.children(http_sampler)
        test_plan = TestPlan(thread_group, html_reporter)
        test_plan.run()
        path_to_stats = os.path.join(output_dir, "statistics.json")
        with open(path_to_stats, "r", encoding="utf-8") as stats_file:
            self.assertEqual(3, json.loads(stats_file.read())["Total"]["errorCount"])


if __name__ == "__main__":
    main()
