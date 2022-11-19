"""
The config module contain classes that define the overall structure of the test script.
Here we will define the overall plan, the setup and teardown processes and the load shapes that the test script generate.

example - 1:
--------------
In this example we use the standard python unittest module with setup and teardown,
The test case it self will rump up 10 threads in 1 second and hold the load for additional 10 seconds.
Note that the setup and teardown code is executed outside of JMeter's context in this example.

      .. code-block:: python

            from unittest import TestCase, main
            from pymeter.api.config import TestPlan, ThreadGroupWithRampUpAndHold
            from pymeter.api.samplers import HttpSampler


            class TestTestPlanClass(TestCase):
                @classmethod
                def setUpClass(cls):
                    print("setUpClass")

                def test_case_1(self):
                    # create HTTP sampler, sends a get request to the given url
                    http_sampler = HttpSampler("echo_get_request", "https://postman-echo.com/get?var=1")

                    # create a thread group that will rump up 10 threads in 1 second and
                    # hold the load for additional 10 seconds, give it the http sampler as a child input
                    thread_group_main = ThreadGroupWithRampUpAndHold(10, 1, 10, http_sampler)

                    # create a test plan with the required thread group
                    test_plan = TestPlan(thread_group_main)

                    # run the test plan and take the results
                    stats = test_plan.run()
                    self.assertLess(stats.sample_time_99_percentile_milliseconds, 2000)

                @classmethod
                def tearDownClass(cls):
                    print("tearDownClass")

example - 2:
--------------
If for some reason it is needed for you to run the setup and teardown code from with in the JMeter context, here's how you can do it:
      .. code-block:: python

            from pymeter.api.config import TestPlan, ThreadGroupWithRampUpAndHold, SetupThreadGroup, TeardownThreadGroup
            from pymeter.api.samplers import HttpSampler


            # create HTTP sampler, sends a get request to the given url
            http_sampler1 = HttpSampler("echo_get_request", "https://postman-echo.com/get?var=1")
            http_sampler2 = HttpSampler("echo_get_request", "https://postman-echo.com/get?var=2")
            http_sampler3 = HttpSampler("echo_get_request", "https://postman-echo.com/get?var=3")


            # create a setup thread group
            thread_group_setup = SetupThreadGroup(http_sampler1)

            # create a thread group that will rump up 10 threads in 1 second and
            # hold the load for additional 10 seconds, give it the http sampler as a child input
            thread_group_main = ThreadGroupWithRampUpAndHold(10, 1,10, http_sampler2)

            # create a teardown thread group
            thread_group_setup = TeardownThreadGroup(http_sampler3)

            # create a test plan with the required thread group
            test_plan = TestPlan(thread_group_setup, thread_group_main, thread_group_setup)

            # run the test plan and take the results
            stats = test_plan.run()


            # Assert that the 99th percentile of response time is less than 2000 milliseconds.
            assert (
                stats.sample_time_99_percentile_milliseconds <= 2000
            ), f"99th precentile should be less than 2000 milliseconds, got {stats.sample_time_99_percentile_milliseconds}"
example - 3:
--------------
We can use a `CsvDataset` to append a unique dataset to our test elements,
In this example, we will generate unique data for our entire test plan:

      .. code-block:: python

            from pymeter.api.config import TestPlan, ThreadGroupSimple, CsvDataset
            from pymeter.api.samplers import HttpSampler
            from pymeter.api.timers import ConstantTimer


            timer = ConstantTimer(2000)
            csv_data_set = CsvDataset("playground/file.csv")
            http_sampler1 = HttpSampler(
                "Echo_${id}", "https://postman-echo.com/get?var=${id}", timer
            )
            thread_group1 = ThreadGroupSimple(3, 1)
            thread_group1.children(http_sampler1)


            http_sampler2 = HttpSampler("Echo_${id}", "https://postman-echo.com/get?var=do", timer)
            thread_group2 = ThreadGroupSimple(3, 1, http_sampler2)
            test_plan = TestPlan(thread_group1, thread_group2, csv_data_set)
            stats = test_plan.run()

example - 4:
--------------

We can create vars from with in JMeters context using the `Vars` class

      .. code-block:: python

            from pymeter.api.config import TestPlan, ThreadGroupSimple, Vars
            from pymeter.api.samplers import HttpSampler
            from pymeter.api.timers import ConstantTimer
            from pymeter.api.reporters import HtmlReporter

            jmeter_variables = Vars(id1="value1", id2="value2")
            html_reporter = HtmlReporter()
            timer = ConstantTimer(2000)
            http_sampler1 = HttpSampler(
                "Echo_${id1}", "https://postman-echo.com/get?var=${id1}", timer
            )
            thread_group1 = ThreadGroupSimple(3, 1)
            thread_group1.children(http_sampler1)


            http_sampler2 = HttpSampler("Echo_${id2}", "https://postman-echo.com/get?var=do", timer)
            thread_group2 = ThreadGroupSimple(3, 1, http_sampler2)
            test_plan = TestPlan(thread_group1, thread_group2, html_reporter, jmeter_variables)
            stats = test_plan.run()

We can also set a single variable using the `set` method
      .. code-block:: python

            from pymeter.api.config import Vars
            jmeter_variables = Vars(id1="value1", id2="value2")
            jmeter_variables.set("id1", "v2")

example - 5:
--------------

We Can also generate data for each thread group:

      .. code-block:: python

            from pymeter.api.config import TestPlan, ThreadGroupSimple, CsvDataset
            from pymeter.api.samplers import HttpSampler
            from pymeter.api.timers import ConstantTimer


            timer = ConstantTimer(2000)
            csv_data_set1 = CsvDataset("playground/file1.csv")
            csv_data_set2 = CsvDataset("playground/file2.csv")
            http_sampler1 = HttpSampler(
                "Echo_${id}", "https://postman-echo.com/get?var=${id}", timer
            )
            thread_group1 = ThreadGroupSimple(3, 1)
            thread_group1.children(http_sampler1, csv_data_set1)


            http_sampler2 = HttpSampler("Echo_${id}", "https://postman-echo.com/get?var=do", timer)
            thread_group2 = ThreadGroupSimple(3, 1, http_sampler2, csv_data_set2)
            test_plan = TestPlan(thread_group1, thread_group2)
            stats = test_plan.run()


Classes
-------------
"""
import os
from jnius import JavaException

from pymeter.api import (
    ChildrenAreNotAllowed,
    TestPlanChildElement,
    ThreadGroupChildElement,
)


class BaseConfigElement(TestPlanChildElement):
    """base class for all config elements"""


class Vars(TestPlanChildElement):
    """Vars are key value pairs"""

    def __init__(self, **variables) -> None:
        self._vars_instance = TestPlanChildElement.jmeter_class.vars()
        for key, value in variables.items():
            self.set(key, value)
        super().__init__()

    def children(self, *children):
        raise ChildrenAreNotAllowed("Cant append children to vars")

    def set(self, key: str, value: str):
        """Sets a single key value pair"""
        if not isinstance(key, str):
            raise TypeError("Keys must be strings")

        self._vars_instance.set(key, str(value))
        return self


class CsvDataset(TestPlanChildElement, ThreadGroupChildElement):
    """
    csv data set allows you to append unique data set to samplers
    """

    def __init__(self, csv_file: str) -> None:
        if not os.path.exists(csv_file):
            raise FileNotFoundError(f"Couldn't find file {csv_file}")
        self._csv_dataset_instance = TestPlanChildElement.jmeter_class.csvDataSet(
            csv_file
        )
        super().__init__()

    def children(self, *children):
        raise ChildrenAreNotAllowed("Cant append children to a csv_data_set")


class TestPlan(BaseConfigElement):
    """
    This is the object that will call on the invocation of the test in the JMeter engine.
    """

    class TestPlanStats(BaseConfigElement):
        """test stats"""

        def __init__(self, java_instance) -> None:
            self._test_plan_stats_instance = java_instance
            super().__init__()

        @property
        def sample_time_mean_milliseconds(self):
            """returns the mean of sample times in milliseconds"""
            return self.java_wrapped_element.overallStats.sampleTime().mean().toMillis()

        @property
        def sample_time_min_milliseconds(self):
            """returns the min of sample times in milliseconds"""
            return self.java_wrapped_element.overallStats.sampleTime().min().toMillis()

        @property
        def sample_time_median_milliseconds(self):
            """returns the median of sample times in milliseconds"""
            return (
                self.java_wrapped_element.overallStats.sampleTime().median().toMillis()
            )

        @property
        def sample_time_90_percentile_milliseconds(self):
            """returns the 90th percentile of sample times in milliseconds"""
            return (
                self.java_wrapped_element.overallStats.sampleTime().perc90().toMillis()
            )

        @property
        def sample_time_95_percentile_milliseconds(self):
            """returns the 95th percentile of sample times in milliseconds"""
            return (
                self.java_wrapped_element.overallStats.sampleTime().perc95().toMillis()
            )

        @property
        def sample_time_99_percentile_milliseconds(self):
            """returns the 99th percentile of sample times in milliseconds"""
            return (
                self.java_wrapped_element.overallStats.sampleTime().perc99().toMillis()
            )

        @property
        def sample_time_max_milliseconds(self):
            """returns the max of sample times in milliseconds"""
            return self.java_wrapped_element.overallStats.sampleTime().max().toMillis()

        @property
        def duration_milliseconds(self):
            """returns the max of sample times in milliseconds"""
            return self.java_wrapped_element.duration().toMillis()

    def __init__(self, *children: TestPlanChildElement) -> None:

        self._test_plan_instance = BaseConfigElement.jmeter_class.testPlan()
        self.children(*children)

        super().__init__()

    def children(self, *children):
        if not all(isinstance(c, TestPlanChildElement) for c in children):
            raise TypeError("only takes children of type `TestPlanChildElement`")
        return super().children(*children)

    def run(self):
        """
        *run()* will execute the test plan code and return an object with aggregated results.

        This method is **blocking** and therefore the entire program will hang until the method is completed.

        By default, run prints stats to the stdio, for other reporting options please do check the `reporters <reporters.html>`_ page

        """
        try:
            return TestPlan.TestPlanStats(self._test_plan_instance.run())
        except JavaException as java_exception:
            print("\n\t at ".join(java_exception.stacktrace))
            raise java_exception


class BaseThreadGroup(BaseConfigElement):
    """base class for all thread groups"""

    def __init__(self, *children: ThreadGroupChildElement) -> None:
        self.children(*children)
        super().__init__()

    def children(self, *children):
        if not all(isinstance(c, ThreadGroupChildElement) for c in children):
            raise TypeError("only takes children of type `ThreadGroupChildElement`")
        return super().children(*children)


class SetupThreadGroup(BaseThreadGroup):
    """thread group for setting up test from within the context of JMeter"""

    def __init__(self, *children: ThreadGroupChildElement) -> None:

        self._setup_thread_group_instance = (
            BaseConfigElement.jmeter_class.setupThreadGroup()
        )
        super().__init__(*children)


class TeardownThreadGroup(BaseThreadGroup):
    """thread group for tearing down test from within the context of JMeter"""

    def __init__(self, *children: ThreadGroupChildElement) -> None:

        self._teardown_thread_group_instance = (
            BaseConfigElement.jmeter_class.teardownThreadGroup()
        )
        super().__init__(*children)


class ThreadGroupSimple(BaseThreadGroup):
    """
    Thread group defined by number of threads and number of iterations

    """

    def __init__(
        self,
        number_of_threads: int,
        iterations: int,
        *children: ThreadGroupChildElement,
        name: str = "Thread Group",
    ) -> None:
        self._thread_group_simple_instance = BaseConfigElement.jmeter_class.threadGroup(
            name, number_of_threads, iterations
        )
        super().__init__(*children)


class ThreadGroupWithRampUpAndHold(BaseThreadGroup):
    """Thread group that rumps up a number of thread in a given number of seconds and then holds the load for a given number of seconds."""

    def __init__(
        self,
        number_of_threads: int,
        rampup_time_seconds: float,
        holdup_time_seconds: float,
        *children,
        name: str = "Thread Group",
    ) -> None:

        self._thread_group_with_ramp_up_and_hold_instance = (
            BaseConfigElement.jmeter_class.threadGroup(name)
        )
        self._ramp_to_and_hold_instance = (
            self._thread_group_with_ramp_up_and_hold_instance.rampToAndHold(
                number_of_threads,
                BaseConfigElement.java_duration.ofSeconds(rampup_time_seconds),
                BaseConfigElement.java_duration.ofSeconds(holdup_time_seconds),
            )
        )
        super().__init__(*children)
