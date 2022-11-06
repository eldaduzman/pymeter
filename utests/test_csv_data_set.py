"""unittest module"""
import os
import uuid
from unittest import TestCase, main
from collections import Counter
from pymeter.api import ChildrenAreNotAllowed
from pymeter.api.config import (
    TestPlan,
    ThreadGroupSimple,
    CsvDataset,
)
from pymeter.api.reporters import HtmlReporter
from pymeter.api.samplers import HttpSampler


CSV_FILE_PATH = "utests/resources/test_data.csv"

class TestCsvDataSet(TestCase):
    """Testing csv data sets"""

    def test_csv_data_set_children(self):
        with self.assertRaises(ChildrenAreNotAllowed) as exp:
            CsvDataset(CSV_FILE_PATH).children()
        self.assertEqual(
            str(exp.exception),
            "Cant append children to a csv_data_set",
        )

    def test_csv_data_set_file_not_found(self):
        with self.assertRaises(FileNotFoundError) as exp:
            CsvDataset("dosntexist.csv").children()
        self.assertEqual(
            str(exp.exception),
            "Couldn't find file dosntexist.csv",
        )

    def test_data_set_for_entire_test_plan(self):

        output_dir = os.path.join("output", str(uuid.uuid4()))
        html_reporter = HtmlReporter(output_dir)
        csv_data_set = CsvDataset(CSV_FILE_PATH)
        http_sampler1 = HttpSampler(
            "Echo_${id}", "https://postman-echo.com/get?var=${id}"
        )
        thread_group1 = ThreadGroupSimple(3, 1)
        thread_group1.children(http_sampler1)

        http_sampler2 = HttpSampler("Echo_${id}", "https://postman-echo.com/get?var=do")
        thread_group2 = ThreadGroupSimple(3, 1, http_sampler2)
        test_plan = TestPlan(thread_group1, thread_group2, html_reporter, csv_data_set)
        test_plan.run()

        self.assertTrue(os.path.exists(output_dir))
        path_to_jtl = os.path.join(output_dir, "report.jtl")
        with open(path_to_jtl, "r", encoding="utf-8") as jtl_file:
            next(jtl_file)
            all_samplers = [line.split(",")[2] for line in jtl_file]
            cntr = Counter(all_samplers)

            self.assertDictEqual({"Echo_2": 2, "Echo_3": 2, "Echo_1": 2}, cntr)

    def test_data_set_for_only_one_thread_group(self):

        output_dir = os.path.join("output", str(uuid.uuid4()))
        html_reporter = HtmlReporter(output_dir)
        csv_data_set = CsvDataset(CSV_FILE_PATH)
        http_sampler1 = HttpSampler(
            "Echo_${id}", "https://postman-echo.com/get?var=${id}"
        )
        thread_group1 = ThreadGroupSimple(3, 1)
        thread_group1.children(http_sampler1, csv_data_set)

        http_sampler2 = HttpSampler("Echo_${id}", "https://postman-echo.com/get?var=do")
        thread_group2 = ThreadGroupSimple(3, 1, http_sampler2)
        test_plan = TestPlan(thread_group1, thread_group2, html_reporter)
        test_plan.run()

        self.assertTrue(os.path.exists(output_dir))
        path_to_jtl = os.path.join(output_dir, "report.jtl")
        with open(path_to_jtl, "r", encoding="utf-8") as jtl_file:
            next(jtl_file)
            all_samplers = [line.split(",")[2] for line in jtl_file]
            cntr = Counter(all_samplers)
            self.assertDictEqual(
                {"Echo_${id}": 3, "Echo_2": 1, "Echo_3": 1, "Echo_1": 1}, cntr
            )

    def test_data_set_too_small(self):

        output_dir = os.path.join("output", str(uuid.uuid4()))
        html_reporter = HtmlReporter(output_dir)
        csv_data_set = CsvDataset(CSV_FILE_PATH)
        http_sampler1 = HttpSampler(
            "Echo_${id}", "https://postman-echo.com/get?var=${id}"
        )
        thread_group = ThreadGroupSimple(6, 1)
        thread_group.children(http_sampler1, csv_data_set)


        test_plan = TestPlan(thread_group, html_reporter)
        test_plan.run()

        self.assertTrue(os.path.exists(output_dir))
        path_to_jtl = os.path.join(output_dir, "report.jtl")
        with open(path_to_jtl, "r", encoding="utf-8") as jtl_file:
            next(jtl_file)
            all_samplers = [line.split(",")[2] for line in jtl_file]
            cntr = Counter(all_samplers)
            self.assertDictEqual(
                {'Echo_3': 2, 'Echo_1': 2, 'Echo_2': 2}, cntr
            )
    def test_data_set_too_big(self):

        output_dir = os.path.join("output", str(uuid.uuid4()))
        html_reporter = HtmlReporter(output_dir)
        csv_data_set = CsvDataset(CSV_FILE_PATH)
        http_sampler1 = HttpSampler(
            "Echo_${id}", "https://postman-echo.com/get?var=${id}"
        )
        thread_group = ThreadGroupSimple(2, 1)
        thread_group.children(http_sampler1)


        test_plan = TestPlan(thread_group, html_reporter, csv_data_set)
        test_plan.run()

        self.assertTrue(os.path.exists(output_dir))
        path_to_jtl = os.path.join(output_dir, "report.jtl")
        with open(path_to_jtl, "r", encoding="utf-8") as jtl_file:
            next(jtl_file)
            all_samplers = [line.split(",")[2] for line in jtl_file]
            cntr = Counter(all_samplers)
            self.assertDictEqual(
                {'Echo_1': 1, 'Echo_2': 1}, cntr
            )


if __name__ == "__main__":
    main()
