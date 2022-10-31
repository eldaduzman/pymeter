"""unittest module"""
import os
import uuid
from unittest import TestCase, main

from pymeter.api import ChildrenAreNotAllowed
from pymeter.api.config import TestPlan, ThreadGroupWithRampUpAndHold
from pymeter.api.reporters import HtmlReporter
from pymeter.api.samplers import HttpSampler


class TestReporter(TestCase):
    """Testing creation of a http sampler object"""

    def test_reporter_children(self):
        with self.assertRaises(ChildrenAreNotAllowed) as exp:
            HtmlReporter().children()
        self.assertEqual(
            str(exp.exception),
            "Cant append children to a reporter",
        )

    def test_http_sampler(self):
        """create an HTML report"""
        http_sampler = HttpSampler("Echo", "https://postman-echo.com/get?var=1")
        tg = ThreadGroupWithRampUpAndHold(2, 1, 2, http_sampler, name="Some Name")
        output_dir = os.path.join("output", str(uuid.uuid4()))
        html_reporter = HtmlReporter(output_dir)
        tp = TestPlan(tg, html_reporter)
        tp.run()
        self.assertEqual(
            html_reporter.get_java_class_name(),
            "us.abstracta.jmeter.javadsl.core.listeners.HtmlReporter",
        )
        self.assertTrue(os.path.exists(output_dir))
        path_to_jtl = os.path.join(output_dir, "report.jtl")
        path_to_json = os.path.join(output_dir, "statistics.json")
        path_to_html = os.path.join(output_dir, "index.html")
        self.assertTrue(os.path.exists(path_to_jtl))
        self.assertTrue(os.path.exists(path_to_json))
        self.assertTrue(os.path.exists(path_to_html))


if __name__ == "__main__":
    main()
