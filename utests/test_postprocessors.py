"""unittest module"""
import os
from unittest import TestCase, main
import uuid
from pymeter.api.config import TestPlan, ThreadGroupSimple
from pymeter.api.postprocessors import JsonExtractor
from pymeter.api.reporters import HtmlReporter
from pymeter.api.samplers import DummySampler, HttpSampler


class TestSampler(TestCase):
    """Testing creation of a http sampler object"""

    def test_http_sampler(self):
        """send request to postman echo"""
        json_extractor = JsonExtractor("variable", "args.var")
        http_sampler = HttpSampler(
            "Echo", "https://postman-echo.com/get?var=1", json_extractor
        )
        dummy_sampler = DummySampler("dummy ${variable}", "hi dummy")
        tg1 = ThreadGroupSimple(1, 1, http_sampler, dummy_sampler)
        output_dir = os.path.join("output", str(uuid.uuid4()))
        html_reporter = HtmlReporter(output_dir)
        test_plan = TestPlan(tg1, html_reporter)
        test_plan.run()
        self.assertEqual(
            json_extractor.get_java_class_name(),
            "us.abstracta.jmeter.javadsl.core.postprocessors.DslJsonExtractor",
        )
        path_to_jtl = os.path.join(output_dir, "report.jtl")
        with open(path_to_jtl, "r", encoding="utf-8") as jtl_file:
            next(jtl_file)
            self.assertIn("dummy 1", [line.split(",")[2] for line in jtl_file])

    def test_postprocessor_on_thread_group(self):
        json_extractor = JsonExtractor("variable", "args.var")


        dummy_sampler = DummySampler("dummy", "hi dummy")
        
        tg1 = ThreadGroupSimple(1, 1, dummy_sampler, json_extractor)
        test_plan = TestPlan(tg1)
        test_plan.run()

if __name__ == "__main__":
    main()
